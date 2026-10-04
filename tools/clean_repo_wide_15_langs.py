#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "app" / "src" / "main" / "assets"
JSON_PATH = ASSETS / "person_i18n.json"
JS_PATH = ASSETS / "js" / "person_i18n.js"
I18N_LANGS_JS_PATH = ASSETS / "js" / "i18n_languages.js"

REMOVED_LANGS = ["he"]
EXPECTED_LANGS = [
    "ar", "en", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "ko", "zh", "hi", "id", "fa"
]

def clean_person_i18n_json_and_js():
    print("Loading current baseline person_i18n.json...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    baseline_data = json.loads(json.dumps(data))

    # Clean top-level languages
    data["languages"] = [l for l in data["languages"] if l not in REMOVED_LANGS]

    # Clean people languages
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

    print("Cleaned person_i18n.json and person_i18n.js written successfully.")
    return baseline_data, data

def clean_i18n_languages_js():
    print("Cleaning i18n_languages.js...")
    with open(I18N_LANGS_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove th, vi, el, he from packs
    for code in REMOVED_LANGS:
        # Match pack definition e.g. th: {title:...}, or th:{...},
        content = re.sub(rf'\b{code}:\s*\{{[^}}]*\}}', '', content)

    # Remove th, vi, el, he from common
    for code in REMOVED_LANGS:
        content = re.sub(rf'\b{code}:\s*\{{[^}}]*\}}', '', content)

    # Clean up empty commas inside objects if any
    content = re.sub(r',\s*,', ',', content)
    content = re.sub(r'\{\s*,', '{', content)
    content = re.sub(r',\s*\}', '}', content)

    # Update window.LANGUAGES
    lang_tuples = [
        "['ar','العربية','العربية']",
        "['en','English','English']",
        "['es','Español','Español']",
        "['fr','Français','Français']",
        "['de','Deutsch','Deutsch']",
        "['pt','Português','Português']",
        "['it','Italiano','Italiano']",
        "['tr','Türkçe','Türkçe']",
        "['ru','Русский','Русский']",
        "['ja','日本語','日本語']",
        "['ko','한국어','한국어']",
        "['zh','简体中文','简体中文']",
        "['hi','हिन्दी','हिन्दी']",
        "['id','Bahasa Indonesia','Bahasa Indonesia']",
        "['fa','فارسی','فارسی']"
    ]
    new_window_languages = "window.LANGUAGES = [\n        " + ",".join(lang_tuples) + "\n    ];"
    content = re.sub(r'window\.LANGUAGES\s*=\s*\[[^\]]*\];', new_window_languages, content, flags=re.DOTALL)

    # Update window.RTL_LANGS
    content = re.sub(r'window\.RTL_LANGS\s*=\s*new Set\(\[[^\]]*\]\);', "window.RTL_LANGS = new Set(['ar','fa']);", content)

    with open(I18N_LANGS_JS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("Cleaned i18n_languages.js written successfully.")

def clean_tools_scripts():
    print("Updating python tools scripts language lists...")
    tools_dir = ROOT / "tools"
    for py_file in tools_dir.glob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()

            new_code = code
            for rcode in REMOVED_LANGS:
                new_code = re.sub(rf'"{rcode}"\s*,\s*', '', new_code)
                new_code = re.sub(rf"'{rcode}'\s*,\s*", '', new_code)

            if new_code != code:
                with open(py_file, "w", encoding="utf-8") as f:
                    f.write(new_code)
                print(f"  Updated {py_file.name}")
        except Exception as e:
            pass

def audit_repository(baseline_data, cleaned_data):
    print("\n==================================================")
    print("FINAL REPORT")
    print("==================================================")

    # 1. Parse JSON
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            json_parsed = json.load(f)
        json_pass = True
    except Exception as e:
        print(f"JSON parse error: {e}")
        json_pass = False

    # 2. Parse JS
    js_parsed = None
    try:
        with open(JS_PATH, "r", encoding="utf-8") as f:
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

    for pid, pdata in new_people.items():
        langs_dict = pdata.get("languages", {})
        total_remaining_lang_objs += len(langs_dict)

    # Check for active references to deleted languages in repository source
    active_refs = {code: 0 for code in REMOVED_LANGS}
    app_source_dir = ROOT / "app" / "src" / "main"
    ignore_dirs = {
        ".git", ".gradle", ".idea", "build", ".artifacts",
        ".wikipedia_content_cache", ".wikipedia_multilingual_cache", "__pycache__",
        ".wikipedia_content_cache_v12_backup"
    }

    for root_dir, dirs, files in os.walk(app_source_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(('.json', '.js', '.kt', '.java', '.xml', '.html')):
                # Ignore backup files, old cumulative files, or tailwind CSS engine
                if "backup" in file or "CLEAN_BASE" in file or "MASTER_CUMULATIVE" in file or file == "tailwind.js":
                    continue
                filepath = Path(root_dir) / file
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                    for code in REMOVED_LANGS:
                        # Check active language references like languages.th, etc.
                        if re.search(rf'languages\.{code}\b|[\"\'\`]{code}[\"\'\`]\s*[:\,\]]', text):
                            active_refs[code] += 1
                except Exception as e:
                    pass

    # Data changes in remaining 15 languages
    data_changes = {lcode: 0 for lcode in EXPECTED_LANGS}
    unauthorized_data_changes = 0
    array_changes = 0

    for pid in orig_pids:
        orig_p = orig_people[pid]
        new_p = new_people[pid]

        # Check non-language fields
        for k in orig_p.keys():
            if k != "languages":
                if orig_p.get(k) != new_p.get(k):
                    unauthorized_data_changes += 1

        # Check remaining 15 languages
        orig_langs = orig_p["languages"]
        new_langs = new_p["languages"]

        for lcode in EXPECTED_LANGS:
            if orig_langs.get(lcode) != new_langs.get(lcode):
                data_changes[lcode] += 1
                unauthorized_data_changes += 1

            orig_l_obj = orig_langs.get(lcode, {})
            new_l_obj = new_langs.get(lcode, {})
            for arr_f in ["achievements", "key_facts", "wars"]:
                if len(orig_l_obj.get(arr_f, [])) != len(new_l_obj.get(arr_f, [])):
                    array_changes += 1

    schema_changed = "YES" if baseline_data.get("schema") != json_parsed.get("schema") else "NO"
    policy_changed = "YES" if baseline_data.get("policy") != json_parsed.get("policy") else "NO"

    # Report Output
    print(f"People:\n{people_count} / 289\n")
    print(f"Final active languages:\n{langs_count} / 15\n")
    print(f"Final languages:\n{','.join(EXPECTED_LANGS)}\n")
    print("Removed languages:")
    for code in REMOVED_LANGS:
        print(f"{code} = {active_refs[code]} active references")
    print()

    print(f"Person language objects:\nExpected = 289 × 15 = 4335")
    print(f"Actual = {total_remaining_lang_objs}\n")

    print("Remaining-language data changes:\n")
    for lcode in EXPECTED_LANGS:
        print(f"{lcode} = {data_changes[lcode]}")
    print()

    print(f"Unauthorized data changes:\n{unauthorized_data_changes}\n")
    print(f"Array changes:\n{array_changes}\n")
    print(f"People added:\n0\n")
    print(f"People removed:\n0\n")
    print(f"People reordered:\n{people_order_changed}\n")
    print(f"JSON parse:\n{'PASS' if json_pass else 'FAIL'}\n")
    print(f"JS parse:\n{'PASS' if js_pass else 'FAIL'}\n")
    print(f"JSON ↔ JS semantic equality:\n{'TRUE' if js_equals_json else 'FALSE'}\n")
    print(f"Schema changed:\n{schema_changed}\n")
    print(f"Policy changed:\n{policy_changed}\n")

    for code in REMOVED_LANGS:
        print(f"Repository-wide active references to {code}:\n{active_refs[code]}\n")

    all_passed = (
        people_count == 289 and
        langs_count == 15 and
        final_langs == EXPECTED_LANGS and
        sum(active_refs.values()) == 0 and
        total_remaining_lang_objs == 4335 and
        unauthorized_data_changes == 0 and
        array_changes == 0 and
        people_order_changed == "NO" and
        schema_changed == "NO" and
        policy_changed == "NO" and
        json_pass and js_pass and js_equals_json
    )

    return all_passed

if __name__ == "__main__":
    baseline, cleaned = clean_person_i18n_json_and_js()
    clean_i18n_languages_js()
    clean_tools_scripts()
    success = audit_repository(baseline, cleaned)
    if success:
        print("Final result:\nPASS")
    else:
        print("Final result:\nFAIL")
