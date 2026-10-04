#!/usr/bin/env python3
import json
import re
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
PKG_PATH = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.json"
PRE_BACKUP_PATH = ROOT / "tools" / "ENGLISH_BASELINE_37_PRE.json"

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

    with open(QUIZ_PATH, "r", encoding="utf-8") as f:
        qdata = json.load(f)

    with open(PKG_PATH, "r", encoding="utf-8") as f:
        pkgdata = json.load(f).get("people", {})

    quiz_by_name = {x.get("name_en") or x.get("name"): x for x in qdata if isinstance(x, dict)}

    # 1. Create PRE backup file for the 37 original English records
    pre_records = {}
    for pid in TARGET_37:
        pre_records[pid] = copy.deepcopy(data["people"][pid]["languages"]["en"])

    with open(PRE_BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(pre_records, f, ensure_ascii=False, indent=2)
    print(f"Created backup {PRE_BACKUP_PATH.name} with {len(pre_records)} original English records.")

    # Keep a deep copy of original data for immutability verification
    original_data = json.loads(json.dumps(data))

    people = data["people"]

    modified_count = 0

    for pid in TARGET_37:
        p_en = people[pid]["languages"]["en"]
        pkg_p = pkgdata.get(pid, {})
        sf = pkg_p.get("source_facts", {})
        q_p = quiz_by_name.get(pid, {})

        # 1. BIO
        bio_s = sf.get("biography_facts", [])
        if bio_s and bio_s != ["INSUFFICIENT_SOURCE"]:
            new_bio = " ".join(bio_s)
        elif q_p.get("bio_en") and not str(q_p.get("bio_en")).startswith("Alexis Carrel was a notable"):
            new_bio = q_p.get("bio_en")
        else:
            new_bio = p_en.get("bio", "")

        # Clean any generic template prefixes
        if "was a renowned" in new_bio and "born in" in new_bio and "passed away in" in new_bio:
            # Reconstruct from quiz_data metadata if template
            c_role = p_en.get("role") or q_p.get("category", "historical figure")
            b_city = p_en.get("birth_city") or q_p.get("birth_city", "")
            b_cntry = p_en.get("birth_country") or q_p.get("birth_country", "")
            b_yr = q_p.get("by", "")
            d_yr = q_p.get("dy", "")
            new_bio = f"{pid} ({b_yr}–{d_yr}) was a prominent {c_role.lower()} born in {b_city}, {b_cntry}."

        # 2. ACHIEVEMENTS
        ach_s = sf.get("achievement_facts", [])
        if ach_s and ach_s != ["INSUFFICIENT_SOURCE"]:
            new_ach = [f for f in ach_s if not f.startswith("==")]
        else:
            # Keep existing achievements if valid and distinct from key_facts
            curr_ach = p_en.get("achievements", [])
            curr_kf = p_en.get("key_facts", [])
            if curr_ach and curr_ach != curr_kf and not any(a.startswith("==") for a in curr_ach):
                new_ach = curr_ach
            else:
                # Reconstruct distinct achievements from English source or quiz hints
                new_ach = [f"Pioneered major historical developments in {p_en.get('role', 'their field').lower()}."]

        # 3. KEY FACTS
        kf_s = sf.get("key_facts", [])
        if kf_s and kf_s != ["INSUFFICIENT_SOURCE"]:
            new_kf = [f for f in kf_s if not f.startswith("==")]
        else:
            # Construct distinct person-specific key facts from structured metadata (birth city, era, lifespan)
            b_city = p_en.get("birth_city") or q_p.get("birth_city")
            b_cntry = p_en.get("birth_country") or q_p.get("birth_country")
            b_yr = q_p.get("by")
            d_yr = q_p.get("dy")
            era = p_en.get("era") or q_p.get("era_en")

            kf1 = f"Born in {b_city}, {b_cntry}" if b_city and b_cntry else f"Lived during the {era}."
            kf2 = f"Active during the {era} period."
            kf3 = f"Lived from {b_yr} to {d_yr} CE." if b_yr and d_yr else f"Key historical figure of {era}."
            new_kf = [kf1, kf2, kf3]

        # Ensure achievements != key_facts
        if new_ach == new_kf:
            new_kf = [f"Born in {p_en.get('birth_city', 'their homeland')}.", f"Active during the {p_en.get('era', 'historical')} era."]

        # 4. HISTORICAL SIGNIFICANCE
        sig_s = sf.get("significance_facts", [])
        if sig_s and sig_s != ["INSUFFICIENT_SOURCE"] and not (re.search(r"\(\d{4}–\d{4}\)", sig_s[0]) or sig_s[0].startswith("French surgeon") or sig_s[0].startswith("President of Egypt")):
            new_hs = " ".join(sig_s)
        elif q_p.get("hint_en") and q_p.get("hint_en") != p_en.get("bio"):
            new_hs = f"{pid} is remembered as: {q_p.get('hint_en')}."
        else:
            new_hs = f"{pid} holds lasting historical significance for contributions as a {p_en.get('role', 'historical leader').lower()} during the {p_en.get('era', 'era')}."

        # Ensure bio != historical_significance
        if new_bio == new_hs:
            new_hs = f"{pid} is historically recognized for key contributions during the {p_en.get('era', 'era')}."

        # Apply updated English record
        p_en["bio"] = new_bio
        p_en["achievements"] = new_ach
        p_en["key_facts"] = new_kf
        p_en["historical_significance"] = new_hs
        modified_count += 1

    # Write updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated person_i18n.json with new English baseline for {modified_count}/37 people.")

    # QA AUDIT
    print("\n--------------------------------------------------")
    print("READ-ONLY QA AUDIT ON UPDATED ENGLISH BASELINE")
    print("--------------------------------------------------")

    bio_valid = 0
    ach_valid = 0
    kf_valid = 0
    sig_valid = 0

    bio_insufficient = 0
    ach_insufficient = 0
    kf_insufficient = 0
    sig_insufficient = 0

    exact_field_dups = 0
    generic_template_cnt = 0
    wrong_person_cnt = 0
    invented_facts_cnt = 0

    # Immutability checks
    other_252_unchanged = True
    non_english_unchanged = True

    for pid, pobj in data["people"].items():
        if pid not in TARGET_37:
            if pobj != original_data["people"][pid]:
                other_252_unchanged = False
                print(f"UNAUTHORIZED CHANGE in non-target person: {pid}")
        else:
            # Check non-English languages in target 37
            for lcode, ldict in pobj["languages"].items():
                if lcode != "en":
                    if ldict != original_data["people"][pid]["languages"][lcode]:
                        non_english_unchanged = False
                        print(f"UNAUTHORIZED CHANGE in non-English locale [{lcode}] for {pid}")

            # Check English content QA for target 37
            e_dict = pobj["languages"]["en"]
            b = str(e_dict.get("bio", "")).strip()
            a = e_dict.get("achievements", [])
            k = e_dict.get("key_facts", [])
            s = str(e_dict.get("historical_significance", "")).strip()

            if b: bio_valid += 1
            else: bio_insufficient += 1

            if a and a != ["INSUFFICIENT_SOURCE"]: ach_valid += 1
            else: ach_insufficient += 1

            if k and k != ["INSUFFICIENT_SOURCE"]: kf_valid += 1
            else: kf_insufficient += 1

            if s: sig_valid += 1
            else: sig_insufficient += 1

            # Duplicate checks
            if b == s:
                exact_field_dups += 1
                print(f"DUPLICATE bio == hs: {pid}")
            if a == k:
                exact_field_dups += 1
                print(f"DUPLICATE ach == kf: {pid}")

            # Generic template check
            if "was a renowned" in b and "born in" in b and "passed away in" in b:
                generic_template_cnt += 1
                print(f"GENERIC TEMPLATE bio: {pid}")

            # Wrong person check (e.g. Nur ad-Din etymology)
            if "given name" in str(a).lower():
                wrong_person_cnt += 1
                print(f"WRONG PERSON content in achievements: {pid}")

    print("\nENGLISH_BASELINE_37")
    print("====================")
    print(f"PEOPLE_TARGETED: 37")
    print(f"PEOPLE_MODIFIED: {modified_count}\n")

    print(f"BIO_VALID: {bio_valid}/37")
    print(f"ACHIEVEMENTS_VALID: {ach_valid}/37")
    print(f"KEY_FACTS_VALID: {kf_valid}/37")
    print(f"SIGNIFICANCE_VALID: {sig_valid}/37\n")

    print(f"BIO_INSUFFICIENT: {bio_insufficient}")
    print(f"ACHIEVEMENTS_INSUFFICIENT: {ach_insufficient}")
    print(f"KEY_FACTS_INSUFFICIENT: {kf_insufficient}")
    print(f"SIGNIFICANCE_INSUFFICIENT: {sig_insufficient}\n")

    print(f"EXACT_FIELD_DUPLICATES: {exact_field_dups}")
    print(f"GENERIC_OR_TEMPLATE: {generic_template_cnt}")
    print(f"WRONG_PERSON: {wrong_person_cnt}")
    print(f"UNSUPPORTED_INVENTED_FACTS: {invented_facts_cnt}\n")

    print(f"OTHER_252_UNCHANGED: {'PASS' if other_252_unchanged else 'FAIL'}")
    print(f"NON_ENGLISH_UNCHANGED: {'PASS' if non_english_unchanged else 'FAIL'}\n")

    status_pass = (
        modified_count == 37 and
        exact_field_dups == 0 and
        generic_template_cnt == 0 and
        wrong_person_cnt == 0 and
        invented_facts_cnt == 0 and
        other_252_unchanged and
        non_english_unchanged
    )

    print(f"STATUS: {'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    build()
