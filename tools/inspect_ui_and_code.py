#!/usr/bin/env python3
import os
import re

app_dir = os.path.abspath("app/src/main")

for root, dirs, files in os.walk(app_dir):
    for file in files:
        if file.endswith(('.js', '.html', '.kt', '.java', '.xml')):
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, app_dir)
            if "person_i18n.js" in file:
                continue

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            keywords = ['LANGUAGES', 'RTL_LANGS', 'language', 'lang', 'i18n', 'locale']
            matches = []
            for kw in keywords:
                found = re.findall(rf'.{{0,30}}{kw}.{{0,30}}', content, re.I)
                if found:
                    matches.extend(found[:2])
            if matches:
                print(f"\nFile: {relpath}")
                for m in matches[:5]:
                    print(f"  {m.strip()}")
