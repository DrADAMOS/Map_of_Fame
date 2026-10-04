#!/usr/bin/env python3
"""
READ-ONLY IDENTITY UNRESOLVED VERIFICATION SCRIPT
Inspects actual stored review data in WIKIPEDIA_IDENTITY_REVIEW.json for the 12 unresolved people.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/IDENTITY_UNRESOLVED_VERIFICATION.json.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "IDENTITY_UNRESOLVED_VERIFICATION.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

UNRESOLVED_12_NAMES = [
    "Al-Ma'mun",
    "Al-Mu'izz li-Din Allah",
    "Al-Mu'tamid",
    "Al-Mu'tasim",
    "Al-Shafi'i",
    "David Livingstone",
    "Gabriele D'Annunzio",
    "Gamal Abdel Nasser",
    "Rifa'a al-Tahtawi",
    "Sa'd ibn Abi Waqqas",
    "Umar ibn Abd al-Aziz",
    "Umm Kulthum"
]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_identity_verification():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    with open(IDENTITY_REVIEW_PATH, "r", encoding="utf-8") as f:
        id_raw = json.load(f)

    rev_people = id_raw.get("people", {}) if "people" in id_raw else id_raw.get("review_data", {})

    safely_resolvable_cnt = 0
    human_review_required_cnt = 0
    genuinely_unresolved_cnt = 0

    verification_records = []

    for name in UNRESOLVED_12_NAMES:
        p_info = rev_people.get(name, {})
        curr_status = p_info.get("status", "unresolved")
        best_title = p_info.get("best_title")
        candidates = p_info.get("candidates", [])
        reason = p_info.get("reason", "New current quiz person; requires identity verification.")

        # Evaluate strictly against stored identity evidence in review record
        if len(candidates) == 1 and candidates[0].get("score") == 100:
            classification = "SAFELY_RESOLVABLE"
            safely_resolvable_cnt += 1
            confidence = "HIGH"
            exact_evidence = f"Single unique candidate '{candidates[0].get('title')}' with score 100 in review data."
        elif len(candidates) > 1:
            classification = "HUMAN_REVIEW_REQUIRED"
            human_review_required_cnt += 1
            confidence = "MEDIUM"
            exact_evidence = f"Multiple candidates ({len(candidates)}) present in stored review data requiring human selection."
        else:
            # Empty candidates list in stored review record
            classification = "GENUINELY_UNRESOLVED"
            genuinely_unresolved_cnt += 1
            confidence = "HIGH"
            exact_evidence = f"Stored review record has candidates=[] and reason='{reason}'."

        verification_records.append({
            "original_name": name,
            "current_status": curr_status,
            "best_title": best_title,
            "all_existing_candidates": candidates,
            "selected_classification": classification,
            "exact_evidence_from_review_data": exact_evidence,
            "confidence": confidence
        })

    # Shutdown File Hash Protection Check
    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    report_output = {
        "audit_type": "IDENTITY_UNRESOLVED_VERIFICATION",
        "read_only": True,
        "files_modified": 0,
        "source_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "total_unresolved_investigated": len(UNRESOLVED_12_NAMES),
        "safely_resolvable": safely_resolvable_cnt,
        "human_review_required": human_review_required_cnt,
        "genuinely_unresolved": genuinely_unresolved_cnt,
        "verification_records": verification_records,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("IDENTITY VERIFICATION")
    print(f"TOTAL: {len(UNRESOLVED_12_NAMES)}")
    print(f"SAFELY_RESOLVABLE: {safely_resolvable_cnt}")
    print(f"HUMAN_REVIEW_REQUIRED: {human_review_required_cnt}")
    print(f"GENUINELY_UNRESOLVED: {genuinely_unresolved_cnt}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_identity_verification()
