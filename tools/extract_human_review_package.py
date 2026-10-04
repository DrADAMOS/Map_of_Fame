#!/usr/bin/env python3
"""
READ-ONLY HUMAN REVIEW EXTRACTION TOOL FOR 43 DUPLICATE CLUSTERS
Extracts complete actual values from person_i18n.json for the 43 clusters in DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json.
Performs NO automated semantic classification, keyword heuristics, or AI adjudication.
Modifies NO application/runtime data files or source packages.
Saves ONLY:
  - tools/DUPLICATE_FIELD_HUMAN_REVIEW_43.json
  - tools/DUPLICATE_FIELD_HUMAN_REVIEW_43.md
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
CLUSTERS_V2_PATH = ROOT / "tools" / "DUPLICATE_FIELD_REVIEW_CLUSTERS_V2.json"

OUTPUT_JSON_PATH = ROOT / "tools" / "DUPLICATE_FIELD_HUMAN_REVIEW_43.json"
OUTPUT_MD_PATH = ROOT / "tools" / "DUPLICATE_FIELD_HUMAN_REVIEW_43.md"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH
]

def calculate_sha256(filepath: Path) -> str:
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_json(filepath: Path) -> Dict[str, Any]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_unresolved_clusters(v2_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    all_clusters = v2_data.get("ALL_CLUSTERS", [])
    unresolved = [c for c in all_clusters if c.get("review_status") == "NEEDS_MANUAL_REVIEW"]
    return unresolved

def parse_field_pair(field_pair_str: str) -> Tuple[str, str]:
    if " ↔ " in field_pair_str:
        parts = field_pair_str.split(" ↔ ")
        return parts[0], parts[1]
    else:
        parts = field_pair_str.split("_")
        return parts[0], parts[-1]

def get_value_type(val: Any) -> str:
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

def extract_cluster_content(cluster: Dict[str, Any], people_data: Dict[str, Any]) -> Dict[str, Any]:
    c_id = cluster["cluster_id"]
    pid = cluster["people"][0]
    field_pair_str = cluster["field_pair"]
    languages = cluster["languages"]
    occ_cnt = cluster["occurrence_count"]
    rep_text = cluster["representative_exact_text"]

    fa, fb = parse_field_pair(field_pair_str)

    p_entry = people_data.get(pid)
    if not p_entry:
        raise ValueError(f"Person '{pid}' from cluster '{c_id}' not found in person_i18n.json")

    p_langs = p_entry.get("languages", {})
    language_records = []

    for lcode in languages:
        ldict = p_langs.get(lcode)
        if ldict is None:
            raise ValueError(f"Language '{lcode}' for person '{pid}' not found in person_i18n.json")

        val_a = ldict.get(fa)
        val_b = ldict.get(fb)

        language_records.append({
            "language": lcode,
            "field_a": {
                "type": get_value_type(val_a),
                "value": val_a
            },
            "field_b": {
                "type": get_value_type(val_b),
                "value": val_b
            }
        })

    return {
        "cluster_id": c_id,
        "person": pid,
        "field_pair": field_pair_str,
        "field_a": fa,
        "field_b": fb,
        "languages": languages,
        "occurrence_count": occ_cnt,
        "representative_exact_text": rep_text,
        "language_records": language_records
    }

def validate_cluster_extraction(extracted_clusters: List[Dict[str, Any]], raw_v2_clusters: List[Dict[str, Any]]) -> bool:
    if len(extracted_clusters) != 43 or len(raw_v2_clusters) != 43:
        return False

    extracted_ids = {c["cluster_id"] for c in extracted_clusters}
    raw_ids = {c["cluster_id"] for c in raw_v2_clusters}

    if len(extracted_ids) != 43 or extracted_ids != raw_ids:
        return False

    for ext_c, raw_c in zip(extracted_clusters, raw_v2_clusters):
        if ext_c["cluster_id"] != raw_c["cluster_id"]:
            return False
        if ext_c["person"] != raw_c["people"][0]:
            return False
        if ext_c["field_pair"] != raw_c["field_pair"]:
            return False
        if ext_c["languages"] != raw_c["languages"]:
            return False
        if ext_c["occurrence_count"] != raw_c["occurrence_count"]:
            return False

    return True

def write_json_report(filepath: Path, report_data: Dict[str, Any]) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

def write_markdown_report(filepath: Path, clusters: List[Dict[str, Any]]) -> None:
    md_lines = []
    md_lines.append("# Duplicate Field Human Review — 43 Clusters\n")
    md_lines.append("## Review Rules\n")
    md_lines.append("- **Read-Only Extraction**: This document contains untruncated, raw current values from `person_i18n.json`.")
    md_lines.append("- **No Automatic Classification**: No automated semantic rules, keywords, or models were used to classify these clusters.")
    md_lines.append("- **Human Adjudication Protocol**: Reviewers must inspect the complete text in each field and evaluate whether the duplication is an inappropriate duplicate, a legitimate overlap, or genuinely ambiguous.")
    md_lines.append("- **Field Roles**: Evaluate whether Field B adds a distinct semantic contribution relative to Field A.\n")

    for idx, c in enumerate(clusters, 1):
        md_lines.append("---")
        md_lines.append(f"\n## Cluster {idx}/43")
        md_lines.append("\n### Identity")
        md_lines.append(f"- **Cluster ID**: {c['cluster_id']}")
        md_lines.append(f"- **Person**: {c['person']}")
        md_lines.append(f"- **Field A**: `{c['field_a']}`")
        md_lines.append(f"- **Field B**: `{c['field_b']}`")
        md_lines.append(f"- **Languages**: `{', '.join(c['languages'])}`")
        md_lines.append(f"- **Occurrence Count**: {c['occurrence_count']}\n")

        for lang_rec in c["language_records"]:
            lcode = lang_rec["language"]
            val_a = lang_rec["field_a"]["value"]
            val_b = lang_rec["field_b"]["value"]

            md_lines.append(f"### Language: `{lcode}`\n")

            md_lines.append(f"#### Field A (`{c['field_a']}`)")
            md_lines.append("```text")
            md_lines.append(json.dumps(val_a, ensure_ascii=False, indent=2) if isinstance(val_a, (dict, list)) else str(val_a))
            md_lines.append("```\n")

            md_lines.append(f"#### Field B (`{c['field_b']}`)")
            md_lines.append("```text")
            md_lines.append(json.dumps(val_b, ensure_ascii=False, indent=2) if isinstance(val_b, (dict, list)) else str(val_b))
            md_lines.append("```\n")

        md_lines.append("### Human Review\n")
        md_lines.append("#### Classification:\n")
        md_lines.append("- [ ] CONFIRMED_DUPLICATE")
        md_lines.append("- [ ] CONFIRMED_LEGITIMATE_OVERLAP")
        md_lines.append("- [ ] AMBIGUOUS\n")
        md_lines.append("#### Reason:\n")
        md_lines.append("\n#### Repair required:\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

def verify_protected_hashes(hashes_before: Dict[str, str], hashes_after: Dict[str, str]) -> bool:
    for fp_str, before_h in hashes_before.items():
        after_h = hashes_after.get(fp_str, "")
        if before_h != after_h:
            return False
    return True

def main() -> None:
    # 1. Startup Protected Hash Check
    startup_hashes = {str(fp): calculate_sha256(fp) for fp in PROTECTED_FILES}

    # 2. Load Inputs
    v2_data = load_json(CLUSTERS_V2_PATH)
    i18n_raw = load_json(PERSON_I18N_PATH)
    people_data = i18n_raw.get("people", {})

    # 3. Identify 43 Unresolved Clusters
    unresolved_v2_clusters = get_unresolved_clusters(v2_data)
    total_found = len(unresolved_v2_clusters)

    # 4. Extract Content for All 43 Clusters
    extracted_clusters = []
    total_lang_records_cnt = 0

    for c in unresolved_v2_clusters:
        extracted = extract_cluster_content(c, people_data)
        extracted_clusters.append(extracted)
        total_lang_records_cnt += len(extracted["language_records"])

    # 5. Validate Extraction Integrity
    extraction_valid = validate_cluster_extraction(extracted_clusters, unresolved_v2_clusters)

    # 6. Shutdown Protected Hash Check
    shutdown_hashes = {str(fp): calculate_sha256(fp) for fp in PROTECTED_FILES}
    hashes_valid = verify_protected_hashes(startup_hashes, shutdown_hashes)
    app_data_modified = not hashes_valid

    # Final Status Determination
    status_pass = (
        total_found == 43 and
        len(extracted_clusters) == 43 and
        extraction_valid and
        hashes_valid and
        not app_data_modified
    )

    final_status = "PASS" if status_pass else "FAIL"

    # Build JSON Report
    json_report = {
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
        "total_clusters_found": total_found,
        "total_clusters_extracted": len(extracted_clusters),
        "total_language_records_extracted": total_lang_records_cnt,
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

    # Write Output Reports
    write_json_report(OUTPUT_JSON_PATH, json_report)
    write_markdown_report(OUTPUT_MD_PATH, extracted_clusters)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("DUPLICATE FIELD HUMAN REVIEW 43")
    print(f"TOTAL_CLUSTERS_FOUND: {total_found}")
    print(f"TOTAL_CLUSTERS_EXTRACTED: {len(extracted_clusters)}")
    print(f"LANGUAGE_RECORDS_EXTRACTED: {total_lang_records_cnt}")
    print("CLASSIFICATION_PERFORMED: NO")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if hashes_valid else 'NO'}")
    print(f"REPORT_JSON_CREATED: {'YES' if OUTPUT_JSON_PATH.exists() else 'NO'}")
    print(f"REPORT_MARKDOWN_CREATED: {'YES' if OUTPUT_MD_PATH.exists() else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    main()
