#!/usr/bin/env python3
"""Rebuild the Wikipedia identity review for the current quiz population.

This script is intentionally offline:
- quiz_data.json is the source of truth for the current people.
- The recovered 289-person identity review is reused where possible.
- Known aliases are reconciled explicitly.
- New quiz people remain unresolved rather than being guessed.
- person_i18n.json is never modified.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

QUIZ_FILE = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
RECOVERED_FILE = ROOT / "WIKIPEDIA_IDENTITY_REVIEW_RECOVERED.json"
OUTPUT_FILE = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
REPORT_FILE = ROOT / "IDENTITY_REVIEW_REBUILD_REPORT.json"


# Existing names that were intentionally represented under another
# canonical identity in the recovered review.
ALIASES: dict[str, str] = {
    "Martin Luther King Jr.": "Martin Luther King",
    "Napoleon Bonaparte": "Napoleon",
    "Omar Mukhtar": "Omar al-Mukhtar",
}


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"Required file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_quiz_names(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        raise ValueError("quiz_data.json must contain a JSON list")

    names: list[str] = []

    for index, person in enumerate(payload):
        if not isinstance(person, dict):
            raise ValueError(
                f"quiz_data.json record {index} is not an object"
            )

        name = person.get("name_en") or person.get("name")

        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                f"quiz_data.json record {index} has no valid name"
            )

        names.append(name.strip())

    if len(names) != len(set(names)):
        duplicates = sorted(
            {
                name
                for name in names
                if names.count(name) > 1
            }
        )
        raise ValueError(
            "quiz_data.json contains duplicate person names: "
            + ", ".join(duplicates)
        )

    return names


def extract_review_people(payload: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        raise ValueError("Recovered identity review must be a JSON object")

    people = payload.get("people")

    if not isinstance(people, dict):
        raise ValueError(
            "Recovered identity review has no valid 'people' object"
        )

    result: dict[str, dict[str, Any]] = {}

    for name, record in people.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Identity review contains an invalid person name")

        if not isinstance(record, dict):
            raise ValueError(
                f"Identity review record for {name!r} is not an object"
            )

        result[name.strip()] = record

    return result


def make_unresolved_record(name: str) -> dict[str, Any]:
    """Create a deliberately unresolved record.

    No Wikipedia title or identity is guessed here.
    """

    return {
        "query": name,
        "status": "unresolved",
        "best_title": None,
        "score": 0,
        "candidates": [],
        "reason": "New current quiz person; requires identity verification.",
    }


def clone_record(record: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(record, ensure_ascii=False))


def rebuild(
    quiz_names: list[str],
    recovered_people: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    rebuilt: dict[str, dict[str, Any]] = {}

    preserved: list[str] = []
    mapped: list[dict[str, str]] = []
    unresolved: list[str] = []
    removed: list[str] = []

    recovered_names = set(recovered_people)

    for quiz_name in quiz_names:
        if quiz_name in recovered_people:
            rebuilt[quiz_name] = clone_record(
                recovered_people[quiz_name]
            )
            preserved.append(quiz_name)
            continue

        source_name = ALIASES.get(quiz_name)

        if source_name is not None and source_name in recovered_people:
            record = clone_record(recovered_people[source_name])

            # Keep the current quiz name as the query/name key while
            # preserving the recovered canonical Wikipedia identity.
            record["query"] = quiz_name

            rebuilt[quiz_name] = record

            mapped.append(
                {
                    "quiz_name": quiz_name,
                    "recovered_name": source_name,
                }
            )
            continue

        rebuilt[quiz_name] = make_unresolved_record(quiz_name)
        unresolved.append(quiz_name)

    quiz_set = set(quiz_names)

    for recovered_name in sorted(recovered_names - quiz_set):
        if recovered_name in ALIASES.values():
            # The record was consumed by an explicit alias mapping.
            alias_target = next(
                (
                    quiz_name
                    for quiz_name, source_name in ALIASES.items()
                    if source_name == recovered_name
                    and quiz_name in quiz_set
                ),
                None,
            )

            if alias_target is not None:
                continue

        removed.append(recovered_name)

    report = {
        "schema": 1,
        "source": {
            "quiz_file": str(QUIZ_FILE.relative_to(ROOT)),
            "recovered_identity_review": str(
                RECOVERED_FILE.relative_to(ROOT)
            ),
        },
        "counts": {
            "current_quiz_people": len(quiz_names),
            "recovered_review_people": len(recovered_people),
            "rebuilt_review_people": len(rebuilt),
            "preserved": len(preserved),
            "mapped_aliases": len(mapped),
            "new_unresolved": len(unresolved),
            "removed_old_only": len(removed),
        },
        "preserved": sorted(preserved),
        "mapped_aliases": mapped,
        "new_unresolved": sorted(unresolved),
        "removed_old_only": sorted(removed),
    }

    return rebuilt, report


def write_json(path: Path, payload: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")

    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=False,
            indent=2,
        )
        handle.write("\n")

    temporary.replace(path)


def main() -> int:
    print("=" * 72)
    print("REBUILD WIKIPEDIA IDENTITY REVIEW")
    print("=" * 72)

    quiz_payload = load_json(QUIZ_FILE)
    recovered_payload = load_json(RECOVERED_FILE)

    quiz_names = extract_quiz_names(quiz_payload)
    recovered_people = extract_review_people(recovered_payload)

    rebuilt_people, report = rebuild(
        quiz_names,
        recovered_people,
    )

    if len(rebuilt_people) != len(quiz_names):
        raise RuntimeError(
            "Rebuild count mismatch: "
            f"quiz={len(quiz_names)} "
            f"rebuilt={len(rebuilt_people)}"
        )

    if set(rebuilt_people) != set(quiz_names):
        missing = sorted(set(quiz_names) - set(rebuilt_people))
        extra = sorted(set(rebuilt_people) - set(quiz_names))

        raise RuntimeError(
            "Rebuild identity mismatch. "
            f"missing={missing} extra={extra}"
        )

    output_payload = {
        "schema": 2,
        "generated_offline": True,
        "source": "quiz_data.json + recovered identity review",
        "people": rebuilt_people,
        "unresolved": sorted(report["new_unresolved"]),
    }

    write_json(OUTPUT_FILE, output_payload)
    write_json(REPORT_FILE, report)

    print()
    print(f"Current quiz people : {len(quiz_names)}")
    print(f"Recovered identities: {len(recovered_people)}")
    print(f"Rebuilt identities  : {len(rebuilt_people)}")
    print(f"Preserved           : {report['counts']['preserved']}")
    print(f"Alias mappings      : {report['counts']['mapped_aliases']}")
    print(f"New unresolved      : {report['counts']['new_unresolved']}")
    print(f"Removed old-only    : {report['counts']['removed_old_only']}")
    print()
    print(f"Created: {OUTPUT_FILE}")
    print(f"Created: {REPORT_FILE}")
    print()
    print("No network access was used.")
    print("person_i18n.json was not modified.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
