#!/usr/bin/env python3
"""
READ-ONLY DUPLICATE FIELD CLUSTERING SCRIPT
Groups 540 exact duplicate field records into semantic clusters based on actual text/meaning.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/DUPLICATE_FIELD_REVIEW_CLUSTERS.json.
"""

import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
INV_540_PATH = ROOT / "tools" / "DUPLICATE_FIELD_INVESTIGATION_540.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "DUPLICATE_FIELD_REVIEW_CLUSTERS.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def evaluate_cluster_semantic_role_and_status(field_pair, text, lang_list, people_list):
    fa, fb = field_pair.split(" ↔ ") if " ↔ " in field_pair else (field_pair.split("_")[0], field_pair.split("_")[-1])
    text_s = str(text).strip()
    text_lower = text_s.lower()

    # Determine Semantic Role
    if fa == "achievements" and fb == "key_facts":
        semantic_role = "ACHIEVEMENT"
        likely_problem = "Concrete achievement list stored verbatim in key_facts field."
        # If verbatim array duplication across multiple locales
        if len(lang_list) > 1 or len(people_list) > 1:
            review_status = "CONFIRMED_DUPLICATE"
        else:
            review_status = "NEEDS_MANUAL_REVIEW"

    elif fa == "bio" and fb == "historical_significance":
        # Check if text is a simple biographical introduction vs historical impact statement
        if text_s.startswith("Born in") or text_s.startswith("Lived from") or "was a" in text_lower or "was an" in text_lower or "is a" in text_lower or "is an" in text_lower:
            semantic_role = "BIOGRAPHICAL"
            likely_problem = "Introductory biography sentence copied into historical_significance without expressing historical impact."
            review_status = "CONFIRMED_DUPLICATE"
        elif any(w in text_lower for w in ["established", "unified", "legacy", "impact", "pioneered", "transformed", "founded"]):
            semantic_role = "HISTORICAL_SIGNIFICANCE"
            likely_problem = "Single summary sentence expressing both identity and historical significance."
            if "en" in lang_list and len(people_list) == 1:
                review_status = "CONFIRMED_LEGITIMATE_OVERLAP"
            else:
                review_status = "CONFIRMED_DUPLICATE" if len(lang_list) > 1 else "NEEDS_MANUAL_REVIEW"
        else:
            semantic_role = "MIXED"
            likely_problem = "Ambiguous overlap between biographical context and historical significance."
            review_status = "NEEDS_MANUAL_REVIEW"

    else:
        semantic_role = "MIXED"
        likely_problem = "Verbatim duplication between fields."
        review_status = "CONFIRMED_DUPLICATE" if len(lang_list) > 1 else "NEEDS_MANUAL_REVIEW"

    return semantic_role, likely_problem, review_status

def run_clustering():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    with open(INV_540_PATH, "r", encoding="utf-8") as f:
        inv_data = json.load(f)

    raw_records = inv_data.get("records", [])
    total_raw_duplicates = len(raw_records)

    # Group records into clusters based on normalized text and field_pair
    clusters_dict = {}

    for r in raw_records:
        pid = r["person"]
        lcode = r["language"]
        fa = r["field_a"]
        fb = r["field_b"]
        exact_text = r["exact_text"]

        f_pair_key = f"{fa} ↔ {fb}"
        norm_text_key = exact_text.strip()

        cluster_key = (f_pair_key, norm_text_key)

        if cluster_key not in clusters_dict:
            clusters_dict[cluster_key] = {
                "field_pair": f_pair_key,
                "people": set(),
                "languages": set(),
                "occurrence_count": 0,
                "representative_exact_text": exact_text,
                "raw_records": []
            }

        clusters_dict[cluster_key]["people"].add(pid)
        clusters_dict[cluster_key]["languages"].add(lcode)
        clusters_dict[cluster_key]["occurrence_count"] += 1
        clusters_dict[cluster_key]["raw_records"].append(r)

    # Convert clusters_dict into structured cluster objects
    clusters_list = []
    cluster_idx = 1

    confirmed_duplicate_clusters_cnt = 0
    confirmed_legitimate_clusters_cnt = 0
    needs_manual_review_clusters_cnt = 0

    confirmed_duplicate_raw_records_cnt = 0
    confirmed_legitimate_raw_records_cnt = 0
    needs_manual_review_raw_records_cnt = 0

    for (f_pair_key, norm_text), c_data in sorted(clusters_dict.items(), key=lambda x: x[1]["occurrence_count"], reverse=True):
        people_sorted = sorted(list(c_data["people"]))
        langs_sorted = sorted(list(c_data["languages"]))
        occ_cnt = c_data["occurrence_count"]
        rep_text = c_data["representative_exact_text"]

        sem_role, likely_prob, rev_status = evaluate_cluster_semantic_role_and_status(f_pair_key, rep_text, langs_sorted, people_sorted)

        if rev_status == "CONFIRMED_DUPLICATE":
            confirmed_duplicate_clusters_cnt += 1
            confirmed_duplicate_raw_records_cnt += occ_cnt
        elif rev_status == "CONFIRMED_LEGITIMATE_OVERLAP":
            confirmed_legitimate_clusters_cnt += 1
            confirmed_legitimate_raw_records_cnt += occ_cnt
        else:
            needs_manual_review_clusters_cnt += 1
            needs_manual_review_raw_records_cnt += occ_cnt

        cluster_obj = {
            "cluster_id": f"CLUSTER_{cluster_idx:03d}",
            "field_pair": f_pair_key,
            "people": people_sorted,
            "languages": langs_sorted,
            "occurrence_count": occ_cnt,
            "representative_exact_text": rep_text,
            "semantic_role": sem_role,
            "likely_problem": likely_prob,
            "review_status": rev_status
        }
        clusters_list.append(cluster_obj)
        cluster_idx += 1

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    report_output = {
        "audit_type": "DUPLICATE_FIELD_REVIEW_CLUSTERS",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "total_raw_duplicates": total_raw_duplicates,
        "total_clusters": len(clusters_list),
        "confirmed_duplicate_clusters_count": confirmed_duplicate_clusters_cnt,
        "confirmed_legitimate_clusters_count": confirmed_legitimate_clusters_cnt,
        "needs_manual_review_clusters_count": needs_manual_review_clusters_cnt,
        "raw_records_by_classification": {
            "CONFIRMED_DUPLICATE": confirmed_duplicate_raw_records_cnt,
            "CONFIRMED_LEGITIMATE_OVERLAP": confirmed_legitimate_raw_records_cnt,
            "NEEDS_MANUAL_REVIEW": needs_manual_review_raw_records_cnt
        },
        "clusters": clusters_list,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("DUPLICATE CLUSTER REVIEW")
    print(f"TOTAL_RAW_DUPLICATES: {total_raw_duplicates}")
    print(f"TOTAL_CLUSTERS: {len(clusters_list)}")
    print(f"CONFIRMED_DUPLICATE_CLUSTERS: {confirmed_duplicate_clusters_cnt}")
    print(f"CONFIRMED_LEGITIMATE_CLUSTERS: {confirmed_legitimate_clusters_cnt}")
    print(f"NEEDS_MANUAL_REVIEW_CLUSTERS: {needs_manual_review_clusters_cnt}")
    print("\nRAW RECORDS BY CLASSIFICATION:")
    print(f"  CONFIRMED_DUPLICATE: {confirmed_duplicate_raw_records_cnt} raw records")
    print(f"  CONFIRMED_LEGITIMATE_OVERLAP: {confirmed_legitimate_raw_records_cnt} raw records")
    print(f"  NEEDS_MANUAL_REVIEW: {needs_manual_review_raw_records_cnt} raw records")

    print("\nTOP 20 LARGEST CLUSTERS:")
    for c in clusters_list[:20]:
        print(f"  [{c['cluster_id']}] ({c['occurrence_count']} occurrences) {c['field_pair']} | People: {c['people'][:2]} | Status: {c['review_status']}")
        print(f"     Text: {repr(c['representative_exact_text'][:80])}")

    manual_review_clusters = [c for c in clusters_list if c["review_status"] == "NEEDS_MANUAL_REVIEW"]
    print(f"\nEVERY NEEDS_MANUAL_REVIEW CLUSTER ({len(manual_review_clusters)} TOTAL):")
    if manual_review_clusters:
        for c in manual_review_clusters:
            print(f"  [{c['cluster_id']}] {c['field_pair']} | People: {c['people']} | Langs: {c['languages']}")
            print(f"     Text: {repr(c['representative_exact_text'][:80])}")
    else:
        print("  - None")

    print(f"\nAPPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_clustering()
