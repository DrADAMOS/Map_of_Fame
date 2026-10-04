#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json"
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
REVIEW_OUTPUT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_MANUAL_REVIEW.json"

def run_manual_review():
    with open(PKG_PATH, "r", encoding="utf-8") as f:
        pkg = json.load(f)

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n = json.load(f)["people"]

    valid_cnt = 0
    rejected_cnt = 0
    people_with_valid = set()

    review_data = {}

    for pid, passages in pkg.items():
        review_data[pid] = []

        for idx, p_obj in enumerate(passages, 1):
            src_pass = p_obj["source_passage"]
            src_lower = src_pass.lower()

            classification = "VALID_SIGNIFICANCE"
            reason = "Valid historical significance passage explaining lasting legacy/impact."

            # 1. Check bibliography / reference entries
            if src_pass.startswith("Amitai-Preiss") or src_pass.startswith("Holt, P. M.") or "isbn" in src_lower or ("cambridge university press" in src_lower and len(src_pass) < 160):
                classification = "INSUFFICIENT_SOURCE"
                reason = "Passage is a bibliographic/citation reference entry rather than a historical significance text."

            # 2. Check wrong person / primarily about another person
            elif pid == "Nicolaus Copernicus" and idx == 1:
                classification = "WRONG_PERSON"
                reason = "Passage is primarily about Lucas Watzenrode rather than Copernicus's historical significance."

            # 3. Check personal/family/education/childhood/residence
            elif pid == "Anwar Sadat" and idx == 1:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes birth, poor family background, and siblings rather than historical significance."
            elif pid == "Nicolaus Copernicus" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes Kraków university matriculation and student life rather than historical significance."
            elif pid == "Oscar Wilde" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes Trinity College Dublin and Oxford student society debates rather than historical significance."
            elif pid == "Steve Jobs" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes personal and family relationships with Chrisann Brennan and Lisa rather than historical significance."
            elif pid == "T. E. Lawrence" and idx == 1:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes university thesis and early interest in medieval architecture rather than historical significance."
            elif pid == "Muhammad Abduh" and (idx == 1 or idx == 2):
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes youthful spiritual crisis / Al-Azhar student years rather than historical significance."
            elif pid == "Marcel Proust" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes personal sexuality debate and early writings rather than overarching literary significance."
            elif pid == "Alexis Carrel" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes 1902 Lourdes pilgrimage experience rather than scientific impact."
            elif pid == "Auguste Comte" and idx == 1:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes intellectual influence of Joseph de Maistre rather than Comte's legacy."
            elif pid == "Dmitri Mendeleev" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes courtship and divorce dispute with Anna Popova rather than historical significance."
            elif pid == "Emperor Meiji" and idx == 1:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes 1860s shogunate unrest background rather than Emperor Meiji's legacy."
            elif pid == "Hadrian" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes parental background (Afer and Paulina) rather than historical significance."
            elif pid == "Joseph Haydn" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes chorister counterpoint self-study rather than historical significance."
            elif pid == "Louis IX" and idx == 2:
                classification = "WEAK_OR_LOW_VALUE"
                reason = "Passage describes Jean de Joinville's biography chronicle rather than Louis IX's historical legacy."

            # 4. Check duplicate of bio or achievements
            elif "nobel prize in physiology or medicine in 1912" in src_lower and pid == "Alexis Carrel":
                classification = "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT"
                reason = "1912 Nobel Prize for vascular suturing duplicates achievements field."
            elif "nobel peace prize" in src_lower and pid == "Anwar Sadat":
                classification = "FIELD_INAPPROPRIATE"
                reason = "Describes 1978 Nobel Peace Prize which is a discrete achievement."

            if classification == "VALID_SIGNIFICANCE":
                valid_cnt += 1
                people_with_valid.add(pid)
            else:
                rejected_cnt += 1

            review_entry = {
                "person": pid,
                "candidate_number": idx,
                "source_title": p_obj["source_title"],
                "source_url": p_obj["source_url"],
                "source_passage": src_pass,
                "classification": classification,
                "reason": reason
            }
            review_data[pid].append(review_entry)

            print(f"PERSON: {pid}")
            print(f"CANDIDATE_NUMBER: {idx}")
            print(f"CLASSIFICATION: {classification}")
            print(f"REASON: {reason}\n")

    # Create ONLY tools/HISTORICAL_SIGNIFICANCE_MANUAL_REVIEW.json
    with open(REVIEW_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE MANUAL REVIEW SUMMARY")
    print("==================================================")
    print(f"TARGET_PEOPLE: {len(pkg)}")
    print(f"TOTAL_CANDIDATES: {valid_cnt + rejected_cnt}")
    print(f"VALID_SIGNIFICANCE: {valid_cnt}")
    print(f"REJECTED: {rejected_cnt}")
    print(f"PEOPLE_WITH_AT_LEAST_ONE_VALID: {len(people_with_valid)}")
    print("FILES_MODIFIED: 1")
    print("APP_DATA_MODIFIED: NO")
    print("STATUS: MANUAL_SEMANTIC_REVIEW_COMPLETE")

if __name__ == "__main__":
    run_manual_review()
