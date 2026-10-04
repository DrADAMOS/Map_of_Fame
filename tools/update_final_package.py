import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def update_final():
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
            "proposed_latitude": 39.1550,
            "proposed_longitude": 20.9899,
            "coordinate_level": "CITY_LEVEL",
            "reason": "This is a CITY_LEVEL representation of ancient Ambracia/modern Arta, not an exact birthplace coordinate. Current runtime coordinate [38.30, 21.10] is in the Gulf of Patras (~100 km south).",
            "source_1": "Digital Atlas of the Roman Empire / Trismegistos / ToposText",
            "source_url_1": "https://dh.gu.se/dare/",
            "source_2": "Wikidata (Q457850 - Ambracia / Q210515 - Arta)",
            "source_url_2": "https://www.wikidata.org/wiki/Q210515",
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
            "reason": "This is the documented HMS Hampshire wreck position. Current coordinate has a longitude sign error (+3.20 E instead of -3.20 W), placing it in the eastern North Sea instead of west of Orkney.",
            "source_1": "Historic Environment Scotland / Canmore (HMS Hampshire Wreck)",
            "source_url_1": "https://canmore.org.uk/site/102927/hms-hampshire",
            "source_2": "Royal Navy / UKHO / Wikidata (Q153037)",
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
    update_final()
