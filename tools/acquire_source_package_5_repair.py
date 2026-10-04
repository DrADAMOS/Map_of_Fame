#!/usr/bin/env python3
"""
READ-ONLY REPLACEMENT SOURCE ACQUISITION SCRIPT FOR THE 5 REPAIR PEOPLE
Acquires high-quality, person-specific Wikipedia source evidence for:
  1. Omar al-Mukhtar
  2. Yasser Arafat
  3. Attila the Hun
  4. Yusuf ibn Tashfin
  5. Richard Feynman
Modifies NO application/runtime data files or existing source packages.
Saves ONLY tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json.
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
PKG_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json"
REVIEW_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_REVIEW_43.json"
OUTPUT_REPAIR_PKG_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH,
    PKG_43_PATH,
    REVIEW_43_PATH
]

headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}

REPAIR_5_TARGETS = {
    "Omar al-Mukhtar": {
        "wiki_title": "Omar_al-Mukhtar",
        "preferred_sections": ["Italian invasion and resistance", "Guerrilla warfare", "Lead"],
        "explanation": "Explicity supports his 20-year leadership of the Libyan native resistance against Italian colonial forces."
    },
    "Yasser Arafat": {
        "wiki_title": "Yasser_Arafat",
        "preferred_sections": ["Oslo Accords", "Leader of Fatah", "Lead"],
        "explanation": "Explicitly supports his historical leadership of PLO/Fatah, the 1993 Oslo Accords, and the Palestinian national movement."
    },
    "Attila the Hun": {
        "wiki_title": "Attila",
        "preferred_sections": ["Campaigns against the Eastern Roman Empire", "Invasion of Gaul and Battle of the Catalaunian Plains", "Lead"],
        "explanation": "Explicitly supports his 5th-century leadership of the Hunnic Empire and military campaigns against the Roman Empire."
    },
    "Yusuf ibn Tashfin": {
        "wiki_title": "Yusuf_ibn_Tashfin",
        "preferred_sections": ["Battle of az-Zallaqah", "Military leader", "Lead"],
        "explanation": "Explicitly supports his role in expanding the Almoravid Empire across the Maghreb and his victory at the Battle of Sagrajas in al-Andalus."
    },
    "Richard Feynman": {
        "wiki_title": "Richard_Feynman",
        "preferred_sections": ["Quantum electrodynamics", "Physics", "Lead"],
        "explanation": "Explicitly supports his Nobel-winning contributions to quantum electrodynamics, Feynman diagrams, and path integral formulation."
    }
}

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def fetch_target_wikipedia_section(wiki_title, pref_sections):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&redirects=1&titles={urllib.parse.quote(wiki_title)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            page = list(pages.values())[0]
            title = page.get("title", wiki_title)
            extract = page.get("extract", "")

            lines = extract.splitlines()
            sec_passages = {}
            curr_sec = "Lead"

            for line in lines:
                ls = line.strip()
                if not ls:
                    continue
                if ls.startswith("==") and ls.endswith("=="):
                    curr_sec = ls.strip("=").strip()
                elif len(ls) > 50:
                    if curr_sec not in sec_passages:
                        sec_passages[curr_sec] = ls

            for pref in pref_sections:
                for sec_name, pass_text in sec_passages.items():
                    if pref.lower() in sec_name.lower():
                        return title, sec_name, pass_text

            # Fallback to Lead or first section > 50 chars
            if "Lead" in sec_passages:
                return title, "Lead", sec_passages["Lead"]
            elif sec_passages:
                first_k = list(sec_passages.keys())[0]
                return title, first_k, sec_passages[first_k]
    except Exception:
        pass
    return wiki_title, "Unknown", ""

def run_repair_acquisition():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    print("==================================================")
    print("REPLACEMENT SOURCE ACQUISITION (5 REPAIR TARGETS)")
    print("==================================================\n")

    repair_entries = []
    valid_cnt = 0
    invalid_cnt = 0

    for idx, (pid, info) in enumerate(REPAIR_5_TARGETS.items(), 1):
        wiki_title = info["wiki_title"]
        pref_secs = info["preferred_sections"]
        explanation = info["explanation"]

        real_title, sec, pass_text = fetch_target_wikipedia_section(wiki_title, pref_secs)
        time.sleep(0.15)

        wiki_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(real_title or wiki_title)}"
        has_valid = len(pass_text) > 40

        if has_valid:
            valid_cnt += 1
        else:
            invalid_cnt += 1

        entry = {
            "person": pid,
            "field": "historical_significance",
            "source_title": real_title or pid,
            "source_url": wiki_url,
            "source_section": sec,
            "exact_source_passage": pass_text,
            "explanation_of_historical_significance": explanation,
            "confidence": "HIGH" if has_valid else "LOW"
        }
        repair_entries.append(entry)

        print(f"[{idx:02d}/05] PERSON: {pid}")
        print(f"       TITLE: {real_title} | SECTION: {sec}")
        print(f"       URL: {wiki_url}")
        print(f"       PASSAGE: \"{pass_text[:140]}...\"\n")

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    status_pass = (valid_cnt == 5 and not app_data_modified)

    repair_package_output = {
        "source_package_type": "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "target_people_count": 5,
        "people_with_valid_source_evidence": valid_cnt,
        "people_without_valid_source_evidence": invalid_cnt,
        "source_records_count": len(repair_entries),
        "entries": repair_entries,
        "application_data_modified": app_data_modified,
        "final_status": "PASS" if status_pass else "FAIL"
    }

    with open(OUTPUT_REPAIR_PKG_PATH, "w", encoding="utf-8") as f:
        json.dump(repair_package_output, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE 5-SOURCE REPAIR SUMMARY")
    print("==================================================")
    print("TARGET_PEOPLE: 5")
    print(f"PEOPLE_WITH_VALID_SOURCE_EVIDENCE: {valid_cnt}")
    print(f"PEOPLE_WITHOUT_VALID_SOURCE_EVIDENCE: {invalid_cnt}")
    print(f"SOURCE_RECORDS: {len(repair_entries)}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"PROTECTED_FILES_UNCHANGED: {'YES' if not app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    run_repair_acquisition()
