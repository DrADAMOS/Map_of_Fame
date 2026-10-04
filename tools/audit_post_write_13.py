#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
POST_WRITE_AUDIT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_POST_WRITE_AUDIT_13.json"

APPROVED_13_HISTORICAL_SIGNIFICANCE = {
    "Alexis Carrel": "Pioneered concepts in tissue culture, transplantology, and thoracic surgery that laid foundational principles for modern organ transplantation.",
    "Anwar Sadat": "Reoriented Egyptian policy by leading the 1978 Camp David Accords and Egypt–Israel peace treaty, making Egypt the first Arab state to recognize Israel.",
    "Clara Barton": "Founded the American Red Cross and directed its humanitarian relief operations during wars and natural disasters for twenty-three years.",
    "Dmitri Mendeleev": "Formulated the Periodic Law and created a predictive periodic table of elements used to correct known properties and anticipate undiscovered elements.",
    "Hadrian": "Built Hadrian's Wall to mark the northern limit of Britannia and sponsored major Roman architectural works including the rebuilt Pantheon.",
    "James Prescott Joule": "Discovered the relationship between heat and mechanical work, establishing energy principles that led to the First Law of Thermodynamics.",
    "Jane Austen": "Critiqued 18th-century novels of sensibility through her fiction and formed part of the transition toward 19th-century literary realism.",
    "Joseph Haydn": "Instrumental in developing classical chamber music, earning the epithets 'Father of the Symphony' and 'Father of the String Quartet'.",
    "Louis IX": "Consolidated French royal authority, reformed medieval judicial institutions, and was canonized as a Catholic saint in 1297.",
    "Muhammad Abduh": "Served as Grand Mufti of Egypt and a central figure of Islamic Modernism, reforming religious thought through rationalist interpretation.",
    "Nicolaus Copernicus": "Published De revolutionibus orbium coelestium in 1543, triggering the Copernican Revolution and contributing fundamentally to the Scientific Revolution.",
    "Oscar Wilde": "Remembered as a leading figure of the 19th-century Aestheticism movement and a master of late Victorian theatrical comedy.",
    "Qutuz": "Halted the westward expansion of the Mongol Empire at the Battle of Ain Jalut in 1260, preserving Islamic civilization in Egypt and the Levant."
}

def perform_post_write_audit():
    # 1. Parse JSON afresh from disk
    json_valid = True
    try:
        with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        json_valid = False
        print(f"JSON_VALID: NO ({e})")
        return

    people = data.get("people", {})

    target_count = len(APPROVED_13_HISTORICAL_SIGNIFICANCE)
    present_cnt = 0
    exact_match_cnt = 0
    missing_cnt = 0
    wrong_val_cnt = 0
    unexpected_occurrences_cnt = 0
    non_english_contam_cnt = 0
    semantic_dup_cnt = 0

    person_current_values = {}

    # Check the 13 target people
    for pid, exp_val in APPROVED_13_HISTORICAL_SIGNIFICANCE.items():
        if pid not in people:
            missing_cnt += 1
            continue

        p_obj = people[pid]
        en = p_obj.get("languages", {}).get("en", {})
        curr_hs = str(en.get("historical_significance", "")).strip()

        person_current_values[pid] = curr_hs

        if curr_hs and curr_hs != "INSUFFICIENT_SOURCE":
            present_cnt += 1
        else:
            missing_cnt += 1

        if curr_hs == exp_val:
            exact_match_cnt += 1
        else:
            wrong_val_cnt += 1

        # Check semantic duplicate against bio, achievements, key_facts
        bio_str = str(en.get("bio", "")).lower()
        ach_str = json.dumps(en.get("achievements", [])).lower()
        kf_str = json.dumps(en.get("key_facts", [])).lower()
        hs_lower = curr_hs.lower()

        if len(hs_lower) > 30 and (hs_lower[:40] in bio_str or hs_lower[:40] in ach_str or hs_lower[:40] in kf_str):
            semantic_dup_cnt += 1

    # Check unexpected occurrences across all 289 people
    approved_vals_set = set(APPROVED_13_HISTORICAL_SIGNIFICANCE.values())

    for pid, pobj in people.items():
        langs = pobj.get("languages", {})
        en = langs.get("en", {})
        curr_hs = str(en.get("historical_significance", "")).strip()

        if pid not in APPROVED_13_HISTORICAL_SIGNIFICANCE:
            if curr_hs in approved_vals_set:
                unexpected_occurrences_cnt += 1

        # Check non-English contamination
        for lcode, ldict in langs.items():
            if lcode != "en":
                l_hs = str(ldict.get("historical_significance", "")).strip()
                if l_hs in approved_vals_set:
                    non_english_contam_cnt += 1

    status_pass = (
        json_valid and
        present_cnt == target_count and
        exact_match_cnt == target_count and
        missing_cnt == 0 and
        wrong_val_cnt == 0 and
        unexpected_occurrences_cnt == 0 and
        non_english_contam_cnt == 0 and
        semantic_dup_cnt == 0
    )

    print("==================================================")
    print("FINAL POST-WRITE AUDIT: 13 HISTORICAL SIGNIFICANCE")
    print("==================================================\n")

    print("ACTUAL CURRENT VALUES FROM DISK:\n")
    for pid, val in person_current_values.items():
        print(f"PERSON: {pid}")
        print(f"HISTORICAL_SIGNIFICANCE: \"{val}\"\n")

    print("==================================================")
    print("AUDIT METRICS SUMMARY")
    print("==================================================")
    print(f"TARGET_COUNT = {target_count}")
    print(f"PRESENT_COUNT = {present_cnt}")
    print(f"EXACT_MATCH_COUNT = {exact_match_cnt}")
    print(f"MISSING_COUNT = {missing_cnt}")
    print(f"WRONG_VALUE_COUNT = {wrong_val_cnt}")
    print(f"UNEXPECTED_APPROVED_VALUE_OCCURRENCES = {unexpected_occurrences_cnt}")
    print(f"NON_ENGLISH_CONTAMINATION = {non_english_contam_cnt}")
    print(f"SEMANTIC_DUPLICATES = {semantic_dup_cnt}")
    print(f"JSON_VALID = {'YES' if json_valid else 'NO'}")
    print("FILES_MODIFIED = 0")
    print(f"STATUS = {'PASS' if status_pass else 'FAIL'}")

    report_output = {
        "TARGET_COUNT": target_count,
        "PRESENT_COUNT": present_cnt,
        "EXACT_MATCH_COUNT": exact_match_cnt,
        "MISSING_COUNT": missing_cnt,
        "WRONG_VALUE_COUNT": wrong_val_cnt,
        "UNEXPECTED_APPROVED_VALUE_OCCURRENCES": unexpected_occurrences_cnt,
        "NON_ENGLISH_CONTAMINATION": non_english_contam_cnt,
        "SEMANTIC_DUPLICATES": semantic_dup_cnt,
        "JSON_VALID": "YES" if json_valid else "NO",
        "FILES_MODIFIED": 0,
        "STATUS": "PASS" if status_pass else "FAIL",
        "person_current_values": person_current_values
    }

    with open(POST_WRITE_AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    perform_post_write_audit()
