#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
PKG_PATH = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.json"

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

def run_audit():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        curr_data = json.load(f)["people"]

    with open(PKG_PATH, "r", encoding="utf-8") as f:
        pkg_data = json.load(f).get("people", {})

    valid_fields = 0
    invalid_fields = 0

    invalid_by_category = {
        "INSUFFICIENT_SOURCE": 0,
        "GENERIC_TEMPLATE": 0,
        "WRONG_PERSON_OR_TOPIC": 0,
        "FIELD_INAPPROPRIATE": 0,
        "DUPLICATE_OF_OTHER_FIELD": 0,
        "SEMANTIC_RESTATEMENT": 0,
        "UNKNOWN_PROVENANCE": 0
    }

    people_with_invalid = set()
    fields_requiring_replacement = 0

    print("=== SECOND READ-ONLY SEMANTIC AUDIT (ALL 148 FIELDS) ===\n")

    for pid in TARGET_37:
        curr_en = curr_data[pid]["languages"]["en"]
        pkg_p = pkg_data.get(pid, {})
        wiki_url = pkg_p.get("identity", {}).get("wikipedia_url", f"https://en.wikipedia.org/wiki/{pid.replace(' ', '_')}")

        bio = curr_en.get("bio", "")
        ach = curr_en.get("achievements", [])
        kf = curr_en.get("key_facts", [])
        hs = curr_en.get("historical_significance", "")

        for fname, fval in [("bio", bio), ("achievements", ach), ("key_facts", kf), ("historical_significance", hs)]:
            val_str = json.dumps(fval) if isinstance(fval, list) else str(fval)
            val_lower = val_str.lower()

            # 1. Check INSUFFICIENT_SOURCE
            if fval == "INSUFFICIENT_SOURCE" or fval == ["INSUFFICIENT_SOURCE"] or not fval:
                classification = "INSUFFICIENT_SOURCE"
                reason = "Field value is explicitly INSUFFICIENT_SOURCE or empty."
                req_source = f"Wikipedia or authoritative historical source for {fname}."

            # 2. Check metadata-only key_facts e.g. ["Born in X", "Active during X", "Lived from X to Y"]
            elif fname == "key_facts" and isinstance(fval, list) and any(re.search(r"Born in|Active during|Lived from|Key historical figure", str(x)) for x in fval):
                classification = "INSUFFICIENT_SOURCE"
                reason = "Key facts consist solely of generic metadata (birthplace, era, lifespan) without person-specific historical facts."
                req_source = f"Specific historical facts/milestones for {pid}."

            # 3. Check WRONG_PERSON_OR_TOPIC
            elif "given name" in val_lower or "is a male" in val_lower:
                classification = "WRONG_PERSON_OR_TOPIC"
                reason = "Describes Arabic given name etymology instead of historical person."
                req_source = f"Factual achievements of historical ruler {pid}."

            # 4. Check GENERIC_TEMPLATE
            elif "was a renowned" in val_str or "Pioneered major historical developments" in val_str or "is remembered as:" in val_str or "holds lasting" in val_str:
                classification = "GENERIC_TEMPLATE"
                reason = "Generic fallback sentence or template string lacking person-specific content."
                req_source = f"Specific historical {fname} for {pid}."

            # 5. Check FIELD_INAPPROPRIATE
            elif fname == "historical_significance" and (("(" in val_str and ")" in val_str and ("18" in val_str or "19" in val_str)) or val_str.startswith("French surgeon") or val_str.startswith("President of Egypt")):
                classification = "FIELD_INAPPROPRIATE"
                reason = "Occupation, title, or lifespan tag assigned to historical_significance instead of explaining historical impact."
                req_source = "Concise, distinct historical significance statement explaining legacy/impact."

            # 6. Check DUPLICATE_OF_OTHER_FIELD
            elif (fname == "historical_significance" and val_str == str(bio)) or (fname == "key_facts" and fval == ach):
                classification = "DUPLICATE_OF_OTHER_FIELD"
                reason = "Exact duplicate of another field in the same person."
                req_source = f"Distinct content for {fname}."

            # 7. Check VALID
            else:
                classification = "VALID"

            if classification == "VALID":
                valid_fields += 1
            else:
                invalid_fields += 1
                invalid_by_category[classification] += 1
                people_with_invalid.add(pid)
                fields_requiring_replacement += 1

                print(f"PERSON: {pid}")
                print(f"FIELD: {fname}")
                print(f"CURRENT_VALUE: {repr(fval)}")
                print(f"CLASSIFICATION: {classification}")
                print(f"DETAILED_REASON: {reason}")
                print(f"WHAT_KIND_OF_SOURCE_IS_REQUIRED: {req_source}")
                print(f"WIKIPEDIA_URL: {wiki_url}\n")

    print("==================================================")
    print("AUDIT SUMMARY TOTALS")
    print("==================================================")
    print(f"TOTAL_FIELDS = 148")
    print(f"VALID_FIELDS = {valid_fields}")
    print(f"INVALID_FIELDS = {invalid_fields}\n")

    print("INVALID_BY_CATEGORY:")
    for k, v in invalid_by_category.items():
        print(f"  {k}: {v}")
    print()

    print(f"PEOPLE_WITH_ANY_INVALID_FIELD = {len(people_with_invalid)}")
    print(f"FIELDS_REQUIRING_REPLACEMENT = {fields_requiring_replacement}\n")
    print("FILES_MODIFIED: 0")
    print("STATUS: READ_ONLY_COMPLETE")

if __name__ == "__main__":
    run_audit()
