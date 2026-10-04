#!/usr/bin/env python3
"""Build historical enrichment from the existing Wikipedia cache only.

The cache is authoritative for this build.  This module never performs HTTP
requests.  The output file is written atomically and a --limit run merges its
changes into the complete existing people set instead of replacing it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urljoin

from lxml import etree

LANGS = [
    "ar", "en", "es", "fr", "de", "pt", "it", "tr", "ru", "ja",
    "zh", "hi", "id", "fa",
]
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
QUIZ = ASSETS / "quiz_data.json"
OUT = ASSETS / "person_i18n.json"
IDENTITY = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
CACHE = ROOT / ".wikipedia_content_cache"
BACKUP_CACHE = ROOT / ".wikipedia_content_cache_v12_backup"
STATE = ROOT / "HISTORICAL_ENRICHMENT_STATE.json"
AUDIT = ROOT / "HISTORICAL_ENRICHMENT_AUDIT.json"

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
}


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def placeholder(value: Any) -> bool:
    if isinstance(value, list):
        return any(placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(placeholder(item) for item in value.values())
    text = clean(value)
    return any(pattern.fullmatch(text) for pattern in PLACEHOLDER_PATTERNS)


def good_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [clean(x) for x in value if clean(x) and not placeholder(x)]


def title_url(lang: str, title: str) -> str:
    return (
        f"https://{lang}.wikipedia.org/wiki/"
        f"{quote(title.replace(' ', '_'), safe='()!,-:,')}"
    )


def cache_candidates(url: str) -> list[Path]:
    """Return current-cache and backup-cache candidates without scanning."""
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    names = [
        f"{digest}.html",
        re.sub(r"[^A-Za-z0-9._-]", "_", quote(url, safe="._-")) + ".html",
        (
            quote(url, safe="")
            .replace("%", "_")
            .replace("/", "_")
            .replace(":", "_")
            + ".html"
        ),
    ]
    return [
        directory / name
        for directory in (CACHE, BACKUP_CACHE)
        for name in names
    ]


def api_cache_candidates(lang: str, query: str) -> list[Path]:
    digest = hashlib.sha256(f"{lang}|{query}".encode("utf-8")).hexdigest()
    names = [
        f"api_{digest}.json",
        "api_"
        + re.sub(
            r"[^A-Za-z0-9._-]",
            "_",
            quote(f"{lang}|{query}", safe="._-"),
        )
        + ".json",
    ]
    return [
        directory / name
        for directory in (CACHE, BACKUP_CACHE)
        for name in names
    ]


def read_cached_text(url: str) -> str:
    if not CACHE.exists():
        raise RuntimeError(f"Wikipedia cache directory does not exist: {CACHE}")
    for path in cache_candidates(url):
        if path.is_file():
            try:
                return path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise RuntimeError(f"Cannot read cache file: {path}") from exc
    return ""


def read_cached_json(lang: str, query: str) -> dict[str, Any] | None:
    for path in api_cache_candidates(lang, query):
        if path.is_file():
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Cannot read API cache file: {path}") from exc
            return value if isinstance(value, dict) else None
    return None


def resolve_local_title(lang: str, english_title: str, person_name: str) -> str:
    """Resolve only from an existing API cache; never query Wikipedia."""
    for query in (clean(english_title), clean(person_name)):
        if not query:
            continue
        data = read_cached_json(lang, query)
        if isinstance(data, dict):
            results = data.get("query", {}).get("search", [])
            if isinstance(results, list) and results:
                title = clean(results[0].get("title"))
                if title:
                    return title
    return ""


def parse_page(html: str, lang: str, title: str, url: str) -> dict[str, Any] | None:
    """Parse cached Wikipedia HTML without network access.

    Uses libxml2's recovery parser so malformed/truncated cached HTML cannot
    stall BeautifulSoup's HTML parser on a single page.
    """
    if not html:
        return None

    parser = etree.HTMLParser(
        recover=True,
        huge_tree=True,
        no_network=True,
    )
    try:
        root = etree.fromstring(html.encode("utf-8", errors="ignore"), parser)
    except (etree.XMLSyntaxError, ValueError, TypeError):
        return None
    if root is None:
        return None

    h1_nodes = root.xpath("//h1")
    if not h1_nodes:
        return None
    h1 = h1_nodes[0]
    parsed_title = clean(" ".join(h1.itertext()))
    if not parsed_title:
        return None

    content_nodes = root.xpath(
        '//*[@id="mw-content-text"]//*[contains(concat(" ", normalize-space(@class), " "), " mw-parser-output ")]'
    )
    if content_nodes:
        content = content_nodes[0]
    else:
        fallback = root.xpath('//*[@id="mw-content-text"]')
        if not fallback:
            return None
        content = fallback[0]

    infobox: dict[str, str] = {}
    for row in content.xpath(
        './/table[contains(concat(" ", normalize-space(@class), " "), " infobox ")]//tr'
    ):
        th = row.xpath("./th")
        td = row.xpath("./td")
        if th and td:
            key = clean(" ".join(th[0].itertext())).casefold()
            value = clean(" ".join(td[0].itertext()))
            if key:
                infobox[key] = value

    remove_nodes = content.xpath(
        ".//script | .//style | .//table | .//nav | .//sup | "
        './/*[contains(concat(" ", normalize-space(@class), " "), " mw-editsection ")] | '
        './/*[contains(concat(" ", normalize-space(@class), " "), " reference ")]'
    )
    for node in remove_nodes:
        parent = node.getparent()
        if parent is not None:
            parent.remove(node)

    paragraphs: list[str] = []
    for node in content.xpath(".//p"):
        text_value = clean(" ".join(node.itertext()))
        if len(text_value) >= 40:
            paragraphs.append(text_value)

    sections: list[tuple[str, str]] = []
    heading = ""
    buffer: list[str] = []
    for node in content.xpath(".//h2 | .//h3 | .//p"):
        if node.tag in {"h2", "h3"}:
            if heading and buffer:
                sections.append((heading, clean(" ".join(buffer))))
            heading = clean(" ".join(node.itertext())).replace("[edit]", "")
            buffer = []
        else:
            text_value = clean(" ".join(node.itertext()))
            if len(text_value) >= 40:
                buffer.append(text_value)
    if heading and buffer:
        sections.append((heading, clean(" ".join(buffer))))

    links: dict[str, str] = {}
    for link in root.xpath('//link[@rel="alternate"]'):
        hreflang = clean(link.get("hreflang"))
        href = clean(link.get("href"))
        if hreflang in LANGS and href:
            links[hreflang] = href

    for link in root.xpath(
        '//a[contains(concat(" ", normalize-space(@class), " "), " interlanguage-link-target ")]'
    ):
        hreflang = clean(link.get("lang"))
        href = clean(link.get("href"))
        if hreflang in LANGS and href:
            links[hreflang] = urljoin(url, href)

    return {
        "title": parsed_title,
        "url": url,
        "lang": lang,
        "paragraphs": paragraphs[:10],
        "sections": sections,
        "infobox": infobox,
        "links": links,
    }


def sentences(text: str) -> list[str]:
    return [clean(x) for x in re.split(r"(?<=[.!?عéي╝ي╝ا])\s+", text) if len(clean(x)) >= 35]


def build_content(person: dict[str, Any], page: dict[str, Any]) -> dict[str, Any]:
    paragraphs = [clean(x) for x in page.get("paragraphs", []) if clean(x)]
    sections = page.get("sections", [])
    lead = " ".join(paragraphs[:6])

    def collect(headings: tuple[str, ...], limit: int = 6) -> list[str]:
        out: list[str] = []
        for heading, text in sections:
            h = clean(heading).casefold()
            if any(k in h for k in headings):
                for sentence in sentences(clean(text)):
                    if sentence not in out:
                        out.append(sentence)
                    if len(out) >= limit:
                        return out
        return out

    facts = sentences(" ".join(paragraphs[:6]))[:5]
    achievements = collect(
        (
            "career", "works", "reign", "political", "achievement",
            "contribution", "invention", "discovery", "literary",
            "philosophy", "science", "artistic", "professional",
        ),
        5,
    )
    significance = collect(
        (
            "legacy", "impact", "influence", "significance", "reception",
            "historical importance", "memory", "aftermath",
        ),
        4,
    )
    wars = collect(
        (
            "military", "war", "battle", "campaign", "invasion",
            "conquest", "revolt", "rebellion", "siege", "conflict",
            "expedition",
        ),
        5,
    )
    info = page.get("infobox", {})
    birth = clean(info.get("born", "") or info.get("birth date", ""))
    death = clean(info.get("died", "") or info.get("death date", ""))
    return {
        "name": clean(page.get("title", "")),
        "hint": facts[0] if facts else "",
        "bio": lead,
        "birth_city": clean(person.get("birth_city", "")),
        "birth_country": clean(person.get("birth_country", "")),
        "death_city": clean(person.get("death_city", "")),
        "death_country": clean(person.get("death_country", "")),
        "role": clean(person.get("role_en", "")),
        "era": clean(person.get("era_en", "")),
        "achievements": achievements,
        "key_facts": facts,
        "wars": wars,
        "historical_significance": " ".join(significance),
        "source": {"type": "wikipedia", "language": page.get("lang", ""), "title": clean(page.get("title", "")), "url": page.get("url", "")},
        **({"birth_date": birth} if birth else {}),
        **({"death_date": death} if death else {}),
    }


def complete(content: Any) -> bool:
    if not isinstance(content, dict):
        return False
    name = clean(content.get("name"))
    bio = clean(content.get("bio"))
    significance = clean(content.get("historical_significance"))
    if not name or len(bio) < 120 or len(significance) < 35:
        return False
    if placeholder(content.get("bio")) or placeholder(content.get("historical_significance")):
        return False
    values: dict[str, str] = {"bio": bio, "historical_significance": significance}
    for key in ("achievements", "key_facts"):
        value = content.get(key)
        if not isinstance(value, list) or not value or any(placeholder(x) for x in value):
            return False
        cleaned = [clean(x) for x in value if clean(x)]
        if len(cleaned) < 2 or len(cleaned) != len(set(cleaned)):
            return False
        values[key] = " | ".join(cleaned)
    # The learning fields must carry distinct information. Falling back from
    # one field to another is a generation error, not valid enrichment.
    normalized = {key: re.sub(r"\W+", " ", value.casefold()).strip() for key, value in values.items()}
    pairs = (("bio", "historical_significance"), ("achievements", "key_facts"))
    if any(normalized[a] == normalized[b] for a, b in pairs):
        return False
    wars = content.get("wars")
    return isinstance(wars, list) and not any(placeholder(x) for x in wars)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp = Path(handle.name)
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build historical enrichment from the existing Wikipedia cache only."
    )
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--languages", nargs="*", default=["en"])
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    requested = list(dict.fromkeys(lang for lang in args.languages if lang in LANGS))
    if not requested:
        raise SystemExit("No valid languages supplied")
    if args.delay < 0:
        raise SystemExit("--delay cannot be negative")
    if args.limit < 0:
        raise SystemExit("--limit cannot be negative")

    if not QUIZ.exists() or not IDENTITY.exists() or not OUT.exists():
        raise SystemExit("Required project data file is missing")
    if not CACHE.exists() and not BACKUP_CACHE.exists():
        raise SystemExit(
            "Wikipedia cache is missing: "
            f"{CACHE} and fallback {BACKUP_CACHE}"
        )

    quiz_payload = json.loads(QUIZ.read_text(encoding="utf-8"))
    people = quiz_payload if isinstance(quiz_payload, list) else quiz_payload.get("people", [])
    identity = json.loads(IDENTITY.read_text(encoding="utf-8"))
    old = json.loads(OUT.read_text(encoding="utf-8"))
    if not isinstance(old.get("people"), dict):
        raise SystemExit("person_i18n.json has an invalid people object")

    # Work from the complete existing output. Nothing is ever removed.
    working: dict[str, Any] = json.loads(json.dumps(old, ensure_ascii=False))
    process_people = people[: args.limit] if args.limit else people

    audit: dict[str, Any] = {
        "schema": 4,
        "processed": 0,
        "skipped": 0,
        "errors": [],
        "missing_languages": [],
        "placeholders": [],
        "cache_only": True,
        "requested_languages": requested,
    }

    for index, person in enumerate(process_people, 1):
        name = clean(person.get("name_en") or person.get("name"))
        identity_record = identity.get("people", {}).get(name, {})
        title = EXPLICIT_WIKIPEDIA_TITLES.get(name) or clean(identity_record.get("title"))

        if identity_record.get("status") != "verified" and name not in EXPLICIT_WIKIPEDIA_TITLES:
            audit["errors"].append({"name": name, "error": "No verified Wikipedia identity"})
            print(f"[{index}/{len(process_people)}] FAILED: {name}")
            continue

        current_record = working["people"].get(name, {})
        current_languages = (
            current_record.get("languages", {})
            if isinstance(current_record, dict)
            else {}
        )
        merged_languages = (
            dict(current_languages)
            if isinstance(current_languages, dict)
            else {}
        )

        # True resume: already-complete requested locales are not parsed again.
        pending = [
            lang
            for lang in requested
            if not complete(merged_languages.get(lang))
        ]

        if not pending:
            audit["skipped"] += 1
            print(f"[{index}/{len(process_people)}] SKIPPED: {name} (complete)")
            continue

        en_url = title_url("en", title)
        en_html = ""
        en_page: dict[str, Any] | None = None

        # English is shared by all locale resolutions. Load it only when needed.
        if "en" in pending or any(lang != "en" for lang in pending):
            en_html = read_cached_text(en_url)
            en_page = parse_page(en_html, "en", title, en_url) if en_html else None

        if "en" in pending:
            if not en_page:
                audit["errors"].append(
                    {
                        "name": name,
                        "language": "en",
                        "error": "English page missing from cache",
                        "title": title,
                    }
                )
            else:
                content = build_content(person, en_page)
                if complete(content):
                    merged_languages["en"] = content
                    audit["processed"] += 1
                    atomic_write_json(
                        OUT,
                        {
                            **working,
                            "people": {
                                **working["people"],
                                name: {
                                    **(
                                        current_record
                                        if isinstance(current_record, dict)
                                        else {}
                                    ),
                                    "languages": dict(merged_languages),
                                },
                            },
                        },
                    )
                    working["people"][name] = {
                        **(
                            current_record
                            if isinstance(current_record, dict)
                            else {}
                        ),
                        "languages": dict(merged_languages),
                    }
                    print(f"[{index}/{len(process_people)}] CACHED: {name} -> {title} [en]")
                else:
                    audit["errors"].append(
                        {
                            "name": name,
                            "language": "en",
                            "error": "incomplete content from cache",
                        }
                    )

        for lang in pending:
            if lang == "en":
                continue

            if en_page is None:
                # Without the cached English page we cannot reliably resolve
                # the interlanguage target from this program's cache-only data.
                audit["missing_languages"].append(
                    {"name": name, "language": lang}
                )
                continue

            href = en_page["links"].get(lang, "")
            if href:
                local_url = (
                    href
                    if href.startswith("http")
                    else urljoin(f"https://{lang}.wikipedia.org", href)
                )
                local_title = unquote(
                    local_url.rsplit("/wiki/", 1)[-1]
                ).replace("_", " ")
            else:
                local_title = resolve_local_title(lang, title, name)
                if not local_title:
                    audit["missing_languages"].append(
                        {"name": name, "language": lang}
                    )
                    continue
                local_url = title_url(lang, local_title)

            html = read_cached_text(local_url)
            page = parse_page(html, lang, local_title, local_url) if html else None
            if not page:
                audit["missing_languages"].append(
                    {"name": name, "language": lang}
                )
                continue

            content = build_content(person, page)
            if not complete(content):
                audit["errors"].append(
                    {
                        "name": name,
                        "language": lang,
                        "error": "incomplete content from cache",
                    }
                )
                continue

            merged_languages[lang] = content
            audit["processed"] += 1

            working["people"][name] = {
                **(
                    current_record
                    if isinstance(current_record, dict)
                    else {}
                ),
                "languages": dict(merged_languages),
            }
            atomic_write_json(OUT, working)
            print(
                f"[{index}/{len(process_people)}] CACHED: "
                f"{name} -> {local_title} [{lang}]"
            )

            if args.delay:
                time.sleep(args.delay)

        # Persist every successful locale even when another requested locale
        # failed. This is the essential incremental/resume behavior.
        working["people"][name] = {
            **(
                current_record
                if isinstance(current_record, dict)
                else {}
            ),
            "languages": dict(merged_languages),
        }
        atomic_write_json(OUT, working)

    if len(working["people"]) < len(old["people"]):
        raise RuntimeError("Safety check failed: output people count would decrease")

    # Verify that no newly written record contains placeholders.
    for person_name, record in working["people"].items():
        languages = record.get("languages", {}) if isinstance(record, dict) else {}
        if not isinstance(languages, dict):
            continue
        for lang, content in languages.items():
            if not isinstance(content, dict):
                continue
            for field in (
                "bio",
                "achievements",
                "key_facts",
                "wars",
                "historical_significance",
            ):
                if placeholder(content.get(field)):
                    audit["placeholders"].append(
                        {
                            "name": person_name,
                            "language": lang,
                            "field": field,
                        }
                    )

    atomic_write_json(AUDIT, audit)

    print(
        f"processed={audit['processed']} "
        f"skipped={audit['skipped']} "
        f"errors={len(audit['errors'])} "
        f"missing_languages={len(audit['missing_languages'])} "
        f"placeholders={len(audit['placeholders'])}"
    )

    # A non-zero result means work remains, but successful incremental work
    # has already been safely committed to person_i18n.json.
    return 2 if (
        audit["errors"]
        or audit["missing_languages"]
        or audit["placeholders"]
    ) else 0


if __name__ == "__main__":
    raise SystemExit(main())
