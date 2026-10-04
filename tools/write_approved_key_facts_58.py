#!/usr/bin/env python3
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
REPORT_PATH = ROOT / "tools" / "KEY_FACTS_WRITE_REPORT.json"

APPROVED_58_KEY_FACTS = {
    "Auguste Comte": [
        "In August 1817 he became a student and secretary to Henri de Saint-Simon, who brought Comte into intellectual society.",
        "Developed the Law of Three Stages, asserting that human thought evolves through theological, metaphysical, and positive stages."
    ],
    "Bob Marley": [
        "Formed the Wailers in 1963 with Peter Tosh and Bunny Wailer, releasing their debut studio album The Wailing Wailers in 1965.",
        "Survived an assassination attempt at his home in Kingston in December 1976, two days before performing at the Smile Jamaica concert."
    ],
    "Caravaggio": [
        "Forged important art friendships in Rome with Prospero Orsi and Cardinal Francesco Maria del Monte, who became his primary patron.",
        "Fled Rome in 1606 after killing Ranuccio Tomassoni in a brawl, spending his remaining years in Naples, Malta, and Sicily."
    ],
    "Clara Barton": [
        "Worked as a clerk in the U.S. Patent Office in Washington, D.C. before becoming an independent battlefield nurse during the Civil War.",
        "Traveled to Europe in 1869 and learned about the International Red Cross during the Franco-Prussian War, inspiring her to establish the U.S. branch."
    ],
    "Constantine the Great": [
        "Proclaimed emperor by his troops at Eboracum (modern York, England) in 306 CE following his father's death."
    ],
    "Dmitri Mendeleev": [
        "Graduated from the Main Pedagogical Institute in Saint Petersburg in 1855 and earned a master's degree in chemistry in 1856.",
        "Served as Director of the Bureau of Weights and Measures in Saint Petersburg from 1893 until his death."
    ],
    "Emperor Meiji": [
        "Acceded to the Chrysanthemum Throne in 1867 at age 14 following the death of Emperor Kōmei.",
        "Moved the imperial capital from Kyoto to Tokyo (formerly Edo) in 1868, taking up residence in Edo Castle."
    ],
    "Francisco Goya": [
        "Studied painting from age 14 under José Luzán in Zaragoza and later moved to Madrid to work in the studio of Francisco Bayeu.",
        "Traveled to Rome in 1770 at his own expense and won second prize in a painting competition organized by the Academy of Parma in 1771."
    ],
    "Giuseppe Verdi": [
        "Studied counterpoint privately in Milan under Vincenzo Lavigna after being denied admission to the Milan Conservatory due to age limits.",
        "Elected as a member of the new Italian Parliament for Borgo San Donnino (Fidenza) in 1861 at Cavour's request."
    ],
    "Grace Hopper": [
        "Earned a master's degree in 1930 and a Ph.D. in mathematics from Yale University in 1934.",
        "Served as a professor of mathematics at Vassar College before taking a leave of absence to join the U.S. Navy Reserve in 1943."
    ],
    "Gustav Mahler": [
        "Studied piano and composition at the Vienna Conservatory under Julius Epstein from 1875 to 1878.",
        "Served as director of the Vienna Court Opera from 1897 to 1907, reforming production standards and orchestral performances."
    ],
    "Hadrian": [
        "Ward of Emperor Trajan, who appointed him to military and administrative commands in Pannonia and Syria.",
        "Spent over half of his 21-year reign travelling across the provinces of the Roman Empire inspecting troops and border defenses."
    ],
    "Hannibal Barca": [
        "Elected chief magistrate (sufet) of Carthage after the Second Punic War, enacting anti-corruption financial and administrative reforms.",
        "Fled Carthage into exile in 195 BCE to escape Roman arrest, serving as military advisor to King Antiochus III of the Seleucid Empire."
    ],
    "Igor Stravinsky": [
        "Studied law at the University of Saint Petersburg while taking private composition and orchestration lessons from Nikolai Rimsky-Korsakov.",
        "Acquired French citizenship in 1934 and later became a naturalized American citizen in 1945."
    ],
    "James Clerk Maxwell": [
        "Graduated Second Wrangler from Trinity College, Cambridge in 1854 and won the Smith's Prize for mathematical physics.",
        "Held professor chairs in natural philosophy at Marischal College in Aberdeen and later at King's College London."
    ],
    "James Prescott Joule": [
        "Collaborated with William Thomson (Lord Kelvin) in the 1850s, conducting joint experiments that discovered the Joule–Thomson effect.",
        "Elected a Fellow of the Royal Society in 1850 and awarded the Copley Medal in 1870 for his experimental research."
    ],
    "Jane Austen": [
        "Published her novels anonymously during her lifetime, with Sense and Sensibility credited to 'By a Lady'."
    ],
    "Joseph Haydn": [
        "Served as court Kapellmeister to the wealthy Esterházy aristocratic family for nearly thirty years from 1761.",
        "Traveled to England in the 1790s under the impresario Johann Peter Salomon, composing his twelve 'London Symphonies'."
    ],
    "Louis IX": [
        "Reigned for 43 years, established the Parlement of Paris, and introduced the presumption of innocence in French judicial procedure."
    ],
    "Ludwig van Beethoven": [
        "Moved from Bonn to Vienna in 1792 to study composition under Joseph Haydn and established a reputation as a virtuoso pianist.",
        "Began losing his hearing in his late 20s, becoming almost completely deaf by 1818 while continuing to compose masterworks."
    ],
    "Malek Bennabi": [
        "Studied electrical engineering in Paris in the 1930s before shifting his focus to Islamic philosophy, sociology, and Islamic civilizational studies.",
        "Appointed Director of Higher Education in post-independence Algeria in 1963."
    ],
    "Marcel Proust": [
        "Published his first book, Les Plaisirs et les Jours, a collection of short prose poems and stories, in 1896."
    ],
    "Marcus Aurelius": [
        "Adopted by Emperor Antoninus Pius in 138 CE as part of Emperor Hadrian's imperial succession plan.",
        "Ruled co-equally with his adoptive brother Lucius Verus from 161 until Verus's death in 169 CE."
    ],
    "Martin Luther King": [
        "Helped found the Southern Christian Leadership Conference (SCLC) in 1957, serving as its first president.",
        "Delivered his landmark 'I Have a Dream' speech at the March on Washington for Jobs and Freedom in August 1963."
    ],
    "Muhammad Abduh": [
        "Appointed Grand Mufti of Egypt in 1899, initiating administrative and legal reforms at Al-Azhar University."
    ],
    "Nicolaus Copernicus": [
        "Studied canon law and medicine at the Universities of Kraków, Bologna, and Padua between 1491 and 1503.",
        "Served as a canon of Frombork Cathedral for most of his adult life, managing cathedral administration and medical care."
    ],
    "Oscar Wilde": [
        "Educated at Trinity College Dublin and Magdalen College, Oxford, winning the Newdigate Prize for his poem Ravenna in 1878.",
        "Conducted a nine-month lecture tour of North America in 1882 explaining Aestheticism and art theory."
    ],
    "Qutuz": [
        "Seized the Mamluk throne in Cairo in November 1259, deposing the 15-year-old Sultan Al-Mansur Ali as Mongol forces approached Syria.",
        "Assassinated in October 1260 by fellow Mamluk commander Baibars while returning victorious to Cairo from Ain Jalut."
    ],
    "Rosa Parks": [
        "Served as secretary for the Montgomery branch of the NAACP during the 1940s and 1950s, investigating racial violence cases.",
        "Attended civil rights leadership training at the Highlander Folk School in Tennessee in the summer of 1955."
    ],
    "Saladin": [
        "Appointed Vizier of Fatimid Egypt in 1169 following the death of his uncle Shirkuh, subsequently abolishing the Fatimid Caliphate in 1171."
    ],
    "Sun Yat-sen": [
        "Graduated as a physician from the Hong Kong College of Medicine for Chinese in 1892 before entering political activism.",
        "Co-founded the Revive China Society in Honolulu in 1894 and the Tongmenghui in Tokyo in 1905."
    ],
    "T. E. Lawrence": [
        "Worked as an archaeologist at Carchemish from 1910 to 1914 under David George Hogarth and Leonard Woolley.",
        "Joined the British Army's Arab Bureau in Cairo in 1914 as an intelligence officer during World War I."
    ]
}

def write_and_verify():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # In-memory before snapshot
    original_data = json.loads(json.dumps(data))
    people = data["people"]

    written_facts_count = 0
    people_with_written_facts = 0

    for pid, facts in APPROVED_58_KEY_FACTS.items():
        if pid in people:
            people[pid]["languages"]["en"]["key_facts"] = facts
            written_facts_count += len(facts)
            people_with_written_facts += 1

    # Save updated person_i18n.json
    with open(PERSON_I18N_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # BEFORE/AFTER SNAPSHOT VALIDATION
    unexpected_field_changes = 0
    unexpected_person_changes = 0

    for pid, pobj in data["people"].items():
        orig_pobj = original_data["people"][pid]

        if pid not in APPROVED_58_KEY_FACTS:
            if pobj != orig_pobj:
                unexpected_person_changes += 1
        else:
            # Check non-English languages
            for lcode, ldict in pobj["languages"].items():
                if lcode != "en":
                    if ldict != orig_pobj["languages"][lcode]:
                        unexpected_field_changes += 1

            # Check other English fields
            curr_e = pobj["languages"]["en"]
            orig_e = orig_pobj["languages"]["en"]

            for fname in ["bio", "achievements", "historical_significance"]:
                if curr_e.get(fname) != orig_e.get(fname):
                    unexpected_field_changes += 1

    # Verify rejected facts specifically
    rejected_checks_passed = True
    
    # 1. Steve Jobs
    jobs_kf = people["Steve Jobs"]["languages"]["en"].get("key_facts", [])
    if any("apple" in str(x).lower() or "pixar" in str(x).lower() for x in jobs_kf):
        rejected_checks_passed = False

    # 2. Constantine
    const_kf = people["Constantine the Great"]["languages"]["en"].get("key_facts", [])
    if any("diocletian" in str(x).lower() for x in const_kf):
        rejected_checks_passed = False

    # 3. Jane Austen
    austen_kf = people["Jane Austen"]["languages"]["en"].get("key_facts", [])
    if any("steventon" in str(x).lower() or "chawton" in str(x).lower() for x in austen_kf):
        rejected_checks_passed = False

    # 4. Marcel Proust
    proust_kf = people["Marcel Proust"]["languages"]["en"].get("key_facts", [])
    if any("asthma" in str(x).lower() or "cork" in str(x).lower() for x in proust_kf):
        rejected_checks_passed = False

    # 5. Louis IX
    louis_kf = people["Louis IX"]["languages"]["en"].get("key_facts", [])
    if any("sainte-chapelle" in str(x).lower() for x in louis_kf):
        rejected_checks_passed = False

    # 6. Muhammad Abduh
    abduh_kf = people["Muhammad Abduh"]["languages"]["en"].get("key_facts", [])
    if any("al-urwah" in str(x).lower() for x in abduh_kf):
        rejected_checks_passed = False

    # 7. Saladin
    saladin_kf = people["Saladin"]["languages"]["en"].get("key_facts", [])
    if any("ayyubid" in str(x).lower() for x in saladin_kf):
        rejected_checks_passed = False

    json_valid = True
    try:
        with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception:
        json_valid = False

    report = {
        "target_people": 33,
        "people_with_written_facts": people_with_written_facts,
        "approved_facts": written_facts_count,
        "rejected_facts": 8,
        "files_modified": 1,
        "modified_file": "app/src/main/assets/person_i18n.json",
        "modified_fields": "English key_facts only",
        "unexpected_changes": unexpected_field_changes + unexpected_person_changes,
        "status": "PASS" if (written_facts_count == 58 and people_with_written_facts == 32 and unexpected_field_changes == 0 and unexpected_person_changes == 0 and rejected_checks_passed and json_valid) else "FAIL"
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    status_pass = (report["status"] == "PASS")

    print(f"FILES_MODIFIED: 1")
    print(f"APPROVED_KEY_FACTS_WRITTEN: {written_facts_count}")
    print(f"PEOPLE_WITH_KEY_FACTS: {people_with_written_facts}")
    print(f"UNEXPECTED_FIELD_CHANGES: {unexpected_field_changes}")
    print(f"UNEXPECTED_PERSON_CHANGES: {unexpected_person_changes}")
    print(f"JSON_VALID: {'YES' if json_valid else 'NO'}")
    print(f"STATUS: {'KEY_FACTS_WRITE_COMPLETE' if status_pass else 'KEY_FACTS_WRITE_FAIL'}")

if __name__ == "__main__":
    write_and_verify()
