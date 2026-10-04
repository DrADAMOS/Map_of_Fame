#!/usr/bin/env python3
"""
READ-ONLY FINAL HUMAN ADJUDICATION DECISION RECORDING SCRIPT
Records the human decision (CONFIRMED_DUPLICATE for all 43 clusters) into tools/DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
HUMAN_REVIEW_43_PATH = ROOT / "tools" / "DUPLICATE_FIELD_HUMAN_REVIEW_43.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

HUMAN_43_CLUSTER_IDS = [
    "SEMANTIC_CLUSTER_010", "SEMANTIC_CLUSTER_018", "SEMANTIC_CLUSTER_020",
    "SEMANTIC_CLUSTER_025", "SEMANTIC_CLUSTER_030", "SEMANTIC_CLUSTER_033",
    "SEMANTIC_CLUSTER_042", "SEMANTIC_CLUSTER_052", "SEMANTIC_CLUSTER_053",
    "SEMANTIC_CLUSTER_056", "SEMANTIC_CLUSTER_061", "SEMANTIC_CLUSTER_063",
    "SEMANTIC_CLUSTER_066", "SEMANTIC_CLUSTER_067", "SEMANTIC_CLUSTER_068",
    "SEMANTIC_CLUSTER_070", "SEMANTIC_CLUSTER_071", "SEMANTIC_CLUSTER_072",
    "SEMANTIC_CLUSTER_073", "SEMANTIC_CLUSTER_074", "SEMANTIC_CLUSTER_079",
    "SEMANTIC_CLUSTER_080", "SEMANTIC_CLUSTER_083", "SEMANTIC_CLUSTER_086",
    "SEMANTIC_CLUSTER_087", "SEMANTIC_CLUSTER_088", "SEMANTIC_CLUSTER_089",
    "SEMANTIC_CLUSTER_090", "SEMANTIC_CLUSTER_093", "SEMANTIC_CLUSTER_096",
    "SEMANTIC_CLUSTER_097", "SEMANTIC_CLUSTER_098", "SEMANTIC_CLUSTER_099",
    "SEMANTIC_CLUSTER_100", "SEMANTIC_CLUSTER_101", "SEMANTIC_CLUSTER_102",
    "SEMANTIC_CLUSTER_103", "SEMANTIC_CLUSTER_104", "SEMANTIC_CLUSTER_105",
    "SEMANTIC_CLUSTER_106", "SEMANTIC_CLUSTER_109", "SEMANTIC_CLUSTER_110",
    "SEMANTIC_CLUSTER_111"
]

def calculate_sha256(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_recording():
    startup_hashes = {str(fp): calculate_sha256(fp) for fp in PROTECTED_FILES}

    # 1. Load tools/DUPLICATE_FIELD_HUMAN_REVIEW_43.json
    with open(HUMAN_REVIEW_43_PATH, "r", encoding="utf-8") as f:
        human_review_data = json.load(f)

    review_clusters = human_review_data.get("clusters", [])

    # 2. Validation Checks
    if len(review_clusters) != 43:
        raise ValueError(f"Expected 43 clusters in human review package, found {len(review_clusters)}")

    adjudicated_clusters = []
    total_raw_records = 0

    for c in review_clusters:
        c_id = c["cluster_id"]
        pid = c["person"]
        field_pair_str = c["field_pair"]
        languages = c["languages"]
        occ_cnt = c["occurrence_count"]

        total_raw_records += occ_cnt

        if c_id not in HUMAN_43_CLUSTER_IDS:
            raise ValueError(f"Cluster ID '{c_id}' not found in human-approved 43 cluster list")

        if field_pair_str != "bio ↔ historical_significance":
            raise ValueError(f"Cluster '{c_id}' field pair '{field_pair_str}' is not 'bio ↔ historical_significance'")

        adjudicated_clusters.append({
            "cluster_id": c_id,
            "person": pid,
            "field_pair": field_pair_str,
            "languages": languages,
            "occurrence_count": occ_cnt,
            "classification": "CONFIRMED_DUPLICATE",
            "reason": "Human-reviewed exact field duplication; historical_significance contains the same content as bio and therefore provides no distinct historical-significance contribution.",
            "repair_target": "historical_significance"
        })

    if total_raw_records != 134:
        raise ValueError(f"Expected sum of occurrence_count to equal 134, found {total_raw_records}")

    # Shutdown File Hash Protection Check
    shutdown_hashes = {str(fp): calculate_sha256(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    report_output = {
        "audit_type": "DUPLICATE_FIELD_ADJUDICATION_FINAL_43",
        "decision_source": "HUMAN_SEMANTIC_REVIEW",
        "automated_semantic_classification": False,
        "total_clusters": len(adjudicated_clusters),
        "summary": {
            "confirmed_duplicates": len(adjudicated_clusters),
            "confirmed_legitimate_overlaps": 0,
            "ambiguous": 0,
            "affected_raw_records": total_raw_records
        },
        "classification_rule": {
            "CONFIRMED_DUPLICATE": "The same information is duplicated between fields with distinct semantic roles, so the second field provides no distinct contribution."
        },
        "clusters": adjudicated_clusters,
        "read_only": True,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("FINAL HUMAN ADJUDICATION")
    print("------------------------")
    print(f"TOTAL_CLUSTERS: {len(adjudicated_clusters)}")
    print(f"CONFIRMED_DUPLICATES: {len(adjudicated_clusters)}")
    print("CONFIRMED_LEGITIMATE_OVERLAPS: 0")
    print("AMBIGUOUS: 0")
    print(f"AFFECTED_RAW_RECORDS: {total_raw_records}")
    print("AUTOMATED_SEMANTIC_CLASSIFICATION: NO")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if not app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_recording()
