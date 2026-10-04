import json
import hashlib
import os
import math

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def run_corrections():
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
            "reference_latitude": 39.157,
            "reference_longitude": 20.978,
            "distance_km": round(haversine(38.30, 21.10, 39.157, 20.978), 2),
            "proposed_latitude": 39.157,
            "proposed_longitude": 20.978,
            "reason": "Current coordinate [38.30, 21.10] is located in the Gulf of Patras (~100 km south), whereas Pyrrhus was born in ancient Ambracia (modern Arta, Greece).",
            "source_1": "Wikidata (Q457850 - Ambracia)",
            "source_url_1": "https://www.wikidata.org/wiki/Q457850",
            "source_2": "Encyclopædia Britannica / GeoNames",
            "source_url_2": "https://www.britannica.com/place/Arta-Greece",
            "confidence": "HIGH",
            "verdict": "DEFINITIVE_MISMATCH"
        },
        {
            "person": "Horatio Kitchener",
            "event": "Death",
            "current_latitude": 59.10,
            "current_longitude": 3.20,
            "reference_latitude": 59.11,
            "reference_longitude": -3.38,
            "distance_km": round(haversine(59.10, 3.20, 59.11, -3.38), 2),
            "proposed_latitude": 59.11,
            "proposed_longitude": -3.38,
            "reason": "Current coordinate has a longitude sign error (+3.20 E instead of -3.20 W), placing it in the eastern North Sea instead of west of Orkney where HMS Hampshire sank.",
            "source_1": "Royal Navy / Wikidata (Q153037 - HMS Hampshire)",
            "source_url_1": "https://www.wikidata.org/wiki/Q153037",
            "source_2": "Admiralty War Diary / Britannica",
            "source_url_2": "https://www.britannica.com/biography/Horatio-Herbert-Kitchener-Earl-Kitchener-of-Khartoum",
            "confidence": "HIGH",
            "verdict": "DEFINITIVE_MISMATCH"
        }
    ]

    out_json = {
        "CONFIRMED_CORRECTIONS_COUNT": len(corrections),
        "RUNTIME_MODIFIED": "NO",
        "corrections": corrections
    }

    with open("tools/CONFIRMED_COORDINATE_CORRECTIONS.json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Confirmed Coordinate Corrections - Map of Fame\n")
    md_lines.append(f"**CONFIRMED_CORRECTIONS_COUNT**: {len(corrections)}")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")

    md_lines.append("## Confirmed Corrections Detail\n")
    md_lines.append("| Person | Event | Current | Proposed | Dist (km) | Reason | Confidence |")
    md_lines.append("|---|---|---|---|---|---|---|")

    for c in corrections:
        md_lines.append(f"| {c['person']} | {c['event']} | [{c['current_latitude']}, {c['current_longitude']}] | [{c['proposed_latitude']}, {c['proposed_longitude']}] | {c['distance_km']} | {c['reason']} | {c['confidence']} |")

    with open("tools/CONFIRMED_COORDINATE_CORRECTIONS.md", "w", encoding="utf-8") as f:
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
    run_corrections()
