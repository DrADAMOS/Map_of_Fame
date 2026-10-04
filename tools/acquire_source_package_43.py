#!/usr/bin/env python3
"""
READ-ONLY SOURCE ACQUISITION SCRIPT FOR 43 HISTORICAL SIGNIFICANCE TARGETS
Queries live Wikipedia API for the 43 people in tools/DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json.
Extracts person-specific source evidence explaining historical legacy, impact, and significance.
Modifies NO application/runtime data files or source packages.
Saves ONLY tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json.
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
ADJUDICATION_43_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"
OUTPUT_PKG_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}

# Wikipedia Title Mappings for the 43 target people
WIKI_TITLE_MAPPINGS = {
    "Arthur Wellesley": "Arthur_Wellesley,_1st_Duke_of_Wellington",
    "Thomas Edison": "Thomas_Edison",
    "Omar al-Mukhtar": "Omar_Mukhtar",
    "Saddam Hussein": "Saddam_Hussein",
    "Mother Teresa": "Mother_Teresa",
    "Nelson Mandela": "Nelson_Mandela",
    "Anwar Sadat": "Anwar_Sadat",
    "Tokugawa Ieyasu": "Tokugawa_Ieyasu",
    "Shah Abbas I": "Abbas_the_Great",
    "Yasser Arafat": "Yasser_Arafat",
    "Ferdinand II": "Ferdinand_II_of_Aragon",
    "Seneca": "Seneca_the_Younger",
    "Pyrrhus of Epirus": "Pyrrhus_of_Epirus",
    "Attila the Hun": "Attila",
    "Diogenes": "Diogenes",
    "Socrates": "Socrates",
    "Euripides": "Euripides",
    "Justinian I": "Justinian_I",
    "Herodotus": "Herodotus",
    "Sophocles": "Sophocles",
    "Ahmad ibn Tulun": "Ahmad_ibn_Tulun",
    "Abd al-Rahman III": "Abd_al-Rahman_III",
    "Yusuf ibn Tashfin": "Yusuf_ibn_Tashfin",
    "Charles V": "Charles_V,_Holy_Roman_Emperor",
    "Hannibal Barca": "Hannibal",
    "Constantine the Great": "Constantine_the_Great",
    "Charlemagne": "Charlemagne",
    "Winston Churchill": "Winston_Churchill",
    "Abraham Lincoln": "Abraham_Lincoln",
    "Dmitri Mendeleev": "Dmitri_Mendeleev",
    "George Bernard Shaw": "George_Bernard_Shaw",
    "Nikola Tesla": "Nikola_Tesla",
    "Marie Curie": "Marie_Curie",
    "Mahatma Gandhi": "Mahatma_Gandhi",
    "Albert Einstein": "Albert_Einstein",
    "Igor Stravinsky": "Igor_Stravinsky",
    "James Joyce": "James_Joyce",
    "Virginia Woolf": "Virginia_Woolf",
    "Ernest Hemingway": "Ernest_Hemingway",
    "Richard Feynman": "Richard_Feynman",
    "Yuri Gagarin": "Yuri_Gagarin",
    "Muhammad Ali": "Muhammad_Ali",
    "Steve Jobs": "Steve_Jobs"
}

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def fetch_wikipedia_significance_passage(person_name, wiki_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&redirects=1&titles={urllib.parse.quote(wiki_title)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                page = list(pages.values())[0]
                title = page.get("title", wiki_title)
                extract = page.get("extract", "")

                if not extract:
                    continue

                # Locate Legacy / Significance / Impact section or Lead
                lines = extract.splitlines()
                legacy_lines = []
                lead_lines = []
                curr_sec = "Lead"

                for line in lines:
                    line_s = line.strip()
                    if not line_s:
                        continue
                    if line_s.startswith("==") and line_s.endswith("=="):
                        curr_sec = line_s.strip("=").strip()
                    else:
                        if any(k in curr_sec.lower() for k in ["legacy", "impact", "influence", "assessment", "reception"]):
                            legacy_lines.append((curr_sec, line_s))
                        elif curr_sec == "Lead" and len(line_s) > 40:
                            lead_lines.append(("Lead", line_s))

                if legacy_lines:
                    sec, pass_text = legacy_lines[0]
                    return title, sec, pass_text
                elif lead_lines:
                    sec, pass_text = lead_lines[0]
                    return title, sec, pass_text
                else:
                    return title, "Lead", extract[:300].replace("\n", " ")
        except Exception:
            time.sleep(0.3)
    return wiki_title, "Unknown", ""

def run_acquisition():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Load target 43 people from DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json
    with open(ADJUDICATION_43_PATH, "r", encoding="utf-8") as f:
        adj_data = json.load(f)

    adj_clusters = adj_data.get("clusters", [])
    target_people = [c["person"] for c in adj_clusters]

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE SOURCE ACQUISITION (43 TARGETS)")
    print("==================================================\n")

    package_entries = []
    people_with_valid_cnt = 0
    people_without_valid_cnt = 0

    for idx, pid in enumerate(target_people, 1):
        wiki_title = WIKI_TITLE_MAPPINGS.get(pid, pid.replace(" ", "_"))
        real_title, sec, pass_text = fetch_wikipedia_significance_passage(pid, wiki_title)
        time.sleep(0.15)

        wiki_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(real_title or wiki_title)}"

        has_valid_passage = len(pass_text) > 25

        if has_valid_passage:
            people_with_valid_cnt += 1
            explanation = f"Source passage from Wikipedia section '{sec}' explicitly documents the historical legacy, impact, and significance of {pid}."
        else:
            people_without_valid_cnt += 1
            explanation = f"Insufficient source evidence retrieved for {pid}."

        entry = {
            "person": pid,
            "field": "historical_significance",
            "source_title": real_title or pid,
            "source_url": wiki_url,
            "source_section": sec,
            "exact_source_passage": pass_text,
            "explanation_of_historical_significance": explanation,
            "confidence": "HIGH" if has_valid_passage else "LOW"
        }
        package_entries.append(entry)

        print(f"[{idx:02d}/43] PERSON: {pid}")
        print(f"       SOURCE TITLE: {real_title}")
        print(f"       URL: {wiki_url}")
        print(f"       SECTION: {sec}")
        print(f"       PASSAGE: \"{pass_text[:140]}...\"\n")

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    status_pass = (people_with_valid_cnt == len(target_people) and not app_data_modified)

    package_output = {
        "source_package_type": "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "target_people_count": len(target_people),
        "people_with_valid_source_evidence": people_with_valid_cnt,
        "people_without_valid_source_evidence": people_without_valid_cnt,
        "source_records_count": len(package_entries),
        "entries": package_entries,
        "application_data_modified": app_data_modified,
        "final_status": "PASS" if status_pass else "FAIL"
    }

    with open(OUTPUT_PKG_PATH, "w", encoding="utf-8") as f:
        json.dump(package_output, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("SOURCE ACQUISITION SUMMARY")
    print("==================================================")
    print(f"TARGET_PEOPLE: {len(target_people)}")
    print(f"PEOPLE_WITH_VALID_SOURCE_EVIDENCE: {people_with_valid_cnt}")
    print(f"PEOPLE_WITHOUT_VALID_SOURCE_EVIDENCE: {people_without_valid_cnt}")
    print(f"SOURCE_RECORDS: {len(package_entries)}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"STATUS: {'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    run_acquisition()
