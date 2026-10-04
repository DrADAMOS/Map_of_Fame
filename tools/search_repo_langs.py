#!/usr/bin/env python3
import os
import re

repo_root = os.path.abspath(".")
ignore_dirs = {
    ".git", ".gradle", ".idea", "build", ".artifacts",
    ".wikipedia_content_cache", ".wikipedia_multilingual_cache", "__pycache__",
    ".wikipedia_content_cache_v12_backup"
}

lang_codes = ["he"]

hits = []

for root, dirs, files in os.walk(repo_root):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if file.endswith(('.json', '.js', '.kt', '.java', '.xml', '.html', '.properties', '.gradle', '.kts', '.py')):
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, repo_root)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                for line_idx, line in enumerate(lines, 1):
                    for code in lang_codes:
                        # Match `th`, : etc.
                        pattern = rf'[\"\'\`]{code}[\"\'\`]'
                        if re.search(pattern, line):
                            hits.append((relpath, line_idx, code, line.strip()))
            except Exception as e:
                pass

print(f"Total matching lines found: {len(hits)}")
by_file = {}
for relpath, line_idx, code, line in hits:
    if relpath not in by_file:
        by_file[relpath] = []
    by_file[relpath].append((line_idx, code, line))

for relpath, line_matches in sorted(by_file.items()):
    print(f"\nFile: {relpath} ({len(line_matches)} matches)")
    for line_idx, code, line in line_matches[:10]:
        print(f"  Line {line_idx} [{code}]: {line[:120]}")
    if len(line_matches) > 10:
        print(f"  ... and {len(line_matches) - 10} more matches")
