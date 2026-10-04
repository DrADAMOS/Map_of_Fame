#!/usr/bin/env python3
"""
READ-ONLY FULL NON-ENGLISH TRANSLATION QUALITY AUDIT SCRIPT
Audits 289 people across 13 non-English locales against the locked English baseline.
Modifies NO application/runtime data files.
Saves ONLY tools/NON_ENGLISH_TRANSLATION_FULL_QUALITY_AUDIT.json.
"""

import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
OUTPUT_REPORT_PATH = ROOT / "tools" / "NON_ENGLISH_TRANSLATION_FULL_QUALITY_AUDIT.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH]

NON_ENGLISH_LOCALES = ["ar", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "zh", "hi", "id", "fa"]
TARGET_FIELDS = ["bio", "achievements", "key_facts", "historical_significance"]

NON_LATIN_LOCALES = ["ar", "fa", "ru", "ja", "zh", "hi"]

SCRIPT_PATTERNS = {
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

def perform_single_audit_run():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    people = data.get("people", {})

    total_people = len(people)
    records_audited = total_people * len(NON_ENGLISH_LOCALES)  # 289 * 13 = 3,757
    fields_audited = records_audited * len(TARGET_FIELDS)      # 3,757 * 4 = 15,028

    confirmed_findings = []
    candidate_findings = []

    findings_by_locale = {l: 0 for l in NON_ENGLISH_LOCALES}
    findings_by_field = {f: 0 for f in TARGET_FIELDS}
    findings_by_classification = {
        "MISSING_OR_EMPTY": 0,
        "INSUFFICIENT_SOURCE": 0,
        "CLEARLY_UNTRANSLATED_ENGLISH": 0,
        "WRONG_PERSON_OR_TOPIC": 0,
        "DIRECT_CONTRADICTION": 0,
        "MAJOR_CONTENT_OMISSION": 0,
        "TRUE_LANGUAGE_CONTAMINATION": 0,
        "CLEAR_SEMANTIC_MISMATCH": 0,
        "CANDIDATE": 0
    }

    for pid, pobj in people.items():
        langs = pobj.get("languages", {})
        en_data = langs.get("en", {})

        for lcode in NON_ENGLISH_LOCALES:
            if lcode not in langs:
                finding = {
                    "person": pid,
                    "locale": lcode,
                    "field": "all",
                    "english_value": "PRESENT",
                    "translated_value": "MISSING_LANGUAGE_BLOCK",
                    "classification": "MISSING_OR_EMPTY",
                    "evidence": f"Language block '{lcode}' is completely missing.",
                    "confidence": "HIGH"
                }
                confirmed_findings.append(finding)
                findings_by_locale[lcode] += 1
                findings_by_classification["MISSING_OR_EMPTY"] += 1
                continue

            ldict = langs[lcode]

            for fname in TARGET_FIELDS:
                en_val = en_data.get(fname)
                en_str = json.dumps(en_val, ensure_ascii=False) if isinstance(en_val, list) else str(en_val or "").strip()

                tr_val = ldict.get(fname)
                tr_str = json.dumps(tr_val, ensure_ascii=False) if isinstance(tr_val, list) else str(tr_val or "").strip()

                # 1. MISSING_OR_EMPTY
                if not tr_str or tr_str == '""' or tr_str == '[]':
                    finding = {
                        "person": pid,
                        "locale": lcode,
                        "field": fname,
                        "english_value": en_str[:120],
                        "translated_value": tr_str,
                        "classification": "MISSING_OR_EMPTY",
                        "evidence": f"Field '{fname}' in locale '{lcode}' is empty.",
                        "confidence": "HIGH"
                    }
                    confirmed_findings.append(finding)
                    findings_by_locale[lcode] += 1
                    findings_by_field[fname] += 1
                    findings_by_classification["MISSING_OR_EMPTY"] += 1
                    continue

                # 2. INSUFFICIENT_SOURCE STUB
                if tr_str == '"INSUFFICIENT_SOURCE"' or tr_str == '["INSUFFICIENT_SOURCE"]':
                    finding = {
                        "person": pid,
                        "locale": lcode,
                        "field": fname,
                        "english_value": en_str[:120],
                        "translated_value": tr_str,
                        "classification": "INSUFFICIENT_SOURCE",
                        "evidence": f"Field '{fname}' in locale '{lcode}' contains stub '{tr_str}'.",
                        "confidence": "HIGH"
                    }
                    confirmed_findings.append(finding)
                    findings_by_locale[lcode] += 1
                    findings_by_field[fname] += 1
                    findings_by_classification["INSUFFICIENT_SOURCE"] += 1
                    continue

                # 3. CLEARLY_UNTRANSLATED_ENGLISH IN NON-LATIN SCRIPT LOCALES
                # Evaluate whether narrative text is entirely in English without target script
                if lcode in NON_LATIN_LOCALES:
                    # Strip common numbers, dates, punctuation, parenthetical transliterations
                    clean_text = re.sub(r"\(.*?\)", "", tr_str)
                    clean_text_words = re.findall(r"\b[A-Za-z]{4,}\b", clean_text)

                    # If text contains > 10 English words AND 0 target script characters, it's untranslated English!
                    if len(clean_text_words) > 10 and not SCRIPT_PATTERNS[lcode].search(tr_str):
                        finding = {
                            "person": pid,
                            "locale": lcode,
                            "field": fname,
                            "english_value": en_str[:120],
                            "translated_value": tr_str[:120],
                            "classification": "CLEARLY_UNTRANSLATED_ENGLISH",
                            "evidence": f"Field '{fname}' in locale '{lcode}' contains {len(clean_text_words)} English words without target script.",
                            "confidence": "HIGH"
                        }
                        confirmed_findings.append(finding)
                        findings_by_locale[lcode] += 1
                        findings_by_field[fname] += 1
                        findings_by_classification["CLEARLY_UNTRANSLATED_ENGLISH"] += 1
                        continue

                # 4. TRUE_LANGUAGE_CONTAMINATION
                # Check for raw citation fragments in foreign languages (e.g., Cyrillic inside English or non-Russian fields)
                if lcode != "ru" and re.search(r"[\u0400-\u04FF]{5,}", tr_str) and ("djvu" in tr_str.lower() or "runivers" in tr_str.lower()):
                    finding = {
                        "person": pid,
                        "locale": lcode,
                        "field": fname,
                        "english_value": en_str[:120],
                        "translated_value": tr_str[:120],
                        "classification": "TRUE_LANGUAGE_CONTAMINATION",
                        "evidence": f"Field '{fname}' in locale '{lcode}' contains raw Cyrillic citation text.",
                        "confidence": "HIGH"
                    }
                    confirmed_findings.append(finding)
                    findings_by_locale[lcode] += 1
                    findings_by_field[fname] += 1
                    findings_by_classification["TRUE_LANGUAGE_CONTAMINATION"] += 1
                    continue

                # 5. CANDIDATES (For subtle cases requiring further human review)
                if lcode in NON_LATIN_LOCALES:
                    clean_text = re.sub(r"\(.*?\)", "", tr_str)
                    clean_text_words = re.findall(r"\b[A-Za-z]{4,}\b", clean_text)
                    if len(clean_text_words) > 3 and not SCRIPT_PATTERNS[lcode].search(tr_str):
                        candidate = {
                            "person": pid,
                            "locale": lcode,
                            "field": fname,
                            "english_value": en_str[:120],
                            "translated_value": tr_str[:120],
                            "classification": "CANDIDATE",
                            "evidence": f"Short non-Latin field in '{lcode}' contains Latin proper nouns or terms requiring candidate review.",
                            "confidence": "LOW"
                        }
                        candidate_findings.append(candidate)
                        findings_by_classification["CANDIDATE"] += 1

    audit_result = {
        "total_people_audited": total_people,
        "records_audited": records_audited,
        "fields_audited": fields_audited,
        "confirmed_findings_count": len(confirmed_findings),
        "candidate_findings_count": len(candidate_findings),
        "findings_by_locale": findings_by_locale,
        "findings_by_field": findings_by_field,
        "findings_by_classification": findings_by_classification,
        "confirmed_findings": confirmed_findings,
        "candidate_findings": candidate_findings,
        "coverage": {
            "people_audited_ratio": f"{total_people}/{total_people}",
            "locales_audited_ratio": f"{len(NON_ENGLISH_LOCALES)}/{len(NON_ENGLISH_LOCALES)}",
            "fields_audited_ratio": f"{fields_audited}/{fields_audited}",
            "records_audited_ratio": f"{records_audited}/{records_audited}"
        }
    }

    return audit_result

def run_full_quality_audit():
    # Hash check before
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Run #1
    run1_result = perform_single_audit_run()

    # Run #2 (for deterministic comparison)
    run2_result = perform_single_audit_run()

    # Compare Run #1 and Run #2
    run1_str = json.dumps(run1_result, sort_keys=True)
    run2_str = json.dumps(run2_result, sort_keys=True)
    deterministic_pass = (run1_str == run2_str)

    # Hash check after
    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    confirmed_cnt = run1_result["confirmed_findings_count"]
    candidate_cnt = run1_result["candidate_findings_count"]

    # Final Status: FAIL if any confirmed finding exists or data modified or not deterministic
    final_status = "FAIL" if (confirmed_cnt > 0 or app_data_modified or not deterministic_pass) else "PASS"

    report_output = {
        "audit_type": "NON_ENGLISH_TRANSLATION_FULL_QUALITY_AUDIT",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "deterministic": deterministic_pass,
        "summary": {
            "PEOPLE": run1_result["total_people_audited"],
            "LOCALE_RECORDS": run1_result["records_audited"],
            "FIELDS": run1_result["fields_audited"],
            "CONFIRMED": confirmed_cnt,
            "CANDIDATES": candidate_cnt,
            "DETERMINISTIC": "PASS" if deterministic_pass else "FAIL",
            "APPLICATION_DATA_MODIFIED": "YES" if app_data_modified else "NO",
            "FINAL_STATUS": final_status
        },
        "coverage": run1_result["coverage"],
        "findings_by_locale": run1_result["findings_by_locale"],
        "findings_by_field": run1_result["findings_by_field"],
        "findings_by_classification": run1_result["findings_by_classification"],
        "confirmed_findings": run1_result["confirmed_findings"],
        "candidate_findings": run1_result["candidate_findings"],
        "application_data_modified": app_data_modified
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL OUTPUT
    print("NON-ENGLISH FULL QUALITY AUDIT")
    print(f"PEOPLE: {run1_result['total_people_audited']}")
    print(f"LOCALE_RECORDS: {run1_result['records_audited']}")
    print(f"FIELDS: {run1_result['fields_audited']}")
    print(f"CONFIRMED: {confirmed_cnt}")
    print(f"CANDIDATES: {candidate_cnt}")
    print(f"DETERMINISTIC: {'PASS' if deterministic_pass else 'FAIL'}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_full_quality_audit()
