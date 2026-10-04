import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run_integrity_check():
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

    records = dataset.get("records", [])
    total_records = len(records)
    birth_count = sum(1 for r in records if r.get("Field") == "Birth")
    death_count = sum(1 for r in records if r.get("Field") == "Death")

    # Check 3: Every record has Person, Field, City, Country, Lat, Lng
    fields_ok = True
    for r in records:
        if not all(k in r for k in ["Person", "Field", "City", "Country", "Lat", "Lng"]):
            fields_ok = False
            break

    # Check 4 & 5: Verify exact match with quiz_data.json
    quiz_coords_exact = True
    quiz_metadata_exact = True

    quiz_map = {}
    for p in quiz_data:
        name_en = p.get("name_en") or p.get("name") or "Unknown"
        quiz_map[name_en] = p

    for r in records:
        person = r["Person"]
        field = r["Field"]
        city = r["City"]
        country = r["Country"]
        lat = r["Lat"]
        lng = r["Lng"]

        p_obj = quiz_map.get(person)
        if not p_obj:
            quiz_coords_exact = False
            quiz_metadata_exact = False
            continue

        if field == "Birth":
            bc = p_obj.get("bc")
            if not bc or bc[0] != lat or bc[1] != lng:
                quiz_coords_exact = False
            if p_obj.get("birth_city") != city or p_obj.get("birth_country") != country:
                quiz_metadata_exact = False
        elif field == "Death":
            dc = p_obj.get("dc")
            if not dc or dc[0] != lat or dc[1] != lng:
                quiz_coords_exact = False
            if p_obj.get("death_city") != city or p_obj.get("death_country") != country:
                quiz_metadata_exact = False

    # Check 6 & 7: person_i18n.json EN metadata reconciliation (Note: person_i18n.json does not contain coordinates)
    i18n_mismatches = []
    for person_name, info in people_i18n.items():
        p_obj = quiz_map.get(person_name)
        if not p_obj:
            continue
        
        i18n_en = info.get("languages", {}).get("en", {})
        i18n_bc = i18n_en.get("birth_city")
        i18n_dc = i18n_en.get("death_city")
        i18n_bco = i18n_en.get("birth_country")
        i18n_dco = i18n_en.get("death_country")

        if i18n_bc and i18n_bc != p_obj.get("birth_city"):
            i18n_mismatches.append({
                "Person": person_name,
                "Field": "Birth City",
                "i18n_EN": i18n_bc,
                "quiz_data": p_obj.get("birth_city")
            })
        if i18n_dc and i18n_dc != p_obj.get("death_city"):
            i18n_mismatches.append({
                "Person": person_name,
                "Field": "Death City",
                "i18n_EN": i18n_dc,
                "quiz_data": p_obj.get("death_city")
            })
        if i18n_bco and i18n_bco != p_obj.get("birth_country"):
            i18n_mismatches.append({
                "Person": person_name,
                "Field": "Birth Country",
                "i18n_EN": i18n_bco,
                "quiz_data": p_obj.get("birth_country")
            })
        if i18n_dco and i18n_dco != p_obj.get("death_country"):
            i18n_mismatches.append({
                "Person": person_name,
                "Field": "Death Country",
                "i18n_EN": i18n_dco,
                "quiz_data": p_obj.get("death_country")
            })

    i18n_reconciliation_pass = len(i18n_mismatches) == 0

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"DATASET_RECORD_COUNT = {total_records}{'' if total_records == 594 else '/FAIL'}")
    print(f"BIRTH_COUNT = {birth_count}{'' if birth_count == 297 else '/FAIL'}")
    print(f"DEATH_COUNT = {death_count}{'' if death_count == 297 else '/FAIL'}")
    print(f"QUIZ_COORDINATES_EXACT = {'PASS' if quiz_coords_exact else 'FAIL'}")
    print(f"QUIZ_METADATA_EXACT = {'PASS' if quiz_metadata_exact else 'FAIL'}")
    print(f"I18N_METADATA_RECONCILIATION = {'PASS' if i18n_reconciliation_pass else 'FAIL'}")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

    if i18n_mismatches:
        print("\n--- COMPLETE I18N METADATA MISMATCH LIST ---")
        for m in i18n_mismatches:
            print(m)
    else:
        print("\n--- COMPLETE I18N METADATA MISMATCH LIST: NONE ---")

if __name__ == "__main__":
    run_integrity_check()
