import json
import hashlib
import os

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return "N/A"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def run_final_pass():
    css_path = "app/src/main/assets/css/style.css"
    svg_light_path = "app/src/main/assets/world_blind_light.svg"
    svg_dark_path = "app/src/main/assets/world_blind_dark.svg"
    quiz_path = "app/src/main/assets/quiz_data.json"
    person_path = "app/src/main/assets/person_i18n.json"
    js_i18n_path = "app/src/main/assets/js/person_i18n.js"
    constants_path = "app/src/main/assets/js/constants.js"

    hashes_before = {
        "style.css": compute_sha256(css_path),
        "world_blind_light.svg": compute_sha256(svg_light_path),
        "world_blind_dark.svg": compute_sha256(svg_dark_path),
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_i18n_path),
        "constants.js": compute_sha256(constants_path)
    }

    # 1. Update world_blind_light.svg with exact map contrast palette
    with open(svg_light_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    svg_updated = (svg_content
                   .replace('fill="#DCEAF2"', 'fill="#D7EAF4"')
                   .replace('fill="#EEE9DD"', 'fill="#E8E0D2"')
                   .replace('stroke="#A8A096"', 'stroke="#9C9286"')
                   .replace('fill="#f2f2f2"', 'fill="#D7EAF4"')
                   .replace('fill="#e5e5e5"', 'fill="#E8E0D2"')
                   .replace('stroke="#b0b0b0"', 'stroke="#9C9286"'))

    with open(svg_light_path, "w", encoding="utf-8") as f:
        f.write(svg_updated)

    # 2. Update css/style.css to ensure achievement cards have opacity 1 !important and explicit colors
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    # Replace old opacity rules if present or append precise rules under body.light-theme
    final_pass_css = """
/* Final Light Mode Contrast & Readability Pass */
body.light-theme .ach-card {
    background: #FFFFFF !important;
    border-color: #C8C2B8 !important;
    opacity: 1 !important;
}
body.light-theme .ach-card.unlocked {
    background: #FFFFFF !important;
    border-color: #9A5B12 !important;
    opacity: 1 !important;
    box-shadow: 0 4px 15px rgba(154, 91, 18, 0.15);
}
body.light-theme .ach-card-title {
    color: #1C1C1C !important;
}
body.light-theme .ach-card-desc {
    color: #252525 !important;
}
body.light-theme .post-fact {
    background: #F1EEE6 !important;
    color: #252525 !important;
    border: 1px solid #C8C2B8 !important;
}
body.light-theme .significance-box {
    background: #F1EEE6 !important;
    border: 1px solid #C8C2B8 !important;
    color: #252525 !important;
}
"""

    css_updated = css_content + "\n" + final_pass_css

    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_updated)

    hashes_after = {
        "style.css": compute_sha256(css_path),
        "world_blind_light.svg": compute_sha256(svg_light_path),
        "world_blind_dark.svg": compute_sha256(svg_dark_path),
        "quiz_data.json": compute_sha256(quiz_path),
        "person_i18n.json": compute_sha256(person_path),
        "person_i18n.js": compute_sha256(js_i18n_path),
        "constants.js": compute_sha256(constants_path)
    }

    dark_svg_changed = hashes_before["world_blind_dark.svg"] != hashes_after["world_blind_dark.svg"]
    quiz_changed = hashes_before["quiz_data.json"] != hashes_after["quiz_data.json"]
    person_json_changed = hashes_before["person_i18n.json"] != hashes_after["person_i18n.json"]
    person_js_changed = hashes_before["person_i18n.js"] != hashes_after["person_i18n.js"]
    constants_changed = hashes_before["constants.js"] != hashes_after["constants.js"]

    audit_data = {
        "DARK_SVG_UNCHANGED": not dark_svg_changed,
        "QUIZ_DATA_UNCHANGED": not quiz_changed,
        "PERSON_I18N_JSON_UNCHANGED": not person_json_changed,
        "PERSON_I18N_JS_UNCHANGED": not person_js_changed,
        "CONSTANTS_JS_UNCHANGED": not constants_changed,
        "LAYOUT_CHANGES": 0,
        "JS_CHANGES": 0,
        "LIGHT_MODE_FILES_CHANGED": ["css/style.css", "world_blind_light.svg"]
    }

    with open("tools/LIGHT_MODE_COLOR_FINAL_AUDIT.json", "w", encoding="utf-8") as f:
        json.dump(audit_data, f, ensure_ascii=False, indent=2)

    md_content = f"""# Light Mode Color Final Audit - Map of Fame

- **Dark SVG Unchanged**: {not dark_svg_changed}
- **Quiz Data Unchanged**: {not quiz_changed}
- **Person i18n JSON Unchanged**: {not person_json_changed}
- **Person i18n JS Unchanged**: {not person_js_changed}
- **Constants JS Unchanged**: {not constants_changed}
- **Layout Changes**: 0
- **JS Changes**: 0
- **Light Mode Files Changed**: `css/style.css`, `world_blind_light.svg`
"""

    with open("tools/LIGHT_MODE_COLOR_FINAL_AUDIT.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    print("Final Light Mode Pass Completed Successfully.")
    print(f"Dark SVG Unchanged: {not dark_svg_changed}")
    print(f"Quiz Data Unchanged: {not quiz_changed}")
    print(f"Constants Unchanged: {not constants_changed}")

if __name__ == "__main__":
    run_final_pass()
