#!/usr/bin/env python3
"""
READ-ONLY JS MIRROR FORENSIC INVESTIGATION SCRIPT
Reads person_i18n.json and person_i18n.js afresh from disk.
Saves ONLY tools/JS_MIRROR_FORENSIC_REPORT.json.
Modifies NO application/runtime data files.
"""

import json
import re
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
OUTPUT_REPORT_PATH = ROOT / "tools" / "JS_MIRROR_FORENSIC_REPORT.json"

PROTECTED_FILES = [PERSON_I18N_PATH, JS_I18N_PATH]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def deep_compare_recursive(obj1, obj2, path=""):
    mismatches = []
    if type(obj1) != type(obj2):
        mismatches.append({
            "path": path or "root",
            "classification": "TYPE_MISMATCH",
            "json_type": str(type(obj1).__name__),
            "js_type": str(type(obj2).__name__)
        })
        return mismatches

    if isinstance(obj1, dict):
        keys1 = set(obj1.keys())
        keys2 = set(obj2.keys())

        for k in sorted(list(keys1 - keys2)):
            sub_path = f"{path}.{k}" if path else k
            mismatches.append({
                "path": sub_path,
                "classification": "MISSING_IN_JS",
                "json_value": str(obj1[k])[:100],
                "js_value": None
            })
        for k in sorted(list(keys2 - keys1)):
            sub_path = f"{path}.{k}" if path else k
            mismatches.append({
                "path": sub_path,
                "classification": "EXTRA_IN_JS",
                "json_value": None,
                "js_value": str(obj2[k])[:100]
            })

        for k in sorted(list(keys1.intersection(keys2))):
            sub_path = f"{path}.{k}" if path else k
            mismatches.extend(deep_compare_recursive(obj1[k], obj2[k], sub_path))

    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            mismatches.append({
                "path": path,
                "classification": "STRUCTURAL_MISMATCH",
                "json_length": len(obj1),
                "js_length": len(obj2),
                "json_value": str(obj1)[:100],
                "js_value": str(obj2)[:100]
            })
        for i in range(min(len(obj1), len(obj2))):
            sub_path = f"{path}[{i}]"
            mismatches.extend(deep_compare_recursive(obj1[i], obj2[i], sub_path))

    else:
        if obj1 != obj2:
            # Extract person, language, field/path from structural path
            path_parts = path.split(".")
            person = path_parts[0] if len(path_parts) > 0 else "UNKNOWN"
            language = path_parts[2] if len(path_parts) > 2 else "UNKNOWN"
            field = ".".join(path_parts[3:]) if len(path_parts) > 3 else path

            mismatches.append({
                "person": person,
                "language": language,
                "field_path": field,
                "path": path,
                "classification": "VALUE_MISMATCH",
                "json_value": str(obj1),
                "js_value": str(obj2)
            })

    return mismatches

def run_forensic_investigation():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # 1. Load person_i18n.json
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_people = json_data.get("people", {})

    # 2. Load person_i18n.js
    with open(JS_I18N_PATH, "r", encoding="utf-8") as f:
        js_text = f.read().strip()

    # Method 1: Extraction & Parsing of JS Object
    js_clean = re.sub(r"^window\.PERSON_I18N\s*=\s*", "", js_text, flags=re.IGNORECASE).rstrip(";").strip()
    js_data = json.loads(js_clean)
    js_people = js_data.get("people", {})

    # Method 2: Canonicalized JSON String Comparison
    canonical_json_str = json.dumps(json_people, sort_keys=True, ensure_ascii=False)
    canonical_js_str = json.dumps(js_people, sort_keys=True, ensure_ascii=False)
    canonical_match = (canonical_json_str == canonical_js_str)

    # Perform Method 1 Deep Comparison
    all_mismatches = deep_compare_recursive(json_people, js_people)

    # Classify Mismatches
    class_counts = {
        "MISSING_IN_JS": 0,
        "EXTRA_IN_JS": 0,
        "VALUE_MISMATCH": 0,
        "TYPE_MISMATCH": 0,
        "KEY_MISMATCH": 0,
        "STRUCTURAL_MISMATCH": 0,
        "PARSER_WRAPPER_ISSUE": 0
    }

    mismatch_records = []

    for m in all_mismatches:
        c_cls = m["classification"]
        if c_cls in class_counts:
            class_counts[c_cls] += 1
        else:
            class_counts["STRUCTURAL_MISMATCH"] += 1
        mismatch_records.append(m)

    total_mismatches = len(all_mismatches)

    # Determine Final Classification
    if total_mismatches > 0 and class_counts["VALUE_MISMATCH"] > 0:
        final_classification = "A_GENUINE_STALE_OR_INCORRECT_JS_MIRROR_DATA"
    elif not canonical_match and total_mismatches == 0:
        final_classification = "B_EXPECTED_REPRESENTATION_WRAPPER_DIFFERENCE"
    elif class_counts["PARSER_WRAPPER_ISSUE"] > 0:
        final_classification = "C_COMPARISON_PARSING_BUG_IN_AUDIT"
    else:
        final_classification = "A_GENUINE_STALE_OR_INCORRECT_JS_MIRROR_DATA"

    # Shutdown File Hash Protection Check
    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    report_output = {
        "audit_type": "JS_MIRROR_FORENSIC_INVESTIGATION",
        "read_only": True,
        "files_modified": 0,
        "source_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "canonical_json_match": canonical_match,
        "total_json_people": len(json_people),
        "total_js_people": len(js_people),
        "total_mismatches": total_mismatches,
        "classification_counts": class_counts,
        "final_classification": final_classification,
        "mismatch_records": mismatch_records,
        "application_data_modified": app_data_modified
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL OUTPUT
    print("JS MIRROR FORENSIC INVESTIGATION")
    print(f"JSON people: {len(json_people)}")
    print(f"JS people: {len(js_people)}")
    print(f"Total mismatches: {total_mismatches}")
    print(f"MISSING_IN_JS: {class_counts['MISSING_IN_JS']}")
    print(f"EXTRA_IN_JS: {class_counts['EXTRA_IN_JS']}")
    print(f"VALUE_MISMATCH: {class_counts['VALUE_MISMATCH']}")
    print(f"TYPE_MISMATCH: {class_counts['TYPE_MISMATCH']}")
    print(f"KEY_MISMATCH: {class_counts['KEY_MISMATCH']}")
    print(f"STRUCTURAL_MISMATCH: {class_counts['STRUCTURAL_MISMATCH']}")
    print(f"PARSER_WRAPPER_ISSUE: {class_counts['PARSER_WRAPPER_ISSUE']}")
    print(f"FINAL_CLASSIFICATION: {final_classification}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")

if __name__ == "__main__":
    run_forensic_investigation()
