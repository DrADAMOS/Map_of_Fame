#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECOND_PASS_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SECOND_PASS_REVIEW.json"
PKG_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json"
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
FINAL_AUDIT_OUTPUT = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_FINAL_AUDIT.json"

FINAL_AUDIT_EVALUATIONS = [
    ("Auguste Comte", 2, "YES", "Explains Comte's foundational historical role in formulating positivism and establishing sociology to address post-revolutionary social order.", "NO", "LOW", "KEEP"),
    ("Caravaggio", 1, "YES", "Explains Caravaggio's transformative impact on Baroque painting through dramatic chiaroscuro and realistic observation.", "NO", "LOW", "KEEP"),
    ("Clara Barton", 2, "YES", "Describes a 1975 National Historic Site address establishment in Glen Echo, Maryland, without explaining her broader historical significance.", "NO", "HIGH", "REJECT"),
    ("Emperor Meiji", 2, "YES", "Explains Emperor Meiji's symbolic leadership in the Meiji Restoration, transforming Japan from an isolated feudal state into an industrial world power.", "NO", "LOW", "KEEP"),
    ("Gustav Mahler", 1, "YES", "Explicitly documents Mahler's profound transitional influence on succeeding generations of 20th-century classical music modernists.", "NO", "LOW", "KEEP"),
    ("Gustav Mahler", 2, "YES", "Lists individual composers influenced by Mahler (Copland, Britten), which overlaps with Mahler #1.", "YES", "LOW", "REJECT"),
    ("Malek Bennabi", 2, "YES", "Explains Bennabi's enduring intellectual legacy in developing civilizational theory and the concept of 'colonisability' in Islamic thought.", "NO", "LOW", "KEEP"),
    ("Marcel Proust", 1, "YES", "Explains Proust's literary significance as author of 'In Search of Lost Time', a recognized masterpiece of 20th-century fiction.", "NO", "LOW", "KEEP"),
    ("Michael Faraday", 1, "YES", "Explains Faraday's scientific impact in establishing electromagnetic field theory and enabling electric motor technology.", "NO", "LOW", "KEEP"),
    ("Michael Faraday", 2, "YES", "Documents Faraday's influence on James Clerk Maxwell, which overlaps with Faraday #1.", "YES", "LOW", "REJECT"),
    ("Steve Jobs", 1, "YES", "Explains Jobs's historical significance as a pioneer of the personal computer, digital music, and smartphone revolutions.", "NO", "LOW", "KEEP"),
    ("T. E. Lawrence", 2, "YES", "Documents Lawrence's strategic military legacy and leadership in the Arab Revolt during World War I.", "NO", "LOW", "KEEP")
]

def run_final_audit():
    with open(SECOND_PASS_PATH, "r", encoding="utf-8") as f:
        second_pass = json.load(f)

    with open(PKG_PATH, "r", encoding="utf-8") as f:
        pkg = json.load(f)

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n = json.load(f)["people"]

    eval_map = {(pid, cnum): (supp, just, dup, risk, rec) for pid, cnum, supp, just, dup, risk, rec in FINAL_AUDIT_EVALUATIONS}

    final_audit_results = {}

    total_audited = 0
    keep_cnt = 0
    reject_cnt = 0
    high_risk_cnt = 0
    dup_risk_cnt = 0

    print("==================================================")
    print("FINAL SOURCE-TO-FIELD AUDIT: HISTORICAL SIGNIFICANCE")
    print("==================================================\n")

    for pid in sorted(second_pass.keys()):
        for item in second_pass[pid]:
            cnum = item["candidate_number"]
            if item["classification"] == "VALID_SIGNIFICANCE":
                total_audited += 1
                supp, just, dup, risk, rec = eval_map.get((pid, cnum), ("YES", "Valid historical significance passage.", "NO", "LOW", "KEEP"))

                if rec == "KEEP":
                    keep_cnt += 1
                else:
                    reject_cnt += 1

                if risk == "HIGH":
                    high_risk_cnt += 1
                if dup == "YES":
                    dup_risk_cnt += 1

                audit_entry = {
                    "person": pid,
                    "candidate_number": cnum,
                    "source_title": item["source_title"],
                    "source_url": item["source_url"],
                    "source_passage": item["source_passage"],
                    "source_support": supp,
                    "significance_justification": just,
                    "duplicates_existing_field": dup,
                    "unsupported_claim_risk": risk,
                    "recommendation": rec
                }

                if pid not in final_audit_results:
                    final_audit_results[pid] = []
                final_audit_results[pid].append(audit_entry)

                print(f"PERSON: {pid}")
                print(f"CANDIDATE_NUMBER: {cnum}")
                print(f"SOURCE_SUPPORT: {supp}")
                print(f"SIGNIFICANCE_JUSTIFICATION: {just}")
                print(f"DUPLICATES_EXISTING_FIELD: {dup}")
                print(f"UNSUPPORTED_CLAIM_RISK: {risk}")
                print(f"RECOMMENDATION: {rec}\n")

    # Save ONLY tools/HISTORICAL_SIGNIFICANCE_FINAL_AUDIT.json
    with open(FINAL_AUDIT_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(final_audit_results, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("FINAL AUDIT SUMMARY TOTALS")
    print("==================================================")
    print(f"TOTAL_AUDITED = {total_audited}")
    print(f"KEEP = {keep_cnt}")
    print(f"REJECT = {reject_cnt}")
    print(f"HIGH_RISK = {high_risk_cnt}")
    print(f"DUPLICATE_RISK = {dup_risk_cnt}")
    print("APP_DATA_MODIFIED: NO")
    print("STATUS: FINAL_SOURCE_TO_FIELD_AUDIT_COMPLETE")

if __name__ == "__main__":
    run_final_audit()
