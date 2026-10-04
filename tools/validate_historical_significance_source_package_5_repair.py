#!/usr/bin/env python3
"""
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.JSON
Validates the replacement source package for the 5 repair targets against protected files and contract requirements.
Modifies NO application/runtime data files or source packages.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
PKG_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json"
REVIEW_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_REVIEW_43.json"
REPAIR_PKG_5_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH,
    PKG_43_PATH,
    REVIEW_43_PATH
]

REPAIR_5_PEOPLE = ["Omar al-Mukhtar", "Yasser Arafat", "Attila the Hun", "Yusuf ibn Tashfin", "Richard Feynman"]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_validation():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Load Repair Package 5
    with open(REPAIR_PKG_5_PATH, "r", encoding="utf-8") as f:
        pkg_data = json.load(f)

    entries = pkg_data.get("entries", [])
    pkg_people = [e["person"] for e in entries]

    valid_cnt = 0
    invalid_cnt = 0
    duplicate_records_cnt = 0

    seen_people = set()

    for entry in entries:
        pid = entry.get("person")
        url = entry.get("source_url")
        passage = entry.get("exact_source_passage")

        if pid in seen_people:
            duplicate_records_cnt += 1
        seen_people.add(pid)

        has_valid_url = url and url.startswith("https://en.wikipedia.org/wiki/")
        has_valid_passage = passage and len(passage) > 30

        if has_valid_url and has_valid_passage:
            valid_cnt += 1
        else:
            invalid_cnt += 1

    exact_target_match = (sorted(REPAIR_5_PEOPLE) == sorted(pkg_people))

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    status_pass = (
        len(entries) == 5 and
        exact_target_match and
        valid_cnt == 5 and
        invalid_cnt == 0 and
        duplicate_records_cnt == 0 and
        not app_data_modified
    )

    final_status = "PASS" if status_pass else "FAIL"

    print("HISTORICAL SIGNIFICANCE 5-SOURCE REPAIR")
    print("----------------------------------------")
    print("TARGET_PEOPLE: 5")
    print(f"PEOPLE_WITH_VALID_SOURCE_EVIDENCE: {valid_cnt}")
    print(f"PEOPLE_WITHOUT_VALID_SOURCE_EVIDENCE: {invalid_cnt}")
    print(f"SOURCE_RECORDS: {len(entries)}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if not app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_validation()
