from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"

def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]

    missing_or_short = []
    generic = []

    generic_fragments = (
        "حققت أثراً كبيراً وإنجازات تاريخية كـ",
        "إنجازات تاريخية كـ",
    )

    for person in people.values():
        if not isinstance(person, dict):
            continue
        languages = person.get("languages", {})
        if not isinstance(languages, dict):
            continue

        en = languages.get("en", {})
        ar = languages.get("ar", {})
        name = en.get("name", "<unknown>")
        achievements = ar.get("achievements")

        if not isinstance(achievements, list) or len(achievements) < 2:
            missing_or_short.append(
                (name, type(achievements).__name__, len(achievements) if isinstance(achievements, list) else 0)
            )

        if isinstance(achievements, list):
            joined = " | ".join(str(x) for x in achievements)
            if any(fragment in joined for fragment in generic_fragments):
                generic.append((name, joined))

    print(f"People: {len(people)}")
    print(f"Arabic achievements >=2: {len(people) - len(missing_or_short)}")
    print(f"Arabic achievements missing/short: {len(missing_or_short)}")
    print()
    print("MISSING / SHORT:")
    for i, (name, typ, count) in enumerate(missing_or_short, 1):
        print(f"{i:03d}. {name} | type={typ} | count={count}")

    print()
    print(f"GENERIC ARABIC ACHIEVEMENT RECORDS STILL PRESENT: {len(generic)}")
    for i, (name, value) in enumerate(generic, 1):
        print(f"{i:03d}. {name} | {value}")

if __name__ == "__main__":
    main()
