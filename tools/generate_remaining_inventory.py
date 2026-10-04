import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
ADJUDICATION_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"
OUT_PATH = ROOT / "tools" / "REMAINING_DUPLICATE_FIELDS_INVENTORY.json"

def main():
    with open(ADJUDICATION_PATH, "r", encoding="utf-8") as f:
        adj = json.load(f)
    excluded_people = {c["person"] for c in adj["clusters"]}

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    people = data.get("people", {})
    field_pairs = [
        ("bio", "historical_significance"),
        ("achievements", "key_facts"),
        ("bio", "achievements"),
        ("bio", "key_facts"),
        ("achievements", "historical_significance"),
        ("key_facts", "historical_significance")
    ]

    remaining_duplicates = []
    people_with_dups = set()
    locales_set = set()
    total_person_lang_records = 0
    unique_person_langs_with_dups = set()

    for pid, pobj in people.items():
        langs = pobj.get("languages", {})
        total_person_lang_records += len(langs)
        for lcode, ldict in langs.items():
            locales_set.add(lcode)
            for fa, fb in field_pairs:
                if pid in excluded_people and {fa, fb} == {"bio", "historical_significance"}:
                    continue

                val_a = ldict.get(fa)
                val_b = ldict.get(fb)

                if val_a is None or val_b is None:
                    continue

                str_a = (json.dumps(val_a, ensure_ascii=False) if isinstance(val_a, list) else str(val_a)).strip()
                str_b = (json.dumps(val_b, ensure_ascii=False) if isinstance(val_b, list) else str(val_b)).strip()

                if str_a and str_b and str_a == str_b and str_a != '"INSUFFICIENT_SOURCE"' and str_a != '["INSUFFICIENT_SOURCE"]':
                    remaining_duplicates.append({
                        "person": pid,
                        "language": lcode,
                        "field_a": fa,
                        "field_b": fb,
                        "exact_text": str_a
                    })
                    people_with_dups.add(pid)
                    unique_person_langs_with_dups.add((pid, lcode))

    by_field_pair = {}
    by_language = {}

    for d in remaining_duplicates:
        fp_key = f"{d['field_a']} ↔ {d['field_b']}"
        by_field_pair[fp_key] = by_field_pair.get(fp_key, 0) + 1
        lang = d["language"]
        by_language[lang] = by_language.get(lang, 0) + 1

    inventory_payload = {
        "audit_type": "REMAINING_DUPLICATE_FIELDS_INVENTORY",
        "read_only": True,
        "excluded_completed_clusters": 43,
        "duplicate_pairs": remaining_duplicates,
        "summary": {
            "total_remaining_raw_duplicates": len(remaining_duplicates),
            "total_remaining_people": len(people_with_dups),
            "total_remaining_locale_records": len(unique_person_langs_with_dups),
            "by_field_pair": by_field_pair,
            "by_language": by_language
        },
        "integrity": {
            "people": len(people),
            "languages": len(locales_set),
            "person_language_records": total_person_lang_records,
            "application_data_modified": False
        }
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(inventory_payload, f, indent=2, ensure_ascii=False)

    print("REMAINING DUPLICATE INVENTORY")
    print("-----------------------------")
    print(f"TOTAL_REMAINING_RAW_DUPLICATES: {len(remaining_duplicates)}")
    print(f"TOTAL_REMAINING_PEOPLE: {len(people_with_dups)}")
    print(f"TOTAL_REMAINING_LOCALE_RECORDS: {len(unique_person_langs_with_dups)}")
    print(f"PEOPLE: {len(people)}")
    print(f"LANGUAGES: {len(locales_set)}")
    print(f"PERSON_LANGUAGE_RECORDS: {total_person_lang_records}")
    print("APPLICATION_DATA_MODIFIED: NO")
    status = "PASS" if len(people) == 289 and len(locales_set) == 14 and total_person_lang_records == 4046 else "FAIL"
    print(f"FINAL_STATUS: {status}")

if __name__ == "__main__":
    main()
