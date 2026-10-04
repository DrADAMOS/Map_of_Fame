#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}

def fetch_wiki_text(title):
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote(title)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            page = list(pages.values())[0]
            return page.get("title", title), page.get("extract", "")
    except Exception as e:
        print(f"Error fetching {title}: {e}")
        return title, ""

claims = [
    ("Caravaggio", 1, "Contarelli Chapel commission / The Martyrdom of Saint Matthew / The Calling of Saint Matthew", "Caravaggio", "Contarelli Chapel", ["Most famous painter in Rome", "Biography"]),
    ("Caravaggio", 2, "Chiaroscuro / tenebrism", "Caravaggio", "tenebrism", ["As an artist", "Style", "Lead"]),
    ("Giuseppe Verdi", 3, "Rigoletto, Il trovatore, La traviata", "Giuseppe_Verdi", "Rigoletto", ["Middle period", "Life", "Lead"]),
    ("Giuseppe Verdi", 4, "Aida / Cairo Opera House / 1871", "Giuseppe_Verdi", "Aida", ["Middle period", "Life", "Lead"]),
    ("Igor Stravinsky", 5, "The Firebird, Petrushka, The Rite of Spring", "Igor_Stravinsky", "Firebird", ["Russian period", "Life", "Lead"]),
    ("Igor Stravinsky", 6, "Oedipus Rex, Apollon musagète, Symphony of Psalms", "Igor_Stravinsky", "Oedipus", ["Neoclassical period", "Music", "Lead"]),
    ("James Clerk Maxwell", 7, "Classical theory of electromagnetic radiation", "James_Clerk_Maxwell", "electromagnetic radiation", ["Electromagnetism", "Lead"]),
    ("James Clerk Maxwell", 8, "1861 color photograph / Maxwell's three-color analysis / Thomas Sutton", "James_Clerk_Maxwell", "color photograph", ["Color analysis", "Scientific legacy", "Lead"]),
    ("James Prescott Joule", 9, "Relationship between heat and mechanical work", "James_Prescott_Joule", "mechanical work", ["The mechanical equivalent of heat", "Lead"]),
    ("James Prescott Joule", 10, "Joule's law / Joule's first law", "James_Prescott_Joule", "Joule's law", ["Joule's law", "Published work", "Lead"]),
    ("Jane Austen", 11, "Sense and Sensibility, Pride and Prejudice, Mansfield Park, Emma", "Jane_Austen", "Sense and Sensibility", ["Ages 34 to 41", "Lead"]),
    ("Jane Austen", 12, "Northanger Abbey and Persuasion", "Jane_Austen", "Northanger Abbey", ["Posthumous publication", "Lead"]),
    ("Marcel Proust", 13, "In Search of Lost Time", "Marcel_Proust", "In Search of Lost Time", ["In Search of Lost Time", "Lead"]),
    ("Marcel Proust", 14, "Prix Goncourt, 1919", "Marcel_Proust", "Prix Goncourt", ["In Search of Lost Time", "Biography", "Lead"]),
    ("Marcus Aurelius", 15, "Meditations", "Marcus_Aurelius", "Meditations", ["Philosophy", "Writings", "Lead"]),
    ("Marcus Aurelius", 16, "Marcomannic War / Danube frontier", "Marcus_Aurelius", "Marcomannic War", ["Emperor", "Marcomannic Wars", "Lead"]),
    ("Nicolaus Copernicus", 17, "De revolutionibus orbium coelestium", "Nicolaus_Copernicus", "De revolutionibus", ["Copernican system", "Lead"]),
    ("Nicolaus Copernicus", 18, "Monetae cudendae ratio / early quantity theory of money", "Nicolaus_Copernicus", "Monetae cudendae ratio", ["Life", "Monetary reform", "Lead"]),
    ("Qutuz", 19, "Battle of Ain Jalut", "Qutuz", "Ain Jalut", ["Battle of Ain Jalut", "Lead"]),
    ("Qutuz", 20, "Battle of Fariskur / Seventh Crusade", "Qutuz", "Fariskur", ["Seventh Crusade", "Background", "Lead"]),
    ("Rosa Parks", 21, "Refusal to vacate her bus seat on December 1, 1955", "Rosa_Parks", "vacate", ["Arrest and bus boycott", "Refusal to move", "Lead"]),
    ("Rosa Parks", 22, "Her action and the Montgomery bus boycott as symbols of the civil rights movement", "Rosa_Parks", "symbols", ["Arrest and bus boycott", "Legacy and honors", "Lead"])
]

def main():
    wiki_texts = {}
    found_cnt = 0
    not_found_cnt = 0

    for person, cid, claim, wiki_title, kw, sec_kws in claims:
        if wiki_title not in wiki_texts:
            real_title, text = fetch_wiki_text(wiki_title)
            wiki_texts[wiki_title] = (real_title, text)

        real_title, text = wiki_texts[wiki_title]
        url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki_title)}"

        # Parse sections
        curr_sec = "Lead"
        sec_map = {curr_sec: []}
        for line in text.splitlines():
            line_s = line.strip()
            if not line_s:
                continue
            if line_s.startswith("==") and line_s.endswith("=="):
                curr_sec = line_s.strip("=").strip()
                sec_map[curr_sec] = []
            else:
                if curr_sec not in sec_map:
                    sec_map[curr_sec] = []
                sec_map[curr_sec].append(line_s)

        found_sec = None
        found_line = None

        # Search preferred sections first
        for sec_name, lines in sec_map.items():
            if any(sk.lower() in sec_name.lower() for sk in sec_kws):
                for l in lines:
                    if kw.lower() in l.lower():
                        found_sec = sec_name
                        found_line = l
                        break
            if found_line:
                break

        # Fallback search across all sections if not found in preferred
        if not found_line:
            for sec_name, lines in sec_map.items():
                for l in lines:
                    if kw.lower() in l.lower():
                        found_sec = sec_name
                        found_line = l
                        break
                if found_line:
                    break

        if found_line:
            found_cnt += 1
            passage = found_line
        else:
            not_found_cnt += 1
            found_sec = "N/A"
            passage = "NOT FOUND"

        print(f"PERSON: {person}")
        print(f"CLAIM_ID: {cid}")
        print(f"CLAIM: {claim}")
        print(f"SOURCE_TITLE: {real_title}")
        print(f"SOURCE_URL: {url}")
        print(f"ACTUAL_SOURCE_SECTION: {found_sec}")
        print(f"ACTUAL_SOURCE_PASSAGE: \"{passage}\"\n")

    print(f"TOTAL_CLAIMS = {len(claims)}")
    print(f"PASSAGES_FOUND = {found_cnt}")
    print(f"PASSAGES_NOT_FOUND = {not_found_cnt}")
    print("FILES_MODIFIED = 0\n")
    print("STATUS: EXTRACTION_ONLY")

if __name__ == "__main__":
    main()
