#!/usr/bin/env python3
"""Apply verified canonical learning content to the Map of Fame Android project.

Default mode is a dry run. Use --apply to modify the project.
Only the canonical language fields supplied by the source file are changed.
All other languages and person metadata remain untouched.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

FIELDS = (
    "hint",
    "bio",
    "achievements",
    "key_facts",
    "wars",
    "historical_significance",
)

GENERIC_PATTERNS = (
    re.compile(r"\brenowned\s+(writer|artist|musician|ruler|philosopher|scientist|military leader)\b", re.I),
    re.compile(r"\bremembered for shaping historical developments\b", re.I),
    re.compile(r"\bremembered for\b.*\bdevelopments\b", re.I),
    re.compile(r"حققت أثراً كبيراً وإنجازات تاريخية", re.I),
    re.compile(r"تركت أثراً تاريخياً", re.I),
    re.compile(r"تعد حلقة بارزة في عصر", re.I),
)

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
CANONICAL_PATH = ROOT / "tools" / "canonical" / "people_learning_en.json"
BACKUP_DIR = ROOT / "tools" / "backups"


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        fail(f"{path} root must be an object")
    return value


def scalar_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def validate_record(name: str, record: dict[str, Any]) -> None:
    for field in FIELDS:
        if field not in record:
            fail(f"{name}: missing canonical field {field!r}")

    hint = record["hint"]
    bio = record["bio"]
    significance = record["historical_significance"]

    if not isinstance(hint, str) or len(hint.strip()) < 30:
        fail(f"{name}: hint is too short")
    if not isinstance(bio, str) or len(bio.strip()) < 120:
        fail(f"{name}: bio is too short")
    if not isinstance(significance, str) or len(significance.strip()) < 80:
        fail(f"{name}: historical_significance is too short")

    for field in ("achievements", "key_facts"):
        value = record[field]
        if not isinstance(value, list) or not 2 <= len(value) <= 5:
            fail(f"{name}: {field} must contain 2–5 items")
        if any(not isinstance(item, str) or len(item.strip()) < 20 for item in value):
            fail(f"{name}: {field} contains a short/non-string item")
        if len({item.strip().casefold() for item in value}) != len(value):
            fail(f"{name}: duplicate items in {field}")

    wars = record["wars"]
    if not isinstance(wars, list):
        fail(f"{name}: wars must be a list")
    if len(wars) > 5:
        fail(f"{name}: wars contains more than 5 items")

    all_strings = [hint, bio, significance]
    all_strings += record["achievements"] + record["key_facts"] + wars
    for text in all_strings:
        for pattern in GENERIC_PATTERNS:
            if pattern.search(text):
                fail(f"{name}: generic/template text detected: {text!r}")

    normalized = {
        field: " ".join(scalar_values(record[field])).casefold()
        for field in ("hint", "bio", "historical_significance")
    }
    if normalized["bio"] == normalized["historical_significance"]:
        fail(f"{name}: bio and historical_significance are identical")

    arrays = {
        field: {" ".join(item.split()).casefold() for item in record[field]}
        for field in ("achievements", "key_facts", "wars")
    }
    overlap = arrays["achievements"] & arrays["key_facts"]
    if overlap:
        fail(f"{name}: achievement/key_fact exact overlap: {sorted(overlap)!r}")


def extract_js_object(text: str) -> dict[str, Any]:
    marker = "window.PERSON_I18N"
    start = text.find(marker)
    if start < 0:
        fail("person_i18n.js does not contain window.PERSON_I18N")

    start = text.find("{", start)
    if start < 0:
        fail("Could not locate JS data object")

    depth = 0
    in_string = False
    quote = ""
    escaped = False
    end = -1

    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue

        if char in ('"', "'"):
            in_string = True
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                break

    if end < 0:
        fail("Unclosed JS object")

    candidate = text[start:end]
    return json.loads(candidate)


def find_person(people: dict[str, Any], canonical_name: str) -> tuple[str, dict[str, Any]]:
    exact = people.get(canonical_name)
    if isinstance(exact, dict):
        return canonical_name, exact

    for key, value in people.items():
        if not isinstance(value, dict):
            continue
        candidates = (
            str(value.get("name_en", "")),
            str(value.get("name", "")),
        )
        if canonical_name in candidates:
            return str(key), value

    fail(f"Canonical person not found in project: {canonical_name}")


def atomic_write(path: Path, text: str) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def build_js(data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f"window.PERSON_I18N = {payload};\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes to the Android project")
    parser.add_argument("--canonical", type=Path, default=CANONICAL_PATH)
    args = parser.parse_args()

    for path in (JSON_PATH, JS_PATH, args.canonical):
        if not path.exists():
            fail(f"Required file not found: {path}")

    data = load_json(JSON_PATH)
    canonical = load_json(args.canonical)

    people = data.get("people")
    if not isinstance(people, dict):
        fail("person_i18n.json: people must be an object")

    if canonical.get("language") != "en":
        fail("Canonical source language must be en")

    canonical_people = canonical.get("people")
    if not isinstance(canonical_people, dict) or not canonical_people:
        fail("Canonical source has no people")

    prepared: list[tuple[str, str, dict[str, Any]]] = []

    for name, source_record in canonical_people.items():
        if not isinstance(source_record, dict):
            fail(f"{name}: canonical record must be an object")
        validate_record(str(name), source_record)

        pid, person = find_person(people, str(name))
        languages = person.get("languages")
        if not isinstance(languages, dict):
            fail(f"{pid}: languages must be an object")

        existing_en = languages.get("en")
        if not isinstance(existing_en, dict):
            fail(f"{pid}: English language record is missing")

        prepared.append((str(name), pid, source_record))

    print(f"Project: {ROOT}")
    print(f"Canonical records: {len(prepared)}")
    print("Mode:", "APPLY" if args.apply else "DRY-RUN")
    print()

    for name, pid, source_record in prepared:
        print(f"  {'UPDATE' if args.apply else 'WOULD UPDATE'}  {pid} <- {name} [en]")

    if not args.apply:
        print("\nDry run complete. No project files were modified.")
        return 0

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    json_backup = BACKUP_DIR / f"person_i18n_{timestamp}.json"
    js_backup = BACKUP_DIR / f"person_i18n_{timestamp}.js"
    json_backup.write_bytes(JSON_PATH.read_bytes())
    js_backup.write_bytes(JS_PATH.read_bytes())

    updated = copy.deepcopy(data)

    for name, pid, source_record in prepared:
        person = updated["people"][pid]
        languages = person["languages"]
        current = dict(languages["en"])
        current.update(copy.deepcopy(source_record))
        current["name"] = current.get("name") or person.get("name_en") or name
        languages["en"] = current

    json_text = json.dumps(updated, ensure_ascii=False, indent=2) + "\n"
    js_text = build_js(updated)

    atomic_write(JSON_PATH, json_text)
    atomic_write(JS_PATH, js_text)

    # Immediate semantic verification.
    written_json = load_json(JSON_PATH)
    written_js = extract_js_object(JS_PATH.read_text(encoding="utf-8"))
    if written_json != written_js:
        # Restore before failing.
        JSON_PATH.write_bytes(json_backup.read_bytes())
        JS_PATH.write_bytes(js_backup.read_bytes())
        fail("JSON↔JS semantic equality failed; original files restored")

    print()
    print("APPLIED successfully.")
    print(f"Backup JSON: {json_backup}")
    print(f"Backup JS:   {js_backup}")
    print("JSON↔JS semantic equality: PASS")
    print("Only English learning-content records in the pilot set were changed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
