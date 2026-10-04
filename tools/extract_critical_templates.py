import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUT = ROOT / "MAP_OF_FAME_CRITICAL_TEMPLATES.md"

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
        return " ".join(value.split()).strip()

    if isinstance(value, list):
        return " || ".join(
            " ".join(str(x).split()).strip()
            for x in value
        )

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
    )


def main():
    with JSON_PATH.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    people = data["people"]

    if not isinstance(people, dict):
        raise RuntimeError("data['people'] is not an object")

    counters = {
        field: Counter()
        for field in FIELDS
    }

    locations = {
        field: defaultdict(list)
        for field in FIELDS
    }

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

                value = normalize(localized[field])

                if not value:
                    continue

                counters[field][value] += 1
                locations[field][value].append(
                    (language, person)
                )

    lines = [
        "# Map of Fame — Critical Exact Templates",
        "",
        "Threshold: values repeated 10 or more times.",
        "",
    ]

    all_templates = []

    for field in FIELDS:
        for text, count in counters[field].items():
            if count >= 10:
                all_templates.append(
                    (
                        count,
                        field,
                        text,
                        locations[field][text],
                    )
                )

    all_templates.sort(
        key=lambda x: (-x[0], x[1], x[2])
    )

    for index, (count, field, text, locs) in enumerate(
        all_templates,
        start=1,
    ):

        lines.append(
            f"## {index}. {field} — {count} uses"
        )
        lines.append("")
        lines.append("### Template")
        lines.append("")
        lines.append("```text")
        lines.append(text)
        lines.append("```")
        lines.append("")
        lines.append("### Locations")
        lines.append("")

        for language, person in locs:
            lines.append(
                f"- `{language}` — {person}"
            )

        lines.append("")

    OUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"Critical templates: {len(all_templates)}"
    )
    print(f"Report: {OUT}")
    print("")

    for count, field, text, locs in all_templates:
        preview = text.replace("\n", " ")

        if len(preview) > 100:
            preview = preview[:100] + "..."

        print(
            f"{count:3}x | "
            f"{field:24} | "
            f"{preview}"
        )


if __name__ == "__main__":
    main()
