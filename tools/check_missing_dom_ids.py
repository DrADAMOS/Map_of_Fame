#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "app" / "src" / "main" / "assets" / "game.html"
UI_JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "ui.js"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

with open(UI_JS_PATH, "r", encoding="utf-8") as f:
    ui_js = f.read()

# Find all direct textContent calls: document.getElementById('XYZ').textContent = ...
direct_calls = re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)\.textContent\s*=", ui_js)

print(f"Total direct getElementById().textContent calls in ui.js: {len(direct_calls)}")

missing = []
for el_id in direct_calls:
    if f'id="{el_id}"' not in html and f"id='{el_id}'" not in html:
        missing.append(el_id)

print(f"Missing DOM IDs in game.html: {len(missing)}")
for m in missing:
    print(f"  MISSING ID: {m}")
