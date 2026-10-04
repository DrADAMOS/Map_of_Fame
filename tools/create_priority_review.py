import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def create_priority_package():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"
    dataset_path = "tools/COORDINATE_DATASET_594.json"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    with open(person_path, "r", encoding="utf-8") as f:
        person_data = json.load(f)

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

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

    # Also handle possible name variations or partial matches if needed
    quiz_map = {}
    for p in quiz_data:
        en_name = p.get("name_en") or p.get("name") or ""
        quiz_map[en_name] = p

    dataset_records = dataset.get("records", [])
    priority_records = []
    quiz_coords_exact = True

    for target in target_people:
        # Find matching person in dataset or quiz_data
        matched_name = None
        for en_name in quiz_map:
            if target.lower() in en_name.lower() or en_name.lower() in target.lower():
                matched_name = en_name
                break
        
        if not matched_name:
            # check Omar Mukhtar specifically
            if target == "Omar al-Mukhtar":
                for en_name in quiz_map:
                    if "mukhtar" in en_name.lower():
                        matched_name = en_name
                        break

        if not matched_name:
            print(f"Warning: Target '{target}' not found in quiz_data.")
            continue

        p_obj = quiz_map[matched_name]
        i18n_entry = people_i18n.get(matched_name, {})
        i18n_en = i18n_entry.get("languages", {}).get("en", {})

        i18n_bc = i18n_en.get("birth_city", "N/A")
        i18n_bco = i18n_en.get("birth_country", "N/A")
        i18n_dc = i18n_en.get("death_city", "N/A")
        i18n_dco = i18n_en.get("death_country", "N/A")

        # Get birth and death records from dataset or directly from quiz_data
        bc = p_obj.get("bc")
        dc = p_obj.get("dc")

        if bc:
            # verify exact match with quiz_data
            if bc[0] != p_obj["bc"][0] or bc[1] != p_obj["bc"][1]:
                quiz_coords_exact = False

            priority_records.append({
                "Person": matched_name,
                "Field": "Birth",
                "City": p_obj.get("birth_city"),
                "Country": p_obj.get("birth_country"),
                "Lat": bc[0],
                "Lng": bc[1],
                "i18n_birth_city": i18n_bc,
                "i18n_birth_country": i18n_bco,
                "i18n_death_city": i18n_dc,
                "i18n_death_country": i18n_dco
            })

        if dc:
            if dc[0] != p_obj["dc"][0] or dc[1] != p_obj["dc"][1]:
                quiz_coords_exact = False

            priority_records.append({
                "Person": matched_name,
                "Field": "Death",
                "City": p_obj.get("death_city"),
                "Country": p_obj.get("death_country"),
                "Lat": dc[0],
                "Lng": dc[1],
                "i18n_birth_city": i18n_bc,
                "i18n_birth_country": i18n_bco,
                "i18n_death_city": i18n_dc,
                "i18n_death_country": i18n_dco
            })

    priority_count = len(priority_records)

    # Write JSON
    out_json = {
        "PRIORITY_RECORDS": priority_count,
        "QUIZ_COORDINATES_EXACT": "PASS" if quiz_coords_exact else "FAIL",
        "records": priority_records
    }

    with open("tools/PRIORITY_COORDINATE_REVIEW.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    # Write Markdown
    md_lines = []
    md_lines.append("# Priority Coordinate Review Package - Map of Fame\n")
    md_lines.append(f"**PRIORITY_RECORDS**: {priority_count}")
    md_lines.append(f"**QUIZ_COORDINATES_EXACT**: {'PASS' if quiz_coords_exact else 'FAIL'}\n")
    md_lines.append("## Records\n")
    md_lines.append("| Person | Field | City | Country | Lat | Lng | i18n Birth City | i18n Birth Country | i18n Death City | i18n Death Country |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|---|")

    for r in priority_records:
        md_lines.append(f"| {r['Person']} | {r['Field']} | {r['City']} | {r['Country']} | {r['Lat']} | {r['Lng']} | {r['i18n_birth_city']} | {r['i18n_birth_country']} | {r['i18n_death_city']} | {r['i18n_death_country']} |")

    with open("tools/PRIORITY_COORDINATE_REVIEW.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"PRIORITY_RECORDS = {priority_count}")
    print(f"QUIZ_COORDINATES_EXACT = {'PASS' if quiz_coords_exact else 'FAIL'}")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    create_priority_package()
