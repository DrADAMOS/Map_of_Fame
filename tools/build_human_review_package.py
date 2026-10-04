#!/usr/bin/env python3
"""
READ-ONLY HUMAN REVIEW PACKAGE GENERATOR FOR 43 DUPLICATE CLUSTERS
Extracts complete actual values from person_i18n.json for the 43 clusters in DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json.
Performs NO automatic semantic classification or adjudication.
Saves ONLY:
  - tools/DUPLICATE_FIELD_HUMAN_REVIEW_43.json
  - tools/DUPLICATE_FIELD_HUMAN_REVIEW_43.md
Modifies NO application/runtime data files or source packages.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
CLUSTERS_V2_PATH = ROOT / "tools" / "DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json"

OUTPUT_JSON_PATH = ROOT / "tools" / "DUPLICATE_FIELD_HUMAN_REVIEW_43.json"
OUTPUT_MD_PATH = ROOT / "tools" / "DUPLICATE_FIELD_HUMAN_REVIEW_43.md"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_value_type(val):
    if val is None:
        return "null"
    elif isinstance(val, str):
        return "string"
    elif isinstance(val, list):
        return "array"
    elif isinstance(val, dict):
        return "object"
    else:
        return "other"

def run_extraction_and_package_build():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Load V2 Clusters Report
    with open(CLUSTERS_V2_PATH, "r", encoding="utf-8") as f:
        v2_raw = json.load(f)

    all_clusters = v2_raw.get("ALL_CLUSTERS", [])
    needs_review_clusters = [c for c in all_clusters if c.get("review_status") == "NEEDS_MANUAL_REVIEW"]

    # Load Current person_i18n.json
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_raw = json.load(f)

    people_data = i18n_raw.get("people", {})

    extracted_clusters = []
    md_lines = []

    # Markdown Header
    md_lines.append("# Duplicate Field Human Review — 43 Clusters\n")
    md_lines.append("## Review Rules\n")
    md_lines.append("- **Read-Only Extraction**: This document contains untruncated, raw current values from `person_i18n.json`.")
    md_lines.append("- **No Automatic Classification**: No automated semantic rules, keywords, or models were used to classify these clusters.")
    md_lines.append("- **Human Adjudication Protocol**: Reviewers must inspect the complete text in each field and evaluate whether the duplication is an inappropriate duplicate, a legitimate overlap, or genuinely ambiguous.")
    md_lines.append("- **Field Roles**: Evaluate whether Field B adds a distinct semantic contribution relative to Field A.\n")

    for idx, c_obj in enumerate(needs_review_clusters, 1):
        c_id = c_obj["cluster_id"]
        pid = c_obj["people"][0]
        field_pair_str = c_obj["field_pair"]
        languages = c_obj["languages"]
        occ_cnt = c_obj["occurrence_count"]
        rep_text = c_obj["representative_exact_text"]

        # Parse field_pair using exact delimiter " ↔ "
        if " ↔ " in field_pair_str:
            fa, fb = field_pair_str.split(" ↔ ")
        else:
            parts = field_pair_str.split("_")
            fa, fb = parts[0], parts[-1]

        p_entry = people_data.get(pid, {})
        p_langs = p_entry.get("languages", {})

        lang_records = []

        # Markdown Cluster Entry
        md_lines.append("---")
        md_lines.append(f"\n## Cluster {idx}/{len(needs_review_clusters)}")
        md_lines.append("\n### Identity")
        md_lines.append(f"- **Cluster ID**: {c_id}")
        md_lines.append(f"- **Person**: {pid}")
        md_lines.append(f"- **Field A**: `{fa}`")
        md_lines.append(f"- **Field B**: `{fb}`")
        md_lines.append(f"- **Languages**: `{', '.join(languages)}`")
        md_lines.append(f"- **Occurrence Count**: {occ_cnt}\n")

        for lcode in languages:
            ldict = p_langs.get(lcode, {})
            val_a = ldict.get(fa)
            val_b = ldict.get(fb)

            type_a = get_value_type(val_a)
            type_b = get_value_type(val_b)

            lang_records.append({
                "language": lcode,
                "field_a": {
                    "type": type_a,
                    "value": val_a
                },
                "field_b": {
                    "type": type_b,
                    "value": val_b
                }
            })

            # Format Markdown for Language
            md_lines.append(f"### Language: `{lcode}`\n")
            md_lines.append(f"#### Field A (`{fa}`)")
            md_lines.append("```text")
            md_lines.append(json.dumps(val_a, ensure_ascii=False, indent=2) if isinstance(val_a, (dict, list)) else str(val_a))
            md_lines.append("```\n")

            md_lines.append(f"#### Field B (`{fb}`)")
            md_lines.append("```text")
            md_lines.append(json.dumps(val_b, ensure_ascii=False, indent=2) if isinstance(val_b, (dict, list)) else str(val_b))
            md_lines.append("```\n")

        extracted_clusters.append({
            "cluster_id": c_id,
            "person": pid,
            "field_pair": field_pair_str,
            "field_a": fa,
            "field_b": fb,
            "languages": languages,
            "occurrence_count": occ_cnt,
            "representative_exact_text": rep_text,
            "language_records": lang_records
        })

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    json_report_output = {
        "audit_type": "DUPLICATE_FIELD_HUMAN_REVIEW_43",
        "read_only": True,
        "classification_performed": False,
        "source_files": {
            "clusters_v2": str(CLUSTERS_V2_PATH),
            "person_i18n": str(PERSON_I18N_PATH)
        },
        "protected_files": [str(fp) for fp in PROTECTED_FILES],
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "total_clusters_found": len(extracted_clusters),
        "clusters": extracted_clusters,
        "human_review_schema": {
            "allowed_classifications": [
                "CONFIRMED_DUPLICATE",
                "CONFIRMED_LEGITIMATE_OVERLAP",
                "AMBIGUOUS"
            ],
            "classification_definition": {
                "CONFIRMED_DUPLICATE": "The two fields contain materially the same information and the duplication is inappropriate for their distinct semantic roles.",
                "CONFIRMED_LEGITIMATE_OVERLAP": "The same information legitimately serves both field roles and retaining the overlap is acceptable.",
                "AMBIGUOUS": "The available content is insufficient to make a reliable semantic determination."
            }
        },
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    # Write JSON report
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(json_report_output, f, ensure_ascii=False, indent=2)

    # Write Markdown document
    with open(OUTPUT_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # PRINT TERMINAL SUMMARY
    print("HUMAN REVIEW EXTRACTION COMPLETE")
    print(f"TOTAL_CLUSTERS_EXTRACTED: {len(extracted_clusters)}")
    print(f"CLASSIFICATION_PERFORMED: NO (false)")
    print(f"OUTPUT_JSON: {OUTPUT_JSON_PATH}")
    print(f"OUTPUT_MARKDOWN: {OUTPUT_MD_PATH}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_extraction_and_package_build()
