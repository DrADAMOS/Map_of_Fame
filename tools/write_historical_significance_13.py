#!/usr/bin/env python3
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
WRITE_REPORT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_WRITE_REPORT_13.json"

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

def perform_write_13():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # In-memory before snapshot
    original_data = json.loads(json.dumps(data))
    people = data["people"]

    write_entries = []
    fields_changed_cnt = 0
    people_changed_cnt = 0

    for pid, new_hs in APPROVED_13_HISTORICAL_SIGNIFICANCE.items():
        if pid in people:
            old_hs = people[pid]["languages"]["en"].get("historical_significance", "")
            people[pid]["languages"]["en"]["historical_significance"] = new_hs

            write_entries.append({
                "person": pid,
                "old_historical_significance": old_hs,
                "new_historical_significance": new_hs
            })

            fields_changed_cnt += 1
            people_changed_cnt += 1

    # Save updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # POST-WRITE VALIDATION
    non_english_changes = 0
    bio_changes = 0
    achievement_changes = 0
    key_fact_changes = 0
    unexpected_people_changed = 0
    approved_matches = True

    for pid, pobj in data["people"].items():
        orig_pobj = original_data["people"][pid]

        if pid not in APPROVED_13_HISTORICAL_SIGNIFICANCE:
            if pobj != orig_pobj:
                unexpected_people_changed += 1
        else:
            # Verify exact match
            curr_val = pobj["languages"]["en"].get("historical_significance")
            if curr_val != APPROVED_13_HISTORICAL_SIGNIFICANCE[pid]:
                approved_matches = False

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
            if curr_e.get("achievements") != orig_e.get("achievements"):
                achievement_changes += 1
            if curr_e.get("key_facts") != orig_e.get("key_facts"):
                key_fact_changes += 1

    json_valid = True
    try:
        with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception:
        json_valid = False

    status_pass = (
        people_changed_cnt == 13 and
        fields_changed_cnt == 13 and
        unexpected_people_changed == 0 and
        non_english_changes == 0 and
        bio_changes == 0 and
        achievement_changes == 0 and
        key_fact_changes == 0 and
        approved_matches and
        json_valid
    )

    report_data = {
        "TARGET_COUNT": 13,
        "FIELDS_CHANGED": fields_changed_cnt,
        "PEOPLE_CHANGED": people_changed_cnt,
        "NON_ENGLISH_CHANGES": non_english_changes,
        "BIO_CHANGES": bio_changes,
        "ACHIEVEMENT_CHANGES": achievement_changes,
        "KEY_FACT_CHANGES": key_fact_changes,
        "UNEXPECTED_PERSON_CHANGES": unexpected_people_changed,
        "JSON_VALID": "YES" if json_valid else "NO",
        "APPROVED_VALUES_MATCH": "YES" if approved_matches else "NO",
        "STATUS": "WRITE_COMPLETE" if status_pass else "WRITE_FAIL",
        "entries": write_entries
    }

    with open(WRITE_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"TARGET_COUNT: 13")
    print(f"FIELDS_CHANGED: {fields_changed_cnt}")
    print(f"PEOPLE_CHANGED: {people_changed_cnt}")
    print(f"NON_ENGLISH_CHANGES: {non_english_changes}")
    print(f"BIO_CHANGES: {bio_changes}")
    print(f"ACHIEVEMENT_CHANGES: {achievement_changes}")
    print(f"KEY_FACT_CHANGES: {key_fact_changes}")
    print(f"UNEXPECTED_PERSON_CHANGES: {unexpected_people_changed}")
    print(f"JSON_VALID: {'YES' if json_valid else 'NO'}")
    print(f"APPROVED_VALUES_MATCH: {'YES' if approved_matches else 'NO'}")
    print(f"STATUS: {'WRITE_COMPLETE' if status_pass else 'WRITE_FAIL'}")

if __name__ == "__main__":
    perform_write_13()
