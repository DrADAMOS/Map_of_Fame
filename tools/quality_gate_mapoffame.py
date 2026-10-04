from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
JSON_PATH = ASSETS / "person_i18n.json"
JS_PATH = ASSETS / "js" / "person_i18n.js"
QUIZ_PATH = ASSETS / "quiz_data.json"
REPORT_PATH = ROOT / "MAP_OF_FAME_QUALITY_GATE_REPORT.md"

EXPECTED_LANGS = [
    "ar", "en", "es", "fr", "de", "pt", "it", "tr",
    "ru", "ja", "ko", "zh", "hi", "id", "fa",
]
FIELDS = ["hint", "bio", "achievements", "key_facts", "historical_significance"]

# Conservative detector: deliberately reports suspicious content; it does not
# delete or rewrite anything.
GENERIC_PATTERNS = [
    r"\bnotable historical work\b",
    r"\ba notable historical figure\b",
    r"\bremembered for shaping historical developments\b",
    r"\bnotable figure in\b",
    r"من أبرز شخصيات العصر الحديث",
    r"تركت أثراً تاريخياً",
    r"حققت أثراً كبيراً وإنجازات تاريخية",
    r"تعد حلقة بارزة في عصر العصر الحديث",
]
GENERIC_RE = [re.compile(p, re.I) for p in GENERIC_PATTERNS]

def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))

def normalize(value: object) -> str:
    if isinstance(value, list):
        return " | ".join(normalize(x) for x in value)
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().casefold()

def scalar_values(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if value is None:
        return []
    return [str(value).strip()] if str(value).strip() else []

def looks_generic(value: object) -> bool:
    text = normalize(value)
    if not text:
        return False
    return any(rx.search(text) for rx in GENERIC_RE)

def parse_js_object(text: str) -> object:
    # person_i18n.js is expected to assign the same JSON-compatible object.
    # Extract the first object following a common assignment/export marker.
    markers = [
        "window.PERSON_I18N",
        "window.personI18n",
        "const PERSON_I18N",
        "const personI18n",
        "PERSON_I18N",
    ]
    start = -1
    for marker in markers:
        idx = text.find(marker)
        if idx >= 0:
            eq = text.find("=", idx)
            if eq >= 0:
                brace = text.find("{", eq)
                if brace >= 0:
                    start = brace
                    break
    if start < 0:
        # Fallback: locate the first top-level object.
        start = text.find("{")
    if start < 0:
        raise ValueError("Could not locate the JS data object")

    depth = 0
    in_string = False
    quote = ""
    escaped = False
    end = -1
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                in_string = False
            continue
        if ch in "\"'":
            in_string = True
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end < 0:
        raise ValueError("Unclosed JS object")
    candidate = text[start:end]
    # Most current files use JSON-compatible quoted keys/strings.
    return json.loads(candidate)

def main() -> int:
    for path in (JSON_PATH, JS_PATH, QUIZ_PATH):
        if not path.exists():
            raise FileNotFoundError(path)

    data = load_json(JSON_PATH)
    quiz = load_json(QUIZ_PATH)
    js_text = JS_PATH.read_text(encoding="utf-8")

    report: list[str] = [
        "# Map of Fame — Learning Content Quality Gate",
        "",
        "**Mode:** read-only audit. No project data was modified.",
        "",
    ]

    if not isinstance(data, dict):
        raise TypeError("person_i18n.json root is not an object")

    people = data.get("people", {})
    if not isinstance(people, dict):
        raise TypeError("person_i18n.json `people` is not an object")

    languages = data.get("languages", [])

    if isinstance(languages, list):
        actual_langs = [str(lang) for lang in languages]
    elif isinstance(languages, dict):
        actual_langs = list(languages.keys())
    else:
        raise TypeError("person_i18n.json `languages` must be a list or object")
    report += [
        "## Structure",
        f"- People: **{len(people)}**",
        f"- Languages: **{len(actual_langs)}**",
        f"- Language codes: `{', '.join(actual_langs)}`",
        f"- Expected 15-language set: **{'PASS' if set(actual_langs) == set(EXPECTED_LANGS) else 'FAIL'}**",
        "",
    ]

    missing: list[str] = []
    empty: list[tuple[str, str, str]] = []
    name_only: list[tuple[str, str, str]] = []
    generic: list[tuple[str, str, str]] = []
    cross_dupes: list[tuple[str, str, str, str]] = []
    repeated_across_people: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    internal_dupes: list[tuple[str, str, str, str]] = []

    for pid, person in people.items():
        if not isinstance(person, dict):
            continue
        name = str(person.get("name_en") or person.get("name") or pid)
        langs = person.get("languages", {})
        if not isinstance(langs, dict):
            missing.append(f"{pid}: languages object missing")
            continue

        for lang in EXPECTED_LANGS:
            record = langs.get(lang)
            if not isinstance(record, dict):
                missing.append(f"{pid}/{lang}: language record missing")
                continue

            field_norms: dict[str, str] = {}
            for field in FIELDS:
                if field not in record:
                    missing.append(f"{pid}/{lang}/{field}: missing")
                    continue
                value = record[field]
                vals = scalar_values(value)
                if not vals:
                    empty.append((pid, lang, field))
                    continue

                norm = normalize(value)
                field_norms[field] = norm
                if norm == normalize(name):
                    name_only.append((pid, lang, field))
                if looks_generic(value):
                    generic.append((pid, lang, field))

                # Detect duplicates inside an array field.
                if isinstance(value, list):
                    seen: set[str] = set()
                    for item in value:
                        n = normalize(item)
                        if n in seen and n:
                            internal_dupes.append((pid, lang, field, str(item)))
                        seen.add(n)

                repeated_across_people[(lang, field, norm)].append(pid)

            for i, a in enumerate(FIELDS):
                if a not in field_norms:
                    continue
                for b in FIELDS[i + 1:]:
                    if b in field_norms and field_norms[a] == field_norms[b]:
                        cross_dupes.append((pid, lang, a, b))

    repeated_real = {
        key: sorted(set(ids))
        for key, ids in repeated_across_people.items()
        if len(set(ids)) >= 3 and key[2]
    }

    report += [
        "## Content quality",
        f"- Missing required fields/records: **{len(missing)}**",
        f"- Empty required fields: **{len(empty)}**",
        f"- Name-only fields: **{len(name_only)}**",
        f"- Generic/template hits: **{len(generic)}**",
        f"- Exact cross-field duplicates: **{len(cross_dupes)}**",
        f"- Duplicate items inside arrays: **{len(internal_dupes)}**",
        f"- Repeated identical values across >=3 people: **{len(repeated_real)} value groups**",
        "",
    ]

    by_lang: dict[str, Counter[str]] = {lang: Counter() for lang in EXPECTED_LANGS}
    for pid, lang, field in name_only:
        by_lang[lang]["name_only"] += 1
    for pid, lang, field in generic:
        by_lang[lang]["generic"] += 1
    for pid, lang, a, b in cross_dupes:
        by_lang[lang]["cross_duplicate"] += 1
    for pid, lang, field in empty:
        by_lang[lang]["empty"] += 1

    report += ["### By language", "", "| Language | Name-only | Generic | Cross-field duplicate | Empty |",
               "|---|---:|---:|---:|---:|"]
    for lang in EXPECTED_LANGS:
        c = by_lang[lang]
        report.append(
            f"| `{lang}` | {c['name_only']} | {c['generic']} | "
            f"{c['cross_duplicate']} | {c['empty']} |"
        )
    report.append("")

    report += ["### Most repeated values", "", "| Language | Field | People | Value |",
               "|---|---|---:|---|"]
    for (lang, field, value), ids in sorted(
        repeated_real.items(), key=lambda item: (-len(item[1]), item[0])
    )[:100]:
        display = value.replace("|", "\\|")
        report.append(f"| `{lang}` | `{field}` | {len(ids)} | `{display[:180]}` |")
    report.append("")

    # Quiz/coordinate sanity checks.
    quiz_records = quiz if isinstance(quiz, list) else (
        quiz.get("questions", []) if isinstance(quiz, dict) else []
    )
    invalid_coords: list[tuple[str, str, object]] = []
    if isinstance(quiz_records, list):
        for record in quiz_records:
            if not isinstance(record, dict):
                continue
            for field in ("birth_coordinates", "death_coordinates", "birth_coords", "death_coords"):
                value = record.get(field)
                if value is None:
                    continue
                if (
                    not isinstance(value, list)
                    or len(value) != 2
                    or not all(isinstance(x, (int, float)) for x in value)
                    or not (-90 <= float(value[0]) <= 90)
                    or not (-180 <= float(value[1]) <= 180)
                ):
                    invalid_coords.append((str(record.get("name_en", record.get("name", "?"))), field, value))

    report += [
        "## Coordinates",
        f"- Quiz records inspected: **{len(quiz_records) if isinstance(quiz_records, list) else 0}**",
        f"- Invalid/out-of-range coordinate arrays: **{len(invalid_coords)}**",
        "- Note: this gate checks coordinate syntax/range only; it does **not** declare a coastal, marine, island, river, or Antarctic coordinate wrong.",
        "",
    ]

    # JSON↔JS comparison.
    js_equal = False
    js_error = ""
    try:
        js_data = parse_js_object(js_text)
        js_equal = js_data == data
    except Exception as exc:  # noqa: BLE001
        js_error = f"{type(exc).__name__}: {exc}"

    report += [
        "## JSON ↔ JS",
        f"- Semantic equality: **{'PASS' if js_equal else 'FAIL'}**",
    ]
    if js_error:
        report.append(f"- Parser error: `{js_error}`")
    report.append("")

    # Hard gate is intentionally strict for the known defects.
    gate_pass = (
        len(missing) == 0
        and len(empty) == 0
        and len(name_only) == 0
        and len(generic) == 0
        and len(cross_dupes) == 0
        and len(internal_dupes) == 0
        and len(invalid_coords) == 0
        and js_equal
        and set(actual_langs) == set(EXPECTED_LANGS)
    )

    report += [
        "## FINAL QUALITY GATE",
        f"**{'PASS' if gate_pass else 'FAIL'}**",
        "",
        "This report is diagnostic only. It never rewrites project data.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"People: {len(people)}")
    print(f"Languages: {len(actual_langs)}")
    print(f"Missing: {len(missing)}")
    print(f"Empty: {len(empty)}")
    print(f"Name-only: {len(name_only)}")
    print(f"Generic/template hits: {len(generic)}")
    print(f"Cross-field duplicates: {len(cross_dupes)}")
    print(f"Internal array duplicates: {len(internal_dupes)}")
    print(f"Invalid coordinate arrays: {len(invalid_coords)}")
    print(f"JSON↔JS semantic equality: {js_equal}")
    print(f"FINAL QUALITY GATE: {'PASS' if gate_pass else 'FAIL'}")
    print(f"Report: {REPORT_PATH}")
    return 0 if gate_pass else 2

if __name__ == "__main__":
    raise SystemExit(main())
