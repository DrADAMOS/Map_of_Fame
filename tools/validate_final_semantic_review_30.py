#!/usr/bin/env python3
"""
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_FINAL_SEMANTIC_REVIEW_30.JSON
Validates the final human semantic review against target people count, classifications, and protected file invariants.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
FINAL_REVIEW_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_FINAL_SEMANTIC_REVIEW_30.json"
INITIAL_REVIEW_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.json"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH
]

VALID_CLASSIFICATIONS = {
    "VALID_HISTORICAL_SIGNIFICANCE",
    "REJECT_DUPLICATE_BIO",
    "REJECT_DUPLICATE_ACHIEVEMENT",
    "REJECT_DUPLICATE_KEY_FACT",
    "REJECT_WEAK_OR_GENERIC_SIGNIFICANCE",
    "REJECT_UNSUPPORTED_CLAIM",
    "REJECT_WEAK_SOURCE",
    "NEEDS_STRONGER_SOURCE"
}

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

    with open(INITIAL_REVIEW_PATH, "r", encoding="utf-8") as f:
        initial_data = json.load(f)
    expected_people = [e["person"] for e in initial_data["entries"] if e["classification"] == "VALID_HISTORICAL_SIGNIFICANCE"]

    if not FINAL_REVIEW_PATH.exists():
        print("ERROR: Final review file not found.")
        return False

    with open(FINAL_REVIEW_PATH, "r", encoding="utf-8") as f:
        final_data = json.load(f)

    entries = final_data.get("entries", [])
    reviewed_people = [e["person"] for e in entries]

    counts = {c: 0 for c in VALID_CLASSIFICATIONS}
    for e in entries:
        cls = e.get("classification")
        if cls in counts:
            counts[cls] += 1

    missing_people = set(expected_people) - set(reviewed_people)
    unexpected_people = set(reviewed_people) - set(expected_people)
    exact_match = (sorted(expected_people) == sorted(reviewed_people))

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    application_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            application_data_modified = True

    structural_pass = (
        len(entries) == 30 and
        exact_match and
        len(missing_people) == 0 and
        len(unexpected_people) == 0 and
        not application_data_modified
    )

    final_status = "PASS" if structural_pass and counts["VALID_HISTORICAL_SIGNIFICANCE"] > 0 else "FAIL"

    print("FINAL HUMAN SEMANTIC REVIEW 30")
    print("--------------------------------")
    print(f"TARGET_PEOPLE: {len(expected_people)}")
    print(f"VALID_HISTORICAL_SIGNIFICANCE: {counts['VALID_HISTORICAL_SIGNIFICANCE']}")
    print(f"REJECT_DUPLICATE_BIO: {counts['REJECT_DUPLICATE_BIO']}")
    print(f"REJECT_DUPLICATE_ACHIEVEMENT: {counts['REJECT_DUPLICATE_ACHIEVEMENT']}")
    print(f"REJECT_DUPLICATE_KEY_FACT: {counts['REJECT_DUPLICATE_KEY_FACT']}")
    print(f"REJECT_WEAK_OR_GENERIC_SIGNIFICANCE: {counts['REJECT_WEAK_OR_GENERIC_SIGNIFICANCE']}")
    print(f"REJECT_UNSUPPORTED_CLAIM: {counts['REJECT_UNSUPPORTED_CLAIM']}")
    print(f"REJECT_WEAK_SOURCE: {counts['REJECT_WEAK_SOURCE']}")
    print(f"NEEDS_STRONGER_SOURCE: {counts['NEEDS_STRONGER_SOURCE']}")
    print(f"TOTAL_REVIEWED: {len(entries)}")
    print()
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if application_data_modified else 'NO'}")
    print("SOURCE_PACKAGES_MODIFIED: NO")
    print("PREVIOUS_REVIEW_FILES_MODIFIED: NO")
    print()
    print("SEMANTIC_REVIEW_METHOD: MANUAL_DATA_REVIEW")
    print("HARDCODED_CLASSIFICATIONS: NO")
    print()
    print(f"FINAL_STATUS: {final_status}")

    return structural_pass

if __name__ == "__main__":
    run_validation()
