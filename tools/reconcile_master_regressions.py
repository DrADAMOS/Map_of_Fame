from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CURRENT = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
CURRENT_JS = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
MASTER = ROOT / "tools" / "canonical" / "person_i18n_MASTER_CUMULATIVE_BATCH08_2026-09-02.json"
BACKUPS = ROOT / "tools" / "backups"

TARGET_FIELDS = {
    "Al-Farabi": {"achievements"},
    "Abd al-Rahman III": {"achievements"},
    "Yusuf ibn Tashfin": {"achievements"},
    "Al-Idrisi": {"achievements"},
    "Tokugawa Ieyasu": {"wars"},
    "Benjamin Franklin": {"achievements"},
    "Rashid Rida": {"achievements"},
    "Mahatma Gandhi": {"achievements"},
    "Amedeo Modigliani": {"achievements"},
    "Marc Chagall": {"achievements"},
    "Yasser Arafat": {"bio", "achievements", "key_facts", "historical_significance"},
    "Elvis Presley": {"achievements"},
    "Muhammad Ali": {"achievements"},
}

def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict) or not isinstance(value.get("people"), dict):
        raise RuntimeError(f"Invalid person_i18n structure: {path}")
    return value

def dump(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

def js_payload(data: dict[str, Any]) -> str:
    return "window.PERSON_I18N = " + json.dumps(
        data, ensure_ascii=False, indent=2, separators=(",", ": ")
    ) + ";\n"

def js_semantic_equal(path: Path, data: dict[str, Any]) -> bool:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\.PERSON_I18N\s*=\s*(\{.*\})\s*;\s*$", text, re.S)
    if not match:
        return False
    return json.loads(match.group(1)) == data

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not CURRENT.exists():
        raise SystemExit(f"Missing current JSON: {CURRENT}")
    if not MASTER.exists():
        raise SystemExit(f"Missing master JSON: {MASTER}")
    if not CURRENT_JS.exists():
        raise SystemExit(f"Missing current JS: {CURRENT_JS}")

    current = load(CURRENT)
    master = load(MASTER)

    changes: list[tuple[str, str, str, Any, Any]] = []

    for person, fields in TARGET_FIELDS.items():
        c_person = current["people"].get(person)
        m_person = master["people"].get(person)
        if not isinstance(c_person, dict) or not isinstance(m_person, dict):
            raise SystemExit(f"Missing person in current/master: {person}")

        c_langs = c_person.get("languages")
        m_langs = m_person.get("languages")
        if not isinstance(c_langs, dict) or not isinstance(m_langs, dict):
            raise SystemExit(f"Invalid languages for: {person}")

        c_en = c_langs.get("en")
        m_en = m_langs.get("en")
        if not isinstance(c_en, dict) or not isinstance(m_en, dict):
            raise SystemExit(f"Missing English record for: {person}")

        for field in sorted(fields):
            old = c_en.get(field)
            new = m_en.get(field)
            if old != new:
                changes.append((person, "en", field, old, new))

    print(f"Project: {ROOT}")
    print(f"Master: {MASTER.name}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Planned field changes: {len(changes)}")
    print()

    for person, lang, field, old, new in changes:
        print(f"  UPDATE  {person} [{lang}] {field}")

    if not args.apply:
        print("\nDRY-RUN only. No files changed.")
        return 0

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    backup_json = BACKUPS / f"person_i18n_reconcile_{stamp}.json"
    backup_js = BACKUPS / f"person_i18n_reconcile_{stamp}.js"
    shutil.copy2(CURRENT, backup_json)
    shutil.copy2(CURRENT_JS, backup_js)

    for person, lang, field, _old, new in changes:
        current["people"][person]["languages"][lang][field] = new

    dump(CURRENT, current)
    CURRENT_JS.write_text(js_payload(current), encoding="utf-8", newline="\n")

    if not js_semantic_equal(CURRENT_JS, current):
        shutil.copy2(backup_json, CURRENT)
        shutil.copy2(backup_js, CURRENT_JS)
        raise SystemExit("JSON↔JS semantic equality FAILED; originals restored.")

    print("\nAPPLIED successfully.")
    print(f"Backup JSON: {backup_json}")
    print(f"Backup JS:   {backup_js}")
    print("JSON↔JS semantic equality: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
