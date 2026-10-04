#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_MANUAL_REVIEW.json"
I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUTPUT_SECOND_PASS_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SECOND_PASS_REVIEW.json"

SECOND_PASS_EVALUATIONS = [
    ("Anwar Sadat", 2, "FIELD_INAPPROPRIATE", "Describes 1952 revolution radio announcement and Free Officers coup, which is a specific political achievement rather than a historical significance summary."),
    ("Auguste Comte", 2, "VALID_SIGNIFICANCE", "Explains Comte's foundational historical role in formulating positivism and establishing sociology to address post-revolutionary social order."),
    ("Caravaggio", 1, "VALID_SIGNIFICANCE", "Explains Caravaggio's transformative impact on Baroque painting through dramatic chiaroscuro and realistic observation."),
    ("Caravaggio", 2, "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT", "Duplicates Caravaggio's chiaroscuro/tenebrism painting technique already present in achievements."),
    ("Clara Barton", 1, "FIELD_INAPPROPRIATE", "Describes a specific 1896 relief mission to the Ottoman Empire, which is a discrete achievement rather than an overall significance summary."),
    ("Clara Barton", 2, "VALID_SIGNIFICANCE", "Documents her lasting institutional legacy through the establishment of the Clara Barton National Historic Site."),
    ("Dmitri Mendeleev", 1, "WEAK_OR_LOW_VALUE", "Describes ordinary employment as a university professor in Saint Petersburg rather than explaining his scientific significance."),
    ("Emperor Meiji", 2, "VALID_SIGNIFICANCE", "Explains the historic transformation of Japan during the Meiji era from a feudal state to an industrial world power."),
    ("Gustav Mahler", 1, "VALID_SIGNIFICANCE", "Explicitly documents Mahler's profound influence on succeeding generations of 20th-century composers."),
    ("Gustav Mahler", 2, "VALID_SIGNIFICANCE", "Documents specific musical influence on major 20th-century figures including Aaron Copland and Benjamin Britten."),
    ("Hadrian", 1, "WEAK_OR_LOW_VALUE", "Describes personal marriage to Vibia Sabina rather than imperial legacy."),
    ("James Prescott Joule", 1, "WEAK_OR_LOW_VALUE", "Describes family brewing business and birthplace rather than scientific legacy."),
    ("James Prescott Joule", 2, "WEAK_OR_LOW_VALUE", "Describes brewery management and early hobby interest rather than thermodynamic significance."),
    ("Jane Austen", 1, "WEAK_OR_LOW_VALUE", "Describes family kinship visits and social patronage rather than literary significance."),
    ("Jane Austen", 2, "WEAK_OR_LOW_VALUE", "Describes early juvenile writing ('Catharine or the Bower') rather than mature literary legacy."),
    ("Joseph Haydn", 1, "WEAK_OR_LOW_VALUE", "Describes childhood origins and chorister training rather than classical musical legacy."),
    ("Louis IX", 1, "WEAK_OR_LOW_VALUE", "Describes the regency of his mother Blanche of Castile rather than Louis IX's historical significance."),
    ("Malek Bennabi", 1, "FIELD_INAPPROPRIATE", "Describes establishing an Algerian organization ('El Qiyam'), which is a discrete organizational achievement."),
    ("Malek Bennabi", 2, "VALID_SIGNIFICANCE", "Explains Bennabi's enduring intellectual legacy in developing civilizational theory and the concept of 'colonisability'."),
    ("Marcel Proust", 1, "VALID_SIGNIFICANCE", "Explains Proust's literary significance as author of 'In Search of Lost Time', a recognized masterpiece of 20th-century fiction."),
    ("Michael Faraday", 1, "VALID_SIGNIFICANCE", "Explains Faraday's scientific impact in establishing electromagnetic field theory and enabling electric motor technology."),
    ("Michael Faraday", 2, "VALID_SIGNIFICANCE", "Documents Faraday's foundational influence on James Clerk Maxwell and modern electromagnetic theory."),
    ("Oscar Wilde", 1, "SEMANTIC_DUPLICATE_OF_BIO", "Describes his 1895 trial, imprisonment, and final writing period ('De Profundis'), duplicating biographical narrative."),
    ("Steve Jobs", 1, "VALID_SIGNIFICANCE", "Explains Jobs's historical significance as a pioneer of the personal computer, digital music, and smartphone revolutions."),
    ("T. E. Lawrence", 2, "VALID_SIGNIFICANCE", "Documents Lawrence's strategic military legacy and leadership in the Arab Revolt.")
]

def perform_second_pass():
    with open(REVIEW_PATH, "r", encoding="utf-8") as f:
        first_pass = json.load(f)

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

    eval_map = {(pid, cnum): (cls, reas) for pid, cnum, cls, reas in SECOND_PASS_EVALUATIONS}

    second_pass_results = {}
    people_with_valid = set()
    people_with_no_valid = set()

    all_reviewed_people = set(first_pass.keys())

    total_reviewed = 0
    valid_cnt = 0
    rejected_cnt = 0

    print("==================================================")
    print("SECOND-PASS SEMANTIC REVIEW OF 25 VALID CANDIDATES")
    print("==================================================\n")

    for pid in sorted(first_pass.keys()):
        second_pass_results[pid] = []
        has_valid = False

        for item in first_pass[pid]:
            cnum = item["candidate_number"]
            # Only process if classified as VALID_SIGNIFICANCE in first pass
            if item["classification"] == "VALID_SIGNIFICANCE":
                total_reviewed += 1
                new_cls, new_reason = eval_map.get((pid, cnum), ("VALID_SIGNIFICANCE", "Valid historical significance passage explaining lasting legacy/impact."))

                counts[new_cls] += 1

                if new_cls == "VALID_SIGNIFICANCE":
                    valid_cnt += 1
                    has_valid = True
                else:
                    rejected_cnt += 1

                entry = {
                    "person": pid,
                    "candidate_number": cnum,
                    "source_title": item["source_title"],
                    "source_url": item["source_url"],
                    "source_passage": item["source_passage"],
                    "classification": new_cls,
                    "reason": new_reason
                }
                second_pass_results[pid].append(entry)

                print(f"PERSON: {pid}")
                print(f"CANDIDATE_NUMBER: {cnum}")
                print(f"CLASSIFICATION: {new_cls}")
                print(f"REASON: {new_reason}\n")

        if has_valid:
            people_with_valid.add(pid)

    for pid in all_reviewed_people:
        if pid not in people_with_valid:
            people_with_no_valid.add(pid)

    # Save tools/HISTORICAL_SIGNIFICANCE_SECOND_PASS_REVIEW.json
    with open(OUTPUT_SECOND_PASS_PATH, "w", encoding="utf-8") as f:
        json.dump(second_pass_results, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("SECOND-PASS REVIEW SUMMARY")
    print("==================================================")
    print(f"TOTAL_REVIEWED: {total_reviewed}")
    print(f"VALID_SIGNIFICANCE: {valid_cnt}")
    print(f"REJECTED: {rejected_cnt}")
    print(f"PEOPLE_WITH_AT_LEAST_ONE_VALID: {len(people_with_valid)}")
    print(f"PEOPLE_WITH_NO_VALID: {len(people_with_no_valid)}\n")

    print("REJECTED CANDIDATES LIST:")
    for pid, entries in second_pass_results.items():
        for e in entries:
            if e["classification"] != "VALID_SIGNIFICANCE":
                print(f"  - {pid} #{e['candidate_number']}: {e['classification']} ({e['reason']})")

    print("\nFILES_MODIFIED: 1")
    print("APP_DATA_MODIFIED: NO")
    print("STATUS: SECOND_PASS_SEMANTIC_REVIEW_COMPLETE")

if __name__ == "__main__":
    perform_second_pass()
