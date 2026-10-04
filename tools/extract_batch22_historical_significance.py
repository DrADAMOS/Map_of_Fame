from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUT_PATH = ROOT / "tools" / "batch22_historical_significance_targets.txt"

def normalize_name(value: str) -> str:
    try:
        return value.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value

def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    groups: dict[tuple[str, str], list[str]] = defaultdict(list)

    for person in data["people"].values():
        if not isinstance(person, dict):
            continue
        languages = person.get("languages", {})
        if not isinstance(languages, dict):
            continue
        en = languages.get("en", {})
        if not isinstance(en, dict):
            continue
        raw_name = en.get("name")
        if not isinstance(raw_name, str):
            continue
        name = normalize_name(raw_name)

        for lang, content in languages.items():
            if not isinstance(content, dict):
                continue
            value = content.get("historical_significance")
            if isinstance(value, str) and value.strip():
                groups[(lang, value)].append(name)

    repeated = [
        (lang, value, names)
        for (lang, value), names in groups.items()
        if len(names) >= 2
    ]
    repeated.sort(key=lambda x: (-len(x[2]), x[0], x[1]))

    with OUT_PATH.open("w", encoding="utf-8") as f:
        f.write(f"Repeated historical_significance groups: {len(repeated)}\n")
        f.write("=" * 100 + "\n\n")
        for i, (lang, value, names) in enumerate(repeated, 1):
            f.write(f"[{i:03d}] {len(names)}x | lang={lang}\n")
            f.write(f"VALUE: {value}\n")
            f.write("PEOPLE:\n")
            for name in names:
                f.write(f"  - {name}\n")
            f.write("\n")

    print(f"Repeated historical_significance groups: {len(repeated)}")
    print(f"Report: {OUT_PATH}")
    print()
    print("Top groups:")
    for i, (lang, value, names) in enumerate(repeated[:30], 1):
        print(f"{i:02d}. {len(names)}x | {lang} | {value}")
        print("    " + " | ".join(names))

if __name__ == "__main__":
    main()
