from __future__ import annotations
import json, shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
CANONICAL = ROOT / "tools" / "canonical" / "arabic_batch01.json"
BACKUPS = ROOT / "tools" / "backups"

def main() -> int:
    apply = "--apply" in __import__("sys").argv
    data = json.loads(DATA.read_text(encoding="utf-8"))
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))["people"]
    changes = []

    for key, fields in canonical.items():
        if key not in data["people"]:
            raise SystemExit(f"Missing person: {key}")
        ar = data["people"][key].setdefault("languages", {}).get("ar")
        if not isinstance(ar, dict):
            raise SystemExit(f"Missing Arabic record: {key}")
        for field, new in fields.items():
            if ar.get(field) != new:
                changes.append((key, field, ar.get(field), new))

    print(f"Mode: {'APPLY' if apply else 'DRY-RUN'}")
    print(f"Arabic people: {len(canonical)}")
    print(f"Planned field changes: {len(changes)}")
    for key, field, _, _ in changes:
        print(f"  UPDATE {key} [ar] {field}")

    if not apply:
        return 0

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUPS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA, BACKUPS / f"arabic_batch01_{stamp}.json")
    shutil.copy2(JS, BACKUPS / f"arabic_batch01_{stamp}.js")

    for key, field, _, new in changes:
        data["people"][key]["languages"]["ar"][field] = new

    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    JS.write_text(
        "window.PERSON_I18N = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    print("APPLIED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
