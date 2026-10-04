#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
JSON_PATH = ASSETS / "person_i18n.json"
JS_PATH = ASSETS / "js" / "person_i18n.js"

REMOVED_LANGS = ["he"]
EXPECTED_LANGS = [
    "ar", "en", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "ko", "zh", "hi", "id", "fa"
]

def perform_cleanup():
    print("Loading current baseline person_i18n.json...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Baseline copy in memory for validation
    baseline_data = json.loads(json.dumps(data))

    # 1. Clean top-level languages list
    data["languages"] = [l for l in data["languages"] if l not in REMOVED_LANGS]

    # 2. Clean each person's languages dict
    for pid, pdata in data["people"].items():
        langs = pdata["languages"]
        for lcode in REMOVED_LANGS:
            if lcode in langs:
                del langs[lcode]

    # Write cleaned JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Write cleaned JS
    js_content = "window.PERSON_I18N = " + json.dumps(data, ensure_ascii=False) + ";"
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Cleaned JSON and JS written successfully.")
    return baseline_data, data

def validate(baseline_data, cleaned_data, json_path=JSON_PATH, js_path=JS_PATH):
    print("\n==================================================")
    print("FINAL 15-LANGUAGE AUDIT")
    print("==================================================")

    # JSON parse
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            json_parsed = json.load(f)
        json_pass = True
    except Exception as e:
        print(f"JSON parse error: {e}")
        json_pass = False

    # JS parse
    js_parsed = None
    try:
        with open(js_path, "r", encoding="utf-8") as f:
            js_text = f.read().strip()
        prefix = "window.PERSON_I18N = "
        if js_text.startswith(prefix) and js_text.endswith(";"):
            js_parsed = json.loads(js_text[len(prefix):-1])
            js_pass = True
        else:
            js_pass = False
    except Exception as e:
        print(f"JS parse error: {e}")
        js_pass = False

    # Semantic equality
    js_equals_json = (json_parsed == js_parsed)

    # People count
    orig_people = baseline_data["people"]
    new_people = json_parsed["people"]
    people_count = len(new_people)

    # Order check
    orig_pids = list(orig_people.keys())
    new_pids = list(new_people.keys())
    people_order_changed = "YES" if orig_pids != new_pids else "NO"

    # Languages check
    final_langs = json_parsed.get("languages", [])
    langs_count = len(final_langs)

    # Count remaining language objects
    total_remaining_lang_objs = 0
    th_count = 0
    vi_count = 0
    el_count = 0
    he_count = 0

    for pid, pdata in new_people.items():
        langs_dict = pdata.get("languages", {})
        total_remaining_lang_objs += len(langs_dict)
        if "th" in langs_dict: th_count += 1
        if "vi" in langs_dict: vi_count += 1
        if "el" in langs_dict: el_count += 1
        if "he" in langs_dict: he_count += 1

    # Unauthorized changes check
    unauthorized_changes = 0
    array_count_changes = 0

    for pid in orig_pids:
        orig_p = orig_people[pid]
        new_p = new_people[pid]

        # Check non-language fields (e.g. id, name, etc.)
        for k in orig_p.keys():
            if k != "languages":
                if orig_p.get(k) != new_p.get(k):
                    unauthorized_changes += 1

        # Check 15 remaining languages
        orig_langs = orig_p["languages"]
        new_langs = new_p["languages"]

        for lcode in EXPECTED_LANGS:
            if orig_langs.get(lcode) != new_langs.get(lcode):
                unauthorized_changes += 1

            # Check array counts
            orig_l_obj = orig_langs.get(lcode, {})
            new_l_obj = new_langs.get(lcode, {})
            for arr_f in ["achievements", "key_facts", "wars"]:
                if len(orig_l_obj.get(arr_f, [])) != len(new_l_obj.get(arr_f, [])):
                    array_count_changes += 1

    schema_changed = "YES" if baseline_data.get("schema") != json_parsed.get("schema") else "NO"
    policy_changed = "YES" if baseline_data.get("policy") != json_parsed.get("policy") else "NO"

    # Print final report strictly formatted
    print(f"People:\n{people_count} / 289\n")
    print(f"Final languages:\n{langs_count} / 15\n")
    print(f"Expected languages:\n{','.join(EXPECTED_LANGS)}\n")
    print(f"Removed:\nth = {th_count}")
    print(f"vi = {vi_count}")
    print(f"el = {el_count}")
    print(f"he = {he_count}\n")
    print(f"Expected remaining language objects:\n4335\n")
    print(f"Actual remaining language objects:\n{total_remaining_lang_objs}\n")
    print(f"Unauthorized changes:\n{unauthorized_changes}\n")
    print(f"Array count changes:\n{array_count_changes}\n")
    print(f"People order changed:\n{people_order_changed}\n")
    print(f"Schema changed:\n{schema_changed}\n")
    print(f"Policy changed:\n{policy_changed}\n")
    print(f"JSON parse:\n{'PASS' if json_pass else 'FAIL'}\n")
    print(f"JS parse:\n{'PASS' if js_pass else 'FAIL'}\n")
    print(f"JSON ↔ JS semantic equality:\n{'TRUE' if js_equals_json else 'FALSE'}\n")

    all_passed = (
        people_count == 289 and
        langs_count == 15 and
        final_langs == EXPECTED_LANGS and
        th_count == 0 and vi_count == 0 and el_count == 0 and he_count == 0 and
        total_remaining_lang_objs == 4335 and
        unauthorized_changes == 0 and
        array_count_changes == 0 and
        people_order_changed == "NO" and
        schema_changed == "NO" and
        policy_changed == "NO" and
        json_pass and js_pass and js_equals_json
    )

    if all_passed:
        print("Final result:")
        print("PASS")
        return True
    else:
        print("Final result:")
        print("FAIL")
        return False

if __name__ == "__main__":
    baseline, cleaned = perform_cleanup()
    validate(baseline, cleaned)
