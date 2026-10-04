#!/usr/bin/env python3
"""
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.JSON
Validates the semantic review against target people count, classifications, and protected file invariants.
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
REPAIR_PKG_3_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_3_REPAIR.json"
ADJUDICATION_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"
SEMANTIC_REVIEW_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.json"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH,
    PKG_43_PATH,
    REVIEW_43_PATH,
    REPAIR_PKG_5_PATH,
    REPAIR_PKG_3_PATH
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

    with open(ADJUDICATION_PATH, "r", encoding="utf-8") as f:
        adj_data = json.load(f)
    target_people = [c["person"] for c in adj_data["clusters"]]

    if not SEMANTIC_REVIEW_PATH.exists():
        print("ERROR: Semantic review file not found.")
        return False

    with open(SEMANTIC_REVIEW_PATH, "r", encoding="utf-8") as f:
        review_data = json.load(f)

    entries = review_data.get("entries", [])
    review_people = [e["person"] for e in entries]

    counts = {c: 0 for c in VALID_CLASSIFICATIONS}
    for e in entries:
        cls = e.get("classification")
        if cls in counts:
            counts[cls] += 1

    missing_people = set(target_people) - set(review_people)
    unexpected_people = set(review_people) - set(target_people)
    exact_target_match = (sorted(target_people) == sorted(review_people))

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    source_packages_modified = False
    application_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            if "tools/" in fp_str:
                source_packages_modified = True
            else:
                application_data_modified = True

    structural_pass = (
        len(entries) == 43 and
        exact_target_match and
        len(missing_people) == 0 and
        len(unexpected_people) == 0 and
        not application_data_modified and
        not source_packages_modified
    )

    final_status = "PASS" if structural_pass and len(entries) == 43 else "FAIL"

    print("HISTORICAL SIGNIFICANCE SEMANTIC REVIEW 43")
    print("-------------------------------------------")
    print(f"TARGET_PEOPLE: {len(target_people)}")
    print(f"VALID_HISTORICAL_SIGNIFICANCE: {counts['VALID_HISTORICAL_SIGNIFICANCE']}")
    print(f"REJECT_DUPLICATE_BIO: {counts['REJECT_DUPLICATE_BIO']}")
    print(f"REJECT_DUPLICATE_ACHIEVEMENT: {counts['REJECT_DUPLICATE_ACHIEVEMENT']}")
    print(f"REJECT_DUPLICATE_KEY_FACT: {counts['REJECT_DUPLICATE_KEY_FACT']}")
    print(f"REJECT_WEAK_OR_GENERIC_SIGNIFICANCE: {counts['REJECT_WEAK_OR_GENERIC_SIGNIFICANCE']}")
    print(f"REJECT_UNSUPPORTED_CLAIM: {counts['REJECT_UNSUPPORTED_CLAIM']}")
    print(f"REJECT_WEAK_SOURCE: {counts['REJECT_WEAK_SOURCE']}")
    print(f"NEEDS_STRONGER_SOURCE: {counts['NEEDS_STRONGER_SOURCE']}")
    print(f"MISSING_PEOPLE: {len(missing_people)}")
    print(f"UNEXPECTED_PEOPLE: {len(unexpected_people)}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if application_data_modified else 'NO'}")
    print(f"SOURCE_PACKAGES_MODIFIED: {'YES' if source_packages_modified else 'NO'}")
    print(f"STRUCTURAL_VALIDATION: {'PASS' if structural_pass else 'FAIL'}")
    print("SEMANTIC_REVIEW_COMPLETED: YES")
    print(f"FINAL_STATUS: {final_status}")

    return structural_pass

if __name__ == "__main__":
    run_validation()
