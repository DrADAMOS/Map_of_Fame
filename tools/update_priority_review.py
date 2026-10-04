import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def update_priority():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    with open(person_path, "r", encoding="utf-8") as f:
        person_data = json.load(f)

    people_i18n = person_data.get("people", {})

    target_people = [
        "Edwin Hubble",
        "Omar al-Mukhtar",
        "Genghis Khan",
        "Ahmad ibn Tulun",
        "Sophocles",
        "Napoleon",
        "Peter the Great",
        "Fyodor Dostoevsky",
        "Alexander Suvorov",
        "Frederick II"
    ]

    quiz_map = {}
    for p in quiz_data:
        en_name = p.get("name_en") or p.get("name") or ""
        quiz_map[en_name] = p

    priority_records = []

    for target in target_people:
        matched_name = None
        for en_name in quiz_map:
            if target.lower() in en_name.lower() or en_name.lower() in target.lower():
                matched_name = en_name
                break
        if not matched_name and "mukhtar" in target.lower():
            for en_name in quiz_map:
                if "mukhtar" in en_name.lower():
                    matched_name = en_name
                    break

        if not matched_name:
            continue

        p_obj = quiz_map[matched_name]
        i18n_entry = people_i18n.get(matched_name, {})
        i18n_en = i18n_entry.get("languages", {}).get("en", {})

        i18n_bc = i18n_en.get("birth_city", "N/A")
        i18n_bco = i18n_en.get("birth_country", "N/A")
        i18n_dc = i18n_en.get("death_city", "N/A")
        i18n_dco = i18n_en.get("death_country", "N/A")

        bc = p_obj.get("bc")
        dc = p_obj.get("dc")

        if bc:
            priority_records.append({
                "Person": matched_name,
                "Field": "Birth",
                "City": p_obj.get("birth_city"),
                "Country": p_obj.get("birth_country"),
                "Latitude": bc[0],
                "Longitude": bc[1],
                "LAND_WATER_STATUS": "NOT_VERIFIED",
                "LAND_WATER_SOURCE": "UNAVAILABLE",
                "GEOGRAPHIC_VERIFICATION_STATUS": "UNAVAILABLE",
                "LOCATION_MATCH_STATUS": "NOT_VERIFIED",
                "i18n_birth_city": i18n_bc,
                "i18n_birth_country": i18n_bco,
                "i18n_death_city": i18n_dc,
                "i18n_death_country": i18n_dco
            })

        if dc:
            priority_records.append({
                "Person": matched_name,
                "Field": "Death",
                "City": p_obj.get("death_city"),
                "Country": p_obj.get("death_country"),
                "Latitude": dc[0],
                "Longitude": dc[1],
                "LAND_WATER_STATUS": "NOT_VERIFIED",
                "LAND_WATER_SOURCE": "UNAVAILABLE",
                "GEOGRAPHIC_VERIFICATION_STATUS": "UNAVAILABLE",
                "LOCATION_MATCH_STATUS": "NOT_VERIFIED",
                "i18n_birth_city": i18n_bc,
                "i18n_birth_country": i18n_bco,
                "i18n_death_city": i18n_dc,
                "i18n_death_country": i18n_dco
            })

    priority_count = len(priority_records)

    out_json = {
        "PRIORITY_RECORDS": priority_count,
        "LAND_WATER_VERIFICATION": "UNAVAILABLE",
        "LOCATION_VERIFICATION": "UNAVAILABLE",
        "RUNTIME_MODIFIED": "NO",
        "records": priority_records
    }

    with open("tools/PRIORITY_COORDINATE_REVIEW.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Priority Coordinate Review Package V2 - Map of Fame\n")
    md_lines.append(f"**PRIORITY_RECORDS**: {priority_count}")
    md_lines.append("**LAND_WATER_VERIFICATION**: UNAVAILABLE")
    md_lines.append("**LOCATION_VERIFICATION**: UNAVAILABLE")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")
    md_lines.append("## Records\n")
    md_lines.append("| Person | Field | City | Country | Latitude | Longitude | LOCATION_MATCH_STATUS | LAND_WATER_STATUS | LAND_WATER_SOURCE | GEOGRAPHIC_VERIFICATION_STATUS |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|---|")

    for r in priority_records:
        md_lines.append(f"| {r['Person']} | {r['Field']} | {r['City']} | {r['Country']} | {r['Latitude']} | {r['Longitude']} | {r['LOCATION_MATCH_STATUS']} | {r['LAND_WATER_STATUS']} | {r['LAND_WATER_SOURCE']} | {r['GEOGRAPHIC_VERIFICATION_STATUS']} |")

    with open("tools/PRIORITY_COORDINATE_REVIEW.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"PRIORITY_RECORDS = {priority_count}")
    print(f"LAND_WATER_VERIFICATION = UNAVAILABLE")
    print(f"LOCATION_VERIFICATION = UNAVAILABLE")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    update_priority()
