from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "MAP_OF_FAME_TEMPLATE_ANALYSIS.md"
OUT = ROOT / "tools" / "template_index.txt"

lines = REPORT.read_text(encoding="utf-8-sig").splitlines()

current_field = None
current_number = None
current_count = None
locations = []
text_lines = []

records = []

def flush():
    global current_number, current_count, locations, text_lines

    if current_field is None or current_number is None:
        return

    text = "\n".join(text_lines).strip()

    if text:
        records.append({
            "field": current_field,
            "number": current_number,
            "count": current_count,
            "locations": list(locations),
            "text": text,
        })

    locations = []
    text_lines = []

for line in lines:
    stripped = line.strip()

    if stripped.startswith("## "):
        current_field = stripped[3:].strip()
        current_number = None
        current_count = None
        locations = []
        text_lines = []
        continue

    match = re.match(r"^###\s+(\d+)\.\s+Used\s+(\d+)\s+times$", stripped)

    if match:
        flush()
        current_number = int(match.group(1))
        current_count = int(match.group(2))
        continue

    if stripped.startswith("- `") and " — " in stripped:
        locations.append(stripped[2:])
        continue

    if stripped == "**Text:**":
        continue

    if stripped.startswith("```"):
        continue

    if current_number is not None and stripped:
        text_lines.append(stripped)

flush()

with OUT.open("w", encoding="utf-8") as handle:

    for record in records:
        handle.write(
            f"[{record['field']}] "
            f"#{record['number']} "
            f"USED={record['count']}\n"
        )

        handle.write(
            f"TEXT={record['text']}\n"
        )

        handle.write("LOCATIONS:\n")

        for location in record["locations"]:
            handle.write(f"  {location}\n")

        handle.write("\n")

print(f"Extracted {len(records)} repeated templates.")
print(f"Index: {OUT}")

print("")
print("Top repeated templates:")

for record in sorted(
    records,
    key=lambda x: x["count"],
    reverse=True
)[:25]:

    print(
        f"{record['count']:3}x | "
        f"{record['field']:24} | "
        f"{record['text'][:100]}"
    )
