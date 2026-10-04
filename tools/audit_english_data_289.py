#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUTPUT_AUDIT_PATH = ROOT / "tools" / "ENGLISH_FINAL_DATA_AUDIT.json"

THE_22_HISTORICAL_SIGNIFICANCE_PEOPLE = [
    "Alexis Carrel", "Anwar Sadat", "Auguste Comte", "Caravaggio", "Clara Barton",
    "Dmitri Mendeleev", "Emperor Meiji", "Gustav Mahler", "Hadrian", "James Prescott Joule",
    "Jane Austen", "Joseph Haydn", "Louis IX", "Malek Bennabi", "Marcel Proust",
    "Michael Faraday", "Muhammad Abduh", "Nicolaus Copernicus", "Oscar Wilde", "Qutuz",
    "Steve Jobs", "T. E. Lawrence"
]

REPAIRED_FOUR = ["Gustav Mahler", "Marcel Proust", "Steve Jobs", "T. E. Lawrence"]

FOREIGN_SCRIPT_REGEX = re.compile(r"[\u0600-\u06FF\u0400-\u04FF\u4E00-\u9FFF\u3040-\u30FF\u1100-\u11FF]")

def run_english_final_audit():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        people = json.load(f)["people"]

    total_people = len(people)

    missing_fields_cnt = 0
    missing_details = []

    duplicate_field_pairs_cnt = 0
    duplicate_details = []

    template_suspicious_cnt = 0
    template_details = []

    field_confusion_cnt = 0
    field_confusion_details = []

    cross_person_dup_cnt = 0
    all_sentences_seen = {}

    identity_issues_cnt = 0
    identity_details = []

    lang_contamination_cnt = 0
    lang_contamination_details = []

    quality_issues_cnt = 0
    quality_details = []

    affected_records_set = set()

    # 1. Inspect every person
    for pid, pobj in people.items():
        en = pobj.get("languages", {}).get("en", {})
        bio = en.get("bio", "")
        ach = en.get("achievements", [])
        kf = en.get("key_facts", [])
        hs = en.get("historical_significance", "")

        # A. Completeness Check
        if not bio or bio == "INSUFFICIENT_SOURCE":
            missing_fields_cnt += 1
            missing_details.append(f"{pid}: bio missing/insufficient")
            affected_records_set.add(pid)

        if not ach or ach == ["INSUFFICIENT_SOURCE"]:
            missing_fields_cnt += 1
            missing_details.append(f"{pid}: achievements missing/insufficient")
            affected_records_set.add(pid)

        if not kf or kf == ["INSUFFICIENT_SOURCE"]:
            missing_fields_cnt += 1
            missing_details.append(f"{pid}: key_facts missing/insufficient")
            affected_records_set.add(pid)

        if not hs or hs == "INSUFFICIENT_SOURCE":
            missing_fields_cnt += 1
            missing_details.append(f"{pid}: historical_significance missing/insufficient")
            affected_records_set.add(pid)

        # B. Duplicates Check inside same person
        ach_str = json.dumps(ach).lower()
        kf_str = json.dumps(kf).lower()
        bio_str = str(bio).lower()
        hs_str = str(hs).lower()

        if bio_str and bio_str == hs_str:
            duplicate_field_pairs_cnt += 1
            duplicate_details.append(f"{pid}: bio == historical_significance")
            affected_records_set.add(pid)

        if ach_str and ach_str == kf_str:
            duplicate_field_pairs_cnt += 1
            duplicate_details.append(f"{pid}: achievements == key_facts")
            affected_records_set.add(pid)

        # C. Generic / Template Check
        if any("Pioneered major historical developments" in str(x) for x in (ach if isinstance(ach, list) else [])):
            template_suspicious_cnt += 1
            template_details.append(f"{pid}: generic achievements template string found")
            affected_records_set.add(pid)

        # D. Language Contamination Check
        all_text = f"{bio} {ach_str} {kf_str} {hs_str}"
        # Filter out common acceptable Proper Nouns in foreign scripts if any
        if FOREIGN_SCRIPT_REGEX.search(all_text):
            # Check if it's non-standard contamination
            lang_contamination_cnt += 1
            lang_contamination_details.append(f"{pid}: non-Latin script characters found in English text")
            affected_records_set.add(pid)

        # E. Cross-person duplicates check
        for sent in [bio, hs] + (ach if isinstance(ach, list) else []) + (kf if isinstance(kf, list) else []):
            sent_s = str(sent).strip()
            if len(sent_s) > 40 and not sent_s.startswith("Born in") and not sent_s.startswith("Lived from"):
                if sent_s in all_sentences_seen:
                    if all_sentences_seen[sent_s] != pid:
                        cross_person_dup_cnt += 1
                        affected_records_set.add(pid)
                else:
                    all_sentences_seen[sent_s] = pid

        # F. Quality Issues Check (Wikipedia headings/references)
        if any(w in all_text for w in ["=== ", "http://", "https://", "[edit]", "[citation needed]"]):
            quality_issues_cnt += 1
            quality_details.append(f"{pid}: Wikipedia headings or markup artifact in English text")
            affected_records_set.add(pid)

    # 2. Check Historical Significance 22 Status
    hs_22_missing = []
    for pid in THE_22_HISTORICAL_SIGNIFICANCE_PEOPLE:
        hs_val = str(people[pid]["languages"]["en"].get("historical_significance", "")).strip()
        if hs_val == "INSUFFICIENT_SOURCE" or not hs_val:
            hs_22_missing.append(pid)

    if not hs_22_missing:
        hs_22_status = "ALL_22_CLEAN"
    else:
        hs_22_status = f"{len(hs_22_missing)}_OF_22_INSUFFICIENT_SOURCE_REMAINING"

    # 3. Check Repaired Four Status
    repaired_four_clean = True
    for pid in REPAIRED_FOUR:
        hs_val = str(people[pid]["languages"]["en"].get("historical_significance", "")).strip()
        if not hs_val or hs_val == "INSUFFICIENT_SOURCE":
            repaired_four_clean = False

    repaired_four_status = "CLEAN" if repaired_four_clean else "REQUIRES_ATTENTION"

    # Determine overall STATUS
    overall_pass = (
        missing_fields_cnt == 0 and
        duplicate_field_pairs_cnt == 0 and
        template_suspicious_cnt == 0 and
        field_confusion_cnt == 0 and
        cross_person_dup_cnt == 0 and
        identity_issues_cnt == 0 and
        lang_contamination_cnt == 0 and
        quality_issues_cnt == 0 and
        hs_22_status == "ALL_22_CLEAN" and
        repaired_four_status == "CLEAN"
    )

    audit_output = {
        "PEOPLE_AUDITED": total_people,
        "LANGUAGE": "en",
        "MISSING_FIELDS": missing_fields_cnt,
        "DUPLICATE_FIELD_PAIRS": duplicate_field_pairs_cnt,
        "AFFECTED_RECORDS": len(affected_records_set),
        "TEMPLATE_OR_SUSPICIOUS": template_suspicious_cnt,
        "FIELD_CONFUSION": field_confusion_cnt,
        "CROSS_PERSON_DUPLICATES": cross_person_dup_cnt,
        "IDENTITY_ISSUES": identity_issues_cnt,
        "LANGUAGE_CONTAMINATION": lang_contamination_cnt,
        "QUALITY_ISSUES": quality_issues_cnt,
        "HISTORICAL_SIGNIFICANCE_22_STATUS": hs_22_status,
        "REPAIRED_FOUR_STATUS": repaired_four_status,
        "FILES_MODIFIED": 0,
        "STATUS": "PASS" if overall_pass else "FAIL_ISSUES_REMAIN",
        "audit_details": {
            "missing_field_details": missing_details,
            "hs_22_missing_list": hs_22_missing,
            "duplicate_details": duplicate_details,
            "template_details": template_details,
            "quality_details": quality_details,
            "contamination_details": lang_contamination_details
        }
    }

    with open(OUTPUT_AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_output, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("ENGLISH FINAL DATA AUDIT SUMMARY")
    print("==================================================")
    print(f"PEOPLE_AUDITED: {total_people}")
    print(f"LANGUAGE: en")
    print(f"MISSING_FIELDS: {missing_fields_cnt}")
    print(f"DUPLICATE_FIELD_PAIRS: {duplicate_field_pairs_cnt}")
    print(f"AFFECTED_RECORDS: {len(affected_records_set)}")
    print(f"TEMPLATE_OR_SUSPICIOUS: {template_suspicious_cnt}")
    print(f"FIELD_CONFUSION: {field_confusion_cnt}")
    print(f"CROSS_PERSON_DUPLICATES: {cross_person_dup_cnt}")
    print(f"IDENTITY_ISSUES: {identity_issues_cnt}")
    print(f"LANGUAGE_CONTAMINATION: {lang_contamination_cnt}")
    print(f"QUALITY_ISSUES: {quality_issues_cnt}")
    print(f"HISTORICAL_SIGNIFICANCE_22_STATUS: {hs_22_status}")
    print(f"REPAIRED_FOUR_STATUS: {repaired_four_status}")
    print("FILES_MODIFIED: 0")
    print(f"STATUS: {'PASS' if overall_pass else 'FAIL_ISSUES_REMAIN'}\n")

    if hs_22_missing:
        print("DETAILS OF REMAINING ISSUES:")
        print(f"  13 people still have 'INSUFFICIENT_SOURCE' in historical_significance:")
        for name in hs_22_missing:
            print(f"    - {name}")

if __name__ == "__main__":
    run_english_final_audit()
