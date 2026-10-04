#!/usr/bin/env python3
"""
READ-ONLY NON-ENGLISH TRANSLATION EVIDENCE INSPECTION SCRIPT
Inspects 3 representative people across 6 non-Latin script locales in person_i18n.json.
Saves ONLY tools/NON_ENGLISH_TRANSLATION_EVIDENCE_SAMPLE.json.
Modifies NO application/runtime data files.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "NON_ENGLISH_TRANSLATION_EVIDENCE_SAMPLE.json"

TARGET_LOCALES = ["ar", "ru", "ja", "zh", "hi", "fa"]
INSPECT_FIELDS = ["achievements", "key_facts", "historical_significance"]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def classify_text_language(val, lcode):
    val_str = json.dumps(val, ensure_ascii=False) if isinstance(val, list) else str(val or "")
    if not val_str or val_str in ['""', '[]', '"INSUFFICIENT_SOURCE"', '["INSUFFICIENT_SOURCE"]']:
        return "UNCERTAIN"

    has_target = False
    if lcode in ["ar", "fa"] and any("\u0600" <= c <= "\u06FF" for c in val_str):
        has_target = True
    elif lcode == "ru" and any("\u0400" <= c <= "\u04FF" for c in val_str):
        has_target = True
    elif lcode == "ja" and any("\u3040" <= c <= "\u30FF" or "\u4E00" <= c <= "\u9FFF" for c in val_str):
        has_target = True
    elif lcode == "zh" and any("\u4E00" <= c <= "\u9FFF" for c in val_str):
        has_target = True
    elif lcode == "hi" and any("\u0900" <= c <= "\u097F" for c in val_str):
        has_target = True

    # Check Latin character presence
    latin_chars = [c for c in val_str if "a" <= c.lower() <= "z"]
    has_substantive_latin = len(latin_chars) > 20

    if has_target and not has_substantive_latin:
        return "CLEARLY_TARGET_LANGUAGE"
    elif has_target and has_substantive_latin:
        return "MIXED_LANGUAGE"
    elif has_substantive_latin and not has_target:
        return "CLEARLY_ENGLISH"
    else:
        return "CLEARLY_TARGET_LANGUAGE" if has_target else "UNCERTAIN"

def run_evidence_inspection():
    startup_hash = calculate_file_hash(PERSON_I18N_PATH)

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    people = data.get("people", {})
    person_keys = list(people.keys())

    first_person = person_keys[0]  # Ramesses II
    middle_person = person_keys[len(person_keys) // 2]  # Auguste Comte
    last_person = person_keys[-1]  # Diego Maradona

    representative_people = [first_person, middle_person, last_person]

    locale_evidence = {}
    byte_identical_counts = {l: {"achievements": 0, "key_facts": 0, "historical_significance": 0} for l in TARGET_LOCALES}

    # 1. Byte-for-byte identical calculations against English across all 289 people
    for pid, pobj in people.items():
        langs = pobj.get("languages", {})
        en_data = langs.get("en", {})

        for lcode in TARGET_LOCALES:
            if lcode in langs:
                ldict = langs[lcode]
                for fn in INSPECT_FIELDS:
                    en_val = en_data.get(fn)
                    tr_val = ldict.get(fn)

                    if en_val == tr_val:
                        byte_identical_counts[lcode][fn] += 1

    # 2. Detailed sample inspection of representative people
    for lcode in TARGET_LOCALES:
        locale_evidence[lcode] = []

        for pid in representative_people:
            pobj = people[pid]
            langs = pobj.get("languages", {})
            ldict = langs.get(lcode, {})

            p_evidence = {
                "person": pid,
                "locale": lcode,
                "fields": {}
            }

            for fn in INSPECT_FIELDS:
                tr_val = ldict.get(fn)
                classification = classify_text_language(tr_val, lcode)

                p_evidence["fields"][fn] = {
                    "actual_complete_value": tr_val,
                    "classification": classification
                }

            locale_evidence[lcode].append(p_evidence)

    shutdown_hash = calculate_file_hash(PERSON_I18N_PATH)
    app_data_modified = (startup_hash != shutdown_hash)

    report_output = {
        "audit_type": "NON_ENGLISH_TRANSLATION_EVIDENCE_SAMPLE",
        "read_only": True,
        "files_modified": 0,
        "representative_people": representative_people,
        "target_locales": TARGET_LOCALES,
        "byte_identical_counts": byte_identical_counts,
        "locale_evidence": locale_evidence,
        "application_data_modified": app_data_modified
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("TRANSLATION EVIDENCE SAMPLE")
    for lcode in TARGET_LOCALES:
        cnts = byte_identical_counts[lcode]
        print(f"{lcode}: achievements_identical={cnts['achievements']}, key_facts_identical={cnts['key_facts']}, historical_significance_identical={cnts['historical_significance']}")
    print(f"APPLICATION DATA MODIFIED: {'YES' if app_data_modified else 'NO'}")

if __name__ == "__main__":
    run_evidence_inspection()
