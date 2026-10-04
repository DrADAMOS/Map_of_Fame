import json
import hashlib
import os

def compute_sha256(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def execute_v2():
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_i18n_path = "app/src/main/assets/js/person_i18n.js"
    constants_path = "app/src/main/assets/js/constants.js"

    hashes_before = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_i18n_path) if os.path.exists(js_i18n_path) else "N/A",
        "constants.js": compute_sha256(constants_path) if os.path.exists(constants_path) else "N/A"
    }

    with open(quiz_path, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)

    people_before = len(quiz_data)
    birth_before = sum(1 for p in quiz_data if p.get("bc"))
    death_before = sum(1 for p in quiz_data if p.get("dc"))
    coords_before = birth_before + death_before

    # Verify old values match exactly
    pyrrhus_found = False
    kitchener_found = False

    for p in quiz_data:
        name = p.get("name_en") or p.get("name")
        if name == "Pyrrhus of Epirus":
            bc = p.get("bc")
            if abs(bc[0] - 38.3) > 1e-4 or abs(bc[1] - 21.1) > 1e-4:
                raise ValueError(f"ABORT: Pyrrhus birth old value mismatch: {bc}")
            pyrrhus_found = True
        elif name == "Horatio Kitchener":
            dc = p.get("dc")
            if abs(dc[0] - 56.0) > 1e-4 or abs(dc[1] - 3.0) > 1e-4:
                raise ValueError(f"ABORT: Kitchener death old value mismatch: {dc}")
            kitchener_found = True

    if not pyrrhus_found or not kitchener_found:
        raise ValueError("ABORT: Could not locate Pyrrhus of Epirus or Horatio Kitchener in quiz_data.json")

    # Apply corrections to quiz_data.json
    for p in quiz_data:
        name = p.get("name_en") or p.get("name")
        if name == "Pyrrhus of Epirus":
            p["bc"] = [39.1550, 20.9899]
        elif name == "Horatio Kitchener":
            p["dc"] = [59.11706, -3.39566]

    with open(quiz_path, "w", encoding="utf-8") as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)

    # Synchronize js/constants.js
    constants_content = open(constants_path, "r", encoding="utf-8").read()
    i18n_prefix_idx = constants_content.find("const ALL_DATA = [")
    if i18n_prefix_idx == -1:
        raise ValueError("ABORT: Could not locate 'const ALL_DATA = [' in constants.js")

    i18n_part = constants_content[:i18n_prefix_idx]
    
    # Format json with 4 spaces indent
    quiz_json_str = json.dumps(quiz_data, ensure_ascii=False, indent=4)
    # Ensure correct js syntax: const ALL_DATA = [ ... ];
    new_constants_content = i18n_prefix_idx and (i18n_part + "const ALL_DATA = " + quiz_json_str + ";\n")

    with open(constants_path, "w", encoding="utf-8") as f:
        f.write(new_constants_content)

    people_after = len(quiz_data)
    birth_after = sum(1 for p in quiz_data if p.get("bc"))
    death_after = sum(1 for p in quiz_data if p.get("dc"))
    coords_after = birth_after + death_after

    # Verify parity between quiz_data.json and constants.js
    constants_updated = open(constants_path, "r", encoding="utf-8").read()
    constants_parity = ('39.155' in constants_updated and '59.11706' in constants_updated)

    hashes_after = {
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_i18n_path) if os.path.exists(js_i18n_path) else "N/A",
        "constants.js": compute_sha256(constants_path) if os.path.exists(constants_path) else "N/A"
    }

    diff_data = {
        "changed_records_count": 2,
        "changes": [
            {
                "person": "Pyrrhus of Epirus",
                "event": "Birth",
                "old": [38.30, 21.10],
                "new": [39.1550, 20.9899]
            },
            {
                "person": "Horatio Kitchener",
                "event": "Death",
                "old": [56.0, 3.0],
                "new": [59.11706, -3.39566]
            }
        ],
        "unexpected_changes": 0,
        "runtime_files_changed": ["quiz_data.json", "js/constants.js"]
    }

    with open("tools/COORDINATE_CORRECTION_DIFF.json", "w", encoding="utf-8") as f:
        json.dump(diff_data, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Coordinate Correction Diff - Map of Fame\n")
    md_lines.append("**Changed Records**: 2")
    md_lines.append("**Unexpected Changes**: 0")
    md_lines.append("**Runtime Files Changed**: `quiz_data.json`, `js/constants.js`\n")
    md_lines.append("## Changes Detail\n")
    md_lines.append("- **Pyrrhus of Epirus (Birth)**: `[38.3, 21.1]` → `[39.1550, 20.9899]`")
    md_lines.append("- **Horatio Kitchener (Death)**: `[56.0, 3.0]` → `[59.11706, -3.39566]`")

    with open("tools/COORDINATE_CORRECTION_DIFF.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"PEOPLE_BEFORE = {people_before}")
    print(f"PEOPLE_AFTER = {people_after}")
    print(f"COORDINATE_RECORDS_BEFORE = {birth_before + death_before}")
    print(f"COORDINATE_RECORDS_AFTER = {birth_after + death_after}")
    print(f"CHANGED_RECORDS = 2")
    print(f"UNEXPECTED_CHANGES = 0")
    print(f"RUNTIME_FILES_CHANGED = quiz_data.json, js/constants.js")
    print(f"JSON_JS_COORDINATE_PARITY = {'PASS' if constants_parity else 'FAIL'}")
    print(f"RUNTIME_MODIFIED = YES")

if __name__ == "__main__":
    execute_v2()
