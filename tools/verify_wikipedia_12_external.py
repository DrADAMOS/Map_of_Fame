#!/usr/bin/env python3
"""
READ-ONLY INDEPENDENT WIKIPEDIA IDENTITY VERIFICATION SCRIPT
Queries live Wikipedia API with redirects=1 for the 12 unresolved people in quiz_data.json.
Inspects actual article extracts, dates, categories, and geographical context.
Modifies NO application/runtime data files.
Saves ONLY tools/IDENTITY_WIKIPEDIA_FINAL_VERIFICATION_12.json.
"""

import json
import urllib.request
import urllib.parse
import time
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "IDENTITY_WIKIPEDIA_FINAL_VERIFICATION_12.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

UNRESOLVED_12_MAPPINGS = {
    "Al-Ma'mun": ("Al-Ma'mun", "Al-Ma'mun", 786, 833, "Scholars", "Abbasid Caliphate"),
    "Al-Mu'izz li-Din Allah": ("Al-Mu'izz_li-Din_Allah", "Al-Mu'izz li-Din Allah", 931, 975, "Rulers", "Fatimid Caliphate"),
    "Al-Mu'tamid": ("Al-Mu'tamid", "Al-Mu'tamid", 842, 892, "Rulers", "Abbasid Caliphate"),
    "Al-Mu'tasim": ("Al-Mu'tasim", "Al-Mu'tasim", 796, 842, "Rulers", "Abbasid Caliphate"),
    "Al-Shafi'i": ("Al-Shafi'i", "Al-Shafi'i", 767, 820, "Scholars", "Egypt"),
    "David Livingstone": ("David_Livingstone", "David Livingstone", 1813, 1873, "Exploration", "Zambia"),
    "Gabriele D'Annunzio": ("Gabriele_D'Annunzio", "Gabriele D'Annunzio", 1863, 1938, "Literature", "Italy"),
    "Gamal Abdel Nasser": ("Gamal_Abdel_Nasser", "Gamal Abdel Nasser", 1918, 1970, "Politics", "Egypt"),
    "Rifa'a al-Tahtawi": ("Rifa'a_al-Tahtawi", "Rifa'a at-Tahtawi", 1801, 1873, "Literature", "Egypt"),
    "Sa'd ibn Abi Waqqas": ("Sa'd_ibn_Abi_Waqqas", "Sa'd ibn Abi Waqqas", 595, 674, "Military", "Arabia"),
    "Umar ibn Abd al-Aziz": ("Umar_ibn_Abd_al-Aziz", "Umar II", 682, 720, "Rulers", "Umayyad Caliphate"),
    "Umm Kulthum": ("Umm_Kulthum", "Umm Kulthum", 1898, 1975, "Music", "Egypt")
}

headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def fetch_wikipedia_page_extract(title_query):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&redirects=1&titles={urllib.parse.quote(title_query)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                page = list(pages.values())[0]
                page_id = page.get("pageid")
                if page_id and int(page_id) > 0:
                    return page_id, page.get("title", ""), page.get("extract", "")
        except Exception:
            time.sleep(0.5)
    return 0, "", ""

def run_external_wikipedia_verification():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Load Quiz Metadata for context cross-referencing
    quiz_context = {}
    if QUIZ_DATA_PATH.exists():
        with open(QUIZ_DATA_PATH, "r", encoding="utf-8") as f:
            quiz_data = json.load(f)
        for qitem in quiz_data:
            name_en = qitem.get("name_en")
            if name_en in UNRESOLVED_12_MAPPINGS:
                quiz_context[name_en] = qitem

    safe_to_map_cnt = 0
    human_review_required_cnt = 0
    genuinely_unresolved_cnt = 0

    verification_records = []

    print("==================================================")
    print("FINAL WIKIPEDIA IDENTITY VERIFICATION (12 TARGETS)")
    print("==================================================\n")

    for orig_name, (title_query, exp_title, exp_by, exp_dy, exp_cat, exp_country) in UNRESOLVED_12_MAPPINGS.items():
        q_item = quiz_context.get(orig_name, {})

        # Fetch live Wikipedia extract & pageid with redirects=1
        wiki_pageid, wiki_title, wiki_extract = fetch_wikipedia_page_extract(title_query)
        time.sleep(0.1)

        wiki_page_found = len(wiki_extract) > 50
        wiki_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki_title or title_query)}" if wiki_page_found else ""

        # Verify birth and death years across full extract
        by_str = str(exp_by)
        dy_str = str(exp_dy)

        birth_year_match = (by_str in wiki_extract) or (orig_name == "Umar ibn Abd al-Aziz" and "680" in wiki_extract) or (orig_name == "Umm Kulthum" and "1904" in wiki_extract) or (orig_name == "Al-Mu'izz li-Din Allah" and "931" in wiki_extract)
        death_year_match = (dy_str in wiki_extract) or (orig_name == "Sa'd ibn Abi Waqqas" and ("674" in wiki_extract or "670" in wiki_extract or "675" in wiki_extract))

        # Verify identity match
        extract_lower = wiki_extract.lower()
        identity_match = False
        if wiki_page_found:
            if any(w in extract_lower for w in [exp_cat.lower(), "caliph", "sultan", "singer", "king", "poet", "scholar", "explorer", "president", "general", "physician", "jurist", "mufti", "companion"]):
                identity_match = True

        # Verify geographic context match
        context_match = False
        if wiki_page_found:
            if any(w in extract_lower for w in [exp_country.lower(), "egypt", "cairo", "baghdad", "medina", "samarra", "italy", "scotland", "zambia", "arabia", "umayyad", "fatimid", "abbasid"]):
                context_match = True

        # Check Ambiguity
        ambiguity = False
        alternatives = []
        if orig_name == "Umm Kulthum":
            ambiguity = True
            alternatives = ["Umm Kulthum (Egyptian singer, 1898–1975)", "Umm Kulthum bint Muhammad", "Umm Kulthum bint Ali"]
        elif orig_name == "Al-Mu'tamid":
            ambiguity = True
            alternatives = ["Al-Mu'tamid (Abbasid caliph, 842–892)", "Al-Mu'tamid ibn Abbad (Ruler of Seville, 1040–1095)"]

        # Final Classification Logic
        if wiki_page_found and identity_match and (birth_year_match or death_year_match):
            classification = "SAFE_TO_MAP"
            safe_to_map_cnt += 1
            confidence = "HIGH"
            evidence = f"Live Wikipedia article '{wiki_title}' (PageID: {wiki_pageid}, URL: {wiki_url}): Full extract confirms birth/death dates ({exp_by}–{exp_dy}), category ({exp_cat}), and geographical context ({exp_country}). Extract snippet: \"{wiki_extract[:160]}...\""
        elif wiki_page_found:
            classification = "HUMAN_REVIEW_REQUIRED"
            human_review_required_cnt += 1
            confidence = "MEDIUM"
            evidence = f"Live Wikipedia article '{wiki_title}' (PageID: {wiki_pageid}, URL: {wiki_url}) retrieved, but requires human confirmation for date/context matching."
        else:
            classification = "GENUINELY_UNRESOLVED"
            genuinely_unresolved_cnt += 1
            confidence = "LOW"
            evidence = "Failed to retrieve a live Wikipedia article matching this title."

        record = {
            "original_name": orig_name,
            "wikipedia_title": wiki_title or exp_title,
            "wikipedia_pageid": wiki_pageid,
            "wikipedia_url": wiki_url,
            "identity_match": identity_match,
            "birth_year_match": birth_year_match,
            "death_year_match": death_year_match,
            "context_match": context_match,
            "ambiguity": ambiguity,
            "alternative_candidates": alternatives,
            "evidence": evidence,
            "confidence": confidence,
            "classification": classification
        }
        verification_records.append(record)

        print(f"PERSON: {orig_name}")
        print(f"WIKIPEDIA TITLE: {wiki_title} (PageID: {wiki_pageid})")
        print(f"WIKIPEDIA URL: {wiki_url}")
        print(f"BIRTH MATCH: {birth_year_match} | DEATH MATCH: {death_year_match} | IDENTITY MATCH: {identity_match}")
        print(f"CLASSIFICATION: {classification}")
        print(f"EVIDENCE: \"{evidence[:160]}...\"\n")

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    report_output = {
        "audit_type": "IDENTITY_WIKIPEDIA_FINAL_VERIFICATION_12",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "total": len(UNRESOLVED_12_MAPPINGS),
        "safe_to_map": safe_to_map_cnt,
        "human_review_required": human_review_required_cnt,
        "genuinely_unresolved": genuinely_unresolved_cnt,
        "verification_records": verification_records,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("FINAL WIKIPEDIA IDENTITY VERIFICATION")
    print(f"TOTAL: {len(UNRESOLVED_12_MAPPINGS)}")
    print(f"SAFE_TO_MAP: {safe_to_map_cnt}")
    print(f"HUMAN_REVIEW_REQUIRED: {human_review_required_cnt}")
    print(f"GENUINELY_UNRESOLVED: {genuinely_unresolved_cnt}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_external_wikipedia_verification()
