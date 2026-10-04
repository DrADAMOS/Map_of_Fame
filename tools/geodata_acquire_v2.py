import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run_geodata_v2():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    os.makedirs("tools/geodata", exist_ok=True)

    required_datasets = [
        "ne_10m_land",
        "ne_10m_ocean",
        "ne_10m_lakes",
        "ne_10m_minor_islands",
        "ne_10m_antarctic_ice_shelves"
    ]

    manual_urls = {
        ds: f"https://www.naturalearthdata.com/download/10m/physical/{ds}.zip" for ds in required_datasets
    }

    report = {
        "DATA_ACQUISITION_STATUS": "UNAVAILABLE",
        "LAND_DATA": "FAIL",
        "OCEAN_DATA": "FAIL",
        "LAKES_DATA": "FAIL",
        "ICE_SHELF_DATA": "FAIL",
        "MINOR_ISLANDS_DATA": "NOT_AVAILABLE",
        "manual_download_instructions": "Automated download returned HTML error pages / HTTP 406 in the sandbox environment. Please manually download the following 5 ZIP files from https://www.naturalearthdata.com/downloads/10m-physical-vectors/ and place them under tools/geodata/:",
        "urls": manual_urls,
        "RUNTIME_MODIFIED": "NO"
    }

    with open("tools/GEODATA_ACQUISITION_REPORT.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Geodata Acquisition Report - Map of Fame\n")
    md_lines.append("**DATA_ACQUISITION_STATUS**: UNAVAILABLE")
    md_lines.append("**LAND_DATA**: FAIL")
    md_lines.append("**OCEAN_DATA**: FAIL")
    md_lines.append("**LAKES_DATA**: FAIL")
    md_lines.append("**ICE_SHELF_DATA**: FAIL")
    md_lines.append("**MINOR_ISLANDS_DATA**: NOT_AVAILABLE")
    md_lines.append("**RUNTIME_MODIFIED**: NO\n")
    md_lines.append("## Manual Download Required\n")
    md_lines.append("Automated direct download returned HTTP errors / redirects in this sandbox environment. The following datasets must be downloaded manually from [Natural Earth 10m Physical Vectors](https://www.naturalearthdata.com/downloads/10m-physical-vectors/) and stored under `tools/geodata/`:\n")
    for ds, url in manual_urls.items():
        md_lines.append(f"- `{ds}.zip`: [{url}]({url})")

    with open("tools/GEODATA_ACQUISITION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    hashes_unchanged = (hashes_before == hashes_after)

    print(f"DATA_ACQUISITION_STATUS = UNAVAILABLE")
    print(f"LAND_DATA = FAIL")
    print(f"OCEAN_DATA = FAIL")
    print(f"LAKES_DATA = FAIL")
    print(f"ICE_SHELF_DATA = FAIL")
    print(f"MINOR_ISLANDS_DATA = NOT_AVAILABLE")
    print(f"RUNTIME_MODIFIED = NO")
    print(f"HASHES_UNCHANGED = {'PASS' if hashes_unchanged else 'FAIL'}")

if __name__ == "__main__":
    run_geodata_v2()
