from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"

GENERIC_PATTERNS = [
    r"\brenowned\s+(writer|artist|musician|ruler|leader|scientist|philosopher)\b",
    r"\bremembered for shaping historical developments\b",
    r"\bhistorical developments as\b",
    r"\bnotable for his historical impact\b",
    r"\bknown for his historical contributions\b",
    r"\bknown for her historical contributions\b",
    r"تركت أثراً تاريخياً",
    r"تركت أثرًا تاريخيًا",
    r"حققت أثراً كبيراً وإنجازات تاريخية",
    r"حققت أثرًا كبيرًا وإنجازات تاريخية",
    r"من أبرز شخصيات العصر الحديث في مجال",
    r"écrivain renommé",
    r"artiste renommé",
    r"musicien renommé",
    r"знаменитый писатель",
    r"renombrado escritor",
]

PATTERNS = [re.compile(x, re.IGNORECASE) for x in GENERIC_PATTERNS]

def norm(v: Any) -> str:
    if isinstance(v, str):
        return re.sub(r"\s+", " ", v).strip()
    return json.dumps(v, ensure_ascii=False, sort_keys=True)

def main() -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]

    generic_by_lang = Counter()
    duplicate_by_lang = Counter()
    generic_examples: dict[str, Counter[str]] = {}
    duplicate_values: dict[str, dict[str, list[str]]] = {}

    for person_key, person in people.items():
        name = person.get("name_en") or person.get("name") or person_key
        langs = person.get("languages", {})

        for lang, record in langs.items():
            if not isinstance(record, dict):
                continue

            generic_examples.setdefault(lang, Counter())
            duplicate_values.setdefault(lang, {})

            values: dict[str, str] = {}
            for field, value in record.items():
                if isinstance(value, (str, list)):
                    text = norm(value)
                    if any(p.search(text) for p in PATTERNS):
                        generic_by_lang[lang] += 1
                        generic_examples[lang][f"{field}: {text}"] += 1

                    if text:
                        values[field] = text

            seen: dict[str, list[str]] = {}
            for field, value in values.items():
                seen.setdefault(value, []).append(field)

            for value, fields in seen.items():
                if len(fields) > 1:
                    duplicate_by_lang[lang] += len(fields) - 1
                    duplicate_values[lang].setdefault(value, [])
                    duplicate_values[lang][value].append(
                        f"{name} :: {', '.join(fields)}"
                    )

    print("=" * 72)
    print("MAP OF FAME CONTENT AUDIT")
    print("=" * 72)
    print()
    print("GENERIC HITS BY LANGUAGE")
    for lang, count in generic_by_lang.most_common():
        print(f"{lang:>3}: {count}")
    print()
    print("CROSS-FIELD DUPLICATES BY LANGUAGE")
    for lang, count in duplicate_by_lang.most_common():
        print(f"{lang:>3}: {count}")
    print()
    print("TOP GENERIC VALUES")
    for lang in generic_examples:
        if not generic_examples[lang]:
            continue
        print(f"\n[{lang}]")
        for value, count in generic_examples[lang].most_common(10):
            print(f"{count:>3}x  {value}")
    print()
    print("TOP CROSS-FIELD DUPLICATES")
    for lang in duplicate_values:
        items = [
            (len(v), k, v)
            for k, v in duplicate_values[lang].items()
        ]
        items.sort(reverse=True)
        if not items:
            continue
        print(f"\n[{lang}]")
        for count, value, people_list in items[:10]:
            print(f"{count}x {value}")
            for item in people_list[:5]:
                print(f"    {item}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
