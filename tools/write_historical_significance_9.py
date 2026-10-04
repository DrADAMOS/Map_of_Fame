#!/usr/bin/env python3
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
SOURCE_PKG_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json"
WRITE_REPORT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_WRITE_REPORT.json"

APPROVED_9_SIGNIFICANCE = {
    "Auguste Comte": "Formulated the philosophical doctrine of positivism and established sociology as a systematic science, seeking to create a scientific framework for social order following the French Revolution.",
    "Caravaggio": "Revolutionized Western European painting through intense realism and a dramatic, high-contrast use of chiaroscuro and tenebrism, profoundly shaping the emergence of Baroque art.",
    "Emperor Meiji": "Served as the imperial symbol of the Meiji Restoration, presiding over Japan's rapid historic transformation from an isolated feudal shogunate into a modern, industrialized world power.",
    "Gustav Mahler": "Acted as a crucial transitional bridge between 19th-century Austro-German Romanticism and 20th-century modernism, exerting a profound influence on succeeding generations of classical composers.",
    "Malek Bennabi": "Developed an influential civilizational philosophy analyzing the decline and renewal of Muslim societies, introducing the key concept of 'colonisability' in post-colonial studies.",
    "Marcel Proust": "Transformed 20th-century literature through his monumental seven-volume masterwork In Search of Lost Time, pioneering modern psychological exploration of involuntary memory and time.",
    "Michael Faraday": "Discovered electromagnetic induction, laws of electrolysis, and diamagnetism, laying the physical foundations for electromagnetic field theory and modern electrical power technology.",
    "Steve Jobs": "Pioneered the personal computer revolution and transformed multiple global industries, including digital typography, animated cinema, digital music distribution, and smartphones.",
    "T. E. Lawrence": "Achieved enduring international renown as 'Lawrence of Arabia' for his strategic military leadership, liaison role in the Arab Revolt, and pioneering development of irregular guerrilla warfare."
}

# The 13 rejected candidate names / facts that must NOT be written
REJECTED_PEOPLE_OR_CANDIDATES = [
    "Alexis Carrel", "Anwar Sadat", "Clara Barton", "Dmitri Mendeleev",
    "Hadrian", "James Prescott Joule", "Jane Austen", "Joseph Haydn",
    "Louis IX", "Muhammad Abduh", "Nicolaus Copernicus", "Oscar Wilde", "Qutuz"
]

def perform_write_and_verify():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(SOURCE_PKG_PATH, "r", encoding="utf-8") as f:
        src_pkg = json.load(f)

    # In-memory before snapshot of all 289 people
    original_data = json.loads(json.dumps(data))
    people = data["people"]

    write_report_entries = []
    fields_changed_cnt = 0
    people_changed_cnt = 0

    for pid, new_hs in APPROVED_9_SIGNIFICANCE.items():
        if pid in people:
            old_hs = people[pid]["languages"]["en"].get("historical_significance", "")
            people[pid]["languages"]["en"]["historical_significance"] = new_hs

            src_item = src_pkg.get(pid, [{}])[0]

            write_report_entries.append({
                "person": pid,
                "old_historical_significance": old_hs,
                "new_historical_significance": new_hs,
                "source_title": src_item.get("source_title", pid),
                "source_url": src_item.get("source_url", ""),
                "source_passage": src_item.get("source_passage", ""),
                "fields_changed": ["historical_significance"],
                "languages_changed": ["en"]
            })

            fields_changed_cnt += 1
            people_changed_cnt += 1

    # Save updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Save write report
    report_data = {
        "TARGET_COUNT": 9,
        "EXPECTED_FIELD": "historical_significance",
        "EXPECTED_LANGUAGE": "en",
        "entries": write_report_entries
    }
    with open(WRITE_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    # MANDATORY POST-WRITE VALIDATION
    non_english_changes = 0
    other_field_changes = 0
    bio_changes = 0
    achievement_changes = 0
    key_fact_changes = 0
    unexpected_people_changed = 0
    rejected_written = 0

    for pid, pobj in data["people"].items():
        orig_pobj = original_data["people"][pid]

        if pid not in APPROVED_9_SIGNIFICANCE:
            if pobj != orig_pobj:
                unexpected_people_changed += 1
            # Check if any rejected candidate received an update
            if pid in REJECTED_PEOPLE_OR_CANDIDATES:
                if pobj["languages"]["en"].get("historical_significance") != orig_pobj["languages"]["en"].get("historical_significance"):
                    rejected_written += 1
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
        people_changed_cnt == 9 and
        fields_changed_cnt == 9 and
        unexpected_people_changed == 0 and
        non_english_changes == 0 and
        other_field_changes == 0 and
        bio_changes == 0 and
        achievement_changes == 0 and
        key_fact_changes == 0 and
        rejected_written == 0 and
        json_valid
    )

    print(f"TARGET_COUNT: 9")
    print(f"FIELDS_CHANGED: {fields_changed_cnt}")
    print(f"PEOPLE_CHANGED: {people_changed_cnt}")
    print(f"NON_ENGLISH_CHANGES: {non_english_changes}")
    print(f"OTHER_FIELD_CHANGES: {other_field_changes}")
    print(f"BIO_CHANGES: {bio_changes}")
    print(f"ACHIEVEMENT_CHANGES: {achievement_changes}")
    print(f"KEY_FACT_CHANGES: {key_fact_changes}")
    print(f"JSON_VALID: {'YES' if json_valid else 'NO'}")
    print(f"REJECTED_CANDIDATES_WRITTEN: {rejected_written}")
    print(f"STATUS: {'HISTORICAL_SIGNIFICANCE_WRITE_COMPLETE' if status_pass else 'HISTORICAL_SIGNIFICANCE_WRITE_FAIL'}")

if __name__ == "__main__":
    perform_write_and_verify()
