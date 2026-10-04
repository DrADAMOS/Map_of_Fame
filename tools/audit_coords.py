import json
import os

json_path = os.path.join("H:", "Android", "Projects", "MapofFame", "app", "main", "assets", "person_i18n.json")
# Or relative
json_path = "../app/src/main/assets/person_i18n.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

people = data.get("people", {})
total_people = len(people)
print(f"Total people: {total_people}")
