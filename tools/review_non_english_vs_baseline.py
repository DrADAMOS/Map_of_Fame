#!/usr/bin/env python3
"""
READ-ONLY NON-ENGLISH VS LOCKED ENGLISH BASELINE AUDIT
Audits 13 non-English locales against the locked English baseline across 289 people.
Saves ONLY tools/NON_ENGLISH_VS_ENGLISH_BASELINE_REVIEW.json.
Modifies NO application/runtime data files.
"""

import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "NON_ENGLISH_VS_ENGLISH_BASELINE_REVIEW.json"

NON_ENGLISH_LOCALES = ["ar", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "zh", "hi", "id", "fa"]
REQUIRED_FIELDS = ["bio", "achievements", "key_facts", "historical_significance"]

# Script expectations per locale
LOCALE_SCRIPT_REGEXES = {
    "ar": re.compile(r"[\u0600-\u06FF]"),
    "fa": re.compile(r"[\u0600-\u06FF]"),
    "ru": re.compile(r"[\u0400-\u04FF]"),
    "ja": re.compile(r"[\u3040-\u30FF\u4E00-\u9FFF]"),
    "zh": re.compile(r"[\u4E00-\u9FFF]"),
    "hi": re.compile(r"[\u0900-\u097F]")
}

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_non_english_review():
    startup_hash = calculate_file_hash(PERSON_I18N_PATH)

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    people = data.get("people", {})

    records_inspected = len(people) * len(NON_ENGLISH_LOCALES)  # 289 * 13 = 3,757
    fields_inspected = records_inspected * len(REQUIRED_FIELDS)  # 3,757 * 4 = 15,028

    confirmed_problems = []
    candidate_review = []

    problems_by_locale = {l: 0 for l in NON_ENGLISH_LOCALES}
    problems_by_field = {f: 0 for f in REQUIRED_FIELDS}

    for pid, pobj in people.items():
        langs = pobj.get("languages", {})
        en_data = langs.get("en", {})

        for lcode in NON_ENGLISH_LOCALES:
            if lcode not in langs:
                # Confirmed Problem: Missing entire language block
                prob = {
                    "person": pid,
                    "locale": lcode,
                    "field": "all",
                    "english_baseline": "PRESENT",
                    "translated_value": "MISSING_LANGUAGE_BLOCK",
                    "problem_type": "MISSING_FIELD",
                    "explanation": f"Language block '{lcode}' is completely missing from person record."
                }
                confirmed_problems.append(prob)
                problems_by_locale[lcode] += 1
                continue

            ldict = langs[lcode]

            for fname in REQUIRED_FIELDS:
                en_val = en_data.get(fname)
                en_str = json.dumps(en_val) if isinstance(en_val, list) else str(en_val or "").strip()

                tr_val = ldict.get(fname)
                tr_str = json.dumps(tr_val) if isinstance(tr_val, list) else str(tr_val or "").strip()

                # 1. MISSING / EMPTY FIELD
                if not tr_str or tr_str == '""' or tr_str == '[]':
                    prob = {
                        "person": pid,
                        "locale": lcode,
                        "field": fname,
                        "english_baseline": en_str[:120],
                        "translated_value": tr_str,
                        "problem_type": "EMPTY_FIELD",
                        "explanation": f"Field '{fname}' in locale '{lcode}' is empty."
                    }
                    confirmed_problems.append(prob)
                    problems_by_locale[lcode] += 1
                    problems_by_field[fname] += 1
                    continue

                # 2. UNTRANSLATED ENGLISH TEXT WHEN TRANSLATION IS EXPECTED
                if lcode in ["ar", "fa", "ru", "ja", "zh", "hi"]:
                    if len(tr_str) > 30 and not LOCALE_SCRIPT_REGEXES[lcode].search(tr_str):
                        prob = {
                            "person": pid,
                            "locale": lcode,
                            "field": fname,
                            "english_baseline": en_str[:120],
                            "translated_value": tr_str[:120],
                            "problem_type": "ENGLISH_TEXT_UNTRANSLATED_WHEN_TRANSLATION_IS_EXPECTED",
                            "explanation": f"Field '{fname}' in locale '{lcode}' contains untranslated English text without target script."
                        }
                        confirmed_problems.append(prob)
                        problems_by_locale[lcode] += 1
                        problems_by_field[fname] += 1

    total_confirmed = len(confirmed_problems)
    total_candidates = len(candidate_review)

    # Shutdown File Hash Protection
    shutdown_hash = calculate_file_hash(PERSON_I18N_PATH)
    app_data_modified = (startup_hash != shutdown_hash)

    report_data = {
        "audit_type": "NON_ENGLISH_VS_ENGLISH_BASELINE_REVIEW",
        "read_only": True,
        "files_modified": 0,
        "english_baseline_status": "LOCKED",
        "locales_inspected": NON_ENGLISH_LOCALES,
        "records_inspected": records_inspected,
        "fields_inspected": fields_inspected,
        "total_confirmed_problems": total_confirmed,
        "total_candidates": total_candidates,
        "problems_by_locale": problems_by_locale,
        "problems_by_field": problems_by_field,
        "confirmed_problems": confirmed_problems,
        "candidate_review": candidate_review,
        "application_data_modified": app_data_modified
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("ENGLISH BASELINE: LOCKED")
    print(f"LOCALES INSPECTED: {len(NON_ENGLISH_LOCALES)}")
    print(f"FIELDS INSPECTED: {fields_inspected}")
    print(f"CONFIRMED PROBLEMS: {total_confirmed}")
    print(f"CANDIDATES: {total_candidates}")
    print(f"APPLICATION DATA MODIFIED: {'YES' if app_data_modified else 'NO'}")

if __name__ == "__main__":
    run_non_english_review()
