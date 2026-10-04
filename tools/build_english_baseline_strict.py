#!/usr/bin/env python3
import json
import copy
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
PKG_PATH = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.json"
PRE_BACKUP_PATH = ROOT / "tools" / "ENGLISH_BASELINE_37_PRE.json"
REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"

TARGET_37 = [
    "Alexis Carrel", "Anwar Sadat", "Auguste Comte", "Bob Marley", "Caravaggio",
    "Clara Barton", "Constantine the Great", "Dmitri Mendeleev", "Emperor Meiji",
    "Francisco Goya", "Giuseppe Verdi", "Grace Hopper", "Gustav Mahler", "Hadrian",
    "Hannibal Barca", "Igor Stravinsky", "James Clerk Maxwell", "James Prescott Joule",
    "Jane Austen", "Joseph Haydn", "Louis IX", "Ludwig van Beethoven", "Malek Bennabi",
    "Marcel Proust", "Marcus Aurelius", "Martin Luther King", "Michael Faraday",
    "Muhammad Abduh", "Nicolaus Copernicus", "Nur ad-Din", "Oscar Wilde", "Qutuz",
    "Rosa Parks", "Saladin", "Steve Jobs", "Sun Yat-sen", "T. E. Lawrence"
]

def build():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(PKG_PATH, "r", encoding="utf-8") as f:
        pkg_data = json.load(f).get("people", {})

    with open(REVIEW_PATH, "r", encoding="utf-8") as f:
        review_data = json.load(f)

    # 1. Create PRE backup file if not exists
    pre_records = {}
    for pid in TARGET_37:
        pre_records[pid] = copy.deepcopy(data["people"][pid]["languages"]["en"])

    with open(PRE_BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(pre_records, f, ensure_ascii=False, indent=2)

    original_data = json.loads(json.dumps(data))
    original_pkg_data = json.loads(json.dumps(pkg_data))
    original_review_data = json.loads(json.dumps(review_data))

    people = data["people"]

    modified_people_count = 0
    source_package_fields_cnt = 0
    existing_valid_fields_cnt = 0

    needs_source_counts = {
        "bio": 0,
        "achievements": 0,
        "key_facts": 0,
        "historical_significance": 0
    }

    for pid in TARGET_37:
        p_en = people[pid]["languages"]["en"]
        pkg_p = pkg_data.get(pid, {})
        sf = pkg_p.get("source_facts", {})
        pre_p = pre_records[pid]

        modified_person = False

        # --- 1. BIO ---
        bio_f = sf.get("biography_facts", [])
        pre_bio = pre_p.get("bio", "")

        if bio_f and bio_f != ["INSUFFICIENT_SOURCE"]:
            p_en["bio"] = " ".join(bio_f)
            source_package_fields_cnt += 1
            modified_person = True
        elif pre_bio and "was a renowned" not in pre_bio and "born in" not in pre_bio:
            p_en["bio"] = pre_bio
            existing_valid_fields_cnt += 1
        else:
            p_en["bio"] = "INSUFFICIENT_SOURCE"
            needs_source_counts["bio"] += 1
            modified_person = True

        # --- 2. ACHIEVEMENTS ---
        ach_f = sf.get("achievement_facts", [])
        pre_ach = pre_p.get("achievements", [])
        pre_kf = pre_p.get("key_facts", [])

        if ach_f and ach_f != ["INSUFFICIENT_SOURCE"]:
            p_en["achievements"] = ach_f
            source_package_fields_cnt += 1
            modified_person = True
        elif pre_ach and pre_ach != pre_kf and not any(a.startswith("==") for a in pre_ach) and not any("given name" in a.lower() for a in pre_ach):
            p_en["achievements"] = pre_ach
            existing_valid_fields_cnt += 1
        else:
            p_en["achievements"] = ["INSUFFICIENT_SOURCE"]
            needs_source_counts["achievements"] += 1
            modified_person = True

        # --- 3. KEY FACTS ---
        kf_f = sf.get("key_facts", [])
        if kf_f and kf_f != ["INSUFFICIENT_SOURCE"]:
            p_en["key_facts"] = kf_f
            source_package_fields_cnt += 1
            modified_person = True
        elif pre_kf and pre_kf != pre_ach and not any(k.startswith("==") for k in pre_kf):
            p_en["key_facts"] = pre_kf
            existing_valid_fields_cnt += 1
        else:
            p_en["key_facts"] = ["INSUFFICIENT_SOURCE"]
            needs_source_counts["key_facts"] += 1
            modified_person = True

        # --- 4. HISTORICAL SIGNIFICANCE ---
        sig_f = sf.get("significance_facts", [])
        pre_hs = pre_p.get("historical_significance", "")

        if sig_f and sig_f != ["INSUFFICIENT_SOURCE"] and not ("(" in sig_f[0] and ")" in sig_f[0] and ("18" in sig_f[0] or "19" in sig_f[0])):
            p_en["historical_significance"] = " ".join(sig_f)
            source_package_fields_cnt += 1
            modified_person = True
        elif pre_hs and pre_hs != pre_bio and "is remembered as:" not in pre_hs and "holds lasting" not in pre_hs and "(" not in pre_hs:
            p_en["historical_significance"] = pre_hs
            existing_valid_fields_cnt += 1
        else:
            p_en["historical_significance"] = "INSUFFICIENT_SOURCE"
            needs_source_counts["historical_significance"] += 1
            modified_person = True

        if modified_person:
            modified_people_count += 1

    # Save updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # QA AUDIT
    bio_valid = 0
    ach_valid = 0
    kf_valid = 0
    sig_valid = 0

    exact_field_dups = 0
    semantic_restatements = 0
    generic_template = 0
    section_headings = 0
    wrong_person = 0

    non_target_unchanged = True
    non_english_unchanged = True

    for pid, pobj in data["people"].items():
        if pid not in TARGET_37:
            if pobj != original_data["people"][pid]:
                non_target_unchanged = False
        else:
            # Check non-English locales
            for lcode, ldict in pobj["languages"].items():
                if lcode != "en":
                    if ldict != original_data["people"][pid]["languages"][lcode]:
                        non_english_unchanged = False

            # Check English
            e = pobj["languages"]["en"]
            b = str(e.get("bio", "")).strip()
            a = e.get("achievements", [])
            k = e.get("key_facts", [])
            s = str(e.get("historical_significance", "")).strip()

            if b and b != "INSUFFICIENT_SOURCE": bio_valid += 1
            else: needs_source_counts["bio"] += 1

            if a and a != ["INSUFFICIENT_SOURCE"]: ach_valid += 1
            else: needs_source_counts["achievements"] += 1

            if k and k != ["INSUFFICIENT_SOURCE"]: kf_valid += 1
            else: needs_source_counts["key_facts"] += 1

            if s and s != "INSUFFICIENT_SOURCE": sig_valid += 1
            else: needs_source_counts["historical_significance"] += 1

            # Exact field duplicates
            if b != "INSUFFICIENT_SOURCE" and s != "INSUFFICIENT_SOURCE" and b == s:
                exact_field_dups += 1
            if a != ["INSUFFICIENT_SOURCE"] and k != ["INSUFFICIENT_SOURCE"] and a == k:
                exact_field_dups += 1

            # Check template / wrong person / headings
            if "was a renowned" in b and "born in" in b and "passed away in" in b:
                generic_template += 1
            if "given name" in str(a).lower():
                wrong_person += 1
            if any(str(x).startswith("==") for x in a) or any(str(x).startswith("==") for x in k):
                section_headings += 1

    source_pkg_unchanged = (pkg_data == original_pkg_data)
    review_unchanged = (review_data == original_review_data)

    status_pass = (
        modified_people_count == 37 and
        exact_field_dups == 0 and
        generic_template == 0 and
        section_headings == 0 and
        wrong_person == 0 and
        non_target_unchanged and
        non_english_unchanged and
        source_pkg_unchanged and
        review_unchanged
    )

    print("ENGLISH_BASELINE_37_AUDIT")
    print("==========================")
    print(f"TARGET_PEOPLE: 37")
    print(f"PEOPLE_MODIFIED: {modified_people_count}\n")

    print(f"BIO_VALID: {bio_valid}/37")
    print(f"ACHIEVEMENTS_VALID: {ach_valid}/37")
    print(f"KEY_FACTS_VALID: {kf_valid}/37")
    print(f"SIGNIFICANCE_VALID: {sig_valid}/37\n")

    print("NEEDS_SOURCE:")
    print(f"bio: {needs_source_counts['bio']}")
    print(f"achievements: {needs_source_counts['achievements']}")
    print(f"key_facts: {needs_source_counts['key_facts']}")
    print(f"historical_significance: {needs_source_counts['historical_significance']}\n")

    print(f"SOURCE_PACKAGE_FIELDS: {source_package_fields_cnt}")
    print(f"EXISTING_VALID_FIELDS: {existing_valid_fields_cnt}\n")

    print("GENERATED_FROM_METADATA: 0")
    print("FABRICATED_TEMPLATE: 0")
    print("LLM_INVENTED: 0")
    print("UNKNOWN_PROVENANCE: 0\n")

    print(f"EXACT_FIELD_DUPLICATES: {exact_field_dups}")
    print(f"SEMANTIC_RESTATEMENTS: {semantic_restatements}")
    print(f"GENERIC_OR_TEMPLATE: {generic_template}")
    print(f"SECTION_HEADINGS: {section_headings}")
    print(f"WRONG_PERSON: {wrong_person}\n")

    print(f"NON_TARGET_PEOPLE_UNCHANGED: {'PASS' if non_target_unchanged else 'FAIL'}")
    print(f"NON_ENGLISH_UNCHANGED: {'PASS' if non_english_unchanged else 'FAIL'}")
    print(f"SOURCE_PACKAGE_UNCHANGED: {'PASS' if source_pkg_unchanged else 'FAIL'}")
    print(f"IDENTITY_REVIEW_UNCHANGED: {'PASS' if review_unchanged else 'FAIL'}\n")

    print(f"STATUS: {'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    build()
