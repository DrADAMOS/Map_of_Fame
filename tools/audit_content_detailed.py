import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUT = ROOT / "MAP_OF_FAME_CONTENT_AUDIT.md"

GENERIC_PATTERNS = [
    "renowned",
    "famous",
    "well-known",
    "historically significant",
    "remembered for shaping",
    "left a lasting historical impact",
    "made significant contributions",
    "prominent figure",
    "historical developments",
    "cultural developments",
    "scientific developments",
    "شخصية بارزة",
    "شخصية مهمة",
    "شخصية تاريخية بارزة",
    "اشتهر بإسهاماته",
    "اشتهرت بإسهاماتها",
    "ترك أثراً تاريخياً",
    "تركت أثراً تاريخياً",
    "حقق أثراً كبيراً",
    "حققت أثراً كبيراً",
    "كان له أثر كبير",
    "كان لها أثر كبير",
    "يعد من أبرز",
    "تعد من أبرز",
    "من أهم الشخصيات",
    "من أبرز الشخصيات",
    "من الشخصيات البارزة",
    "حلقة بارزة",
]

FIELDS = [
    "hint",
    "bio",
    "achievements",
    "key_facts",
    "wars",
    "historical_significance",
]


def normalize(value):
    if isinstance(value, str):
        return " ".join(value.lower().split())

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
    )


def generic_matches(value):
    text = normalize(value)

    return [
        pattern
        for pattern in GENERIC_PATTERNS
        if pattern.lower() in text
    ]


def main():
    with JSON_PATH.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise RuntimeError("person_i18n.json is not an object")

    people = data.get("people")

    if not isinstance(people, dict):
        raise RuntimeError(
            f"Expected data['people'] to be an object, "
            f"got {type(people).__name__}"
        )

    hits = []

    by_language = Counter()
    by_field = Counter()
    by_person = Counter()
    by_pattern = Counter()

    profile_count = 0
    invalid_people = []

    for person, record in people.items():

        if not isinstance(record, dict):
            invalid_people.append(person)
            continue

        languages = record.get("languages")

        if not isinstance(languages, dict):
            invalid_people.append(person)
            continue

        profile_count += 1

        for language, localized in languages.items():

            if not isinstance(localized, dict):
                continue

            for field in FIELDS:

                if field not in localized:
                    continue

                value = localized[field]
                matches = generic_matches(value)

                for pattern in matches:
                    hits.append(
                        (
                            person,
                            language,
                            field,
                            pattern,
                            value,
                        )
                    )

                    by_language[language] += 1
                    by_field[field] += 1
                    by_person[person] += 1
                    by_pattern[pattern] += 1

    lines = []

    lines.append("# Map of Fame — Detailed Content Audit")
    lines.append("")
    lines.append(f"- Top-level JSON entries: **{len(data)}**")
    lines.append(f"- Person profiles detected: **{profile_count}**")
    lines.append(f"- Invalid person records: **{len(invalid_people)}**")
    lines.append(
        f"- Generic hits detected by this audit: **{len(hits)}**"
    )
    lines.append("")

    lines.append("## Invalid person records")
    lines.append("")

    if invalid_people:
        for person in invalid_people:
            lines.append(f"- `{person}`")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Generic hits by language")
    lines.append("")

    if by_language:
        for language, count in by_language.most_common():
            lines.append(f"- `{language}`: **{count}**")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Generic hits by field")
    lines.append("")

    if by_field:
        for field, count in by_field.most_common():
            lines.append(f"- `{field}`: **{count}**")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Most affected people")
    lines.append("")

    if by_person:
        for person, count in by_person.most_common(100):
            lines.append(f"- **{person}** — {count}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Most common patterns")
    lines.append("")

    if by_pattern:
        for pattern, count in by_pattern.most_common():
            lines.append(f"- `{pattern}` — {count}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Detailed hits")
    lines.append("")

    current_person = None

    for person, language, field, pattern, value in hits:

        if person != current_person:
            lines.append("")
            lines.append(f"### {person}")
            current_person = person

        preview = normalize(value)

        if len(preview) > 700:
            preview = preview[:700] + "..."

        lines.append(
            f"- `{language}` / `{field}` / `{pattern}`"
        )
        lines.append(f"  - {preview}")

    OUT.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("Detailed content audit completed.")
    print(f"Person profiles detected: {profile_count}")
    print(f"Invalid person records: {len(invalid_people)}")
    print(f"Generic hits detected: {len(hits)}")
    print("")
    print("Top languages:")

    for language, count in by_language.most_common():
        print(f"  {language}: {count}")

    print("")
    print("Top fields:")

    for field, count in by_field.most_common():
        print(f"  {field}: {count}")

    print("")
    print("Top 20 people:")

    for person, count in by_person.most_common(20):
        print(f"  {count:3}  {person}")

    print("")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
