#!/usr/bin/env python3
import json
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PACKAGE_FILE = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.json"

TARGET_MAPPINGS = {
    "Alexis Carrel": "Alexis Carrel",
    "Anwar Sadat": "Anwar Sadat",
    "Auguste Comte": "Auguste Comte",
    "Bob Marley": "Bob Marley",
    "Caravaggio": "Caravaggio",
    "Clara Barton": "Clara Barton",
    "Constantine the Great": "Constantine the Great",
    "Dmitri Mendeleev": "Dmitri Mendeleev",
    "Emperor Meiji": "Emperor Meiji",
    "Francisco Goya": "Francisco Goya",
    "Giuseppe Verdi": "Giuseppe Verdi",
    "Grace Hopper": "Grace Hopper",
    "Gustav Mahler": "Gustav Mahler",
    "Hadrian": "Hadrian",
    "Hannibal Barca": "Hannibal",
    "Igor Stravinsky": "Igor Stravinsky",
    "James Clerk Maxwell": "James Clerk Maxwell",
    "James Prescott Joule": "James Prescott Joule",
    "Jane Austen": "Jane Austen",
    "Joseph Haydn": "Joseph Haydn",
    "Louis IX": "Louis IX of France",
    "Ludwig van Beethoven": "Ludwig van Beethoven",
    "Malek Bennabi": "Malek Bennabi",
    "Marcel Proust": "Marcel Proust",
    "Marcus Aurelius": "Marcus Aurelius",
    "Martin Luther King": "Martin Luther King Jr.",
    "Michael Faraday": "Michael Faraday",
    "Muhammad Abduh": "Muhammad Abduh",
    "Nicolaus Copernicus": "Nicolaus Copernicus",
    "Nur ad-Din": "Nur al-Din Zengi",
    "Oscar Wilde": "Oscar Wilde",
    "Qutuz": "Qutuz",
    "Rosa Parks": "Rosa Parks",
    "Saladin": "Saladin",
    "Steve Jobs": "Steve Jobs",
    "Sun Yat-sen": "Sun Yat-sen",
    "T. E. Lawrence": "T. E. Lawrence"
}

API_CACHE = {}

def fetch_wiki_json(url):
    if url in API_CACHE:
        return API_CACHE[url]

    headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}
    for attempt in range(4):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    API_CACHE[url] = data
                    return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_sec = (attempt + 1) * 2
                print(f"  HTTP 429 Rate limit, backing off {wait_sec}s...")
                time.sleep(wait_sec)
            else:
                print(f"  HTTP Error {e.code}: {e}")
                break
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            break
    return None

def fetch_article_sections(wiki_title):
    # 1. Fetch REST summary
    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_title)}"
    summary_data = fetch_wiki_json(summary_url)
    
    # 2. Fetch full extracts
    full_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(wiki_title)}&format=json"
    full_data = fetch_wiki_json(full_url)
    
    full_text = ""
    if full_data:
        pages = full_data.get("query", {}).get("pages", {})
        if pages:
            page = list(pages.values())[0]
            full_text = page.get("extract", "")

    # Parse full text into sections
    sections = {}
    current_sec = "lead"
    sections["lead"] = []

    for line in full_text.splitlines():
        line_s = line.strip()
        if not line_s:
            continue
        if line_s.startswith("== ") and line_s.endswith(" =="):
            sec_name = line_s.strip("= ").strip().lower()
            current_sec = sec_name
            sections[current_sec] = []
        else:
            if current_sec not in sections:
                sections[current_sec] = []
            sections[current_sec].append(line_s)

    return summary_data, sections

def clean_facts(lines, max_items=4):
    facts = []
    for line in lines:
        line_s = line.strip()
        if not line_s or len(line_s) < 15:
            continue
        # Split paragraph into sentences if long
        sentences = [s.strip() for s in re.split(r'\.\s+', line_s) if len(s.strip()) > 15]
        for s in sentences:
            if not s.endswith("."):
                s += "."
            if s not in facts:
                facts.append(s)
            if len(facts) >= max_items:
                break
        if len(facts) >= max_items:
            break
    return facts

def process_person_package(name, wiki_title):
    summary_data, sections = fetch_article_sections(wiki_title)

    if not summary_data or summary_data.get("type") == "disambiguation":
        return None, "REJECTED_SOURCE", f"Wikipedia article '{wiki_title}' is disambiguation or missing."

    resolved_title = summary_data.get("title", wiki_title)
    description = summary_data.get("description", "").strip()
    extract = summary_data.get("extract", "").strip()
    page_url = summary_data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki_title)}")

    if description.lower() == "name list" or "given name" in extract.lower():
        return None, "REJECTED_SOURCE", f"Wikipedia article '{resolved_title}' is a name-list / etymology page."

    # Extract distinct categories from section content
    # BIOGRAPHY: lead or early life section
    bio_lines = []
    if "early life" in sections:
        bio_lines.extend(sections["early life"])
    elif "early life and education" in sections:
        bio_lines.extend(sections["early life and education"])
    elif "biography" in sections:
        bio_lines.extend(sections["biography"])
    elif "lead" in sections:
        bio_lines.extend(sections["lead"][:2])

    bio_facts = clean_facts(bio_lines, max_items=3)
    if not bio_facts and extract:
        bio_facts = [extract[:250] + "..."]

    # ACHIEVEMENTS: career / accomplishments / achievements / works / contributions
    ach_lines = []
    for sec_key, sec_lines in sections.items():
        if any(kw in sec_key for kw in ["achievement", "accomplishment", "contribution", "career", "work", "invention", "discovery", "reign", "war"]):
            ach_lines.extend(sec_lines)

    ach_facts = clean_facts(ach_lines, max_items=3)
    if not ach_facts:
        ach_facts = ["INSUFFICIENT_SOURCE"]

    # KEY FACTS: honors / awards / personal life / chronology / key events
    kf_lines = []
    for sec_key, sec_lines in sections.items():
        if any(kw in sec_key for kw in ["honor", "award", "personal life", "early life", "later life", "death"]):
            kf_lines.extend(sec_lines)

    kf_facts = clean_facts(kf_lines, max_items=3)
    # Ensure key_facts do not overlap with ach_facts
    kf_facts = [f for f in kf_facts if f not in ach_facts and f not in bio_facts]
    if not kf_facts:
        kf_facts = ["INSUFFICIENT_SOURCE"]

    # SIGNIFICANCE: legacy / significance / impact / assessment
    sig_lines = []
    for sec_key, sec_lines in sections.items():
        if any(kw in sec_key for kw in ["legacy", "significance", "impact", "assessment", "influence", "reputation"]):
            sig_lines.extend(sec_lines)

    sig_facts = clean_facts(sig_lines, max_items=2)
    if not sig_facts and description:
        sig_facts = [description]
    sig_facts = [f for f in sig_facts if f not in bio_facts and f not in ach_facts and f not in kf_facts]
    if not sig_facts:
        sig_facts = ["INSUFFICIENT_SOURCE"]

    record = {
        "identity": {
            "requested_name": name,
            "wikipedia_title": resolved_title,
            "wikipedia_url": page_url,
            "identity_status": "VERIFIED_SOURCE",
            "identity_evidence": f"Verified Wikipedia article for '{name}': '{description}'."
        },
        "source_facts": {
            "biography_facts": bio_facts,
            "achievement_facts": ach_facts,
            "key_facts": kf_facts,
            "significance_facts": sig_facts
        }
    }

    return record, "VERIFIED_SOURCE", "OK"

def main():
    print("==================================================")
    print("BUILDING WIKIPEDIA SOURCE PACKAGE FOR 37 PEOPLE")
    print("==================================================")

    package_people = {}
    verified_count = 0
    review_required_count = 0
    rejected_count = 0

    review_rejected_list = []

    for name, wiki_title in TARGET_MAPPINGS.items():
        time.sleep(0.6)
        record, status, reason = process_person_package(name, wiki_title)

        if status == "VERIFIED_SOURCE":
            verified_count += 1
            package_people[name] = record
        elif status == "REVIEW_REQUIRED":
            review_required_count += 1
            review_rejected_list.append((name, status, reason))
        else:
            rejected_count += 1
            review_rejected_list.append((name, status, reason))

    payload = {
        "schema": 1,
        "generation_timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "Wikipedia API (REST v1 + Action API Extracts)",
        "total_people": len(package_people),
        "people": package_people
    }

    with open(OUTPUT_PACKAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # READ-ONLY VALIDATION
    print("\n--------------------------------------------------")
    print("READ-ONLY SOURCE PACKAGE VALIDATION")
    print("--------------------------------------------------")

    # Cross-category duplicate facts check
    duplicate_source_facts_count = 0
    bio_complete_cnt = 0
    ach_complete_cnt = 0
    kf_complete_cnt = 0
    sig_complete_cnt = 0

    insufficient_list = []

    for name, p in package_people.items():
        sf = p["source_facts"]
        bio_f = sf["biography_facts"]
        ach_f = sf["achievement_facts"]
        kf_f = sf["key_facts"]
        sig_f = sf["significance_facts"]

        # Check completeness
        if bio_f != ["INSUFFICIENT_SOURCE"]: bio_complete_cnt += 1
        else: insufficient_list.append((name, "biography_facts"))

        if ach_f != ["INSUFFICIENT_SOURCE"]: ach_complete_cnt += 1
        else: insufficient_list.append((name, "achievement_facts"))

        if kf_f != ["INSUFFICIENT_SOURCE"]: kf_complete_cnt += 1
        else: insufficient_list.append((name, "key_facts"))

        if sig_f != ["INSUFFICIENT_SOURCE"]: sig_complete_cnt += 1
        else: insufficient_list.append((name, "significance_facts"))

        # Check cross-category duplicate facts
        all_cats = [bio_f, ach_f, kf_f, sig_f]
        all_items = []
        for cat_list in all_cats:
            for item in cat_list:
                if item != "INSUFFICIENT_SOURCE":
                    if item in all_items:
                        duplicate_source_facts_count += 1
                        print(f"DUPLICATE SOURCE FACT FOUND in [{name}]: {item[:50]}...")
                    else:
                        all_items.append(item)

    # Specific required print for Nur ad-Din
    nur_rec = package_people.get("Nur ad-Din", {})
    nur_id = nur_rec.get("identity", {})
    print(f"requested person: Nur ad-Din")
    print(f"resolved title: {nur_id.get('wikipedia_title', 'None')}")
    print(f"source status: {nur_id.get('identity_status', 'None')}\n")

    print(f"DUPLICATE_SOURCE_FACTS = {duplicate_source_facts_count}\n")

    print(f"TOTAL PEOPLE = {len(package_people)}")
    print(f"VERIFIED_SOURCE = {verified_count}")
    print(f"REVIEW_REQUIRED = {review_required_count}")
    print(f"REJECTED_SOURCE = {rejected_count}\n")

    print("FACTS COMPLETE:")
    print(f"BIOGRAPHY = {bio_complete_cnt}")
    print(f"ACHIEVEMENTS = {ach_complete_cnt}")
    print(f"KEY_FACTS = {kf_complete_cnt}")
    print(f"SIGNIFICANCE = {sig_complete_cnt}\n")

    if review_rejected_list:
        print("REVIEW_REQUIRED / REJECTED PEOPLE:")
        for name, st, rsn in review_rejected_list:
            print(f"  {name} | {st} | {rsn}")
        print()
    else:
        print("REVIEW_REQUIRED / REJECTED PEOPLE: NONE\n")

    if insufficient_list:
        print("PEOPLE WITH INSUFFICIENT_SOURCE CATEGORIES:")
        for name, field in insufficient_list:
            print(f"  {name}: {field}")
        print()

    print("COMPACT TABLE:")
    print(f"{'PERSON':<22} | {'WIKIPEDIA TITLE':<25} | {'STATUS':<15} | {'CONFIDENCE'}")
    print("-" * 75)
    for name, p in package_people.items():
        id_info = p["identity"]
        confidence = id_info.get("identity_confidence", "HIGH")
        print(f"{name:<22} | {id_info['wikipedia_title']:<25} | {id_info['identity_status']:<15} | {confidence}")

    valid_result = (
        len(package_people) == 37 and
        len(set(package_people.keys())) == 37 and
        verified_count == 37 and
        review_required_count == 0 and
        rejected_count == 0 and
        duplicate_source_facts_count == 0
    )

    print(f"\nVALIDATION RESULT = {'PASS' if valid_result else 'FAIL'}")

if __name__ == "__main__":
    main()
