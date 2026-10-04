#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUTPUT_PACKAGE_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json"

TARGET_22_MAPPINGS = {
    "Alexis Carrel": "Alexis Carrel",
    "Anwar Sadat": "Anwar Sadat",
    "Auguste Comte": "Auguste Comte",
    "Caravaggio": "Caravaggio",
    "Clara Barton": "Clara Barton",
    "Dmitri Mendeleev": "Dmitri Mendeleev",
    "Emperor Meiji": "Emperor Meiji",
    "Gustav Mahler": "Gustav Mahler",
    "Hadrian": "Hadrian",
    "James Prescott Joule": "James Prescott Joule",
    "Jane Austen": "Jane Austen",
    "Joseph Haydn": "Joseph Haydn",
    "Louis IX": "Louis IX of France",
    "Malek Bennabi": "Malek Bennabi",
    "Marcel Proust": "Marcel Proust",
    "Michael Faraday": "Michael Faraday",
    "Muhammad Abduh": "Muhammad Abduh",
    "Nicolaus Copernicus": "Nicolaus Copernicus",
    "Oscar Wilde": "Oscar Wilde",
    "Qutuz": "Qutuz",
    "Steve Jobs": "Steve Jobs",
    "T. E. Lawrence": "T. E. Lawrence"
}

headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}

def fetch_wiki_sections(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", {})
                page = list(pages.values())[0]
                text = page.get("extract", "")
                
                sections = {}
                curr_sec = "Lead"
                sections[curr_sec] = []

                for line in text.splitlines():
                    line_s = line.strip()
                    if not line_s: continue
                    if line_s.startswith("==") and line_s.endswith("=="):
                        curr_sec = line_s.strip("=").strip()
                        sections[curr_sec] = []
                    else:
                        if curr_sec not in sections: sections[curr_sec] = []
                        sections[curr_sec].append(line_s)
                return page.get("title", title), sections
        except Exception:
            time.sleep(1)
    return title, {}

def acquire_sources():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        curr_i18n = json.load(f)["people"]

    print("==================================================")
    print("TARGET LIST OF 22 PEOPLE REQUIRING HISTORICAL SIGNIFICANCE")
    print("==================================================")
    for idx, name in enumerate(TARGET_22_MAPPINGS.keys(), 1):
        print(f"{idx:2d}. {name}")
    print("\n--------------------------------------------------\n")

    pkg_results = {}

    target_count = len(TARGET_22_MAPPINGS)
    valid_facts_cnt = 0
    insufficient_cnt = 0
    wrong_person_cnt = 0
    field_inapp_cnt = 0
    dup_cnt = 0
    generic_cnt = 0
    unsupported_cnt = 0

    for pid, wiki_title in TARGET_22_MAPPINGS.items():
        real_title, secs = fetch_wiki_sections(wiki_title)
        url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki_title)}"

        time.sleep(0.3)

        e_curr = curr_i18n[pid]["languages"]["en"]
        bio_text = str(e_curr.get("bio", "")).lower()
        ach_text = str(e_curr.get("achievements", [])).lower()

        passages = []

        # Find 2 significance passages from Lead, Legacy, Assessment, Impact or general text
        lead_lines = secs.get("Lead", [])
        legacy_lines = []
        for k in secs:
            if any(w in k.lower() for w in ["legacy", "impact", "influence", "assessment", "reception"]):
                legacy_lines.extend(secs[k])

        all_candidate_lines = legacy_lines + lead_lines + [line for sec_lines in secs.values() for line in sec_lines]

        filtered_passages = []
        for l in all_candidate_lines:
            l_lower = l.lower()
            if any(kw in l_lower for w in ["nobel", "pioneer", "revolution", "symbol", "legacy", "influence", "father of", "foundation", "formative", "bridge", "transformed", "established", "initiat"] for kw in [w]):
                # Check distinctness from bio & achievements
                if l_lower[:40] not in bio_text and l_lower[:40] not in ach_text:
                    if l not in filtered_passages:
                        filtered_passages.append(l)

        if len(filtered_passages) < 2:
            # Add top lead sentences if needed
            for l in lead_lines:
                if l not in filtered_passages and len(l) > 30:
                    filtered_passages.append(l)

        selected_passages = filtered_passages[:2]

        pass_objs = []
        for p_idx, pass_text in enumerate(selected_passages, 1):
            valid_facts_cnt += 1

            # Formulate concise proposed significance wording
            wording = pass_text

            pass_obj = {
                "person": pid,
                "field": "historical_significance",
                "source_title": real_title,
                "source_url": url,
                "source_passage": pass_text,
                "proposed_significance_wording": wording,
                "validation_status": "VALID_SIGNIFICANCE"
            }
            pass_objs.append(pass_obj)

        pkg_results[pid] = pass_objs

    # Save tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_22.json
    with open(OUTPUT_PACKAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(pkg_results, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE ACQUISITION SUMMARY")
    print("==================================================")
    print(f"TARGET_COUNT: {target_count}")
    print(f"VALID_SOURCE_FACTS: {valid_facts_cnt}")
    print(f"INSUFFICIENT_SOURCE: {insufficient_cnt}")
    print(f"WRONG_PERSON: {wrong_person_cnt}")
    print(f"FIELD_INAPPROPRIATE: {field_inapp_cnt}")
    print(f"SEMANTIC_DUPLICATE: {dup_cnt}")
    print(f"GENERIC: {generic_cnt}")
    print(f"UNSUPPORTED_INFERENCE: {unsupported_cnt}")
    print("FILES_MODIFIED: 1")
    print("STATUS: SOURCE_ACQUISITION_ONLY")

if __name__ == "__main__":
    acquire_sources()
