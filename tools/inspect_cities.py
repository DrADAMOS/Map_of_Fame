import json

with open("app/src/main/assets/quiz_data.json", "r", encoding="utf-8") as f:
    quiz_data = json.load(f)

cities = set()
for p in quiz_data:
    if p.get("birth_city"): cities.add(p["birth_city"])
    if p.get("death_city"): cities.add(p["death_city"])

print(f"Total unique cities in quiz_data: {len(cities)}")
print(list(cities)[:20])
