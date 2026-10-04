#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"

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

def audit():
    # 1. Parse JSON
    json_valid = True
    try:
        with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        json_valid = False
        print(f"JSON_VALID: NO ({e})")
        return

    people = data.get("people", {})

    # 2. Audit 58 approved key_facts
    approved_present_cnt = 0
    people_with_approved_cnt = 0

    all_written_facts_list = []
    cross_person_dup_set = set()

    for pid, expected_facts in APPROVED_58_KEY_FACTS.items():
        actual_facts = people.get(pid, {}).get("languages", {}).get("en", {}).get("key_facts", [])
        
        has_approved = False
        for exp_f in expected_facts:
            if exp_f in actual_facts:
                approved_present_cnt += 1
                has_approved = True
                if exp_f in all_written_facts_list:
                    cross_person_dup_set.add(exp_f)
                else:
                    all_written_facts_list.append(exp_f)

        if has_approved:
            people_with_approved_cnt += 1

    # 3. Check rejected facts
    rejected_facts_found = 0

    # Steve Jobs
    jobs_kf = people.get("Steve Jobs", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("apple" in str(x).lower() or "pixar" in str(x).lower() for x in jobs_kf):
        rejected_facts_found += 1

    # Constantine the Great
    const_kf = people.get("Constantine the Great", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("diocletian" in str(x).lower() for x in const_kf):
        rejected_facts_found += 1

    # Jane Austen
    austen_kf = people.get("Jane Austen", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("steventon" in str(x).lower() or "chawton" in str(x).lower() for x in austen_kf):
        rejected_facts_found += 1

    # Marcel Proust
    proust_kf = people.get("Marcel Proust", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("asthma" in str(x).lower() or "cork" in str(x).lower() for x in proust_kf):
        rejected_facts_found += 1

    # Louis IX
    louis_kf = people.get("Louis IX", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("sainte-chapelle" in str(x).lower() for x in louis_kf):
        rejected_facts_found += 1

    # Muhammad Abduh
    abduh_kf = people.get("Muhammad Abduh", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("al-urwah" in str(x).lower() for x in abduh_kf):
        rejected_facts_found += 1

    # Saladin
    saladin_kf = people.get("Saladin", {}).get("languages", {}).get("en", {}).get("key_facts", [])
    if any("ayyubid" in str(x).lower() for x in saladin_kf):
        rejected_facts_found += 1

    # 4. Check duplicate key_facts within same person
    duplicate_kf_within_person = 0
    for pid, pobj in people.items():
        kf = pobj.get("languages", {}).get("en", {}).get("key_facts", [])
        if isinstance(kf, list) and len(kf) != len(set(kf)):
            duplicate_kf_within_person += 1

    # 5. Check unexpected changes using KEY_FACTS_WRITE_REPORT.json
    report_path = ROOT / "tools" / "KEY_FACTS_WRITE_REPORT.json"
    if report_path.exists():
        with open(report_path, "r", encoding="utf-8") as f:
            write_rep = json.load(f)
        unexpected_person_changes = write_rep.get("unexpected_changes", 0)
        non_english_verified = "YES" if unexpected_person_changes == 0 else "NO"
        other_fields_verified = "YES" if unexpected_person_changes == 0 else "NO"
    else:
        unexpected_person_changes = "NOT_VERIFIABLE"
        non_english_verified = "NOT_VERIFIABLE"
        other_fields_verified = "NOT_VERIFIABLE"

    status_pass = (
        json_valid and
        approved_present_cnt == 58 and
        people_with_approved_cnt == 32 and
        rejected_facts_found == 0 and
        duplicate_kf_within_person == 0 and
        len(cross_person_dup_set) == 0 and
        unexpected_person_changes == 0
    )

    print(f"JSON_VALID: {'YES' if json_valid else 'NO'}")
    print(f"APPROVED_KEY_FACTS_PRESENT: {approved_present_cnt}/58")
    print(f"PEOPLE_WITH_APPROVED_KEY_FACTS: {people_with_approved_cnt}/32")
    print(f"REJECTED_FACTS_FOUND: {rejected_facts_found}")
    print(f"DUPLICATE_KEY_FACTS: {duplicate_kf_within_person}")
    print(f"CROSS_PERSON_DUPLICATES: {len(cross_person_dup_set)}")
    print(f"NON_ENGLISH_CHANGES_VERIFIED: {non_english_verified}")
    print(f"OTHER_ENGLISH_FIELD_CHANGES_VERIFIED: {other_fields_verified}")
    print(f"UNEXPECTED_PERSON_CHANGES: {unexpected_person_changes}")
    print(f"STATUS: {'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    audit()
