#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app" / "src" / "main"
REMOVED = ["he"]

for fpath in APP_DIR.rglob("*"):
    if fpath.is_file() and fpath.suffix in [".json", ".js", ".kt", ".java", ".xml", ".html"]:
        if "backup" in fpath.name or fpath.name == "tailwind.js":
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for code in REMOVED:
                # Match "th", 'th', "th":, 'th':, "th"], 'th']
                pattern = rf"[\"\'\`]{code}[\"\'\`]\s*[:\,\]]"
                matches = re.findall(pattern, text)
                if matches:
                    print(f"File: {fpath.relative_to(APP_DIR)} [{code}]: {len(matches)} matches")
                    for line_idx, line in enumerate(text.splitlines(), 1):
                        if re.search(pattern, line):
                            print(f"  Line {line_idx}: {line.strip()[:100]}")
        except Exception as e:
            pass
