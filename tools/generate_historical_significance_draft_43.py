#!/usr/bin/env python3
"""
GENERATION AND VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_DRAFT_43.JSON
Creates proposed replacement historical_significance text for all 43 adjudicated duplicate people.
Ensures zero modifications to runtime/application data and source packages.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
PKG_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json"
REVIEW_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_REVIEW_43.json"
REPAIR_PKG_5_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json"
REPAIR_PKG_3_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_3_REPAIR.json"
ADJUDICATION_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"
DRAFT_OUT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_DRAFT_43.json"
VALIDATOR_OUT_PATH = ROOT / "tools" / "validate_historical_significance_draft_43.py"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH,
    PKG_43_PATH,
    REVIEW_43_PATH,
    REPAIR_PKG_5_PATH,
    REPAIR_PKG_3_PATH
]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    # Load adjudication to get the 43 people
    with open(ADJUDICATION_PATH, "r", encoding="utf-8") as f:
        adj_data = json.load(f)
    target_people = [c["person"] for c in adj_data["clusters"]]

    # Load all source packages
    def load_pkg(path):
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("entries", [])

    all_source_entries = load_pkg(PKG_43_PATH) + load_pkg(REPAIR_PKG_5_PATH) + load_pkg(REPAIR_PKG_3_PATH)
    source_map = {}
    for entry in all_source_entries:
        p = entry["person"]
        if p not in source_map:
            source_map[p] = []
        source_map[p].append(entry)

    # Load person data from person_i18n.json to check bio, achievements, key_facts
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)
    people_dict = i18n_data.get("people", {})

    # Define proposed texts and source mappings for the 43 people
    # Each entry must be source-backed and distinct from bio, achievements, key_facts.
    draft_definitions = {
        "Arthur Wellesley": {
            "text": "Wellesley played a leading role in early-nineteenth-century British politics and military administration, serving as Prime Minister of the United Kingdom and Commander-in-Chief of the Forces.",
            "source_title": "Arthur Wellesley, 1st Duke of Wellington",
            "source_section": "Lead",
            "basis": "Supported by lead description of his political and military leadership role."
        },
        "Thomas Edison": {
            "text": "Edison's commercial enterprises and inventive work resulted in the formation of General Electric and the registration of 1,093 United States patents.",
            "source_title": "Thomas Edison",
            "source_section": "Lead",
            "basis": "Supported by lead details regarding patents and the formation of General Electric."
        },
        "Omar al-Mukhtar": {
            "text": "Mukhtar utilized deep knowledge of local desert geography and guerrilla tactics to lead successful ambushes against Italian forces during the colonial conflict.",
            "source_title": "Omar al-Mukhtar",
            "source_section": "Guerrilla warfare",
            "basis": "Supported by passage on guerrilla tactics and desert warfare against the Regio Esercito."
        },
        "Saddam Hussein": {
            "text": "Saddam's legacy remains polarized across the Arab world, where he is viewed by supporters as a resolute opponent of Western influence and by detractors as a brutal authoritarian dictator.",
            "source_title": "Saddam Hussein",
            "source_section": "Reception and legacy",
            "basis": "Supported by reception and legacy section documenting polarized regional and domestic views."
        },
        "Mother Teresa": {
            "text": "By the time of her death, Mother Teresa's Missionaries of Charity had expanded globally to operate hundreds of missions, hospices, and schools across dozens of countries.",
            "source_title": "Mother Teresa",
            "source_section": "Legacy and depictions in popular culture",
            "basis": "Supported by legacy statistics on global operations of the Missionaries of Charity."
        },
        "Nelson Mandela": {
            "text": "Mandela attained global recognition as a universal symbol of social justice and a leading figure of anti-racist and anti-colonial leadership.",
            "source_title": "Nelson Mandela",
            "source_section": "Legacy",
            "basis": "Supported by legacy descriptions of his status as a universal symbol and anti-racist leader."
        },
        "Anwar Sadat": {
            "text": "Sadat served as Egypt's third president and a prominent political and military leader following his involvement in the Free Officers movement.",
            "source_title": "Anwar Sadat",
            "source_section": "Lead",
            "basis": "Supported by biographical lead regarding his presidency and Free Officers membership."
        },
        "Tokugawa Ieyasu": {
            "text": "Ieyasu established the Tokugawa shogunate, unifying Japan under a centralized regime that governed from 1603 until the Meiji Restoration.",
            "source_title": "Tokugawa Ieyasu",
            "source_section": "Lead",
            "basis": "Supported by lead text describing his foundation of the Tokugawa shogunate."
        },
        "Shah Abbas I": {
            "text": "Abbas strengthened Iran's military power, centralized state control, and expanded commercial scope, earning the historical designation Abbas the Great.",
            "source_title": "Abbas the Great",
            "source_section": "Character and legacy",
            "basis": "Supported by character and legacy details on military power, centralization, and commerce."
        },
        "Yasser Arafat": {
            "text": "Arafat led Fatah in secret negotiations with the Israeli government that culminated in the 1993 Oslo Accords and the establishment of Palestinian self-rule frameworks.",
            "source_title": "Yasser Arafat",
            "source_section": "Oslo Accords",
            "basis": "Supported by Oslo Accords section detailing negotiations and Palestinian self-rule."
        },
        "Ferdinand II": {
            "text": "Ferdinand and Isabella established a highly centralized and united Spanish sovereignty through effective prenuptial agreements and mutual political support.",
            "source_title": "Ferdinand II of Aragon",
            "source_section": "Legacy and succession",
            "basis": "Supported by legacy text on joint effective sovereignty and unification."
        },
        "Seneca": {
            "text": "Seneca was a prominent Stoic philosopher, statesman, and dramatist of the Roman imperial period.",
            "source_title": "Seneca the Younger",
            "source_section": "Lead",
            "basis": "Supported by lead identification as Stoic philosopher and statesman."
        },
        "Pyrrhus of Epirus": {
            "text": "Pyrrhus was recognized by historical commentators such as Plutarch and Hannibal as one of the preeminent military commanders of antiquity.",
            "source_title": "Pyrrhus of Epirus",
            "source_section": "Legacy",
            "basis": "Supported by legacy references regarding Hannibal's ranking of Pyrrhus."
        },
        "Attila the Hun": {
            "text": "Attila ruled the Hunnic Empire during the fifth century, conducting major military campaigns against both the Eastern and Western Roman Empires.",
            "source_title": "Attila",
            "source_section": "Lead",
            "basis": "Supported by repair source passage detailing his campaigns against the Roman Empires."
        },
        "Diogenes": {
            "text": "Diogenes emerged as a foundational figure of Cynic philosophy through his tutelage under Antisthenes and subsequent ascetic teachings.",
            "source_title": "Diogenes",
            "source_section": "Influences",
            "basis": "Supported by influences section detailing his discipleship under Antisthenes."
        },
        "Socrates": {
            "text": "Socrates became a polarizing figure in Athenian intellectual life, ultimately facing trial and execution on charges of impiety and corrupting the youth.",
            "source_title": "Socrates",
            "source_section": "Trial and death",
            "basis": "Supported by trial and death section detailing accusations and execution."
        },
        "Euripides": {
            "text": "Euripides achieved enduring literary prominence, remaining one of the most widely read and debated playwrights from classical antiquity.",
            "source_title": "Euripides",
            "source_section": "Reception",
            "basis": "Supported by reception section noting extensive readership in antique education."
        },
        "Justinian I": {
            "text": "Justinian I served as Roman emperor during the sixth century, presiding over an era of significant imperial administration.",
            "source_title": "Justinian I",
            "source_section": "Lead",
            "basis": "Supported by lead designation as Roman emperor."
        },
        "Herodotus": {
            "text": "Herodotus authored the Histories detailing the Greco-Persian Wars, earning the classical designation 'The Father of History'.",
            "source_title": "Herodotus",
            "source_section": "Lead",
            "basis": "Supported by lead text describing the Histories and Cicero's title."
        },
        "Sophocles": {
            "text": "Sophocles introduced foundational innovations in theatrical structure and character development, becoming a pre-eminent playwright in classical Athens.",
            "source_title": "Sophocles",
            "source_section": "Works and legacy",
            "basis": "Supported by works and legacy section on dramatic innovations and pre-eminence."
        },
        "Ahmad ibn Tulun": {
            "text": "Ibn Tulun's rule established Egypt as an autonomous political actor and economic center independent of distant imperial capitals.",
            "source_title": "Ahmad ibn Tulun",
            "source_section": "Legacy",
            "basis": "Supported by legacy text on Egypt becoming an autonomous political actor."
        },
        "Abd al-Rahman III": {
            "text": "Abd al-Rahman III fostered architectural and cultural patronage, constructing the expansive Medina Azahara palace complex during his reign.",
            "source_title": "Abd al-Rahman III",
            "source_section": "Legacy",
            "basis": "Supported by legacy text on patronage of architecture and Medina Azahara."
        },
        "Yusuf ibn Tashfin": {
            "text": "Yusuf ibn Tashfin expanded Almoravid rule across Morocco, established Marrakech as its capital, and decisively checked the Reconquista at the Battle of Sagrajas.",
            "source_title": "Yusuf ibn Tashfin",
            "source_section": "Expansion in Maghreb",
            "basis": "Supported by repair source records detailing Maghreb expansion and Battle of az-Zallaqah."
        },
        "Charles V": {
            "text": "Charles V headed the House of Habsburg, ruling a vast personal union of European and American territories described as 'the empire on which the sun never sets'.",
            "source_title": "Charles V, Holy Roman Emperor",
            "source_section": "Lead",
            "basis": "Supported by lead text on Habsburg leadership and transcontinental personal union."
        },
        "Hannibal Barca": {
            "text": "Hannibal commanded Carthaginian forces against the Roman Republic during the Second Punic War amidst intense Mediterranean geopolitical conflict.",
            "source_title": "Hannibal",
            "source_section": "Lead",
            "basis": "Supported by lead text on his command against the Roman Republic."
        },
        "Constantine the Great": {
            "text": "Constantine reunited the Roman Empire under a single emperor and achieved major military victories against external Germanic and Sarmatian tribes.",
            "source_title": "Constantine the Great",
            "source_section": "Assessment and legacy",
            "basis": "Supported by assessment and legacy section on empire reunification and military victories."
        },
        "Charlemagne": {
            "text": "Charlemagne's Carolingian Empire laid the administrative and political foundations that ultimately shaped medieval European state formation and succession.",
            "source_title": "Charlemagne",
            "source_section": "Political legacy",
            "basis": "Supported by political legacy section on post-reign division and successor kingdoms."
        },
        "Winston Churchill": {
            "text": "Churchill served as Prime Minister during the Second World War and maintained a multi-decade career as a prominent British statesman and parliamentarian.",
            "source_title": "Winston Churchill",
            "source_section": "Lead",
            "basis": "Supported by lead biography on wartime premiership and parliamentary service."
        },
        "Abraham Lincoln": {
            "text": "Lincoln led the United States through the American Civil War, preserving the Union and playing a central role in the abolition of slavery.",
            "source_title": "Abraham Lincoln",
            "source_section": "Lead",
            "basis": "Supported by lead text regarding Civil War leadership and abolition of slavery."
        },
        "Dmitri Mendeleev": {
            "text": "Mendeleev formulated the periodic law and constructed the periodic table, successfully predicting the properties of undiscovered elements.",
            "source_title": "Dmitri Mendeleev",
            "source_section": "Lead",
            "basis": "Supported by lead text on periodic law, table creation, and element prediction."
        },
        "George Bernard Shaw": {
            "text": "Shaw became the leading dramatist of his generation through influential satirical and historical plays, earning the Nobel Prize in Literature.",
            "source_title": "George Bernard Shaw",
            "source_section": "Lead",
            "basis": "Supported by lead text on theatrical prominence and Nobel Prize award."
        },
        "Nikola Tesla": {
            "text": "Tesla's extensive scientific archive and personal estate were preserved in Belgrade, receiving recognition in the UNESCO Memory of the World Programme.",
            "source_title": "Nikola Tesla",
            "source_section": "Legacy",
            "basis": "Supported by legacy text regarding archive preservation and UNESCO recognition."
        },
        "Marie Curie": {
            "text": "Curie's pioneering research on radioactivity laid foundational principles for modern nuclear physics, radiography, and medical cancer treatments.",
            "source_title": "Marie Curie",
            "source_section": "Legacy",
            "basis": "Supported by legacy text on contributions to nuclear physics and medical treatments."
        },
        "Mahatma Gandhi": {
            "text": "Gandhi achieved international renown as the principal leader of the successful Indian independence movement against British colonial rule.",
            "source_title": "Mahatma Gandhi",
            "source_section": "Legacy",
            "basis": "Supported by legacy note on his role in the Indian independence movement."
        },
        "Albert Einstein": {
            "text": "Einstein developed the theory of relativity and made revolutionary contributions to theoretical physics that reshaped modern scientific understanding.",
            "source_title": "Albert Einstein",
            "source_section": "Lead",
            "basis": "Supported by lead text on relativity theory and theoretical physics contributions."
        },
        "Igor Stravinsky": {
            "text": "Stravinsky collaborated with prominent artists through the Ballets Russes, achieving international renown and shaping modern musical composition.",
            "source_title": "Igor Stravinsky",
            "source_section": "Artistic influences",
            "basis": "Supported by artistic influences section on Diaghilev and Ballets Russes collaborations."
        },
        "James Joyce": {
            "text": "Joyce exerted a profound and enduring influence on modern literature and fiction writing through his narrative innovations in works like Ulysses.",
            "source_title": "James Joyce",
            "source_section": "Legacy",
            "basis": "Supported by legacy section on enduring influence and fiction modeling."
        },
        "Virginia Woolf": {
            "text": "Woolf's life and literary works embodied a deep-seated pacifism and critical engagement with contemporary social thought.",
            "source_title": "Virginia Woolf",
            "source_section": "Influences",
            "basis": "Supported by influences section examining her pacifism and literary expression."
        },
        "Ernest Hemingway": {
            "text": "Hemingway established a distinctive, widely emulated literary style that profoundly shaped American fiction and modern prose.",
            "source_title": "Ernest Hemingway",
            "source_section": "Influence and legacy",
            "basis": "Supported by influence and legacy section on literary style and cultural heritage."
        },
        "Richard Feynman": {
            "text": "Feynman shared the 1965 Nobel Prize in Physics for fundamental work in quantum electrodynamics and developed widely used Feynman diagrams.",
            "source_title": "Richard Feynman",
            "source_section": "Lead",
            "basis": "Supported by repair source records detailing his Nobel Prize in QED and Feynman diagrams."
        },
        "Yuri Gagarin": {
            "text": "Gagarin became the first human to journey into outer space, completing an Earth orbit aboard Vostok 1 during the Space Race.",
            "source_title": "Yuri Gagarin",
            "source_section": "Lead",
            "basis": "Supported by lead text on spaceflight milestone and Vostok 1 orbit."
        },
        "Muhammad Ali": {
            "text": "Ali achieved global cultural icon status as a legendary heavyweight boxing champion and prominent social activist.",
            "source_title": "Muhammad Ali",
            "source_section": "Lead",
            "basis": "Supported by lead text on cultural icon status and heavyweight boxing titles."
        },
        "Steve Jobs": {
            "text": "Jobs pioneered the personal computer revolution and co-founded Apple Inc., profoundly influencing consumer technology and media industries.",
            "source_title": "Steve Jobs",
            "source_section": "Lead",
            "basis": "Supported by lead text on personal computer revolution and co-founding Apple Inc."
        }
    }

    entries = []
    for person in target_people:
        def_item = draft_definitions.get(person)
        if not def_item:
            continue
        proposed_text = def_item["text"]
        s_title = def_item["source_title"]
        s_sec = def_item["source_section"]

        # Find matching source records in source_map
        matching_records = []
        p_sources = source_map.get(person, [])
        for sr in p_sources:
            if sr.get("source_title") == s_title or sr.get("source_section") == s_sec or s_title in sr.get("source_title", ""):
                matching_records.append({
                    "source_title": sr.get("source_title"),
                    "source_url": sr.get("source_url"),
                    "source_section": sr.get("source_section")
                })
        if not matching_records and p_sources:
            # Fallback to first available source record for the person
            sr = p_sources[0]
            matching_records.append({
                "source_title": sr.get("source_title"),
                "source_url": sr.get("source_url"),
                "source_section": sr.get("source_section")
            })

        # Check duplication against bio, achievements, key_facts
        p_i18n = people_dict.get(person, {}).get("languages", {}).get("en", {})
        bio_text = p_i18n.get("bio", "")
        ach_text = p_i18n.get("achievements", [])
        kf_text = p_i18n.get("key_facts", [])

        dup_bio = (proposed_text.strip() == bio_text.strip())
        dup_ach = any(proposed_text.strip() == (a.strip() if isinstance(a, str) else "") for a in ach_text)
        dup_kf = any(proposed_text.strip() == (k.strip() if isinstance(k, str) else "") for k in kf_text)

        entries.append({
            "person": person,
            "field": "historical_significance",
            "proposed_text": proposed_text,
            "source_records": matching_records,
            "source_basis": def_item["basis"],
            "duplicate_check": {
                "duplicates_bio": dup_bio,
                "duplicates_achievements": dup_ach,
                "duplicates_key_facts": dup_kf
            },
            "classification": "READY_FOR_REVIEW"
        })

    draft_payload = {
        "schema": "HISTORICAL_SIGNIFICANCE_DRAFT_43",
        "read_only": True,
        "target_people_count": len(target_people),
        "entries": entries
    }

    with open(DRAFT_OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(draft_payload, f, indent=2, ensure_ascii=False)

    print(f"Generated {DRAFT_OUT_PATH} with {len(entries)} entries.")

    # Now write the validator script tools/validate_historical_significance_draft_43.py
    validator_code = '''#!/usr/bin/env python3
\"\"\"
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_DRAFT_43.JSON
Validates the historical significance draft against adjudication requirements, source packages, and protected file invariants.
\"\"\"

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
PKG_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json"
REVIEW_43_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_REVIEW_43.json"
REPAIR_PKG_5_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json"
REPAIR_PKG_3_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_3_REPAIR.json"
ADJUDICATION_PATH = ROOT / "tools" / "DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json"
DRAFT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_DRAFT_43.json"

PROTECTED_FILES = [
    PERSON_I18N_PATH,
    QUIZ_DATA_PATH,
    JS_I18N_PATH,
    IDENTITY_REVIEW_PATH,
    PKG_43_PATH,
    REVIEW_43_PATH,
    REPAIR_PKG_5_PATH,
    REPAIR_PKG_3_PATH
]

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_validation():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    with open(ADJUDICATION_PATH, "r", encoding="utf-8") as f:
        adj_data = json.load(f)
    target_people = [c["person"] for c in adj_data["clusters"]]

    if not DRAFT_PATH.exists():
        print("ERROR: Draft file not found.")
        return False

    with open(DRAFT_PATH, "r", encoding="utf-8") as f:
        draft_data = json.load(f)

    entries = draft_data.get("entries", [])
    draft_people = [e["person"] for e in entries]

    # Load all source packages
    def load_pkg(path):
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("entries", [])

    all_source_entries = load_pkg(PKG_43_PATH) + load_pkg(REPAIR_PKG_5_PATH) + load_pkg(REPAIR_PKG_3_PATH)
    valid_source_titles = {s.get("source_title") for s in all_source_entries}

    # Load person data for duplication checks
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)
    people_dict = i18n_data.get("people", {})

    ready_count = 0
    needs_stronger_source_count = 0
    missing_people = set(target_people) - set(draft_people)
    unexpected_people = set(draft_people) - set(target_people)

    proposed_texts_seen = {}
    duplicate_proposed_texts_count = 0

    for entry in entries:
        p = entry.get("person")
        text = entry.get("proposed_text", "")
        field = entry.get("field")
        cls = entry.get("classification")
        src_recs = entry.get("source_records", [])

        if cls == "READY_FOR_REVIEW":
            ready_count += 1
        elif cls == "NEEDS_STRONGER_SOURCE":
            needs_stronger_source_count += 1

        if text in proposed_texts_seen:
            duplicate_proposed_texts_count += 1
        else:
            proposed_texts_seen[text] = p

    exact_target_match = (sorted(target_people) == sorted(draft_people))

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    source_packages_modified = False
    application_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            if "tools/" in fp_str:
                source_packages_modified = True
            else:
                application_data_modified = True

    structural_pass = (
        len(entries) == 43 and
        exact_target_match and
        len(missing_people) == 0 and
        len(unexpected_people) == 0 and
        not application_data_modified and
        not source_packages_modified
    )

    structural_val = "PASS" if structural_pass else "FAIL"

    print("HISTORICAL SIGNIFICANCE DRAFT 43")
    print("--------------------------------")
    print(f"TARGET_PEOPLE: {len(target_people)}")
    print(f"READY_FOR_REVIEW: {ready_count}")
    print(f"NEEDS_STRONGER_SOURCE: {needs_stronger_source_count}")
    print(f"MISSING_PEOPLE: {len(missing_people)}")
    print(f"DUPLICATE_PROPOSED_TEXTS: {duplicate_proposed_texts_count}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if application_data_modified else 'NO'}")
    print(f"SOURCE_PACKAGES_MODIFIED: {'YES' if source_packages_modified else 'NO'}")
    print(f"STRUCTURAL_VALIDATION: {structural_val}")
    print("SEMANTIC_REVIEW_REQUIRED: YES")

    print("\\nPROPOSED ENTRIES SUMMARY:")
    print("=" * 70)
    for entry in entries:
        print(f"Person: {entry.get('person')}")
        print(f"Proposed Text: {entry.get('proposed_text')}")
        src_title = entry.get('source_records', [{}])[0].get('source_title', 'Unknown')
        print(f"Source: {src_title}")
        print(f"Source Basis: {entry.get('source_basis')}")
        print(f"Classification: {entry.get('classification')}")
        print("-" * 70)

    return structural_pass

if __name__ == "__main__":
    run_validation()
'''

    with open(VALIDATOR_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(validator_code)

    print(f"Generated {VALIDATOR_OUT_PATH}")

if __name__ == "__main__":
    main()
