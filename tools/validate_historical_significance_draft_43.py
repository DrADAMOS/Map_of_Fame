#!/usr/bin/env python3
"""
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_DRAFT_43.JSON
Validates the historical significance draft against adjudication requirements, source packages, and protected file invariants.
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
DRAFT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_DRAFT_43.json"

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

    if not DRAFT_PATH.exists():
        print("ERROR: Draft file not found.")
        return False

    with open(DRAFT_PATH, "r", encoding="utf-8") as f:
        draft_data = json.load(f)

    entries = draft_data.get("entries", [])
    draft_people = [e["person"] for e in entries]

    # Load all source packages
    def load_pkg(path):
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("entries", [])

    all_source_entries = load_pkg(PKG_43_PATH) + load_pkg(REPAIR_PKG_5_PATH) + load_pkg(REPAIR_PKG_3_PATH)
    valid_source_titles = {s.get("source_title") for s in all_source_entries}

    # Load person data for duplication checks
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)
    people_dict = i18n_data.get("people", {})

    ready_count = 0
    needs_stronger_source_count = 0
    missing_people = set(target_people) - set(draft_people)
    unexpected_people = set(draft_people) - set(target_people)

    proposed_texts_seen = {}
    duplicate_proposed_texts_count = 0

    for entry in entries:
        p = entry.get("person")
        text = entry.get("proposed_text", "")
        field = entry.get("field")
        cls = entry.get("classification")
        src_recs = entry.get("source_records", [])

        if cls == "READY_FOR_REVIEW":
            ready_count += 1
        elif cls == "NEEDS_STRONGER_SOURCE":
            needs_stronger_source_count += 1

        if text in proposed_texts_seen:
            duplicate_proposed_texts_count += 1
        else:
            proposed_texts_seen[text] = p

    exact_target_match = (sorted(target_people) == sorted(draft_people))

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

    structural_val = "PASS" if structural_pass else "FAIL"

    print("HISTORICAL SIGNIFICANCE DRAFT 43")
    print("--------------------------------")
    print(f"TARGET_PEOPLE: {len(target_people)}")
    print(f"READY_FOR_REVIEW: {ready_count}")
    print(f"NEEDS_STRONGER_SOURCE: {needs_stronger_source_count}")
    print(f"MISSING_PEOPLE: {len(missing_people)}")
    print(f"DUPLICATE_PROPOSED_TEXTS: {duplicate_proposed_texts_count}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if application_data_modified else 'NO'}")
    print(f"SOURCE_PACKAGES_MODIFIED: {'YES' if source_packages_modified else 'NO'}")
    print(f"STRUCTURAL_VALIDATION: {structural_val}")
    print("SEMANTIC_REVIEW_REQUIRED: YES")

    print("\nPROPOSED ENTRIES SUMMARY:")
    print("=" * 70)
    for entry in entries:
        print(f"Person: {entry.get('person')}")
        print(f"Proposed Text: {entry.get('proposed_text')}")
        src_title = entry.get('source_records', [{}])[0].get('source_title', 'Unknown')
        print(f"Source: {src_title}")
        print(f"Source Basis: {entry.get('source_basis')}")
        print(f"Classification: {entry.get('classification')}")
        print("-" * 70)

    return structural_pass

if __name__ == "__main__":
    run_validation()
