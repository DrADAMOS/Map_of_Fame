#!/usr/bin/env python3
"""Validate learning content for placeholders and missing names."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app/src/main/assets/person_i18n.json"
PATTERNS = (
    re.compile(r"^Notable historical work$", re.I),
    re.compile(r"^Notable historical event$", re.I),
    re.compile(r"^Notable fact$", re.I),
    re.compile(r"^Notable work$", re.I),
    re.compile(r"^Notable event$", re.I),
    re.compile(r"^A notable historical figure(?: in the field of .*)?$", re.I),
    re.compile(r"^An important historical fact about this person\.?$", re.I),
    re.compile(r"^A major contribution to the field of .*$", re.I),
    re.compile(r"^A lasting influence on the history of .*$", re.I),
    re.compile(r"^A notable figure in history$", re.I),
)


def contains_placeholder(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return any(p.fullmatch(value.strip()) for p in PATTERNS)
    if isinstance(value, list):
        return any(contains_placeholder(v) for v in value)
    if isinstance(value, dict):
        return any(contains_placeholder(v) for v in value.values())
    return False


def main() -> int:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    people = payload.get("people", {})
    errors: list[str] = []
    for person, record in people.items():
        for lang, content in record.get("languages", {}).items():
            for field in ("bio", "achievements", "key_facts", "wars", "historical_significance"):
                if contains_placeholder(content.get(field, "")):
                    errors.append(f"{person}/{lang}/{field}: placeholder")
            if not content.get("name"):
                errors.append(f"{person}/{lang}/name: missing")
    print(f"people={len(people)} errors={len(errors)}")
    if errors:
        print("\n".join(errors[:100]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
