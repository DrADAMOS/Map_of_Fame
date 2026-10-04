import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run_full_geo_audit():
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

    duplicate_candidates = ["omar al-mukhtar", "omar mukhtar", "napoleon", "martin luther king"]

    records = []
    idx = 0
    total_birth = 0
    total_death = 0

    for person in quiz_data:
        name_en = person.get("name_en") or person.get("name") or "Unknown"
        birth_city = person.get("birth_city") or "Unknown"
        death_city = person.get("death_city") or "Unknown"
        birth_country = person.get("birth_country") or "Unknown"
        death_country = person.get("death_country") or "Unknown"

        bc = person.get("bc")
        dc = person.get("dc")

        is_dup = any(d in name_en.lower() for d in duplicate_candidates)

        if bc and isinstance(bc, list) and len(bc) == 2:
            total_birth += 1
            idx += 1
            records.append({
                "person": name_en,
                "record_index": idx,
                "field": "Birth",
                "city": birth_city,
                "country": birth_country,
                "latitude": bc[0],
                "longitude": bc[1],
                "physical_status": "UNKNOWN",
                "location_match_status": "NOT_VERIFIED",
                "location_source": "UNAVAILABLE",
                "evidence": "Natural Earth 10m shapefiles unavailable in offline environment; point-in-polygon test could not be performed.",
                "duplicate_identity_review": is_dup
            })

        if dc and isinstance(dc, list) and len(dc) == 2:
            total_death += 1
            idx += 1
            records.append({
                "person": name_en,
                "record_index": idx,
                "field": "Death",
                "city": death_city,
                "country": death_country,
                "latitude": dc[0],
                "longitude": dc[1],
                "physical_status": "UNKNOWN",
                "location_match_status": "NOT_VERIFIED",
                "location_source": "UNAVAILABLE",
                "evidence": "Natural Earth 10m shapefiles unavailable in offline environment; point-in-polygon test could not be performed.",
                "duplicate_identity_review": is_dup
            })

    total_coords = total_birth + total_death

    out_json = {
        "TOTAL_PEOPLE": len(quiz_data),
        "TOTAL_BIRTH": total_birth,
        "TOTAL_DEATH": total_death,
        "TOTAL_COORDINATES": total_coords,
        "LAND_WATER_VERIFICATION": "UNAVAILABLE",
        "LOCATION_VERIFICATION": "UNAVAILABLE",
        "RUNTIME_MODIFIED": "NO",
        "PHYSICAL_STATUS_COUNTS": {
            "LAND": 0,
            "OPEN_WATER": 0,
            "INLAND_WATER": 0,
            "ICE_SHELF": 0,
            "COASTAL_AMBIGUOUS": 0,
            "UNKNOWN": total_coords
        },
        "LOCATION_MATCH_COUNTS": {
            "VERIFIED": 0,
            "MISMATCH": 0,
            "UNCERTAIN": 0,
            "NOT_VERIFIED": total_coords
        },
        "records": records
    }

    with open("tools/FULL_GEOGRAPHIC_COORDINATE_AUDIT.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Full Geographic Coordinate Audit Report - Map of Fame\n")
    md_lines.append(f"**TOTAL_PEOPLE**: {len(quiz_data)}")
    md_lines.append(f"**TOTAL_BIRTH**: {total_birth}")
    md_lines.append(f"**TOTAL_DEATH**: {total_death}")
    md_lines.append(f"**TOTAL_COORDINATES**: {total_coords}")
    md_lines.append("**LAND_WATER_VERIFICATION**: UNAVAILABLE")
    md_lines.append("**LOCATION_VERIFICATION**: UNAVAILABLE")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")

    md_lines.append("## Summary Counts\n")
    md_lines.append("### PHYSICAL_STATUS_COUNTS")
    md_lines.append("- LAND = 0")
    md_lines.append("- OPEN_WATER = 0")
    md_lines.append("- INLAND_WATER = 0")
    md_lines.append("- ICE_SHELF = 0")
    md_lines.append("- COASTAL_AMBIGUOUS = 0")
    md_lines.append(f"- UNKNOWN = {total_coords}\n")

    md_lines.append("### LOCATION_MATCH_COUNTS")
    md_lines.append("- VERIFIED = 0")
    md_lines.append("- MISMATCH = 0")
    md_lines.append("- UNCERTAIN = 0")
    md_lines.append(f"- NOT_VERIFIED = {total_coords}\n")

    md_lines.append("## All 594 Records\n")
    md_lines.append("| Index | Person | Field | City | Country | Latitude | Longitude | Physical Status | Location Match | Dup Review |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|---|")

    for r in records:
        md_lines.append(f"| {r['record_index']} | {r['person']} | {r['field']} | {r['city']} | {r['country']} | {r['latitude']} | {r['longitude']} | {r['physical_status']} | {r['location_match_status']} | {r['duplicate_identity_review']} |")

    with open("tools/FULL_GEOGRAPHIC_COORDINATE_AUDIT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"TOTAL_PEOPLE = {len(quiz_data)}")
    print(f"TOTAL_BIRTH = {total_birth}")
    print(f"TOTAL_DEATH = {total_death}")
    print(f"TOTAL_COORDINATES = {total_coords}")
    print(f"LAND_WATER_VERIFICATION = UNAVAILABLE")
    print(f"LOCATION_VERIFICATION = UNAVAILABLE")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}", flush=True)

if __name__ == "__main__":
    run_full_geo_audit()
