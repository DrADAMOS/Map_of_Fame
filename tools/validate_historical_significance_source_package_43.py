#!/usr/bin/env python3
"""
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.JSON
Validates the acquired source package against protected application files and contract requirements.
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
ADJUDICATION_43_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"
SOURCE_PKG_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

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

    # Load Adjudication 43 targets
    with open(ADJUDICATION_43_PATH, "r", encoding="utf-8") as f:
        adj_data = json.load(f)

    target_people = [c["person"] for c in adj_data.get("clusters", [])]

    # Load Source Package 43
    with open(SOURCE_PKG_43_PATH, "r", encoding="utf-8") as f:
        pkg_data = json.load(f)

    entries = pkg_data.get("entries", [])
    pkg_people = [e["person"] for e in entries]

    valid_cnt = 0
    invalid_cnt = 0
    weak_cnt = 0
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
        has_valid_passage = passage and len(passage) > 20

        if has_valid_url and has_valid_passage:
            valid_cnt += 1
        else:
            invalid_cnt += 1
            if not has_valid_passage:
                weak_cnt += 1

    # Check matches exact target 43
    exact_target_match = (sorted(target_people) == sorted(pkg_people))

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    status_pass = (
        len(entries) == 43 and
        exact_target_match and
        valid_cnt == 43 and
        invalid_cnt == 0 and
        duplicate_records_cnt == 0 and
        not app_data_modified
    )

    final_status = "PASS" if status_pass else "FAIL"

    print("HISTORICAL SIGNIFICANCE SOURCE ACQUISITION")
    print("------------------------------------------")
    print(f"TARGET_PEOPLE: {len(target_people)}")
    print(f"PEOPLE_WITH_VALID_SOURCE_EVIDENCE: {valid_cnt}")
    print(f"PEOPLE_WITHOUT_VALID_SOURCE_EVIDENCE: {invalid_cnt}")
    print(f"SOURCE_RECORDS: {len(entries)}")
    print(f"WEAK_OR_INSUFFICIENT: {weak_cnt}")
    print(f"DUPLICATE_SOURCE_RECORDS: {duplicate_records_cnt}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if not app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_validation()
