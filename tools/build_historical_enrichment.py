#!/usr/bin/env python3
"""Build source-backed historical content from the verified Wikipedia identities.

No Wikidata calls are made. English identities come exclusively from
WIKIPEDIA_IDENTITY_REVIEW.json; localized records use the corresponding
Wikipedia language edition when an interlanguage link exists. Existing
non-placeholder structured fields are preserved.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urljoin

import requests
from bs4 import BeautifulSoup

LANGS = ["ar", "en", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "ko", "zh", "hi", "id", "fa"]
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
QUIZ = ASSETS / "quiz_data.json"
OUT = ASSETS / "person_i18n.json"
IDENTITY = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
CACHE = ROOT / ".wikipedia_content_cache"
STATE = ROOT / "HISTORICAL_ENRICHMENT_STATE.json"
AUDIT = ROOT / "HISTORICAL_ENRICHMENT_AUDIT.json"
UA = "MapOfFame/1.0 (build-time historical data enrichment; local development)"

PLACEHOLDER_PATTERNS = (
    re.compile(r"^notable historical work$", re.I),
    re.compile(r"^notable historical event$", re.I),
    re.compile(r"^notable fact$", re.I),
    re.compile(r"^notable work$", re.I),
    re.compile(r"^notable event$", re.I),
    re.compile(r"^a notable historical figure(?: in the field of .*)?$", re.I),
    re.compile(r"^an important historical fact about this person\.?$", re.I),
    re.compile(r"^a major contribution to the field of .*$", re.I),
    re.compile(r"^a lasting influence on the history of .*$", re.I),
    re.compile(r"^a notable figure in history$", re.I),
)

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def placeholder(value: Any) -> bool:
    if isinstance(value, list):
        return not value or any(placeholder(item) for item in value)
    text = clean(value)
    return any(pattern.fullmatch(text) for pattern in PLACEHOLDER_PATTERNS)


def good_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [clean(x) for x in value if clean(x) and not placeholder(x)]


def existing_value(existing: dict[str, Any], key: str, default: Any = "") -> Any:
    value = existing.get(key, default)
    return default if placeholder(value) else value


def title_url(lang: str, title: str) -> str:
    return "https://%s.wikipedia.org/wiki/%s" % (lang, quote(title.replace(" ", "_"), safe="()!,-:,") )


def cache_path(url: str) -> Path:
    """Return a Windows-safe, bounded-length cache filename for a URL."""
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return CACHE / f"{digest}.html"


def fetch(url: str, delay: float) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = cache_path(url)
    if path.exists():
        return path.read_text(encoding="utf-8")
    for attempt in range(7):
        try:
            response = SESSION.get(url, timeout=30)
            if response.status_code == 200:
                path.write_text(response.text, encoding="utf-8")
                if delay:
                    time.sleep(delay)
                return response.text
            if response.status_code == 404:
                return ""
            if response.status_code == 429:
                retry = clean(response.headers.get("Retry-After"))
                try:
                    wait = max(2, int(float(retry)))
                except ValueError:
                    wait = min(60, 5 * (attempt + 1))
                time.sleep(min(wait, 120))
                continue
            response.raise_for_status()
        except requests.RequestException:
            if attempt == 6:
                return ""
            time.sleep(min(60, 2**attempt))
    return ""


EXPLICIT_WIKIPEDIA_TITLES = {
    "Buddha": "The Buddha",
    "Hannibal Barca": "Hannibal",
    "Attila the Hun": "Attila",
    "Thabit ibn Qurra": "Thābit ibn Qurra",
    "Tughril Beg": "Tughril I",
    "Al-Idrisi": "Muhammad al-Idrisi",
    "Nur ad-Din": "Nur al-Din",
    "Richard the Lionheart": "Richard I of England",
    "Louis IX": "Louis IX of France",
    "Isabella I": "Isabella I of Castile",
    "Shah Abbas I": "Abbas the Great",
    "Muhammad Ali Pasha": "Muhammad Ali of Egypt",
    "Pyotr Tchaikovsky": "Pyotr Ilyich Tchaikovsky",
    "Horatio Kitchener": "Herbert Kitchener, 1st Earl Kitchener",
    "King Faisal I": "Faisal I",
    "Abbas al-Aqqad": "Abbas Mahmoud al-Aqqad",
    "Martin Luther King": "Martin Luther King Jr.",
    "Ferdinand II": "Ferdinand II of Aragon",
    "Arthur Wellesley": "Arthur Wellesley, 1st Duke of Wellington",
}

def identity_title(name: str, identity: dict[str, Any]) -> str:
    explicit = EXPLICIT_WIKIPEDIA_TITLES.get(name)
    if explicit:
        return explicit
    item = identity.get("people", {}).get(name, {})
    if item.get("status") != "verified":
        return ""
    return clean(item.get("title"))



def api_cache_path(lang: str, query: str) -> Path:
    digest = hashlib.sha256(f"{lang}|{query}".encode("utf-8")).hexdigest()
    return CACHE / f"api_{digest}.json"


def resolve_local_title(lang: str, english_title: str, person_name: str, delay: float) -> str:
    """Resolve a missing interlanguage link using the target Wikipedia search API."""
    candidates = [english_title, person_name]
    for query in candidates:
        query = clean(query)
        if not query:
            continue
        path = api_cache_path(lang, query)
        data: dict[str, Any] | None = None
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                data = None
        if data is None:
            url = f"https://{lang}.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srnamespace": 0,
                "srlimit": 5,
                "format": "json",
            }
            for attempt in range(7):
                try:
                    response = SESSION.get(url, params=params, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                        if delay:
                            time.sleep(delay)
                        break
                    if response.status_code == 404:
                        break
                    if response.status_code == 429:
                        retry = clean(response.headers.get("Retry-After"))
                        try:
                            wait = max(2, int(float(retry)))
                        except ValueError:
                            wait = min(60, 5 * (attempt + 1))
                        time.sleep(min(wait, 120))
                        continue
                    response.raise_for_status()
                except (requests.RequestException, ValueError):
                    if attempt == 6:
                        break
                    time.sleep(min(60, 2**attempt))
        if isinstance(data, dict):
            results = data.get("query", {}).get("search", [])
            if results:
                title = clean(results[0].get("title"))
                if title:
                    return title
    return ""

def parse_page(html: str, lang: str, title: str, url: str) -> dict[str, Any] | None:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if not h1:
        return None
    content = soup.select_one("#mw-content-text .mw-parser-output") or soup.select_one("#mw-content-text")
    if content is None:
        return None
    for node in content.select("script,style,table,nav,sup,.mw-editsection,.reference"):
        node.decompose()

    paragraphs: list[str] = []
    for node in content.find_all("p"):
        text_value = clean(node.get_text(" ", strip=True))
        if len(text_value) >= 25:
            paragraphs.append(text_value)

    # Some cached Wikipedia pages expose useful prose outside the
    # conventional <p> nodes. Use visible text from the article body
    # as a cache-only fallback; never fabricate content.
    if not paragraphs:
        fallback_nodes = content.find_all(["div", "section", "blockquote"])

        for node in fallback_nodes:
            text_value = clean(node.get_text(" ", strip=True))
            if len(text_value) >= 25:
                paragraphs.append(text_value)

        # Remove duplicates while preserving source order.
        paragraphs = list(dict.fromkeys(paragraphs))

    sections: list[tuple[str, str]] = []
    heading = ""
    buffer: list[str] = []
    for node in content.find_all(["h2", "h3", "p"]):
        if node.name in {"h2", "h3"}:
            if heading and buffer:
                sections.append((heading, clean(" ".join(buffer))))
            heading = clean(node.get_text(" ", strip=True)).replace("[edit]", "")
            buffer = []
        else:
            text = clean(node.get_text(" ", strip=True))
            if len(text) >= 40:
                buffer.append(text)
    if heading and buffer:
        sections.append((heading, clean(" ".join(buffer))))
    infobox: dict[str, str] = {}
    box = soup.select_one("table.infobox")
    if box:
        for row in box.select("tr"):
            th, td = row.find("th"), row.find("td")
            if th and td:
                infobox[clean(th.get_text(" ", strip=True)).casefold()] = clean(td.get_text(" ", strip=True))
    links: dict[str, str] = {}
    for link in soup.find_all("link", rel="alternate"):
        hreflang = clean(link.get("hreflang"))
        href = clean(link.get("href"))
        if hreflang in LANGS and href:
            links[hreflang] = href
    for link in soup.select("a.interlanguage-link-target"):
        hreflang = clean(link.get("lang"))
        href = clean(link.get("href"))
        if hreflang in LANGS and href:
            links[hreflang] = urljoin(url, href)
    return {
        "title": clean(h1.get_text(" ", strip=True)),
        "url": url,
        "lang": lang,
        "paragraphs": paragraphs[:10],
        "sections": sections,
        "infobox": infobox,
        "links": links,
    }


def sentences(text: str) -> list[str]:
    cleaned = clean(text)
    if not cleaned:
        return []

    parts = re.split(r"(?<=[.!?])\s+", cleaned)

    result: list[str] = []
    for part in parts:
        sentence = clean(part)
        if len(sentence) >= 35 and sentence not in result:
            result.append(sentence)

    return result


def build_content(person: dict[str, Any], existing: dict[str, Any], page: dict[str, Any]) -> dict[str, Any]:
    paragraphs = page["paragraphs"]
    sections = page["sections"]
    lead = " ".join(paragraphs[:6])

    def collect(headings: tuple[str, ...], limit: int = 6) -> list[str]:
        out: list[str] = []
        for heading, text in sections:
            h = heading.casefold()
            if any(k in h for k in headings):
                for sentence in sentences(text):
                    if sentence not in out:
                        out.append(sentence)
                    if len(out) >= limit:
                        return out
        return out

    facts = sentences(" ".join(paragraphs[:6]))[:5]

    achievements = collect(
        (
            "career",
            "works",
            "legacy",
            "reign",
            "political",
            "achievements",
            "contribution",
            "invention",
            "discovery",
            "literary",
            "philosophy",
            "science",
        ),
        5,
    )

    if not achievements:
        achievements = facts[:5]

    wars = collect(("military", "war", "battle", "campaign", "invasion", "conquest", "revolt", "rebellion", "siege", "conflict", "expedition"), 5)
    # Empty is valid: not every historical person was a military figure.

    info = page["infobox"]
    birth = info.get("born", "") or info.get("birth date", "")
    death = info.get("died", "") or info.get("death date", "")

    # Preserve only genuinely useful existing structured content.
    old_ach = good_list(existing.get("achievements"))
    old_facts = good_list(existing.get("key_facts"))
    old_wars = good_list(existing.get("wars"))
    old_sig = existing_value(existing, "historical_significance", "")
    old_bio = existing_value(existing, "bio", "")

    result: dict[str, Any] = {
        "name": clean(existing_value(existing, "name", person.get("name_en"))),
        "hint": clean(existing_value(existing, "hint", facts[0] if facts else lead[:300])),
        "bio": clean(old_bio or lead),
        "birth_city": clean(existing_value(existing, "birth_city", person.get("birth_city", ""))),
        "birth_country": clean(existing_value(existing, "birth_country", person.get("birth_country", ""))),
        "death_city": clean(existing_value(existing, "death_city", person.get("death_city", ""))),
        "death_country": clean(existing_value(existing, "death_country", person.get("death_country", ""))),
        "role": clean(existing_value(existing, "role", person.get("role_en", ""))),
        "era": clean(existing_value(existing, "era", person.get("era_en", ""))),
        "achievements": old_ach or achievements,
        "key_facts": old_facts or facts,
        "wars": old_wars or wars,
        "historical_significance": clean(old_sig or lead),
        "source": {"type": "wikipedia", "language": page["lang"], "title": page["title"], "url": page["url"]},
    }
    # Never put a date into a city field.
    if not result["birth_city"] and birth:
        result["birth_city"] = ""
        result["birth_date"] = birth
    if not result["death_city"] and death:
        result["death_city"] = ""
        result["death_date"] = death
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=1.2)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--languages", nargs="*", default=["en"])
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--people",
        nargs="+",
        default=[],
        help="Process only the specified English person names.",
    )
    args = parser.parse_args()
    requested = [x for x in args.languages if x in LANGS]
    if not requested:
        raise SystemExit("No valid languages supplied")

    people = json.loads(QUIZ.read_text(encoding="utf-8"))
    if args.people:
        requested_people = {
            clean(name).casefold()
            for name in args.people
            if clean(name)
        }

        process_people = [
            person
            for person in people
            if clean(person.get("name_en") or person.get("name")).casefold()
            in requested_people
        ]

        found_people = {
            clean(person.get("name_en") or person.get("name")).casefold()
            for person in process_people
        }

        missing_people = sorted(requested_people - found_people)

        if missing_people:
            raise SystemExit(
                "Requested people were not found in quiz_data.json: "
                + ", ".join(missing_people)
            )
    elif args.limit:
        process_people = people[: args.limit]
    else:
        process_people = people
    identity = json.loads(IDENTITY.read_text(encoding="utf-8"))
    # Always preserve an existing output file.  A limited run must update only
    # the selected people; it must never replace the full database with a
    # partial result.  This is intentionally independent of --resume.
    if OUT.exists():
        old = json.loads(OUT.read_text(encoding="utf-8"))
        if not isinstance(old, dict) or not isinstance(old.get("people"), dict):
            raise SystemExit(f"Invalid enrichment output: {OUT}")
    else:
        old = {"schema": 5, "languages": LANGS, "policy": "source-backed-no-cross-language-fallback", "people": {}}
    state = json.loads(STATE.read_text(encoding="utf-8")) if args.resume and STATE.exists() else {"schema": 1, "completed": {}}
    audit: dict[str, Any] = {"schema": 2, "processed": 0, "errors": [], "missing_languages": [], "placeholders": [], "explicit_identity_mappings": sorted(EXPLICIT_WIKIPEDIA_TITLES)}

    for index, person in enumerate(process_people, 1):
        name = clean(person.get("name_en") or person.get("name"))
        existing_record = old.get("people", {}).get(name, {}) if args.resume else {}
        existing_languages = existing_record.get("languages", {}) if isinstance(existing_record, dict) else {}
        if args.resume and all(isinstance(existing_languages.get(lang), dict) for lang in requested):
            print(f"[{index}/{len(process_people)}] CACHED: {name}")
            audit["processed"] += 1
            continue
        title = identity_title(name, identity)
        if not title:
            audit["errors"].append({"name": name, "error": "No verified Wikipedia identity"})
            continue
        en_url = title_url("en", title)
        en_html = fetch(en_url, args.delay)
        en_page = parse_page(en_html, "en", title, en_url) if en_html else None
        if not en_page:
            audit["errors"].append({"name": name, "error": "English Wikipedia page unavailable", "title": title})
            continue
        localized = dict(existing_languages) if isinstance(existing_languages, dict) else {}
        for lang in requested:
            if lang == "en":
                page = en_page
            else:
                href = en_page["links"].get(lang, "")
                if href:
                    local_url = href if href.startswith("http") else urljoin(f"https://{lang}.wikipedia.org", href)
                    local_title = unquote(local_url.rsplit("/wiki/", 1)[-1]).replace("_", " ")
                else:
                    local_title = resolve_local_title(lang, title, name, args.delay)
                    if not local_title:
                        audit["missing_languages"].append({"name": name, "language": lang})
                        continue
                    local_url = title_url(lang, local_title)
                html = fetch(local_url, args.delay)
                page = parse_page(html, lang, local_title, local_url) if html else None
                if not page:
                    audit["missing_languages"].append({"name": name, "language": lang})
                    continue
            existing = localized.get(lang, {}) if isinstance(localized.get(lang), dict) else {}
            localized[lang] = build_content(person, existing, page)
        old.setdefault("people", {})[name] = {"languages": localized}
        if all(isinstance(localized.get(lang), dict) for lang in requested):
            state.setdefault("completed", {})[name] = True
        else:
            state.setdefault("completed", {}).pop(name, None)
        audit["processed"] += 1
        print(f"[{index}/{len(process_people)}] ENRICHED: {name} -> {title}")
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    for name, record in old.get("people", {}).items():
        for lang, content in record.get("languages", {}).items():
            if isinstance(content, dict):
                for field in ("bio", "achievements", "key_facts", "historical_significance"):
                    if placeholder(content.get(field)):
                        audit["placeholders"].append({"name": name, "language": lang, "field": field})
                wars = content.get("wars")
                if isinstance(wars, list) and any(placeholder(x) for x in wars):
                    audit["placeholders"].append({"name": name, "language": lang, "field": "wars"})
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    # Write atomically so an interrupted build cannot leave a truncated JSON.
    tmp_out = OUT.with_suffix(".json.tmp")
    tmp_out.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_out.replace(OUT)
    print(f"processed={audit['processed']} errors={len(audit['errors'])} missing_languages={len(audit['missing_languages'])} placeholders={len(audit['placeholders'])}")
    return 0 if not audit["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
