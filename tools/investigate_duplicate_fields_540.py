#!/usr/bin/env python3
"""
READ-ONLY DUPLICATE FIELD INVESTIGATION SCRIPT (540 CASES)
Investigates all exact duplicate field pairs in person_i18n.json across 289 people and 14 locales.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/DUPLICATE_FIELD_INVESTIGATION_540.json.
"""

import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "DUPLICATE_FIELD_INVESTIGATION_540.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

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

def classify_duplicate_pair(fa, fb, text, lcode):
    text_lower = text.lower()

    # Rule A: achievements <-> key_facts
    if (fa == "achievements" and fb == "key_facts") or (fa == "key_facts" and fb == "achievements"):
        # Verbatim array duplication of concrete accomplishment items
        return "TRUE_FIELD_DUPLICATE", "HIGH", f"Field '{fb}' in locale '{lcode}' verbatim duplicates the accomplishment array of '{fa}'."

    # Rule B: bio <-> historical_significance
    if (fa == "bio" and fb == "historical_significance") or (fa == "historical_significance" and fb == "bio"):
        # Check if text explains broader historical impact vs simple biographical introduction
        if any(w in text_lower for w in ["legacy", "impact", "influence", "revolution", "symbol", "fostered", "reoriented", "pioneered", "transformed", "established"]):
            return "LEGITIMATE_OVERLAP", "MEDIUM", f"Text in locale '{lcode}' explains historical significance and legacy beyond simple biographical facts."
        else:
            return "TRUE_FIELD_DUPLICATE", "HIGH", f"Biographical narrative in locale '{lcode}' was copied directly into '{fb}' without articulating historical impact."

    # Rule C: Other field pairs
    return "TRUE_FIELD_DUPLICATE", "HIGH", f"Identical text stored in both '{fa}' and '{fb}' in locale '{lcode}'."

def run_duplicate_investigation():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)["people"]

    total_candidates = 0
    investigated_cnt = 0
    true_field_duplicates_cnt = 0
    legitimate_overlaps_cnt = 0
    false_positives_cnt = 0

    records = []
    cross_person_records = []
    text_person_map = {}

    for pid, pobj in i18n_data.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fa, fb in FIELD_PAIRS:
                val_a = ldict.get(fa)
                val_b = ldict.get(fb)

                str_a = (json.dumps(val_a, ensure_ascii=False) if isinstance(val_a, list) else str(val_a or "")).strip()
                str_b = (json.dumps(val_b, ensure_ascii=False) if isinstance(val_b, list) else str(val_b or "")).strip()

                if str_a and str_b and str_a == str_b and str_a != '"INSUFFICIENT_SOURCE"' and str_a != '["INSUFFICIENT_SOURCE"]':
                    total_candidates += 1
                    investigated_cnt += 1

                    classification, confidence, reason = classify_duplicate_pair(fa, fb, str_a, lcode)

                    if classification == "TRUE_FIELD_DUPLICATE":
                        true_field_duplicates_cnt += 1
                    elif classification == "LEGITIMATE_OVERLAP":
                        legitimate_overlaps_cnt += 1
                    else:
                        false_positives_cnt += 1

                    records.append({
                        "person": pid,
                        "language": lcode,
                        "field_a": fa,
                        "field_b": fb,
                        "exact_text": str_a,
                        "text_length": len(str_a),
                        "classification": classification,
                        "confidence": confidence,
                        "reason": reason
                    })

                    # Cross-Person Check for duplicated text
                    str_clean = str_a.lower()
                    if len(str_clean) > 40 and not str_clean.startswith("born in") and not str_clean.startswith("lived from"):
                        map_key = (lcode, fa, str_clean)
                        if map_key in text_person_map:
                            prev_p = text_person_map[map_key]
                            if prev_p != pid:
                                cross_person_records.append({
                                    "person_a": prev_p,
                                    "person_b": pid,
                                    "language": lcode,
                                    "field": fa,
                                    "exact_text": str_a[:140],
                                    "classification": "CONFIRMED_CROSS_PERSON_MATCH",
                                    "reason": f"Identical text in locale '{lcode}' field '{fa}' shared between '{prev_p}' and '{pid}'."
                                })
                        else:
                            text_person_map[map_key] = pid

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    report_output = {
        "audit_type": "DUPLICATE_FIELD_INVESTIGATION_540",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "source_file": "app/src/main/assets/person_i18n.json",
        "total_candidates": total_candidates,
        "investigated": investigated_cnt,
        "true_field_duplicates": true_field_duplicates_cnt,
        "legitimate_overlaps": legitimate_overlaps_cnt,
        "false_positives": false_positives_cnt,
        "cross_person_exact_duplicates": len(cross_person_records),
        "records": records,
        "cross_person_records": cross_person_records,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("DUPLICATE FIELD INVESTIGATION")
    print(f"TOTAL_CANDIDATES: {total_candidates}")
    print(f"INVESTIGATED: {investigated_cnt}")
    print(f"TRUE_FIELD_DUPLICATES: {true_field_duplicates_cnt}")
    print(f"LEGITIMATE_OVERLAPS: {legitimate_overlaps_cnt}")
    print(f"FALSE_POSITIVES: {false_positives_cnt}")
    print(f"CROSS_PERSON_EXACT_DUPLICATES: {len(cross_person_records)}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_duplicate_investigation()
