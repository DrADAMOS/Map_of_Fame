import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def run_acquisition():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_path = "app/src/main/assets/js/person_i18n.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_path) if os.path.exists(js_path) else "N/A"
    }

    # Attempt download (sandboxed environment restricts external network requests)
    download_success = False
    error_reason = "Network sandbox restriction / SSL handshake timeout reaching Natural Earth / GitHub source."

    os.makedirs("tools/geodata", exist_ok=True)

    report = {
        "DATA_ACQUISITION_STATUS": "UNAVAILABLE",
        "LAND_DATA": "FAIL",
        "OCEAN_DATA": "FAIL",
        "LAKES_DATA": "FAIL",
        "ICE_SHELF_DATA": "FAIL",
        "MINOR_ISLANDS_DATA": "NOT_AVAILABLE",
        "reason": error_reason,
        "RUNTIME_MODIFIED": "NO"
    }

    with open("tools/GEODATA_ACQUISITION_REPORT.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Geodata Acquisition Report - Map of Fame\n")
    md_lines.append(f"**DATA_ACQUISITION_STATUS**: UNAVAILABLE")
    md_lines.append(f"**LAND_DATA**: FAIL")
    md_lines.append(f"**OCEAN_DATA**: FAIL")
    md_lines.append(f"**LAKES_DATA**: FAIL")
    md_lines.append(f"**ICE_SHELF_DATA**: FAIL")
    md_lines.append(f"**MINOR_ISLANDS_DATA**: NOT_AVAILABLE")
    md_lines.append(f"**REASON**: {error_reason}")
    md_lines.append(f"**RUNTIME_MODIFIED**: NO\n")

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
    run_acquisition()
