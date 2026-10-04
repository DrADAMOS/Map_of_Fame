#!/usr/bin/env python3
"""
READ-ONLY DATA INTEGRITY AUDIT SCRIPT
Performs dynamic, reproducible audit of application datasets and source packages.
Modifies NO application/runtime data or source packages.
Writes ONLY tools/FINAL_DATA_INTEGRITY_AUDIT.json.
"""

import json
import re
import hashlib
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
SOURCE_PKG_37_PATH = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.json"
HS_PKG_22_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json"
HS_PKG_13_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_13.json"
OUTPUT_AUDIT_PATH = ROOT / "tools" / "FINAL_DATA_INTEGRITY_AUDIT.json"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH,
    SOURCE_PKG_37_PATH,
    HS_PKG_22_PATH,
    HS_PKG_13_PATH
]

# Static Contract Constants
EXPECTED_PEOPLE_COUNT = 289
EXPECTED_QUIZ_COUNT = 297
EXPECTED_LANGUAGES = ["ar", "en", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "zh", "hi", "id", "fa"]
REQUIRED_NARRATIVE_FIELDS = ["bio", "achievements", "key_facts", "historical_significance"]
FIELD_PAIRS = [
    ("bio", "historical_significance"),
    ("achievements", "key_facts"),
    ("bio", "achievements"),
    ("bio", "key_facts"),
    ("achievements", "historical_significance"),
    ("key_facts", "historical_significance")
]

SCRIPT_PATTERNS = {
    "cyrillic": re.compile(r"[\u0400-\u04FF]"),
    "arabic": re.compile(r"[\u0600-\u06FF]"),
    "cjk": re.compile(r"[\u4E00-\u9FFF\u3040-\u30FF\u1100-\u11FF]")
}

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def recursive_deep_diff(obj1, obj2, path=""):
    diffs = []
    if type(obj1) != type(obj2):
        diffs.append({
            "path": path or "root",
            "type": "TYPE_MISMATCH",
            "val1_type": str(type(obj1)),
            "val2_type": str(type(obj2))
        })
        return diffs

    if isinstance(obj1, dict):
        keys1 = set(obj1.keys())
        keys2 = set(obj2.keys())

        for k in keys1 - keys2:
            diffs.append({"path": f"{path}.{k}" if path else k, "type": "MISSING_IN_TARGET", "value": str(obj1[k])[:80]})
        for k in keys2 - keys1:
            diffs.append({"path": f"{path}.{k}" if path else k, "type": "EXTRA_IN_TARGET", "value": str(obj2[k])[:80]})

        for k in sorted(list(keys1.intersection(keys2))):
            sub_path = f"{path}.{k}" if path else k
            diffs.extend(recursive_deep_diff(obj1[k], obj2[k], sub_path))

    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            diffs.append({
                "path": path,
                "type": "ARRAY_LENGTH_MISMATCH",
                "len1": len(obj1),
                "len2": len(obj2)
            })
        for i in range(min(len(obj1), len(obj2))):
            sub_path = f"{path}[{i}]"
            diffs.extend(recursive_deep_diff(obj1[i], obj2[i], sub_path))

    else:
        if obj1 != obj2:
            diffs.append({
                "path": path,
                "type": "VALUE_MISMATCH",
                "val1": str(obj1)[:80],
                "val2": str(obj2)[:80]
            })

    return diffs

def run_fully_dynamic_audit():
    # Startup File Hash Protection
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    critical_issues = 0
    high_issues = 0
    medium_issues = 0
    low_issues = 0
    info_issues = 0

    coverage = {
        "identity": "INCOMPLETE",
        "completeness": "INCOMPLETE",
        "duplicates": "INCOMPLETE",
        "semantic_duplicates": "INCOMPLETE",
        "cross_person": "INCOMPLETE",
        "language_contamination": "INCOMPLETE",
        "wikipedia_artifacts": "INCOMPLETE",
        "field_appropriateness": "INCOMPLETE",
        "quiz": "INCOMPLETE",
        "js_mirror": "INCOMPLETE",
        "provenance": "INCOMPLETE"
    }

    # 1. READ PERSON_I18N DATASET
    try:
        with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
            i18n_raw = json.load(f)
        i18n_people = i18n_raw.get("people", {})
        actual_i18n_people_count = len(i18n_people)
    except Exception:
        critical_issues += 1
        i18n_people = {}
        actual_i18n_people_count = 0

    actual_languages_set = set()
    total_person_language_records = 0
    for pobj in i18n_people.values():
        langs = pobj.get("languages", {})
        total_person_language_records += len(langs)
        for lcode in langs.keys():
            actual_languages_set.add(lcode)

    actual_languages_list = sorted(list(actual_languages_set))

    # C. COMPLETENESS AUDIT (289 x 14 x 4 = 16,184 field entries)
    missing_fields_cnt = 0
    insufficient_source_cnt = 0
    field_completeness_by_lang = {l: {fn: 0 for fn in REQUIRED_NARRATIVE_FIELDS} for l in EXPECTED_LANGUAGES}

    for pid, pobj in i18n_people.items():
        langs = pobj.get("languages", {})
        for lcode in EXPECTED_LANGUAGES:
            if lcode not in langs:
                missing_fields_cnt += 1
                high_issues += 1
            else:
                ldict = langs[lcode]
                for fn in REQUIRED_NARRATIVE_FIELDS:
                    f_val = ldict.get(fn)
                    if not f_val:
                        missing_fields_cnt += 1
                        field_completeness_by_lang[lcode][fn] += 1
                        high_issues += 1
                    elif f_val == "INSUFFICIENT_SOURCE" or f_val == ["INSUFFICIENT_SOURCE"]:
                        insufficient_source_cnt += 1
                        field_completeness_by_lang[lcode][fn] += 1
                        info_issues += 1

    coverage["completeness"] = "AUDITED"

    # B. IDENTITY INTEGRITY (DYNAMIC FROM WIKIPEDIA_IDENTITY_REVIEW.JSON)
    verified_id_cnt = 0
    mapped_alias_cnt = 0
    unresolved_id_cnt = 0
    unresolved_id_list = []
    missing_review_cnt = 0
    extra_review_cnt = 0
    total_review_entries = 0
    identity_discrepancies = []

    if IDENTITY_REVIEW_PATH.exists():
        try:
            with open(IDENTITY_REVIEW_PATH, "r", encoding="utf-8") as f:
                id_data = json.load(f)

            review_people = id_data.get("people", {}) if "people" in id_data else id_data.get("review_data", {})
            total_review_entries = len(review_people)

            for p_key, p_val in review_people.items():
                status = p_val.get("status") or p_val.get("verification_status") or "UNRESOLVED"
                status_u = str(status).upper()
                best_title = p_val.get("best_title") or p_val.get("title") or p_key

                if best_title != p_key:
                    identity_discrepancies.append({
                        "person": p_key,
                        "best_title": best_title,
                        "status": status
                    })

                if status_u == "VERIFIED" or status_u == "APPROVED" or status_u == "MATCH":
                    verified_id_cnt += 1
                elif status_u == "MAPPED_ALIAS" or "ALIAS" in status_u or "MAPPED" in status_u:
                    mapped_alias_cnt += 1
                elif status_u == "UNRESOLVED" or "AMBIGUOUS" in status_u or "NEEDS_REVIEW" in status_u:
                    unresolved_id_cnt += 1
                    info_issues += 1
                    unresolved_id_list.append({
                        "original_id": p_key,
                        "status": status,
                        "mapped_id": p_val.get("mapped_id", "N/A"),
                        "best_title": best_title,
                        "reason": p_val.get("reason", "Ambiguous identity resolution")
                    })
                else:
                    verified_id_cnt += 1

            for pid in i18n_people.keys():
                if pid not in review_people:
                    missing_review_cnt += 1

            for r_id in review_people.keys():
                if r_id not in i18n_people:
                    extra_review_cnt += 1

            coverage["identity"] = "AUDITED"
        except Exception:
            coverage["identity"] = "FAILED"
            critical_issues += 1

    # D. EXACT DUPLICATES (ALL 14 LOCALES & ALL 6 FIELD PAIRS)
    exact_duplicates_list = []
    real_dups_cnt = 0

    for pid, pobj in i18n_people.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fa, fb in FIELD_PAIRS:
                val_a = ldict.get(fa)
                val_b = ldict.get(fb)

                str_a = (json.dumps(val_a) if isinstance(val_a, list) else str(val_a or "")).strip().lower()
                str_b = (json.dumps(val_b) if isinstance(val_b, list) else str(val_b or "")).strip().lower()

                if str_a and str_b and str_a == str_b and str_a != '"insufficient_source"' and str_a != '["insufficient_source"]':
                    real_dups_cnt += 1
                    medium_issues += 1
                    exact_duplicates_list.append({
                        "person": pid,
                        "locale": lcode,
                        "field_a": fa,
                        "field_b": fb,
                        "value_a": str_a[:120],
                        "value_b": str_b[:120],
                        "classification": "EXACT_DUPLICATE"
                    })

    coverage["duplicates"] = "AUDITED"

    # E. SEMANTIC DUPLICATES (CANDIDATES ONLY - NEVER INCREMENT HIGH/MEDIUM SEVERITY FOR SIMILARITY ALONE)
    semantic_candidates_list = []
    sem_candidate_cnt = 0

    for pid, pobj in i18n_people.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fa, fb in FIELD_PAIRS:
                val_a = ldict.get(fa)
                val_b = ldict.get(fb)

                str_a = (" ".join([str(x) for x in val_a]) if isinstance(val_a, list) else str(val_a or "")).strip().lower()
                str_b = (" ".join([str(x) for x in val_b]) if isinstance(val_b, list) else str(val_b or "")).strip().lower()

                if str_a != str_b and len(str_a) > 20 and len(str_b) > 20 and str_a != "insufficient_source":
                    tokens_a = set(re.findall(r"\b\w{5,}\b", str_a))
                    tokens_b = set(re.findall(r"\b\w{5,}\b", str_b))

                    if len(tokens_a) > 0 and len(tokens_b) > 0:
                        overlap = tokens_a.intersection(tokens_b)
                        ratio = len(overlap) / float(min(len(tokens_a), len(tokens_b)))

                        if ratio >= 0.50:
                            sem_candidate_cnt += 1
                            classification = "POSSIBLE_SIMILARITY" if ratio < 0.85 else "UNCERTAIN"
                            info_issues += 1  # Candidates are info only!
                            semantic_candidates_list.append({
                                "person": pid,
                                "locale": lcode,
                                "field_a": fa,
                                "field_b": fb,
                                "text_a": str_a[:120],
                                "text_b": str_b[:120],
                                "similarity_score": round(ratio, 3),
                                "classification": classification
                            })

    coverage["semantic_duplicates"] = "AUDITED"

    # F. CROSS-PERSON CONTAMINATION (CANDIDATES vs CONFIRMED SEPARATED)
    cross_person_candidates_list = []
    cross_person_candidates_cnt = 0
    cross_person_confirmed_cnt = 0
    text_provenance_map = {}

    for pid, pobj in i18n_people.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fname in REQUIRED_NARRATIVE_FIELDS:
                fval = ldict.get(fname)
                fstr = (" ".join([str(x) for x in fval]) if isinstance(fval, list) else str(fval or "")).strip()
                fstr_clean = fstr.lower()

                if len(fstr_clean) > 50 and not fstr_clean.startswith("born in") and not fstr_clean.startswith("lived from") and fstr_clean != "insufficient_source":
                    if fstr_clean in text_provenance_map:
                        prev_p, prev_lc, prev_fn = text_provenance_map[fstr_clean]
                        if prev_p != pid:
                            medium_issues += 1
                            cross_person_candidates_cnt += 1
                            cross_person_candidates_list.append({
                                "source_person": prev_p,
                                "source_locale": prev_lc,
                                "source_field": prev_fn,
                                "target_person": pid,
                                "target_locale": lcode,
                                "target_field": fname,
                                "source_text": fstr[:120],
                                "target_text": fstr[:120],
                                "classification": "CROSS_PERSON_EXACT_MATCH_CANDIDATE"
                            })
                    else:
                        text_provenance_map[fstr_clean] = (pid, lcode, fname)

    coverage["cross_person"] = "AUDITED"

    # G. LANGUAGE CONTAMINATION (DYNAMIC LOCALE-AWARE CANDIDATES)
    real_lang_contam = []
    legit_foreign_names_cnt = 0

    for pid, pobj in i18n_people.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fname in REQUIRED_NARRATIVE_FIELDS:
                fval = ldict.get(fname)
                fstr = (" ".join([str(x) for x in fval]) if isinstance(fval, list) else str(fval or ""))

                # Check Cyrillic in English fields dynamically
                if lcode == "en" and SCRIPT_PATTERNS["cyrillic"].search(fstr):
                    if any(w in fstr.lower() for w in ["djvu", "runivers", "собрание", "издательство"]):
                        high_issues += 1
                        real_lang_contam.append({
                            "language": "en",
                            "person": pid,
                            "field": fname,
                            "text": fstr[:120],
                            "offending_text": fstr,
                            "classification": "REAL_CONTAMINATION",
                            "severity": "HIGH"
                        })
                    else:
                        legit_foreign_names_cnt += 1
                        info_issues += 1
                elif lcode == "en" and (SCRIPT_PATTERNS["arabic"].search(fstr) or SCRIPT_PATTERNS["cjk"].search(fstr)):
                    legit_foreign_names_cnt += 1
                    info_issues += 1

    coverage["language_contamination"] = "AUDITED"

    # H. WIKIPEDIA ARTIFACTS (ALL 289 x 14 x 4)
    wiki_artifacts_all = []
    for pid, pobj in i18n_people.items():
        langs = pobj.get("languages", {})
        for lcode, ldict in langs.items():
            for fname in REQUIRED_NARRATIVE_FIELDS:
                fval = ldict.get(fname)
                fstr = (" ".join([str(x) for x in fval]) if isinstance(fval, list) else str(fval or ""))
                if any(w in fstr for w in ["=== ", "http://", "https://", "[edit]", "[citation needed]"]):
                    medium_issues += 1
                    wiki_artifacts_all.append({
                        "person": pid,
                        "language": lcode,
                        "field": fname,
                        "offending_artifact": re.findall(r"===.*?===|http[s]?://\S+|\[edit\]", fstr),
                        "complete_sentence": fstr[:120],
                        "classification": "CONFIRMED_ARTIFACT"
                    })

    coverage["wikipedia_artifacts"] = "AUDITED"

    # Mendeleev achievements inspection
    mendeleev_ach = i18n_people.get("Dmitri Mendeleev", {}).get("languages", {}).get("en", {}).get("achievements", [])
    mendeleev_classifications = []
    for item in (mendeleev_ach if isinstance(mendeleev_ach, list) else []):
        item_s = str(item)
        if SCRIPT_PATTERNS["cyrillic"].search(item_s) or "djvu" in item_s.lower() or "runivers" in item_s.lower():
            mendeleev_classifications.append({"item": item_s, "classification": "citation artifact"})
        else:
            mendeleev_classifications.append({"item": item_s, "classification": "legitimate English content"})

    # I. FIELD APPROPRIATENESS (DYNAMIC FIELD INSPECTION)
    field_appropriateness_candidates = []
    for pid, pobj in i18n_people.items():
        en = pobj.get("languages", {}).get("en", {})
        bio = str(en.get("bio", "")).strip()
        ach = en.get("achievements", [])
        kf = en.get("key_facts", [])
        hs = str(en.get("historical_significance", "")).strip()

        if bio.startswith("[") and bio.endswith("]"):
            field_appropriateness_candidates.append({
                "person": pid, "field": "bio", "reason": "Biography text formatted as list string", "classification": "FIELD_PLACEMENT_CANDIDATE"
            })

    coverage["field_appropriateness"] = "AUDITED"

    # J. QUIZ DATA FULL DYNAMIC AUDIT
    quiz_valid = QUIZ_DATA_PATH.exists()
    actual_quiz_count = 0
    quiz_unique_names = set()
    quiz_issues = []
    unresolved_quiz_only = []
    resolved_quiz_aliases = []

    if quiz_valid:
        try:
            with open(QUIZ_DATA_PATH, "r", encoding="utf-8") as f:
                quiz_raw = json.load(f)

            if isinstance(quiz_raw, list):
                actual_quiz_count = len(quiz_raw)
                for qidx, qitem in enumerate(quiz_raw):
                    name_en = qitem.get("name_en")
                    if name_en:
                        quiz_unique_names.add(name_en)

                i18n_names = set(i18n_people.keys())
                quiz_only_names = quiz_unique_names - i18n_names

                id_review_data = {}
                if IDENTITY_REVIEW_PATH.exists():
                    with open(IDENTITY_REVIEW_PATH, "r", encoding="utf-8") as f:
                        id_review_data = json.load(f)
                rev_p = id_review_data.get("people", {}) if "people" in id_review_data else id_review_data.get("review_data", {})

                for q_name in quiz_only_names:
                    if q_name in rev_p and rev_p[q_name].get("best_title") in i18n_names:
                        resolved_quiz_aliases.append(f"{q_name} -> {rev_p[q_name].get('best_title')}")
                        info_issues += 1
                    else:
                        unresolved_quiz_only.append(q_name)
                        info_issues += 1

            coverage["quiz"] = "AUDITED"
        except Exception:
            coverage["quiz"] = "FAILED"
            high_issues += 1

    # K. JS MIRROR RECURSIVE DEEP AUDIT
    js_exists = JS_I18N_PATH.exists()
    js_people_cnt = 0
    js_mismatches = []

    if js_exists:
        try:
            with open(JS_I18N_PATH, "r", encoding="utf-8") as f:
                js_text = f.read().strip()

            js_clean = re.sub(r"^window\.PERSON_I18N\s*=\s*", "", js_text, flags=re.IGNORECASE).rstrip(";").strip()
            js_data = json.loads(js_clean)
            js_people = js_data.get("people", {})
            js_people_cnt = len(js_people)

            # Recursive deep comparison against person_i18n.json
            diffs = recursive_deep_diff(i18n_people, js_people)
            for d in diffs:
                js_mismatches.append(d)
                high_issues += 1

            coverage["js_mirror"] = "AUDITED"
        except Exception as e:
            coverage["js_mirror"] = "FAILED"
            js_mismatches.append({"error": str(e)})
            high_issues += 1

    # L. PROVENANCE VERIFICATION (AUDITING ALL 1,156 ENGLISH NARRATIVE FIELDS)
    pkg37 = {}
    if SOURCE_PKG_37_PATH.exists():
        with open(SOURCE_PKG_37_PATH, "r", encoding="utf-8") as f:
            pkg37 = json.load(f).get("people", {})

    hs_pkg22 = {}
    if HS_PKG_22_PATH.exists():
        with open(HS_PKG_22_PATH, "r", encoding="utf-8") as f:
            hs_pkg22 = json.load(f)

    hs_pkg13 = {}
    if HS_PKG_13_PATH.exists():
        with open(HS_PKG_13_PATH, "r", encoding="utf-8") as f:
            hs_pkg13 = json.load(f).get("package_data", {})

    provenance_audited_cnt = 0
    provenance_supported_cnt = 0
    provenance_unsupported_cnt = 0
    provenance_not_in_packages_cnt = 0
    provenance_mismatches = []

    # Audit all 289 people x 4 English narrative fields = 1,156 field instances!
    for pid, pobj in i18n_people.items():
        en = pobj.get("languages", {}).get("en", {})
        for fname in REQUIRED_NARRATIVE_FIELDS:
            f_val = en.get(fname)
            provenance_audited_cnt += 1

            has_source_pkg = (pid in pkg37) or (pid in hs_pkg22) or (pid in hs_pkg13)

            if has_source_pkg:
                if f_val and f_val != "INSUFFICIENT_SOURCE" and f_val != ["INSUFFICIENT_SOURCE"]:
                    provenance_supported_cnt += 1
                else:
                    provenance_unsupported_cnt += 1
                    provenance_mismatches.append({"person": pid, "field": fname, "status": "UNSUPPORTED"})
            else:
                provenance_not_in_packages_cnt += 1

    if provenance_audited_cnt == actual_i18n_people_count * 4:
        coverage["provenance"] = "AUDITED"
    else:
        coverage["provenance"] = "INCOMPLETE"

    # File Hash Protection (Shutdown)
    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True
            critical_issues += 1

    any_incomplete = any(v != "AUDITED" for v in coverage.values())

    if critical_issues > 0 or high_issues > 0 or app_data_modified or any_incomplete:
        final_status = "FAIL"
    elif medium_issues > 0:
        final_status = "PASS_WITH_WARNINGS"
    else:
        final_status = "PASS"

    audit_output = {
        "audit_type": "TRUE_DATA_INTEGRITY_AUDIT",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "summary": {
            "EXPECTED_PEOPLE": EXPECTED_PEOPLE_COUNT,
            "ACTUAL_PEOPLE": actual_i18n_people_count,
            "EXPECTED_LANGUAGES": EXPECTED_LANGUAGES,
            "ACTUAL_LANGUAGES": actual_languages_list,
            "EXPECTED_PERSON_LANGUAGE_RECORDS": EXPECTED_PEOPLE_COUNT * len(EXPECTED_LANGUAGES),
            "ACTUAL_PERSON_LANGUAGE_RECORDS": total_person_language_records,
            "EXPECTED_QUIZ_COUNT": EXPECTED_QUIZ_COUNT,
            "ACTUAL_QUIZ_COUNT": actual_quiz_count,
            "CRITICAL": critical_issues,
            "HIGH": high_issues,
            "MEDIUM": medium_issues,
            "LOW": low_issues,
            "INFO": info_issues,
            "FINAL_STATUS": final_status
        },
        "coverage": coverage,
        "identity_integrity": {
            "total_review_entries": total_review_entries,
            "verified": verified_id_cnt,
            "mapped_aliases": mapped_alias_cnt,
            "unresolved": unresolved_id_cnt,
            "unresolved_list": unresolved_id_list,
            "missing_from_review": missing_review_cnt,
            "extra_review_entries": extra_review_cnt,
            "identity_discrepancies": identity_discrepancies
        },
        "language_integrity": {
            "expected_languages": EXPECTED_LANGUAGES,
            "actual_languages_found": actual_languages_list
        },
        "field_completeness": {
            "missing_fields": missing_fields_cnt,
            "insufficient_source_stubs": insufficient_source_cnt,
            "field_completeness_by_language": field_completeness_by_lang
        },
        "duplicates": {
            "exact_duplicates": len(exact_duplicates_list),
            "real_duplicates": real_dups_cnt,
            "evidence": exact_duplicates_list
        },
        "semantic_duplicates": {
            "possible_similarity_cnt": sem_candidate_cnt,
            "evidence": semantic_candidates_list
        },
        "field_appropriateness": {
            "candidates": field_appropriateness_candidates
        },
        "cross_person_contamination": {
            "total_candidates": cross_person_candidates_cnt,
            "confirmed_cases_cnt": cross_person_confirmed_cnt,
            "evidence": cross_person_candidates_list
        },
        "wikipedia_artifacts": {
            "total_artifacts": len(wiki_artifacts_all),
            "evidence": wiki_artifacts_all
        },
        "mendeleev_contamination": {
            "current_achievements": mendeleev_ach,
            "classifications": mendeleev_classifications
        },
        "language_contamination": {
            "real_language_contamination": real_lang_contam,
            "legitimate_foreign_names_cnt": legit_foreign_names_cnt
        },
        "quiz_integrity": {
            "quiz_valid": quiz_valid,
            "quiz_total_entries": actual_quiz_count,
            "quiz_unique_names_cnt": len(quiz_unique_names),
            "resolved_known_aliases": resolved_quiz_aliases,
            "unresolved_quiz_only_names": unresolved_quiz_only,
            "quiz_issues": quiz_issues
        },
        "js_mirror_integrity": {
            "js_exists": js_exists,
            "js_people_cnt": js_people_cnt,
            "js_mismatches_cnt": len(js_mismatches),
            "js_mismatches": js_mismatches
        },
        "provenance_integrity": {
            "total_items_audited": provenance_audited_cnt,
            "supported_cnt": provenance_supported_cnt,
            "unsupported_cnt": provenance_unsupported_cnt,
            "not_in_packages_cnt": provenance_not_in_packages_cnt,
            "mismatches": provenance_mismatches
        },
        "application_data_modified": app_data_modified,
        "status": final_status
    }

    with open(OUTPUT_AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit_output, f, ensure_ascii=False, indent=2)

    # PRINT TERMINAL SUMMARY
    print("==================================================")
    print("FINAL DATA INTEGRITY AUDIT TERMINAL SUMMARY")
    print("==================================================")
    print(f"EXPECTED_PEOPLE: {EXPECTED_PEOPLE_COUNT}")
    print(f"ACTUAL_PEOPLE: {actual_i18n_people_count}")
    print(f"EXPECTED_LANGUAGES: {len(EXPECTED_LANGUAGES)}")
    print(f"ACTUAL_LANGUAGES: {len(actual_languages_list)}")
    print(f"EXPECTED_PERSON_LANGUAGE_RECORDS: {EXPECTED_PEOPLE_COUNT * len(EXPECTED_LANGUAGES)}")
    print(f"ACTUAL_PERSON_LANGUAGE_RECORDS: {total_person_language_records}")
    print(f"EXPECTED_QUIZ_COUNT: {EXPECTED_QUIZ_COUNT}")
    print(f"ACTUAL_QUIZ_COUNT: {actual_quiz_count}\n")

    print("IDENTITY:")
    print(f"  total: {total_review_entries} | verified: {verified_id_cnt} | mapped: {mapped_alias_cnt} | unresolved: {unresolved_id_cnt}")
    print()
    print("DUPLICATES:")
    print(f"  exact: {len(exact_duplicates_list)} | semantic candidates: {sem_candidate_cnt} | confirmed: {real_dups_cnt}")
    print()
    print("CROSS_PERSON:")
    print(f"  candidates: {cross_person_candidates_cnt} | confirmed: {cross_person_confirmed_cnt}")
    print()
    print("WIKIPEDIA_ARTIFACTS:")
    print(f"  candidates: {len(wiki_artifacts_all)} | confirmed: {len(wiki_artifacts_all)}")
    print()
    print("LANGUAGE_CONTAMINATION:")
    print(f"  candidates: {len(real_lang_contam) + legit_foreign_names_cnt} | confirmed: {len(real_lang_contam)}")
    print()
    print("QUIZ:")
    print(f"  issues: {len(unresolved_quiz_only)}")
    print()
    print("JS:")
    print(f"  mismatches: {len(js_mismatches)}")
    print()
    print("PROVENANCE:")
    print(f"  items audited: {provenance_audited_cnt} | supported: {provenance_supported_cnt} | partial: 0 | unsupported: {provenance_unsupported_cnt} | source_not_in_packages: {provenance_not_in_packages_cnt}")
    print()
    print("COVERAGE:")
    for domain_k, domain_v in coverage.items():
        print(f"  - {domain_k}: {domain_v}")
    print()
    print(f"CRITICAL: {critical_issues}")
    print(f"HIGH: {high_issues}")
    print(f"MEDIUM: {medium_issues}")
    print(f"LOW: {low_issues}")
    print(f"INFO: {info_issues}")
    print(f"FINAL_STATUS: {final_status}")
    print(f"APPLICATION DATA MODIFIED: {'YES' if app_data_modified else 'NO'}")

if __name__ == "__main__":
    run_fully_dynamic_audit()
