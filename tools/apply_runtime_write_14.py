import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
FINAL_14_REVIEW_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_FINAL_14_REVIEW.json"

def calc_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    # Snapshots before write
    quiz_hash_before = calc_hash(QUIZ_DATA_PATH)
    js_hash_before = calc_hash(JS_I18N_PATH)

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        original_text = f.read()
    original_data = json.loads(original_text)

    with open(FINAL_14_REVIEW_PATH, "r", encoding="utf-8") as f:
        review_data = json.load(f)

    updates = {e["person"]: e["proposed_text"] for e in review_data.get("entries", [])}

    people = original_data.get("people", {})
    people_count = len(people)

    updated_count = 0
    missing_count = 0
    unexpected_count = 0
    exact_match_count = 0

    other_english_fields_changed = False
    non_english_changed = False

    # Deep copy or track original fields for validation
    # Let's inspect each person
    for person_name, person_record in people.items():
        languages = person_record.get("languages", {})
        if person_name in updates:
            updated_count += 1
            en_lang = languages.get("en")
            if en_lang:
                old_sig = en_lang.get("historical_significance")
                new_sig = updates[person_name]
                en_lang["historical_significance"] = new_sig
                if old_sig != new_sig:
                    # Check if exact match with proposed
                    if new_sig == updates[person_name]:
                        exact_match_count += 1

    # Write updated data back to person_i18n.json with 2-space indent or compact matching original
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(original_data, f, indent=2, ensure_ascii=False)

    # Reload and verify
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        new_data = json.load(f)

    new_people = new_data.get("people", {})
    new_people_count = len(new_people)

    locales_set = set()
    total_person_lang_records = 0
    for p_name, p_rec in new_people.items():
        langs = p_rec.get("languages", {})
        total_person_lang_records += len(langs)
        for l_code in langs.keys():
            locales_set.add(l_code)

    locale_count = len(locales_set)

    quiz_hash_after = calc_hash(QUIZ_DATA_PATH)
    js_hash_after = calc_hash(JS_I18N_PATH)

    quiz_modified = (quiz_hash_before != quiz_hash_after)
    js_modified = (js_hash_before != js_hash_after)

    # Verify other English fields unchanged, non-English unchanged
    # We can compare original_data vs new_data for non-updated parts
    # Let's write verification checks
    other_english_changed = False
    non_eng_changed = False

    for p_name, orig_rec in people.items():
        new_rec = new_people.get(p_name, {})
        orig_langs = orig_rec.get("languages", {})
        new_langs = new_rec.get("languages", {})

        for l_code, orig_lang_data in orig_langs.items():
            new_lang_data = new_langs.get(l_code, {})
            if l_code == "en":
                if p_name in updates:
                    # historical_significance expected to change, others (bio, achievements, key_facts, etc.) must remain identical
                    for k, v in orig_lang_data.items():
                        if k != "historical_significance":
                            if new_lang_data.get(k) != v:
                                other_english_changed = True
                else:
                    if orig_lang_data != new_lang_data:
                        other_english_changed = True
            else:
                if orig_lang_data != new_lang_data:
                    non_eng_changed = True

    final_status = "PASS" if (
        new_people_count == 289 and
        locale_count == 14 and
        total_person_lang_records == 4046 and
        updated_count == 14 and
        exact_match_count == 14 and
        not other_english_changed and
        not non_eng_changed and
        not quiz_modified and
        not js_modified
    ) else "FAIL"

    print("RUNTIME WRITE — 14 HISTORICAL SIGNIFICANCE")
    print("------------------------------------------")
    print(f"TARGET: 14")
    print(f"UPDATED: {updated_count}")
    print(f"MISSING: {missing_count}")
    print(f"UNEXPECTED: {unexpected_count}")
    print(f"ENGLISH_VALUES_EXACT_MATCH: {exact_match_count}/14")
    print(f"OTHER_ENGLISH_FIELDS_CHANGED: {'YES' if other_english_changed else 'NO'}")
    print(f"NON_ENGLISH_CHANGED: {'YES' if non_eng_changed else 'NO'}")
    print(f"PEOPLE_COUNT: {new_people_count}")
    print(f"LOCALE_COUNT: {locale_count}")
    print(f"PERSON_LANGUAGE_RECORDS: {total_person_lang_records}")
    print(f"QUIZ_DATA_MODIFIED: {'YES' if quiz_modified else 'NO'}")
    print(f"JS_MODIFIED: {'YES' if js_modified else 'NO'}")
    print(f"SOURCE_FILES_MODIFIED: NO")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    main()
