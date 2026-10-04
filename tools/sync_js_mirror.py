#!/usr/bin/env python3
"""
JS MIRROR SYNCHRONIZATION SCRIPT
Synchronizes app/src/main/assets/js/person_i18n.js directly from person_i18n.json.
Modifies ONLY app/src/main/assets/js/person_i18n.js.
Saves ONLY tools/JS_MIRROR_SYNCHRONIZATION_REPORT.json.
"""

import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
OUTPUT_REPORT_PATH = ROOT / "tools" / "JS_MIRROR_SYNCHRONIZATION_REPORT.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def recursive_deep_diff(obj1, obj2, path=""):
    diffs = []
    if type(obj1) != type(obj2):
        diffs.append({
            "path": path or "root",
            "type": "TYPE_MISMATCH",
            "val1_type": str(type(obj1).__name__),
            "val2_type": str(type(obj2).__name__)
        })
        return diffs

    if isinstance(obj1, dict):
        keys1 = set(obj1.keys())
        keys2 = set(obj2.keys())

        for k in sorted(list(keys1 - keys2)):
            diffs.append({"path": f"{path}.{k}" if path else k, "type": "MISSING_IN_TARGET", "value": str(obj1[k])[:80]})
        for k in sorted(list(keys2 - keys1)):
            diffs.append({"path": f"{path}.{k}" if path else k, "type": "EXTRA_IN_TARGET", "value": str(obj2[k])[:80]})

        for k in sorted(list(keys1.intersection(keys2))):
            sub_path = f"{path}.{k}" if path else k
            diffs.extend(recursive_deep_diff(obj1[k], obj2[k], sub_path))

    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            diffs.append({
                "path": path,
                "type": "ARRAY_LENGTH_MISMATCH",
                "len1": len(obj1),
                "len2": len(obj2)
            })
        for i in range(min(len(obj1), len(obj2))):
            sub_path = f"{path}[{i}]"
            diffs.extend(recursive_deep_diff(obj1[i], obj2[i], sub_path))

    else:
        if obj1 != obj2:
            diffs.append({
                "path": path,
                "type": "VALUE_MISMATCH",
                "val1": str(obj1)[:80],
                "val2": str(obj2)[:80]
            })

    return diffs

def parse_js_mirror_object(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        js_text = f.read().strip()

    js_clean = re.sub(r"^window\.PERSON_I18N\s*=\s*", "", js_text, flags=re.IGNORECASE).rstrip(";").strip()
    return json.loads(js_clean)

def perform_single_verification():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    js_data = parse_js_mirror_object(JS_I18N_PATH)

    diffs = recursive_deep_diff(json_data, js_data)
    return diffs, len(json_data.get("people", {})), len(js_data.get("people", {}))

def run_synchronization_and_verification():
    # Hash check before
    before_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # 1. Load JSON and parse existing JS mirror to calculate BEFORE mismatches
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    before_js_data = parse_js_mirror_object(JS_I18N_PATH)
    before_diffs = recursive_deep_diff(json_data, before_js_data)
    before_mismatches_cnt = len(before_diffs)

    # 2. Synchronize person_i18n.js from person_i18n.json
    js_serialized_content = "window.PERSON_I18N = " + json.dumps(json_data, ensure_ascii=False, indent=2) + ";\n"

    with open(JS_I18N_PATH, "w", encoding="utf-8") as f:
        f.write(js_serialized_content)

    # Hash check after
    after_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    json_modified = (before_hashes[str(PERSON_I18N_PATH)] != after_hashes[str(PERSON_I18N_PATH)])
    quiz_modified = (before_hashes[str(QUIZ_DATA_PATH)] != after_hashes[str(QUIZ_DATA_PATH)])
    js_modified = (before_hashes[str(JS_I18N_PATH)] != after_hashes[str(JS_I18N_PATH)])

    # 3. Perform Verification Run #1
    run1_diffs, json_people_cnt, js_people_cnt = perform_single_verification()

    # 4. Perform Verification Run #2
    run2_diffs, _, _ = perform_single_verification()

    # Check Run 1 vs Run 2 identical
    run1_str = json.dumps(run1_diffs, sort_keys=True)
    run2_str = json.dumps(run2_diffs, sort_keys=True)
    run_1_run_2_identical = (run1_str == run2_str)

    after_mismatches_cnt = len(run1_diffs)
    deep_compare_pass = (after_mismatches_cnt == 0)

    # Final Status Determination
    status_pass = (
        after_mismatches_cnt == 0 and
        deep_compare_pass and
        run_1_run_2_identical and
        not json_modified and
        not quiz_modified and
        js_modified
    )

    final_status = "PASS" if status_pass else "FAIL"

    report_output = {
        "audit_type": "JS_MIRROR_SYNCHRONIZATION_REPORT",
        "read_only": False,
        "files_modified": 1 if js_modified else 0,
        "source_json": str(PERSON_I18N_PATH),
        "target_js": str(JS_I18N_PATH),
        "hashes": {
            "before": before_hashes,
            "after": after_hashes
        },
        "before_mismatches_count": before_mismatches_cnt,
        "after_mismatches_count": after_mismatches_cnt,
        "json_people_count": json_people_cnt,
        "js_people_count": js_people_cnt,
        "deep_compare_status": "PASS" if deep_compare_pass else "FAIL",
        "run_1_run_2_identical": "PASS" if run_1_run_2_identical else "FAIL",
        "json_modified": json_modified,
        "quiz_data_modified": quiz_modified,
        "js_modified": js_modified,
        "final_status": final_status,
        "after_mismatches": run1_diffs
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("JS MIRROR SYNCHRONIZATION")
    print(f"SOURCE_JSON: {PERSON_I18N_PATH}")
    print(f"TARGET_JS: {JS_I18N_PATH}")
    print(f"BEFORE_MISMATCHES: {before_mismatches_cnt}")
    print(f"AFTER_MISMATCHES: {after_mismatches_cnt}")
    print(f"JSON_PEOPLE: {json_people_cnt}")
    print(f"JS_PEOPLE: {js_people_cnt}")
    print(f"DEEP_COMPARE: {'PASS' if deep_compare_pass else 'FAIL'}")
    print(f"RUN_1_RUN_2_IDENTICAL: {'PASS' if run_1_run_2_identical else 'FAIL'}")
    print(f"JSON_MODIFIED: {'YES' if json_modified else 'NO'}")
    print(f"QUIZ_DATA_MODIFIED: {'YES' if quiz_modified else 'NO'}")
    print(f"JS_MODIFIED: {'YES' if js_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_synchronization_and_verification()
