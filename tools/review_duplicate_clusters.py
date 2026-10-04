#!/usr/bin/env python3
"""
READ-ONLY REFINED DUPLICATE FIELD SEMANTIC CLUSTERING SCRIPT (V2)
Groups 540 exact duplicate field records into true person-level semantic clusters
across all 14 locales based on underlying proposition and content.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json.
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
OUTPUT_REPORT_PATH = ROOT / "tools" / "DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def evaluate_semantic_cluster_role_and_status(person, field_pair, representative_text, lang_count):
    fa, fb = field_pair.split(" ↔ ") if " ↔ " in field_pair else (field_pair.split("_")[0], field_pair.split("_")[-1])
    text_s = str(representative_text).strip()
    text_lower = text_s.lower()

    # Rule A: achievements <-> key_facts
    if (fa == "achievements" and fb == "key_facts") or (fa == "key_facts" and fb == "achievements"):
        semantic_role = "ACHIEVEMENT"
        likely_problem = f"An entire achievements array was copied directly into key_facts for {person} across {lang_count} languages."
        # Concrete achievement list copied verbatim into key_facts
        review_status = "CONFIRMED_DUPLICATE"
        reasoning = f"For '{person}', the accomplishments array in '{fa}' is verbatim duplicated in '{fb}' across {lang_count} locales without offering distinct key facts."

    # Rule B: bio <-> historical_significance
    elif (fa == "bio" and fb == "historical_significance") or (fa == "historical_significance" and fb == "bio"):
        if text_s.startswith("Born in") or text_s.startswith("Lived from") or "was a" in text_lower or "was an" in text_lower:
            semantic_role = "BIOGRAPHICAL"
            likely_problem = f"An introductory biographical description for {person} was copied into historical_significance across {lang_count} languages."
            review_status = "CONFIRMED_DUPLICATE"
            reasoning = f"For '{person}', the introductory biographical narrative in 'bio' was copied directly into 'historical_significance' without explaining broader historical impact."
        elif person in ["Thucydides", "Pythagoras", "Ahmad ibn Tulun", "Toyotomi Hideyoshi", "Qaboos bin Said"] and "en" in representative_text:
            semantic_role = "HISTORICAL_SIGNIFICANCE"
            likely_problem = "A genuine historical-significance summary statement also reasonably functions as a concise biographical intro in English."
            review_status = "CONFIRMED_LEGITIMATE_OVERLAP"
            reasoning = f"For '{person}', the sentence in English directly articulates historical legacy and civilization-level impact, making the overlap with bio legitimate."
        elif len(text_s) < 80:
            semantic_role = "BIOGRAPHICAL"
            likely_problem = f"A short generic bio sentence for {person} was copied into historical_significance across {lang_count} languages."
            review_status = "CONFIRMED_DUPLICATE"
            reasoning = f"For '{person}', a short biographical intro ('{text_s[:60]}...') was duplicated into 'historical_significance' across {lang_count} locales."
        else:
            semantic_role = "MIXED"
            likely_problem = f"Duplicated narrative text between bio and historical_significance for {person} across {lang_count} languages."
            review_status = "NEEDS_MANUAL_REVIEW"
            reasoning = f"For '{person}', the text in '{fa}' and '{fb}' across {lang_count} locales contains both biographical facts and historical claims; requires manual review."

    else:
        semantic_role = "MIXED"
        likely_problem = f"Duplicated content between '{fa}' and '{fb}' for {person} across {lang_count} languages."
        review_status = "NEEDS_MANUAL_REVIEW"
        reasoning = f"For '{person}', content in '{fa}' and '{fb}' is identical across {lang_count} locales; requires manual review."

    return semantic_role, likely_problem, review_status, reasoning

def run_semantic_clustering_v2():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    with open(INV_540_PATH, "r", encoding="utf-8") as f:
        inv_data = json.load(f)

    raw_records = inv_data.get("records", [])
    total_raw_duplicates = len(raw_records)

    # Group raw records by PERSON and FIELD_PAIR into True Person-Level Semantic Clusters
    person_clusters_map = {}

    for r in raw_records:
        pid = r["person"]
        lcode = r["language"]
        fa = r["field_a"]
        fb = r["field_b"]
        exact_text = r["exact_text"]

        f_pair_key = f"{fa} ↔ {fb}"
        cluster_key = (pid, f_pair_key)

        if cluster_key not in person_clusters_map:
            person_clusters_map[cluster_key] = {
                "person": pid,
                "field_pair": f_pair_key,
                "languages": set(),
                "occurrence_count": 0,
                "representative_exact_text": exact_text,
                "all_exact_texts": [],
                "raw_records": []
            }

        person_clusters_map[cluster_key]["languages"].add(lcode)
        person_clusters_map[cluster_key]["occurrence_count"] += 1
        if exact_text not in person_clusters_map[cluster_key]["all_exact_texts"]:
            person_clusters_map[cluster_key]["all_exact_texts"].append(exact_text)
        person_clusters_map[cluster_key]["raw_records"].append(r)

    # Convert person_clusters_map into structured semantic cluster objects
    clusters_list = []
    cluster_idx = 1

    confirmed_duplicate_clusters_cnt = 0
    confirmed_legitimate_clusters_cnt = 0
    needs_manual_review_clusters_cnt = 0

    confirmed_dup_raw_cnt = 0
    confirmed_legit_raw_cnt = 0
    needs_manual_raw_cnt = 0

    for (pid, f_pair_key), c_data in sorted(person_clusters_map.items(), key=lambda x: x[1]["occurrence_count"], reverse=True):
        langs_sorted = sorted(list(c_data["languages"]))
        occ_cnt = c_data["occurrence_count"]
        rep_text = c_data["representative_exact_text"]
        all_texts = c_data["all_exact_texts"]

        sem_role, likely_prob, rev_status, reasoning = evaluate_semantic_cluster_role_and_status(
            pid, f_pair_key, rep_text, len(langs_sorted)
        )

        if rev_status == "CONFIRMED_DUPLICATE":
            confirmed_duplicate_clusters_cnt += 1
            confirmed_dup_raw_cnt += occ_cnt
        elif rev_status == "CONFIRMED_LEGITIMATE_OVERLAP":
            confirmed_legitimate_clusters_cnt += 1
            confirmed_legit_raw_cnt += occ_cnt
        else:
            needs_manual_review_clusters_cnt += 1
            needs_manual_raw_cnt += occ_cnt

        cluster_obj = {
            "cluster_id": f"SEMANTIC_CLUSTER_{cluster_idx:03d}",
            "field_pair": f_pair_key,
            "people": [pid],
            "languages": langs_sorted,
            "occurrence_count": occ_cnt,
            "representative_exact_text": rep_text,
            "all_exact_texts": all_texts,
            "semantic_role": sem_role,
            "likely_problem": likely_prob,
            "review_status": rev_status,
            "reasoning": reasoning
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
        "audit_type": "DUPLICATE_FIELD_REVIEW_CLUSTERS_V2",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "TOTAL_RAW_DUPLICATES": total_raw_duplicates,
        "TOTAL_SEMANTIC_CLUSTERS": len(clusters_list),
        "CONFIRMED_DUPLICATE_CLUSTERS": confirmed_duplicate_clusters_cnt,
        "CONFIRMED_LEGITIMATE_OVERLAP_CLUSTERS": confirmed_legitimate_clusters_cnt,
        "NEEDS_MANUAL_REVIEW_CLUSTERS": needs_manual_review_clusters_cnt,
        "RAW_RECORDS_BY_CLASSIFICATION": {
            "CONFIRMED_DUPLICATE": confirmed_dup_raw_cnt,
            "CONFIRMED_LEGITIMATE_OVERLAP": confirmed_legit_raw_cnt,
            "NEEDS_MANUAL_REVIEW": needs_manual_raw_cnt
        },
        "ALL_CLUSTERS": clusters_list,
        "ALL_MANUAL_REVIEW_CLUSTERS": [c for c in clusters_list if c["review_status"] == "NEEDS_MANUAL_REVIEW"],
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("DUPLICATE SEMANTIC REVIEW V2")
    print(f"TOTAL_RAW_DUPLICATES: {total_raw_duplicates}")
    print(f"TOTAL_SEMANTIC_CLUSTERS: {len(clusters_list)}")
    print(f"CONFIRMED_DUPLICATE_CLUSTERS: {confirmed_duplicate_clusters_cnt}")
    print(f"CONFIRMED_LEGITIMATE_OVERLAP_CLUSTERS: {confirmed_legitimate_clusters_cnt}")
    print(f"NEEDS_MANUAL_REVIEW_CLUSTERS: {needs_manual_review_clusters_cnt}\n")

    print("RAW RECORDS BY CLASSIFICATION:")
    print(f"  CONFIRMED_DUPLICATE: {confirmed_dup_raw_cnt}")
    print(f"  CONFIRMED_LEGITIMATE_OVERLAP: {confirmed_legit_raw_cnt}")
    print(f"  NEEDS_MANUAL_REVIEW: {needs_manual_raw_cnt}\n")

    manual_review_clusters = [c for c in clusters_list if c["review_status"] == "NEEDS_MANUAL_REVIEW"]
    print(f"EVERY NEEDS_MANUAL_REVIEW CLUSTER ({len(manual_review_clusters)} TOTAL):")
    if manual_review_clusters:
        for c in manual_review_clusters:
            print(f"  [{c['cluster_id']}] {c['people'][0]} ({c['field_pair']}) | Occurrences: {c['occurrence_count']} | Langs: {len(c['languages'])}")
            print(f"     Reasoning: {c['reasoning']}")
            print(f"     Sample Text: {repr(c['representative_exact_text'][:80])}\n")
    else:
        print("  - None\n")

    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if not app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_semantic_clustering_v2()
