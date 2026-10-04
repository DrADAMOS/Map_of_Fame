#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
QUIZ = ASSETS / "quiz_data.json"
I18N = ASSETS / "person_i18n.json"
REPORT = ROOT / "IDENTITY_RECONCILIATION_REPORT.json"

GROUPS = {
    "Wolfgang Amadeus Mozart": ["Mozart", "Wolfgang Amadeus Mozart"],
    "Ludwig van Beethoven": ["Beethoven", "Ludwig van Beethoven"],
    "Ibn Saud": ["Ibn Saud", "King Abdulaziz"],
}

PLACEHOLDERS = {
    "Notable historical work",
    "Important historical fact",
    "A notable historical figure...",
}


def meaningful(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, list):
        return any(meaningful(item) for item in value)
    if isinstance(value, str):
        text = value.strip()
        return bool(text) and text not in PLACEHOLDERS and "notable historical figure" not in text.lower()
    return True


def merge_value(canonical: object, alias: object) -> object:
    if meaningful(canonical):
        return canonical
    return deepcopy(alias) if meaningful(alias) else canonical


def merge_record(canonical: dict, alias: dict) -> dict:
    result = deepcopy(canonical)
    for key, value in alias.items():
        if key not in result or not meaningful(result[key]):
            if meaningful(value):
                result[key] = deepcopy(value)
    return result


def main() -> int:
    quiz = json.loads(QUIZ.read_text(encoding="utf-8"))
    original_count = len(quiz)
    by_name = {str(p.get("name_en") or p.get("name")): p for p in quiz}
    removed: list[dict[str, object]] = []
    merged: list[dict[str, object]] = []

    for canonical_name, names in GROUPS.items():
        if canonical_name not in by_name:
            raise RuntimeError(f"Canonical record missing: {canonical_name}")
        canonical = by_name[canonical_name]
        aliases = [n for n in names if n != canonical_name and n in by_name]
        for alias_name in aliases:
            canonical = merge_record(canonical, by_name[alias_name])
            removed.append({"alias": alias_name, "canonical": canonical_name})
        by_name[canonical_name] = canonical
        merged.append({"canonical": canonical_name, "aliases": aliases})

    new_quiz = []
    removed_names = {x["alias"] for x in removed}
    for person in quiz:
        name = str(person.get("name_en") or person.get("name"))
        if name in removed_names:
            continue
        if name in by_name:
            new_quiz.append(by_name[name])
        else:
            new_quiz.append(person)

    I18N_backup = json.loads(I18N.read_text(encoding="utf-8"))
    people_i18n = I18N_backup.get("people", {})
    i18n_removed = []
    for group in merged:
        canonical = group["canonical"]
        canonical_data = deepcopy(people_i18n.get(canonical, {}))
        for alias in group["aliases"]:
            alias_data = people_i18n.get(alias)
            if isinstance(alias_data, dict):
                canonical_data = merge_record(canonical_data, alias_data)
                i18n_removed.append(alias)
        if canonical_data:
            people_i18n[canonical] = canonical_data
        for alias in group["aliases"]:
            people_i18n.pop(alias, None)

    quiz_out = json.dumps(new_quiz, ensure_ascii=False, indent=2) + "\n"
    QUIZ.write_text(quiz_out, encoding="utf-8")
    I18N_backup["people"] = people_i18n
    I18N.write_text(json.dumps(I18N_backup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = {
        "schema": 1,
        "policy": "merge confirmed duplicate historical identities; preserve canonical records; remove aliases",
        "original_quiz_people": original_count,
        "final_quiz_people": len(new_quiz),
        "merged_groups": merged,
        "removed_quiz_aliases": removed,
        "removed_i18n_aliases": i18n_removed,
        "remaining_unique_identities": len(new_quiz),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
