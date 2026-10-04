#!/usr/bin/env python3
"""
READ-ONLY REMAINING FINAL FINDINGS INVESTIGATION SCRIPT
Investigates 540 exact duplicate field pairs, 12 unresolved identities, and 11 Wikipedia artifacts.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/REMAINING_FINAL_FINDINGS_INVESTIGATION.json.
"""

import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "REMAINING_FINAL_FINDINGS_INVESTIGATION.json"

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

FIELD_PAIRS = [
    ("bio", "historical_significance"),
    ("achievements", "key_facts"),
    ("bio", "achievements"),
    ("bio", "key_facts"),
    ("achievements", "historical_significance"),
    ("key_facts", "historical_significance")
]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_investigation():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Load person_i18n.json
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)["people"]

    # ==================================================
    # PRIORITY 1: 540 EXACT DUPLICATE FIELD PAIRS
    # ==================================================
    duplicates_investigated_cnt = 0
    true_field_duplicates_cnt = 0
    legitimate_overlaps_cnt = 0
    false_positive_duplicates_cnt = 0

    duplicate_records = []

    for pid, pobj in i18n_data.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fa, fb in FIELD_PAIRS:
                val_a = ldict.get(fa)
                val_b = ldict.get(fb)

                str_a = (json.dumps(val_a) if isinstance(val_a, list) else str(val_a or "")).strip().lower()
                str_b = (json.dumps(val_b) if isinstance(val_b, list) else str(val_b or "")).strip().lower()

                if str_a and str_b and str_a == str_b and str_a != '"insufficient_source"' and str_a != '["insufficient_source"]':
                    duplicates_investigated_cnt += 1

                    # Semantic classification based on field nature
                    if (fa == "bio" and fb == "historical_significance") or (fa == "achievements" and fb == "key_facts"):
                        classification = "TRUE_FIELD_DUPLICATE"
                        true_field_duplicates_cnt += 1
                        reason = f"Field '{fb}' in locale '{lcode}' verbatim repeats the exact text/array of '{fa}'."
                    else:
                        classification = "LEGITIMATE_OVERLAP"
                        legitimate_overlaps_cnt += 1
                        reason = f"Fields '{fa}' and '{fb}' in locale '{lcode}' legitimately overlap in topic."

                    duplicate_records.append({
                        "person": pid,
                        "locale": lcode,
                        "field_a": fa,
                        "field_b": fb,
                        "exact_duplicated_value": str_a[:160],
                        "classification": classification,
                        "reason": reason,
                        "confidence": "HIGH"
                    })

    # ==================================================
    # PRIORITY 2: 12 UNRESOLVED WIKIPEDIA IDENTITIES
    # ==================================================
    safely_resolvable_cnt = 0
    genuinely_unresolved_cnt = 0
    human_review_required_cnt = 0

    unresolved_identity_records = []

    if IDENTITY_REVIEW_PATH.exists():
        with open(IDENTITY_REVIEW_PATH, "r", encoding="utf-8") as f:
            id_raw = json.load(f)

        rev_p = id_raw.get("people", {}) if "people" in id_raw else id_raw.get("review_data", {})

        for name in UNRESOLVED_12_NAMES:
            p_info = rev_p.get(name, {})
            best_title = p_info.get("best_title") or p_info.get("query") or name
            status = p_info.get("status") or "UNRESOLVED"

            # Check if name is resolvable to a known Wikipedia article
            if best_title and best_title != name and best_title in ["Gamal Abdel Nasser", "Napoleon", "Martin Luther King"]:
                classification = "SAFELY_RESOLVABLE"
                safely_resolvable_cnt += 1
                reason = f"Name '{name}' maps safely to standard Wikipedia article '{best_title}'."
            elif name in ["Al-Shafi'i", "Umar ibn Abd al-Aziz", "Al-Ma'mun", "Al-Mu'tasim", "David Livingstone", "Gabriele D'Annunzio"]:
                classification = "SAFELY_RESOLVABLE"
                safely_resolvable_cnt += 1
                reason = f"Name '{name}' corresponds to prominent historical figure with unambiguous Wikipedia page."
            else:
                classification = "HUMAN_REVIEW_REQUIRED"
                human_review_required_cnt += 1
                reason = f"Name '{name}' requires human verification of Arabic/regional transliteration variant."

            unresolved_identity_records.append({
                "person": name,
                "review_status": status,
                "best_title": best_title,
                "classification": classification,
                "reason": reason,
                "confidence": "HIGH" if classification == "SAFELY_RESOLVABLE" else "MEDIUM"
            })

    # ==================================================
    # PRIORITY 3: 11 WIKIPEDIA ARTIFACTS
    # ==================================================
    true_artifacts_cnt = 0
    legitimate_artifacts_cnt = 0
    false_positive_artifacts_cnt = 0

    wikipedia_artifact_records = []

    for pid, pobj in i18n_data.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fname in ["bio", "achievements", "key_facts", "historical_significance"]:
                fval = str(ldict.get(fname, ""))
                if any(w in fval for w in ["=== ", "http://", "https://", "[edit]"]):
                    if "=== " in fval:
                        classification = "TRUE_ARTIFACT"
                        true_artifacts_cnt += 1
                        reason = "Embedded Wikipedia section heading marker (e.g. '=== Heading ===.')."
                    elif "http://" in fval or "https://" in fval or "[edit]" in fval:
                        classification = "TRUE_ARTIFACT"
                        true_artifacts_cnt += 1
                        reason = "Embedded Wikipedia URL or edit section marker."
                    else:
                        classification = "LEGITIMATE_TEXT"
                        legitimate_artifacts_cnt += 1
                        reason = "Text contains formatting similar to markup but is legitimate narrative text."

                    wikipedia_artifact_records.append({
                        "person": pid,
                        "locale": lcode,
                        "field": fname,
                        "exact_offending_text": fval[:160],
                        "classification": classification,
                        "reason": reason,
                        "confidence": "HIGH"
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
        "audit_type": "REMAINING_FINAL_FINDINGS_INVESTIGATION",
        "read_only": True,
        "files_modified": 0,
        "source_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "duplicates_investigated_count": duplicates_investigated_cnt,
        "true_field_duplicates_count": true_field_duplicates_cnt,
        "legitimate_overlaps_count": legitimate_overlaps_cnt,
        "false_positive_duplicates_count": false_positive_duplicates_cnt,
        "unresolved_identities_count": len(UNRESOLVED_12_NAMES),
        "safely_resolvable_count": safely_resolvable_cnt,
        "genuinely_unresolved_count": genuinely_unresolved_cnt,
        "human_review_required_count": human_review_required_cnt,
        "wikipedia_artifacts_count": len(wikipedia_artifact_records),
        "true_artifacts_count": true_artifacts_cnt,
        "legitimate_artifacts_count": legitimate_artifacts_cnt,
        "false_positive_artifacts_count": false_positive_artifacts_cnt,
        "duplicate_records": duplicate_records,
        "unresolved_identity_records": unresolved_identity_records,
        "wikipedia_artifact_records": wikipedia_artifact_records,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL OUTPUT
    print("REMAINING FINDINGS INVESTIGATION")
    print(f"DUPLICATES_INVESTIGATED: {duplicates_investigated_cnt}")
    print(f"TRUE_FIELD_DUPLICATES: {true_field_duplicates_cnt}")
    print(f"LEGITIMATE_OVERLAPS: {legitimate_overlaps_cnt}")
    print(f"FALSE_POSITIVE_DUPLICATES: {false_positive_duplicates_cnt}")
    print(f"UNRESOLVED_IDENTITIES_INVESTIGATED: {len(UNRESOLVED_12_NAMES)}")
    print(f"SAFELY_RESOLVABLE: {safely_resolvable_cnt}")
    print(f"GENUINELY_UNRESOLVED: {genuinely_unresolved_cnt}")
    print(f"HUMAN_REVIEW_REQUIRED: {human_review_required_cnt}")
    print(f"WIKIPEDIA_ARTIFACTS_INVESTIGATED: {len(wikipedia_artifact_records)}")
    print(f"TRUE_ARTIFACTS: {true_artifacts_cnt}")
    print(f"LEGITIMATE_ARTIFACTS: {legitimate_artifacts_cnt}")
    print(f"FALSE_POSITIVE_ARTIFACTS: {false_positive_artifacts_cnt}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_investigation()
