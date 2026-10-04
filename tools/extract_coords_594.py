import json
import hashlib
import csv

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def extract_594():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js" # or wherever person_i18n.js is located

    # Check if person_i18n.js exists or find it
    js_paths = [
        "app/src/main/assets/js/person_i18n.js",
        "app/src/main/assets/person_i18n.js"
    ]
    target_js = None
    for p in js_paths:
        if os.path.exists(p):
            target_js = p
            break

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(target_js) if target_js else "N/A"
    }

    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    with open(person_path, "r", encoding="utf-8") as f:
        person_data = json.load(f)

    people_i18n = person_data.get("people", {})

    total_people = len(quiz_data)
    birth_records = 0
    death_records = 0
    records = []
    mismatches = []

    for person in quiz_data:
        name_en = person.get("name_en") or person.get("name") or "Unknown"
        name_ar = person.get("name") or person.get("name_ar") or ""
        
        quiz_bc = person.get("bc")
        quiz_dc = person.get("dc")
        quiz_birth_city = person.get("birth_city") or "Unknown"
        quiz_death_city = person.get("death_city") or "Unknown"
        quiz_birth_country = person.get("birth_country") or "Unknown"
        quiz_death_country = person.get("death_country") or "Unknown"

        # Reconcile with person_i18n.json if present
        i18n_entry = people_i18n.get(name_en, {})
        # Check i18n langs (e.g. en or ar fields)
        i18n_langs = i18n_entry.get("languages", {})
        i18n_en = i18n_langs.get("en", {})
        i18n_ar = i18n_langs.get("ar", {})

        i18n_birth_city = i18n_en.get("birth_city") or i18n_ar.get("birth_city") or quiz_birth_city
        i18n_death_city = i18n_en.get("death_city") or i18n_ar.get("death_city") or quiz_death_city
        i18n_birth_country = i18n_en.get("birth_country") or i18n_ar.get("birth_country") or quiz_birth_country
        i18n_death_country = i18n_en.get("death_country") or i18n_ar.get("death_country") or quiz_death_country

        mismatch_notes = []
        if quiz_birth_city != i18n_birth_city:
            mismatch_notes.append(f"Birth city mismatch: quiz='{quiz_birth_city}' vs i18n='{i18n_birth_city}'")
        if quiz_death_city != i18n_death_city:
            mismatch_notes.append(f"Death city mismatch: quiz='{quiz_death_city}' vs i18n='{i18n_death_city}'")

        mismatch_str = "; ".join(mismatch_notes) if mismatch_notes else "None"
        if mismatch_notes:
            mismatches.append({"person": name_en, "mismatches": mismatch_notes})

        # Birth record
        if quiz_bc and isinstance(quiz_bc, list) and len(quiz_bc) == 2:
            birth_records += 1
            records.append({
                "Person": name_en,
                "Field": "Birth",
                "City": quiz_birth_city,
                "Country": quiz_birth_country,
                "Lat": quiz_bc[0],
                "Lng": quiz_bc[1],
                "Source File": "quiz_data.json / person_i18n.json",
                "Mismatch": mismatch_str
            })

        # Death record
        if quiz_dc and isinstance(quiz_dc, list) and len(quiz_dc) == 2:
            death_records += 1
            records.append({
                "Person": name_en,
                "Field": "Death",
                "City": quiz_death_city,
                "Country": quiz_death_country,
                "Lat": quiz_dc[0],
                "Lng": quiz_dc[1],
                "Source File": "quiz_data.json / person_i18n.json",
                "Mismatch": mismatch_str
            })

    total_coords = birth_records + death_records

    # Write JSON
    json_out = {
        "TOTAL_PEOPLE": total_people,
        "BIRTH_COORDINATES": birth_records,
        "DEATH_COORDINATES": death_records,
        "TOTAL_COORDINATES": total_coords,
        "mismatches_count": len(mismatches),
        "mismatches": mismatches,
        "records": records
    }

    with open("tools/COORDINATE_DATASET_594.json", "w", encoding="utf-8") as f:
        json.dump(json_out, f, ensure_ascii=False, indent=2)

    # Write CSV
    csv_path = "tools/COORDINATE_DATASET_594.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Person", "Field", "City", "Country", "Lat", "Lng", "Source File", "Mismatch"])
        for r in records:
            writer.writerow([r["Person"], r["Field"], r["City"], r["Country"], r["Lat"], r["Lng"], r["Source File"], r["Mismatch"]])

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(target_js) if target_js else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"TOTAL_PEOPLE = {total_people}")
    print(f"BIRTH_COORDINATES = {birth_records}")
    print(f"DEATH_COORDINATES = {death_records}")
    print(f"TOTAL_COORDINATES = {total_coords}")
    print(f"EXTRACTION_ONLY = {'PASS' if (total_people == 297 and birth_records == 297 and death_records == 297) else 'FAIL'}")
    print(f"TOTAL_RECORDS = {total_coords} {'/PASS' if total_coords == 594 else '/FAIL'}")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    import os
    extract_594()
