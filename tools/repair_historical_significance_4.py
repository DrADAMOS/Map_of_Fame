#!/usr/bin/env python3
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
WRITE_REPORT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_WRITE_REPORT.json"
REPAIR_REPORT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_REPAIR_REPORT.json"

TARGET_4_REPAIR = {
    "Gustav Mahler": {
        "new_value": "Exerted a profound and wide-ranging influence on succeeding generations of 20th-century classical composers.",
        "removed_claims": "Removed 'transitional bridge between 19th-century Romanticism and 20th-century modernism' to match the exact source passage focus on composer influence.",
        "source_passage": "Donald Mitchell writes that Mahler's influence on succeeding generations of composers is 'a complete subject in itself'. Mahler's influence on succeeding generations of composers was profound."
    },
    "Marcel Proust": {
        "new_value": "Authored the monumental seven-volume novel In Search of Lost Time, widely considered a masterpiece of 20th-century literature.",
        "removed_claims": "Removed 'pioneering modern psychological exploration of involuntary memory and time' to strictly align with the exact source passage.",
        "source_passage": "In 1908, Proust began work on À la recherche du temps perdu when he was 38... The novel is widely considered a masterpiece of 20th-century fiction."
    },
    "Steve Jobs": {
        "new_value": "Pioneered the personal computer revolution of the 1970s and 1980s as a leading inventor and entrepreneur.",
        "removed_claims": "Removed 'digital typography, animated cinema, digital music distribution, and smartphones' list to match the 1-sentence lead passage.",
        "source_passage": "Steven Paul Jobs was an American businessman, inventor, and investor. A pioneer of the personal computer revolution of the 1970s and 1980s..."
    },
    "T. E. Lawrence": {
        "new_value": "Played a key historical role in the Arab Revolt through his military strategy and liaison with British Armed Forces.",
        "removed_claims": "Removed 'pioneering development of irregular guerrilla warfare' and 'Lawrence of Arabia' epithet to strictly match the strategy/liaison passage.",
        "source_passage": "Lawrence's most important contributions to the Arab Revolt were in the area of strategy and liaison with British Armed Forces, but he also participated personally in several military engagements..."
    }
}

def run_repair():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # In-memory before snapshot
    original_data = json.loads(json.dumps(data))
    people = data["people"]

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE REPAIR PHASE (4 TARGETS)")
    print("==================================================\n")

    fields_changed_cnt = 0
    people_changed_cnt = 0

    repair_details = []

    for pid, rep_info in TARGET_4_REPAIR.items():
        if pid in people:
            old_val = people[pid]["languages"]["en"].get("historical_significance", "")
            new_val = rep_info["new_value"]

            print(f"PERSON: {pid}")
            print(f"OLD VALUE: \"{old_val}\"")
            print(f"SOURCE PASSAGE: \"{rep_info['source_passage']}\"")
            print(f"NEW VALUE: \"{new_val}\"")
            print(f"REMOVED CLAIMS & REASON: {rep_info['removed_claims']}\n")

            people[pid]["languages"]["en"]["historical_significance"] = new_val
            fields_changed_cnt += 1
            people_changed_cnt += 1

            repair_details.append({
                "person": pid,
                "old_value": old_val,
                "new_value": new_val,
                "source_passage": rep_info["source_passage"],
                "removed_claims": rep_info["removed_claims"]
            })

    # Save updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # MANDATORY POST-WRITE VALIDATION
    non_english_changes = 0
    other_field_changes = 0
    bio_changes = 0
    achievement_changes = 0
    key_fact_changes = 0
    unexpected_people_changed = 0

    for pid, pobj in data["people"].items():
        orig_pobj = original_data["people"][pid]

        if pid not in TARGET_4_REPAIR:
            if pobj != orig_pobj:
                unexpected_people_changed += 1
        else:
            # Check non-English locales
            for lcode, ldict in pobj["languages"].items():
                if lcode != "en":
                    if ldict != orig_pobj["languages"][lcode]:
                        non_english_changes += 1

            # Check other English fields
            curr_e = pobj["languages"]["en"]
            orig_e = orig_pobj["languages"]["en"]

            if curr_e.get("bio") != orig_e.get("bio"):
                bio_changes += 1
                other_field_changes += 1
            if curr_e.get("achievements") != orig_e.get("achievements"):
                achievement_changes += 1
                other_field_changes += 1
            if curr_e.get("key_facts") != orig_e.get("key_facts"):
                key_fact_changes += 1
                other_field_changes += 1

    json_valid = True
    try:
        with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception:
        json_valid = False

    status_pass = (
        people_changed_cnt == 4 and
        fields_changed_cnt == 4 and
        unexpected_people_changed == 0 and
        non_english_changes == 0 and
        other_field_changes == 0 and
        bio_changes == 0 and
        achievement_changes == 0 and
        key_fact_changes == 0 and
        json_valid
    )

    report_data = {
        "TARGET_COUNT": 4,
        "FIELDS_CHANGED": fields_changed_cnt,
        "PEOPLE_CHANGED": people_changed_cnt,
        "NON_ENGLISH_CHANGES": non_english_changes,
        "OTHER_FIELD_CHANGES": other_field_changes,
        "BIO_CHANGES": bio_changes,
        "ACHIEVEMENT_CHANGES": achievement_changes,
        "KEY_FACT_CHANGES": key_fact_changes,
        "UNEXPECTED_PERSON_CHANGES": unexpected_people_changed,
        "JSON_VALID": "YES" if json_valid else "NO",
        "STATUS": "HISTORICAL_SIGNIFICANCE_REPAIR_COMPLETE" if status_pass else "HISTORICAL_SIGNIFICANCE_REPAIR_FAIL",
        "details": repair_details
    }

    with open(REPAIR_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("REPAIR SUMMARY TOTALS")
    print("==================================================")
    print(f"TARGET_COUNT: 4")
    print(f"FIELDS_CHANGED: {fields_changed_cnt}")
    print(f"PEOPLE_CHANGED: {people_changed_cnt}")
    print(f"NON_ENGLISH_CHANGES: {non_english_changes}")
    print(f"OTHER_FIELD_CHANGES: {other_field_changes}")
    print(f"BIO_CHANGES: {bio_changes}")
    print(f"ACHIEVEMENT_CHANGES: {achievement_changes}")
    print(f"KEY_FACT_CHANGES: {key_fact_changes}")
    print(f"UNEXPECTED_PERSON_CHANGES: {unexpected_people_changed}")
    print(f"JSON_VALID: {'YES' if json_valid else 'NO'}")
    print(f"STATUS: {'HISTORICAL_SIGNIFICANCE_REPAIR_COMPLETE' if status_pass else 'HISTORICAL_SIGNIFICANCE_REPAIR_FAIL'}")

if __name__ == "__main__":
    run_repair()
