import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUT = ROOT / "MAP_OF_FAME_TEMPLATE_ANALYSIS_DIRECT.md"

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
            " ".join(str(item).split()).strip()
            for item in value
        )

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

    counters = {
        field: Counter()
        for field in FIELDS
    }

    locations = {
        field: defaultdict(list)
        for field in FIELDS
    }

    total_profiles = 0

    for person, record in people.items():

        if not isinstance(record, dict):
            continue

        languages = record.get("languages")

        if not isinstance(languages, dict):
            continue

        total_profiles += 1

        for language, localized in languages.items():

            if not isinstance(localized, dict):
                continue

            for field in FIELDS:

                if field not in localized:
                    continue

                normalized = normalize(localized[field])

                if not normalized:
                    continue

                counters[field][normalized] += 1

                locations[field][normalized].append(
                    (language, person)
                )

    lines = []

    lines.append("# Map of Fame — Direct Template Analysis")
    lines.append("")
    lines.append(
        f"Profiles analyzed: **{total_profiles}**"
    )
    lines.append("")
    lines.append(
        "Only exact repeated values are listed. "
        "This report does not modify project files."
    )
    lines.append("")

    grand_total = 0

    for field in FIELDS:

        repeated = [
            (text, count)
            for text, count in counters[field].items()
            if count >= 3
        ]

        repeated.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        lines.append("")
        lines.append(f"## {field}")
        lines.append("")
        lines.append(
            f"Repeated values >= 3: **{len(repeated)}**"
        )
        lines.append("")

        for index, (text, count) in enumerate(
            repeated,
            start=1,
        ):

            grand_total += count

            lines.append(
                f"### {index}. USED={count}"
            )

            lines.append("")
            lines.append("**TEXT:**")
            lines.append("")
            lines.append("```text")
            lines.append(text)
            lines.append("```")
            lines.append("")

            lines.append("**LOCATIONS:**")

            for language, person in locations[field][text]:
                lines.append(
                    f"- `{language}` — {person}"
                )

            lines.append("")

    lines.append("")
    lines.append(
        f"Total repeated-value occurrences: **{grand_total}**"
    )

    OUT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("Direct template analysis completed.")
    print(f"Profiles analyzed: {total_profiles}")
    print(f"Report: {OUT}")
    print("")

    for field in FIELDS:

        repeated = [
            count
            for count in counters[field].values()
            if count >= 3
        ]

        print(
            f"{field:24} "
            f"{len(repeated):3} repeated values"
        )

    print("")
    print("Top 30 exact repeated values:")

    all_repeated = []

    for field in FIELDS:
        for text, count in counters[field].items():
            if count >= 3:
                all_repeated.append(
                    (count, field, text)
                )

    all_repeated.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    for count, field, text in all_repeated[:30]:
        preview = text.replace("\n", " ")

        if len(preview) > 120:
            preview = preview[:120] + "..."

        print(
            f"{count:3}x | "
            f"{field:24} | "
            f"{preview}"
        )


if __name__ == "__main__":
    main()
