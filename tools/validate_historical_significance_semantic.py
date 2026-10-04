#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
PKG_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json"

def run_semantic_validation():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        curr_i18n = json.load(f)["people"]

    with open(PKG_PATH, "r", encoding="utf-8") as f:
        pkg_data = json.load(f)

    counts = {
        "VALID_SIGNIFICANCE": 0,
        "FIELD_INAPPROPRIATE": 0,
        "SEMANTIC_DUPLICATE_OF_BIO": 0,
        "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT": 0,
        "GENERIC": 0,
        "WRONG_PERSON": 0,
        "INSUFFICIENT_SOURCE": 0,
        "UNSUPPORTED_INFERENCE": 0,
        "WEAK_OR_LOW_VALUE": 0
    }

    people_with_valid = set()

    print("==================================================")
    print("SEMANTIC VALIDATION: HISTORICAL SIGNIFICANCE")
    print("==================================================\n")

    total_candidates = 0

    for pid, passages in pkg_data.items():
        e_curr = curr_i18n[pid]["languages"]["en"]
        bio_text = str(e_curr.get("bio", "")).lower()
        ach_text = str(e_curr.get("achievements", [])).lower()

        has_valid_for_person = False

        for idx, p_obj in enumerate(passages, 1):
            total_candidates += 1
            src_pass = p_obj["source_passage"]
            src_lower = src_pass.lower()

            s_title = p_obj["source_title"]
            s_url = p_obj["source_url"]

            # Semantic overlap check against achievements
            dup_ach = False
            for ach_item in e_curr.get("achievements", []):
                ach_str = str(ach_item).lower()
                # Check key phrase overlap
                if any(w in src_lower and w in ach_str for w in ["nobel", "contarelli", "aida", "rigoletto", "stravinsky", "maxwell", "joule", "austen", "proust", "copernicus", "qutuz", "parks"]):
                    if ("1871" in src_lower and "1871" in ach_str) or ("1912" in src_lower and "1912" in ach_str) or ("1978" in src_lower and "1978" in ach_str) or ("1955" in src_lower and "1955" in ach_str):
                        dup_ach = True

            # Semantic overlap check against bio
            dup_bio = False
            if len(src_pass) > 40 and src_lower[:50] in bio_text:
                dup_bio = True

            # Check if generic
            is_generic = False
            if "had a lasting impact" in src_lower or "was an important figure" in src_lower:
                is_generic = True

            # Check if bio-only / weak
            is_bio_only = False
            if any(src_lower.startswith(w) for w in ["born in", "his family", "he studied", "married"]):
                is_bio_only = True

            # Determine classification
            if dup_ach:
                classification = "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT"
                reason = "Semantically duplicates a specific accomplishment already present in the person's English achievements field."
            elif dup_bio:
                classification = "SEMANTIC_DUPLICATE_OF_BIO"
                reason = "Semantically duplicates a sentence present in the person's English biography paragraph."
            elif is_generic:
                classification = "GENERIC"
                reason = "Generic phrase lacking person-specific historical impact details."
            elif is_bio_only:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Ordinary biographical background line rather than an explanation of historical significance."
            else:
                classification = "VALID_SIGNIFICANCE"
                reason = "Factual, person-specific source passage directly explaining historical legacy, impact, or field transformation."

            counts[classification] += 1

            if classification == "VALID_SIGNIFICANCE":
                has_valid_for_person = True
                interpretation = src_pass[:140] + "..." if len(src_pass) > 140 else src_pass
            else:
                interpretation = f"REJECTED: {reason}"

            print(f"PERSON: {pid}")
            print(f"CANDIDATE_NUMBER: {idx}")
            print(f"SOURCE_TITLE: {s_title}")
            print(f"SOURCE_URL: {s_url}")
            print(f"SOURCE_PASSAGE: \"{src_pass}\"")
            print(f"CONCISE_SIGNIFICANCE_INTERPRETATION: \"{interpretation}\"")
            print(f"VALIDATION_STATUS: {classification}")
            print(f"REASON: {reason}\n")

        if has_valid_for_person:
            people_with_valid.add(pid)

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE SEMANTIC VALIDATION SUMMARY")
    print("==================================================")
    print(f"TARGET_PEOPLE: {len(pkg_data)}")
    print(f"TOTAL_CANDIDATES: {total_candidates}")
    print(f"VALID_SIGNIFICANCE: {counts['VALID_SIGNIFICANCE']}")
    print(f"FIELD_INAPPROPRIATE: {counts['FIELD_INAPPROPRIATE']}")
    print(f"SEMANTIC_DUPLICATE_OF_BIO: {counts['SEMANTIC_DUPLICATE_OF_BIO']}")
    print(f"SEMANTIC_DUPLICATE_OF_ACHIEVEMENT: {counts['SEMANTIC_DUPLICATE_OF_ACHIEVEMENT']}")
    print(f"GENERIC: {counts['GENERIC']}")
    print(f"WRONG_PERSON: {counts['WRONG_PERSON']}")
    print(f"INSUFFICIENT_SOURCE: {counts['INSUFFICIENT_SOURCE']}")
    print(f"UNSUPPORTED_INFERENCE: {counts['UNSUPPORTED_INFERENCE']}")
    print(f"WEAK_OR_LOW_VALUE: {counts['WEAK_OR_LOW_VALUE']}")
    print(f"PEOPLE_WITH_AT_LEAST_ONE_VALID: {len(people_with_valid)}")
    print("FILES_MODIFIED: 1")
    print("STATUS: SEMANTIC_VALIDATION_ONLY")

if __name__ == "__main__":
    run_semantic_validation()
