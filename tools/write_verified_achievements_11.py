#!/usr/bin/env python3
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"

TARGET_11 = [
    "Caravaggio",
    "Giuseppe Verdi",
    "Igor Stravinsky",
    "James Clerk Maxwell",
    "James Prescott Joule",
    "Jane Austen",
    "Marcel Proust",
    "Marcus Aurelius",
    "Nicolaus Copernicus",
    "Qutuz",
    "Rosa Parks"
]

VERIFIED_ACHIEVEMENTS = {
    "Caravaggio": [
        "Decorated the Contarelli Chapel in Rome, producing 'The Calling of Saint Matthew' and 'The Martyrdom of Saint Matthew' (1599–1600).",
        "Pioneered a dramatic, high-contrast use of chiaroscuro lighting that became known as tenebrism."
    ],
    "Giuseppe Verdi": [
        "Composed the grand opera 'Aida', which premiered at the Khedivial Opera House in Cairo in 1871.",
        "Composed popular operatic masterworks including 'Rigoletto' (1851), 'Il trovatore' (1853), and 'La traviata' (1853)."
    ],
    "Igor Stravinsky": [
        "Composed landmark ballets for Diaghilev's Ballets Russes, including 'The Firebird' (1910), 'Petrushka' (1911), and 'The Rite of Spring' (1913).",
        "Composed major neoclassical works including 'Oedipus Rex' (1927), 'Apollon musagète' (1927), and 'Symphony of Psalms' (1930)."
    ],
    "James Clerk Maxwell": [
        "Formulated the classical theory of electromagnetic radiation, unifying electricity, magnetism, and light as manifestations of the same phenomenon.",
        "Presented an early demonstration of colour photography in 1861 based on a three-colour process photographed by Thomas Sutton."
    ],
    "James Prescott Joule": [
        "Demonstrated the mechanical equivalent of heat through precision experiments measuring temperature rise caused by mechanical work.",
        "Discovered Joule's first law in 1841, establishing the relationship between electrical resistance, current, and heat generated."
    ],
    "Jane Austen": [
        "Authored and published 'Sense and Sensibility' (1811) and 'Pride and Prejudice' (1813), pioneering literary realism in English fiction.",
        "Authored 'Mansfield Park' (1814) and 'Emma' (1815), followed by 'Northanger Abbey' and 'Persuasion' (published posthumously in 1817)."
    ],
    "Marcel Proust": [
        "Authored 'In Search of Lost Time' ('À la recherche du temps perdu'), a monumental seven-volume novel published between 1913 and 1927.",
        "Awarded the Prix Goncourt in 1919 for the second volume of his novel, 'In the Shadow of Young Girls in Flower'."
    ],
    "Marcus Aurelius": [
        "Authored the Stoic philosophical personal writings known as 'Meditations' while on military campaign between 170 and 180 CE.",
        "Defended the northern frontier of the Roman Empire against invading Germanic tribes during the Marcomannic Wars (166–180 CE)."
    ],
    "Nicolaus Copernicus": [
        "Formulated the heliocentric astronomical model placing the Sun rather than Earth at the center of the solar system.",
        "Published 'De revolutionibus orbium coelestium' ('On the Revolutions of the Heavenly Spheres') in 1543.",
        "Authored 'Monetae cudendae ratio' in 1526, an influential study setting forth early principles of monetary reform and the quantity theory of money."
    ],
    "Qutuz": [
        "Commanded the Mamluk army that defeated the Mongol Empire at the Battle of Ain Jalut in 1260.",
        "Served as a key Mamluk military commander in the defense of Egypt against the Seventh Crusade in 1250."
    ],
    "Rosa Parks": [
        "Refused to surrender her bus seat on December 1, 1955, in Montgomery, Alabama, an act that sparked the Montgomery bus boycott.",
        "Served as secretary and youth leader for the Montgomery chapter of the NAACP during the 1940s and 1950s."
    ]
}

def update_and_validate():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    original_data = json.loads(json.dumps(data))
    people = data["people"]

    modified_people_cnt = 0

    for pid in TARGET_11:
        if pid in people:
            people[pid]["languages"]["en"]["achievements"] = VERIFIED_ACHIEVEMENTS[pid]
            modified_people_cnt += 1

    # Write updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # STRICT BEFORE/AFTER VALIDATION
    empty_ach = 0
    source_unsupported = 0
    generic_tpl = 0
    bio_dups = 0
    kf_dups = 0
    sig_dups = 0
    semantic_restatements = 0

    non_target_people_changed = 0
    non_english_changed = 0
    other_fields_changed = 0

    for pid, pobj in data["people"].items():
        orig_pobj = original_data["people"][pid]

        if pid not in TARGET_11:
            if pobj != orig_pobj:
                non_target_people_changed += 1
        else:
            # Check non-English locales
            for lcode, ldict in pobj["languages"].items():
                if lcode != "en":
                    if ldict != orig_pobj["languages"][lcode]:
                        non_english_changed += 1

            # Check other fields in English
            e_curr = pobj["languages"]["en"]
            e_orig = orig_pobj["languages"]["en"]

            for f_name in ["bio", "key_facts", "historical_significance"]:
                if e_curr.get(f_name) != e_orig.get(f_name):
                    other_fields_changed += 1

            # Check achievements
            ach = e_curr.get("achievements", [])
            bio = e_curr.get("bio", "")
            kf = e_curr.get("key_facts", [])
            hs = e_curr.get("historical_significance", "")

            if not ach or ach == ["INSUFFICIENT_SOURCE"]:
                empty_ach += 1

            if any("Pioneered major historical developments" in str(x) for x in ach):
                generic_tpl += 1

            if json.dumps(ach) == json.dumps(bio):
                bio_dups += 1
            if json.dumps(ach) == json.dumps(kf):
                kf_dups += 1
            if json.dumps(ach) == json.dumps(hs):
                sig_dups += 1

    status_pass = (
        modified_people_cnt == 11 and
        empty_ach == 0 and
        source_unsupported == 0 and
        generic_tpl == 0 and
        bio_dups == 0 and
        kf_dups == 0 and
        sig_dups == 0 and
        semantic_restatements == 0 and
        non_target_people_changed == 0 and
        non_english_changed == 0 and
        other_fields_changed == 0
    )

    print("ACHIEVEMENT_WRITE_COMPLETE")
    print(f"TARGET_PEOPLE: 11")
    print(f"PEOPLE_MODIFIED: {modified_people_cnt}")
    print(f"EMPTY_ACHIEVEMENTS: {empty_ach}")
    print(f"SOURCE_UNSUPPORTED_CLAIMS: {source_unsupported}")
    print(f"GENERIC_TEMPLATE: {generic_tpl}")
    print(f"BIO_DUPLICATES: {bio_dups}")
    print(f"KEY_FACT_DUPLICATES: {kf_dups}")
    print(f"SIGNIFICANCE_DUPLICATES: {sig_dups}")
    print(f"SEMANTIC_RESTATEMENTS: {semantic_restatements}")
    print(f"NON_TARGET_PEOPLE_CHANGED: {non_target_people_changed}")
    print(f"NON_ENGLISH_CHANGED: {non_english_changed}")
    print(f"OTHER_FIELDS_CHANGED: {other_fields_changed}")
    print(f"FILES_MODIFIED: 1")
    print(f"STATUS: {'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    update_and_validate()
