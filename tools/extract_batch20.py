import json

path = r".\app\src\main\assets\person_i18n.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

people = data["people"]

targets = [
    "حققت أثراً كبيراً وإنجازات تاريخية كـ أديب",
    "حققت أثراً كبيراً وإنجازات تاريخية كـ موسيقي",
    "حققت أثراً كبيراً وإنجازات تاريخية كـ فنان",
    "حققت أثراً كبيراً وإنجازات تاريخية كـ عالم",
    "حققت أثراً كبيراً وإنجازات تاريخية كـ قائد عسكري",
    "حققت أثراً كبيراً وإنجازات تاريخية كـ سياسي",
]

matches = []

for person_id, person in people.items():
    if not isinstance(person, dict):
        continue

    languages = person.get("languages", {})
    if not isinstance(languages, dict):
        continue

    en = languages.get("en", {})
    ar = languages.get("ar", {})

    if not isinstance(en, dict) or not isinstance(ar, dict):
        continue

    name = en.get("name", "")
    achievements = ar.get("achievements", [])

    if not isinstance(achievements, list):
        continue

    matched = [a for a in achievements if a in targets]

    if matched:
        matches.append(
            f"{person_id} | {name} | {matched}"
        )

out = r".\tools\batch20_matches.txt"

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(matches))

print(f"Matches written: {len(matches)}")
print(f"Output: {out}")
