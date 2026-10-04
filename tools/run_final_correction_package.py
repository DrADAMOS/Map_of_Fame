import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run_final_package():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    corrections = [
        {
            "person": "Pyrrhus of Epirus",
            "event": "Birth",
            "current_latitude": 38.30,
            "current_longitude": 21.10,
            "proposed_latitude": 39.157,
            "proposed_longitude": 20.978,
            "coordinate_level": "CITY_LEVEL",
            "reason": "Current coordinate [38.30, 21.10] is in the Gulf of Patras (~100 km south). Ancient Ambracia corresponds to modern Arta, Greece.",
            "source_1": "Wikidata (Q457850 - Ambracia / Q210515 - Arta)",
            "source_url_1": "https://www.wikidata.org/wiki/Q457850",
            "source_2": "Encyclopædia Britannica / GeoNames",
            "source_url_2": "https://www.britannica.com/place/Arta-Greece",
            "confidence": "HIGH"
        },
        {
            "person": "Horatio Kitchener",
            "event": "Death",
            "current_latitude": 59.10,
            "current_longitude": 3.20,
            "proposed_latitude": 59.11706,
            "proposed_longitude": -3.39566,
            "coordinate_level": "SITE_LEVEL",
            "reason": "Current coordinate has a longitude sign error (+3.20 E instead of -3.20 W). The HMS Hampshire wreck/sinking site west of Orkney is at 59.11706, -3.39566 WGS84.",
            "source_1": "Historic Environment Scotland / Canmore (HMS Hampshire Wreck)",
            "source_url_1": "https://canmore.org.uk/site/102927/hms-hampshire",
            "source_2": "Royal Navy / Wikidata (Q153037)",
            "source_url_2": "https://www.wikidata.org/wiki/Q153037",
            "confidence": "HIGH"
        }
    ]

    out_json = {
        "FINAL_CONFIRMED_CORRECTIONS_COUNT": len(corrections),
        "RUNTIME_MODIFIED": "NO",
        "corrections": corrections
    }

    with open("tools/FINAL_CONFIRMED_COORDINATE_CORRECTIONS.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Final Confirmed Coordinate Corrections - Map of Fame\n")
    md_lines.append(f"**FINAL_CONFIRMED_CORRECTIONS_COUNT**: {len(corrections)}")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")

    md_lines.append("## Corrections Detail\n")
    for c in corrections:
        md_lines.append(f"### {c['person']} ({c['event']})")
        md_lines.append(f"- **Current Coordinate**: `[{c['current_latitude']}, {c['current_longitude']}]`")
        md_lines.append(f"- **Proposed Coordinate**: `[{c['proposed_latitude']}, {c['proposed_longitude']}]`")
        md_lines.append(f"- **Coordinate Level**: {c['coordinate_level']}")
        md_lines.append(f"- **Reason**: {c['reason']}")
        md_lines.append(f"- **Source 1**: [{c['source_1']}]({c['source_url_1']})")
        md_lines.append(f"- **Source 2**: [{c['source_2']}]({c['source_url_2']})")
        md_lines.append(f"- **Confidence**: {c['confidence']}\n")

    with open("tools/FINAL_CONFIRMED_COORDINATE_CORRECTIONS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    run_final_package()
