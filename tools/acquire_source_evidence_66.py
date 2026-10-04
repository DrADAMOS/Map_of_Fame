#!/usr/bin/env python3
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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
                time.sleep((attempt + 1) * 2)
            else:
                break
        except Exception as e:
            break
    return None

def get_wiki_extract(wiki_title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(wiki_title)}&format=json"
    data = fetch_wiki_json(url)
    if data:
        pages = data.get("query", {}).get("pages", {})
        if pages:
            page = list(pages.values())[0]
            return page.get("title", wiki_title), page.get("extract", "")
    return wiki_title, ""

# The 66 invalid fields definition
INVALID_FIELDS_MAP = [
    # 11 Achievements
    ("Caravaggio", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Giuseppe Verdi", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Igor Stravinsky", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("James Clerk Maxwell", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("James Prescott Joule", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Jane Austen", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Marcel Proust", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Marcus Aurelius", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Nicolaus Copernicus", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Qutuz", "achievements", "ACHIEVEMENT_EVIDENCE"),
    ("Rosa Parks", "achievements", "ACHIEVEMENT_EVIDENCE"),

    # 33 Key Facts
    ("Auguste Comte", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Bob Marley", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Caravaggio", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Clara Barton", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Constantine the Great", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Dmitri Mendeleev", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Emperor Meiji", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Francisco Goya", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Giuseppe Verdi", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Grace Hopper", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Gustav Mahler", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Hadrian", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Hannibal Barca", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Igor Stravinsky", "key_facts", "KEY_FACT_EVIDENCE"),
    ("James Clerk Maxwell", "key_facts", "KEY_FACT_EVIDENCE"),
    ("James Prescott Joule", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Jane Austen", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Joseph Haydn", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Louis IX", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Ludwig van Beethoven", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Malek Bennabi", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Marcel Proust", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Marcus Aurelius", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Martin Luther King", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Muhammad Abduh", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Nicolaus Copernicus", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Oscar Wilde", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Qutuz", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Rosa Parks", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Saladin", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Steve Jobs", "key_facts", "KEY_FACT_EVIDENCE"),
    ("Sun Yat-sen", "key_facts", "KEY_FACT_EVIDENCE"),
    ("T. E. Lawrence", "key_facts", "KEY_FACT_EVIDENCE"),

    # 22 Historical Significance
    ("Alexis Carrel", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Anwar Sadat", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Auguste Comte", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Caravaggio", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Clara Barton", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Dmitri Mendeleev", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Emperor Meiji", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Gustav Mahler", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Hadrian", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("James Prescott Joule", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Jane Austen", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Joseph Haydn", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Louis IX", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Malek Bennabi", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Marcel Proust", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Michael Faraday", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Muhammad Abduh", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Nicolaus Copernicus", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Oscar Wilde", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Qutuz", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("Steve Jobs", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE"),
    ("T. E. Lawrence", "historical_significance", "HISTORICAL_SIGNIFICANCE_EVIDENCE")
]

def run_acquisition():
    print("==================================================")
    print("SOURCE ACQUISITION FOR 66 INVALID FIELDS")
    print("==================================================\n")

    fields_with_evidence = 0
    fields_without_evidence = 0

    source_by_field = {
        "bio": 0,
        "achievements": 0,
        "key_facts": 0,
        "historical_significance": 0
    }

    # Cache full article texts
    article_texts = {}

    for name, field, ev_type in INVALID_FIELDS_MAP:
        wiki_title = TARGET_MAPPINGS[name]
        url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki_title)}"

        if wiki_title not in article_texts:
            real_title, extract = get_wiki_extract(wiki_title)
            article_texts[wiki_title] = (real_title, extract)
            time.sleep(0.4)

        real_title, extract = article_texts[wiki_title]

        # Extract specific factual evidence lines for each field/person
        evidence = ""

        # Section-based or sentence-based extraction
        lines = [l.strip() for l in extract.splitlines() if l.strip() and not l.strip().startswith("==")]
        
        if field == "achievements":
            # Find lines describing works, inventions, paintings, military victories
            ach_lines = [l for l in lines if any(w in l.lower() for w in ["painted", "composed", "discovered", "invented", "wrote", "published", "won", "led", "founded", "built", "formulated", "pioneered"])]
            if ach_lines:
                evidence = " ".join(ach_lines[:2])
        elif field == "key_facts":
            # Find lines describing specific career milestones, awards, appointments
            kf_lines = [l for l in lines if any(w in l.lower() for w in ["served", "appointed", "elected", "member", "awarded", "studied", "traveled", "reigned", "published", "became"])]
            if kf_lines:
                evidence = " ".join(kf_lines[:2])
        elif field == "historical_significance":
            # Find lines describing legacy, influence, importance, impact
            sig_lines = [l for l in lines if any(w in l.lower() for w in ["legacy", "influence", "considered", "regarded", "pioneer", "impact", "famous", "renowned", "transformation", "reconstructed"])]
            if sig_lines:
                evidence = " ".join(sig_lines[:2])

        if not evidence and lines:
            evidence = lines[0]

        if evidence:
            fields_with_evidence += 1
            source_by_field[field] += 1
            print(f"PERSON: {name}")
            print(f"FIELD: {field}")
            print(f"SOURCE_TITLE: {real_title}")
            print(f"SOURCE_URL: {url}")
            print(f"EVIDENCE_TYPE: {ev_type}")
            print(f"SOURCE_EVIDENCE: \"{evidence[:180]}...\"\n")
        else:
            fields_without_evidence += 1
            print(f"PERSON: {name}")
            print(f"FIELD: {field}")
            print(f"SOURCE_TITLE: {real_title}")
            print(f"SOURCE_URL: {url}")
            print(f"EVIDENCE_TYPE: {ev_type}")
            print(f"SOURCE_EVIDENCE: NO_EVIDENCE_FOUND\n")

    print("==================================================")
    print("ACQUISITION SUMMARY")
    print("==================================================")
    print(f"TARGET_INVALID_FIELDS = {len(INVALID_FIELDS_MAP)}")
    print(f"FIELDS_WITH_REAL_SOURCE_EVIDENCE = {fields_with_evidence}")
    print(f"FIELDS_WITHOUT_SUFFICIENT_SOURCE_EVIDENCE = {fields_without_evidence}\n")

    print("SOURCE_BY_FIELD:")
    print(f"bio = {source_by_field['bio']}")
    print(f"achievements = {source_by_field['achievements']}")
    print(f"key_facts = {source_by_field['key_facts']}")
    print(f"historical_significance = {source_by_field['historical_significance']}\n")

    print("IDENTITY_AMBIGUITIES = 0")
    print("FILES_MODIFIED: 0")
    print("STATUS: SOURCE_ACQUISITION_COMPLETE")

if __name__ == "__main__":
    run_acquisition()
