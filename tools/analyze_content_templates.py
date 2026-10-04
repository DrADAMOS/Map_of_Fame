import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUT = ROOT / "MAP_OF_FAME_TEMPLATE_ANALYSIS.md"

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

    if isinstance(value, list):
        return " || ".join(normalize(x) for x in value)

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
    )


def main():
    with JSON_PATH.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)

    people = data.get("people")

    if not isinstance(people, dict):
        raise RuntimeError("data['people'] is not an object")

    counters = {}

    for field in FIELDS:
        counters[field] = Counter()

    locations = {}

    for person, record in people.items():

        if not isinstance(record, dict):
            continue

        languages = record.get("languages")

        if not isinstance(languages, dict):
            continue

        for language, localized in languages.items():

            if not isinstance(localized, dict):
                continue

            for field in FIELDS:

                if field not in localized:
                    continue

                value = localized[field]
                key = normalize(value)

                if not key:
                    continue

                counters[field][key] += 1

                locations.setdefault(
                    (field, key),
                    [],
                ).append(
                    (person, language)
                )

    lines = []

    lines.append("# Map of Fame — Template / Exact Duplicate Analysis")
    lines.append("")
    lines.append("This report is read-only and does not modify project data.")
    lines.append("")

    for field in FIELDS:

        lines.append("")
        lines.append(f"## {field}")
        lines.append("")

        repeated = [
            (text, count)
            for text, count in counters[field].items()
            if count >= 3
        ]

        repeated.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        if not repeated:
            lines.append("No exact repeated values found >= 3.")
            continue

        for index, (text, count) in enumerate(
            repeated[:50],
            start=1,
        ):
            lines.append(
                f"### {index}. Used {count} times"
            )

            locations_list = locations[(field, text)]

            sample_locations = locations_list[:20]

            lines.append("")
            lines.append("**Locations:**")

            for person, language in sample_locations:
                lines.append(
                    f"- `{language}` — {person}"
                )

            if len(locations_list) > 20:
                lines.append(
                    f"- ... and {len(locations_list) - 20} more"
                )

            lines.append("")
            lines.append("**Text:**")
            lines.append("")
            lines.append("```text")
            lines.append(text)
            lines.append("```")
            lines.append("")

    OUT.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("Template analysis completed.")
    print(f"Report: {OUT}")

    print("")
    print("Repeated exact values by field:")

    for field in FIELDS:
        repeated_count = sum(
            1
            for count in counters[field].values()
            if count >= 3
        )

        print(
            f"  {field}: {repeated_count}"
        )


if __name__ == "__main__":
    main()
