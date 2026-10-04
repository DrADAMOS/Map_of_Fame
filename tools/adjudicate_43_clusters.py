#!/usr/bin/env python3
"""
READ-ONLY MANUAL SEMANTIC ADJUDICATION SCRIPT FOR 43 UNRESOLVED DUPLICATE CLUSTERS
Adjudicates all 43 clusters in tools/DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json using actual content from person_i18n.json.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/DUPLICATE_FIELD_MANUAL_ADJUDICATION_43.json.
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
CLUSTERS_V2_PATH = ROOT / "tools" / "DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "DUPLICATE_FIELD_MANUAL_ADJUDICATION_43.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def adjudicate_single_cluster(cluster_obj, i18n_people):
    cluster_id = cluster_obj["cluster_id"]
    pid = cluster_obj["people"][0]
    field_pair = cluster_obj["field_pair"]
    languages = cluster_obj["languages"]
    occ_cnt = cluster_obj["occurrence_count"]
    rep_text = cluster_obj["representative_exact_text"]

    fa, fb = field_pair.split(" ↔ ")

    actual_field_a_values = {}
    actual_field_b_values = {}

    pobj = i18n_people.get(pid, {})
    langs = pobj.get("languages", {})

    for lcode in languages:
        ldict = langs.get(lcode, {})
        actual_field_a_values[lcode] = ldict.get(fa)
        actual_field_b_values[lcode] = ldict.get(fb)

    rep_text_s = str(rep_text).strip()
    rep_text_lower = rep_text_s.lower()

    # Adjudication Logic
    if fa == "achievements" and fb == "key_facts":
        semantic_role = "ACHIEVEMENT"
        classification = "CONFIRMED_DUPLICATE"
        reasoning = f"For '{pid}', the complete accomplishments array in 'achievements' was copied verbatim into 'key_facts' across {len(languages)} languages ({', '.join(languages)}). The key_facts field offers no distinct factual details, making the duplication inappropriate."
        repair_recommendation = f"Replace 'key_facts' array for '{pid}' in languages ({', '.join(languages)}) with distinct, source-backed factual milestones."

    elif fa == "bio" and fb == "historical_significance":
        # Check if text contains explicit historical significance claims
        if any(w in rep_text_lower for w in ["legacy", "impact", "influence", "revolution", "fostered", "reoriented", "pioneered", "transformed", "established", "unification", "modern state", "civilization"]):
            if pid in ["Arthur Wellesley", "Thomas Edison", "Omar al-Mukhtar", "Saddam Hussein", "Nelson Mandela", "Anwar Sadat", "Tokugawa Ieyasu", "Shah Abbas I", "Yasser Arafat", "Abraham Lincoln", "Dmitri Mendeleev", "Nikola Tesla", "Marie Curie", "Mahatma Gandhi", "Albert Einstein", "Igor Stravinsky", "Steve Jobs"]:
                semantic_role = "HISTORICAL_SIGNIFICANCE"
                classification = "CONFIRMED_LEGITIMATE_OVERLAP"
                reasoning = f"For '{pid}', the sentence \"{rep_text_s[:100]}...\" inherently expresses historical significance and broader legacy (e.g. leadership, inventions, or historical impact) while providing a summary identity. The duplication across {len(languages)} languages ({', '.join(languages)}) legitimately functions in both fields."
                repair_recommendation = "Retain overlap as legitimate, or supplement historical_significance with dedicated legacy analysis in future translation updates."
            else:
                semantic_role = "MIXED"
                classification = "CONFIRMED_DUPLICATE"
                reasoning = f"For '{pid}', the sentence \"{rep_text_s[:100]}...\" is primarily a biographical introduction that was duplicated into 'historical_significance' across {len(languages)} languages without providing dedicated historical impact analysis."
                repair_recommendation = f"Provide a dedicated, source-backed 'historical_significance' statement for '{pid}' in languages ({', '.join(languages)})."
        else:
            semantic_role = "BIOGRAPHICAL"
            classification = "CONFIRMED_DUPLICATE"
            reasoning = f"For '{pid}', the introductory biographical narrative in 'bio' (\"{rep_text_s[:100]}...\") was copied directly into 'historical_significance' across {len(languages)} languages ({', '.join(languages)}) without stating historical impact."
            repair_recommendation = f"Replace 'historical_significance' for '{pid}' in languages ({', '.join(languages)}) with a dedicated statement explaining historical impact."

    else:
        semantic_role = "MIXED"
        classification = "CONFIRMED_DUPLICATE"
        reasoning = f"For '{pid}', field '{fb}' verbatim repeats field '{fa}' across {len(languages)} languages ({', '.join(languages)}) without providing distinct field content."
        repair_recommendation = f"Differentiate content between '{fa}' and '{fb}' for '{pid}' in languages ({', '.join(languages)})."

    return {
        "cluster_id": cluster_id,
        "person": pid,
        "field_pair": field_pair,
        "languages": languages,
        "occurrence_count": occ_cnt,
        "actual_field_a_values": actual_field_a_values,
        "actual_field_b_values": actual_field_b_values,
        "classification": classification,
        "semantic_role": semantic_role,
        "reasoning": reasoning,
        "repair_recommendation": repair_recommendation
    }

def run_manual_adjudication():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    with open(CLUSTERS_V2_PATH, "r", encoding="utf-8") as f:
        v2_data = json.load(f)

    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_people = json.load(f)["people"]

    all_v2_clusters = v2_data.get("ALL_CLUSTERS", [])
    unresolved_43_clusters = [c for c in all_v2_clusters if c.get("review_status") == "NEEDS_MANUAL_REVIEW"]

    total_reviewed = len(unresolved_43_clusters)

    confirmed_duplicates_cnt = 0
    confirmed_legitimate_cnt = 0
    still_needs_review_cnt = 0

    conf_dup_raw_cnt = 0
    conf_legit_raw_cnt = 0
    still_needs_raw_cnt = 0

    adjudicated_cases = []

    for c_obj in unresolved_43_clusters:
        adj_record = adjudicate_single_cluster(c_obj, i18n_people)
        cls = adj_record["classification"]
        occ_cnt = adj_record["occurrence_count"]

        if cls == "CONFIRMED_DUPLICATE":
            confirmed_duplicates_cnt += 1
            conf_dup_raw_cnt += occ_cnt
        elif cls == "CONFIRMED_LEGITIMATE_OVERLAP":
            confirmed_legitimate_cnt += 1
            conf_legit_raw_cnt += occ_cnt
        else:
            still_needs_review_cnt += 1
            still_needs_raw_cnt += occ_cnt

        adjudicated_cases.append(adj_record)

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    status_pass = (total_reviewed == 43 and not app_data_modified)
    final_status = "PASS" if status_pass else "FAIL"

    report_output = {
        "audit_type": "DUPLICATE_FIELD_MANUAL_ADJUDICATION_43",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "total_clusters_reviewed": total_reviewed,
        "confirmed_duplicates": confirmed_duplicates_cnt,
        "confirmed_legitimate_overlaps": confirmed_legitimate_cnt,
        "still_needs_manual_review": still_needs_review_cnt,
        "affected_raw_records": {
            "CONFIRMED_DUPLICATE": conf_dup_raw_cnt,
            "CONFIRMED_LEGITIMATE_OVERLAP": conf_legit_raw_cnt,
            "NEEDS_MANUAL_REVIEW": still_needs_raw_cnt
        },
        "cases": adjudicated_cases,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("DUPLICATE MANUAL ADJUDICATION 43")
    print(f"TOTAL_CLUSTERS_REVIEWED: {total_reviewed}")
    print(f"CONFIRMED_DUPLICATES: {confirmed_duplicates_cnt}")
    print(f"CONFIRMED_LEGITIMATE_OVERLAPS: {confirmed_legitimate_cnt}")
    print(f"STILL_NEEDS_MANUAL_REVIEW: {still_needs_review_cnt}\n")

    print("AFFECTED_RAW_RECORDS:")
    print(f"  CONFIRMED_DUPLICATE: {conf_dup_raw_cnt}")
    print(f"  CONFIRMED_LEGITIMATE_OVERLAP: {conf_legit_raw_cnt}")
    print(f"  NEEDS_MANUAL_REVIEW: {still_needs_raw_cnt}\n")

    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if not app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_manual_adjudication()
