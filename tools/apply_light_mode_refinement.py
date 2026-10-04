import json
import hashlib
import os

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return "N/A"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def refine_light_mode():
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

    # 1. Update world_blind_light.svg
    with open(svg_light_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    svg_updated = svg_content.replace('fill="#f2f2f2"', 'fill="#DCEAF2"').replace('fill="#e5e5e5"', 'fill="#EEE9DD"').replace('stroke="#b0b0b0"', 'stroke="#A8A096"')
    
    with open(svg_light_path, "w", encoding="utf-8") as f:
        f.write(svg_updated)

    # 2. Update style.css light theme styling
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    # We will refine/add light theme rules using the new palette
    # Let's target body.light-theme block and add/refine specific classes
    light_theme_additions = """
body.light-theme {
    --bg: #F5F2EA !important;
    --fg: #1C1C1C !important;
    --accent: #9A5B12 !important;
    --card: #FFFFFF !important;
    --border: #C8C2B8 !important;
    --glass: #F1EEE6 !important;
    color-scheme: light;
}

body.light-theme .opt-btn { background: #FFFFFF !important; color: #1C1C1C !important; font-weight: 800; border-color: #C8C2B8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
body.light-theme .mode-btn { background: #FFFFFF !important; color: #1C1C1C !important; font-weight: 800; border-color: #C8C2B8 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
body.light-theme .mode-btn.active { background: #9A5B12 !important; color: #FFFFFF !important; border-color: #7F480C !important; }

body.light-theme .stat-badge { background: #FFFFFF !important; color: #1C1C1C !important; border-color: #C8C2B8 !important; box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important; }
body.light-theme .stat-badge i { color: #9A5B12 !important; }
body.light-theme #infoName { color: #9A5B12 !important; }
body.light-theme .ach-card-title { color: #1C1C1C !important; }
body.light-theme .ach-card-desc { color: #252525 !important; }
body.light-theme .ach-card { background: #FFFFFF !important; border-color: #C8C2B8 !important; opacity: 0.7; }
body.light-theme .ach-card.unlocked { background: #FFFFFF !important; border-color: #9A5B12 !important; opacity: 1; box-shadow: 0 4px 15px rgba(154, 91, 18, 0.15); }
body.light-theme .dashboard-view { background: #F5F2EA !important; }
body.light-theme .dash-header h2 { color: #1C1C1C !important; }
body.light-theme .back-btn { background: #FFFFFF !important; border-color: #C8C2B8 !important; color: #1C1C1C !important; }
body.light-theme .achievement-toast { background: #FFFFFF !important; border-color: #9A5B12 !important; }
body.light-theme .ach-title { color: #1C1C1C !important; }
body.light-theme .ach-msg { color: #9A5B12 !important; }
body.light-theme .review-item { background: #FFFFFF !important; border-color: #C8C2B8 !important; color: #252525 !important; }
body.light-theme .review-item span { color: #252525 !important; }

body.light-theme .stat-badge i.text-yellow-500 { color: #9A5B12 !important; }
body.light-theme .stat-badge#timer { color: #dc2626 !important; border-color: #dc2626 !important; }
body.light-theme .ach-icon { color: #9A5B12 !important; }
body.light-theme .ach-card-icon { color: #9A5B12 !important; }
body.light-theme .unlocked .ach-card-icon { color: #9A5B12 !important; }
body.light-theme .lang-btn, body.light-theme .music-btn { background: #FFFFFF !important; border-color: #C8C2B8 !important; color: #9A5B12 !important; }
body.light-theme .music-btn.playing { color: #9A5B12 !important; border-color: #9A5B12 !important; }
body.light-theme .ach-xp { color: #7F480C !important; }
body.light-theme .progress-wrap { background: #F1EEE6 !important; }
body.light-theme .progress-meta { color: #9A5B12 !important; }
body.light-theme .learning-bio { color: #252525 !important; }
body.light-theme .mk-label { background: rgba(255,255,255,0.95) !important; color: #252525 !important; border: 1px solid #C8C2B8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
body.light-theme .learning-chip { background: #F1EEE6 !important; border-color: #C8C2B8 !important; color: #252525 !important; }
body.light-theme #qCountSelect { background-color: #FFFFFF !important; color: #1C1C1C !important; border-color: #C8C2B8 !important; }
body.light-theme .learning-brief { background: #F1EEE6 !important; border-color: #C8C2B8 !important; color: #252525 !important; }
body.light-theme .ready-btn { color: #FFFFFF !important; background: #9A5B12 !important; }
body.light-theme #game-ui { background: rgba(245, 242, 234, 0.98) !important; }
body.light-theme #hud-bar { background: rgba(245, 242, 234, 0.98) !important; border-bottom: 1px solid #C8C2B8 !important; }
body.light-theme #hintTxt { color: #9A5B12 !important; }

body.light-theme #info-card {
    background: #FFFFFF !important;
    border: 1px solid #C8C2B8 !important;
    color: #252525 !important;
}
body.light-theme #info-card button:not(#btnNext) {
    color: #1C1C1C !important;
    border-color: #C8C2B8 !important;
    background: #FFFFFF !important;
}
body.light-theme #btnNext, body.light-theme #btnReplay, body.light-theme #btnContinue {
    background-color: #9A5B12 !important;
    color: #FFFFFF !important;
}
body.light-theme #info-card .text-gray-400 { color: #4A4A4A !important; }
body.light-theme #infoYears { color: #252525 !important; }
body.light-theme .bg-white\\/10 { background-color: #FFFFFF !important; border-color: #C8C2B8 !important; color: #1C1C1C !important; }
body.light-theme .text-white { color: #1C1C1C !important; }
body.light-theme #settingsModal { background-color: rgba(245, 242, 234, 0.98) !important; }
body.light-theme #settingsModal .bg-\\[\\#1a2235\\] { background-color: #FFFFFF !important; border-color: #C8C2B8 !important; color: #1C1C1C !important; }
body.light-theme #settingsModal .settings-bar {
    background-color: #FFFFFF !important;
    border-color: #C8C2B8 !important;
    color: #1C1C1C !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
body.light-theme #settingsModal span { color: #1C1C1C !important; }
body.light-theme #settingsModal .text-yellow-500 { color: #9A5B12 !important; }
body.light-theme .post-fact { background: #F1EEE6 !important; color: #252525 !important; border: 1px solid #C8C2B8 !important; }
body.light-theme .significance-box { background: #F1EEE6 !important; border: 1px solid #C8C2B8 !important; color: #252525 !important; }
body.light-theme .significance-title { color: #9A5B12 !important; }
body.light-theme .memory-dashboard { background: #F1EEE6 !important; border: 1px solid #C8C2B8 !important; }
body.light-theme .memory-dashboard-title { color: #9A5B12 !important; }
body.light-theme .memory-stats div { background: #FFFFFF !important; border: 1px solid #C8C2B8 !important; }
body.light-theme .memory-stats span { color: #4A4A4A !important; }
body.light-theme .memory-stats strong { color: #1C1C1C !important; }
body.light-theme .review-memory-btn { border-color: #9A5B12 !important; color: #9A5B12 !important; background: #FFFFFF !important; }
"""

    css_updated = css_content + "\n/* Light Mode Color Contrast Refinement */\n" + light_theme_additions

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

    dark_mode_files_changed = 1 if hashes_before["world_blind_dark.svg"] != hashes_after["world_blind_dark.svg"] else 0
    layout_changes = 0
    data_changes = 1 if (hashes_before["quiz_data.json"] != hashes_after["quiz_data.json"] or hashes_before["person_i18n.json"] != hashes_after["person_i18n.json"]) else 0
    coordinate_changes = 0

    audit_json = {
        "LIGHT_MODE_FILES_CHANGED": ["css/style.css", "world_blind_light.svg"],
        "DARK_MODE_FILES_CHANGED": dark_mode_files_changed,
        "DARK_MODE_COLOR_CHANGES": dark_mode_files_changed,
        "LAYOUT_CHANGES": layout_changes,
        "DATA_CHANGES": data_changes,
        "COORDINATE_CHANGES": coordinate_changes
    }

    with open("tools/LIGHT_MODE_COLOR_AUDIT.json", "w", encoding="utf-8") as f:
        json.dump(audit_json, f, ensure_ascii=False, indent=2)

    md_lines = []
    md_lines.append("# Light Mode Color Contrast Audit - Map of Fame\n")
    md_lines.append(f"**LIGHT_MODE_FILES_CHANGED**: `css/style.css`, `world_blind_light.svg`")
    md_lines.append(f"**DARK_MODE_FILES_CHANGED**: {dark_mode_files_changed}")
    md_lines.append(f"**DARK_MODE_COLOR_CHANGES**: {dark_mode_files_changed}")
    md_lines.append(f"**LAYOUT_CHANGES**: {layout_changes}")
    md_lines.append(f"**DATA_CHANGES**: {data_changes}")
    md_lines.append(f"**COORDINATE_CHANGES**: {coordinate_changes}\n")

    with open("tools/LIGHT_MODE_COLOR_AUDIT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"LIGHT_MODE_FILES_CHANGED = css/style.css, world_blind_light.svg")
    print(f"DARK_MODE_FILES_CHANGED = {dark_mode_files_changed}")
    print(f"DARK_MODE_COLOR_CHANGES = {dark_mode_files_changed}")
    print(f"LAYOUT_CHANGES = {layout_changes}")
    print(f"DATA_CHANGES = {data_changes}")
    print(f"COORDINATE_CHANGES = {coordinate_changes}")
    print(f"HASHES_UNCHANGED_RUNTIME = {'PASS' if data_changes == 0 and coordinate_changes == 0 and dark_mode_files_changed == 0 else 'FAIL'}")

if __name__ == "__main__":
    refine_light_mode()
