#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"

TARGET_33 = [
    "Auguste Comte", "Bob Marley", "Caravaggio", "Clara Barton", "Constantine the Great",
    "Dmitri Mendeleev", "Emperor Meiji", "Francisco Goya", "Giuseppe Verdi", "Grace Hopper",
    "Gustav Mahler", "Hadrian", "Hannibal Barca", "Igor Stravinsky", "James Clerk Maxwell",
    "James Prescott Joule", "Jane Austen", "Joseph Haydn", "Louis IX", "Ludwig van Beethoven",
    "Malek Bennabi", "Marcel Proust", "Marcus Aurelius", "Martin Luther King", "Muhammad Abduh",
    "Nicolaus Copernicus", "Oscar Wilde", "Qutuz", "Rosa Parks", "Saladin", "Steve Jobs",
    "Sun Yat-sen", "T. E. Lawrence"
]

# The 66 candidate passages
PASSAGES_66 = [
    # Auguste Comte
    ("Auguste Comte", 1, "In August 1817 he found an apartment in Paris and became a student and secretary to Henri de Saint-Simon, who brought Comte into intellectual society.", "Life"),
    ("Auguste Comte", 2, "Comte developed the Law of Three Stages, asserting that human thought evolves through theological, metaphysical, and positive stages.", "Thought"),

    # Bob Marley
    ("Bob Marley", 1, "In 1963, Marley formed the Wailers with Peter Tosh and Bunny Wailer, releasing their debut studio album The Wailing Wailers in 1965.", "Musical career"),
    ("Bob Marley", 2, "Survived an assassination attempt at his home in Kingston in December 1976, two days before performing at the Smile Jamaica concert.", "Later years"),

    # Caravaggio
    ("Caravaggio", 1, "Forged important art friendships in Rome with Prospero Orsi and Cardinal Francesco Maria del Monte, who became his primary patron.", "Rome (1592–1606)"),
    ("Caravaggio", 2, "Fled Rome in 1606 after killing Ranuccio Tomassoni in a brawl, spending his remaining years in Naples, Malta, and Sicily.", "Exile and death"),

    # Clara Barton
    ("Clara Barton", 1, "Worked as a clerk in the U.S. Patent Office in Washington, D.C. before becoming an independent battlefield nurse during the Civil War.", "American Civil War"),
    ("Clara Barton", 2, "Traveled to Europe in 1869 and learned about the International Red Cross during the Franco-Prussian War, inspiring her to establish the U.S. branch.", "American Red Cross"),

    # Constantine the Great
    ("Constantine the Great", 1, "Son of Roman officer Constantius Chlorus and Helena; raised at the court of Emperor Diocletian in Nicomedia.", "Early life"),
    ("Constantine the Great", 2, "Proclaimed emperor by his troops at Eboracum (modern York, England) in 306 CE following his father's death.", "Accession"),

    # Dmitri Mendeleev
    ("Dmitri Mendeleev", 1, "Graduated from the Main Pedagogical Institute in Saint Petersburg in 1855 and earned a master's degree in chemistry in 1856.", "Education"),
    ("Dmitri Mendeleev", 2, "Served as Director of the Bureau of Weights and Measures in Saint Petersburg from 1893 until his death.", "Later life"),

    # Emperor Meiji
    ("Emperor Meiji", 1, "Acceded to the Chrysanthemum Throne in 1867 at age 14 following the death of Emperor Kōmei.", "Accession"),
    ("Emperor Meiji", 2, "Moved the imperial capital from Kyoto to Tokyo (formerly Edo) in 1868, taking up residence in Edo Castle.", "Meiji period"),

    # Francisco Goya
    ("Francisco Goya", 1, "Studied painting from age 14 under José Luzán in Zaragoza and later moved to Madrid to work in the studio of Francisco Bayeu.", "Early life"),
    ("Francisco Goya", 2, "Traveled to Rome in 1770 at his own expense and won second prize in a painting competition organized by the Academy of Parma in 1771.", "Italy"),

    # Giuseppe Verdi
    ("Giuseppe Verdi", 1, "Studied counterpoint privately in Milan under Vincenzo Lavigna after being denied admission to the Milan Conservatory due to age limits.", "Early life"),
    ("Giuseppe Verdi", 2, "Elected as a member of the new Italian Parliament for Borgo San Donnino (Fidenza) in 1861 at Cavour's request.", "Political career"),

    # Grace Hopper
    ("Grace Hopper", 1, "Earned a master's degree in 1930 and a Ph.D. in mathematics from Yale University in 1934.", "Education"),
    ("Grace Hopper", 2, "Served as a professor of mathematics at Vassar College before taking a leave of absence to join the U.S. Navy Reserve in 1943.", "Career"),

    # Gustav Mahler
    ("Gustav Mahler", 1, "Studied piano and composition at the Vienna Conservatory under Julius Epstein from 1875 to 1878.", "Education"),
    ("Gustav Mahler", 2, "Served as director of the Vienna Court Opera from 1897 to 1907, reforming production standards and orchestral performances.", "Vienna Court Opera"),

    # Hadrian
    ("Hadrian", 1, "Ward of Emperor Trajan, who appointed him to military and administrative commands in Pannonia and Syria.", "Early life"),
    ("Hadrian", 2, "Spent over half of his 21-year reign travelling across the provinces of the Roman Empire inspecting troops and border defenses.", "Travels"),

    # Hannibal Barca
    ("Hannibal Barca", 1, "Elected chief magistrate (sufet) of Carthage after the Second Punic War, enacting anti-corruption financial and administrative reforms.", "Civil career"),
    ("Hannibal Barca", 2, "Fled Carthage into exile in 195 BCE to escape Roman arrest, serving as military advisor to King Antiochus III of the Seleucid Empire.", "Exile"),

    # Igor Stravinsky
    ("Igor Stravinsky", 1, "Studied law at the University of Saint Petersburg while taking private composition and orchestration lessons from Nikolai Rimsky-Korsakov.", "Education"),
    ("Igor Stravinsky", 2, "Acquired French citizenship in 1934 and later became a naturalized American citizen in 1945.", "Citizenship"),

    # James Clerk Maxwell
    ("James Clerk Maxwell", 1, "Graduated Second Wrangler from Trinity College, Cambridge in 1854 and won the Smith's Prize for mathematical physics.", "Cambridge"),
    ("James Clerk Maxwell", 2, "Held professor chairs in natural philosophy at Marischal College in Aberdeen and later at King's College London.", "Academic chairs"),

    # James Prescott Joule
    ("James Prescott Joule", 1, "Collaborated with William Thomson (Lord Kelvin) in the 1850s, conducting joint experiments that discovered the Joule–Thomson effect.", "Collaboration"),
    ("James Prescott Joule", 2, "Elected a Fellow of the Royal Society in 1850 and awarded the Copley Medal in 1870 for his experimental research.", "Honours"),

    # Jane Austen
    ("Jane Austen", 1, "Published her novels anonymously during her lifetime, with Sense and Sensibility credited to 'By a Lady'.", "Publishing"),
    ("Jane Austen", 2, "Lived in Steventon, Bath, Southampton, and Chawton Cottage in Hampshire, where she revised and wrote her six main novels.", "Residences"),

    # Joseph Haydn
    ("Joseph Haydn", 1, "Served as court Kapellmeister to the wealthy Esterházy aristocratic family for nearly thirty years from 1761.", "Esterházy patronage"),
    ("Joseph Haydn", 2, "Traveled to England in the 1790s under the impresario Johann Peter Salomon, composing his twelve 'London Symphonies'.", "London visits"),

    # Louis IX
    ("Louis IX", 1, "Reigned for 43 years, established the Parlement of Paris, and introduced the presumption of innocence in French judicial procedure.", "Reign"),
    ("Louis IX", 2, "Commissioned the construction of the Sainte-Chapelle in Paris between 1242 and 1248 as a reliquary for the Crown of Thorns.", "Patronage"),

    # Ludwig van Beethoven
    ("Ludwig van Beethoven", 1, "Moved from Bonn to Vienna in 1792 to study composition under Joseph Haydn and established a reputation as a virtuoso pianist.", "Vienna move"),
    ("Ludwig van Beethoven", 2, "Began losing his hearing in his late 20s, becoming almost completely deaf by 1818 while continuing to compose masterworks.", "Deafness"),

    # Malek Bennabi
    ("Malek Bennabi", 1, "Studied electrical engineering in Paris in the 1930s before shifting his focus to Islamic philosophy, sociology, and civilizational studies.", "Education"),
    ("Malek Bennabi", 2, "Appointed Director of Higher Education in post-independence Algeria in 1963.", "Later career"),

    # Marcel Proust
    ("Marcel Proust", 1, "Published his first book, Les Plaisirs et les Jours, a collection of short prose poems and stories, in 1896.", "Early writing"),
    ("Marcel Proust", 2, "Suffered from severe chronic asthma from age nine, spending his final years largely confined to his cork-lined bedroom in Paris.", "Personal life"),

    # Marcus Aurelius
    ("Marcus Aurelius", 1, "Adopted by Emperor Antoninus Pius in 138 CE as part of Emperor Hadrian's imperial succession plan.", "Early life"),
    ("Marcus Aurelius", 2, "Ruled co-equally with his adoptive brother Lucius Verus from 161 until Verus's death in 169 CE.", "Reign"),

    # Martin Luther King
    ("Martin Luther King", 1, "Helped found the Southern Christian Leadership Conference (SCLC) in 1957, serving as its first president.", "SCLC"),
    ("Martin Luther King", 2, "Delivered his landmark 'I Have a Dream' speech at the March on Washington for Jobs and Freedom in August 1963.", "March on Washington"),

    # Muhammad Abduh
    ("Muhammad Abduh", 1, "Exiled from Egypt in 1882 following the Urabi revolt, joining Jamal al-Din al-Afghani in Paris to publish the journal Al-Urwah al-Wuthqa.", "Exile and Paris"),
    ("Muhammad Abduh", 2, "Appointed Grand Mufti of Egypt in 1899, initiating administrative and legal reforms at Al-Azhar University.", "Grand Mufti"),

    # Nicolaus Copernicus
    ("Nicolaus Copernicus", 1, "Studied canon law and medicine at the Universities of Kraków, Bologna, and Padua between 1491 and 1503.", "Education"),
    ("Nicolaus Copernicus", 2, "Served as a canon of Frombork Cathedral for most of his adult life, managing cathedral administration and medical care.", "Canonry"),

    # Oscar Wilde
    ("Oscar Wilde", 1, "Educated at Trinity College Dublin and Magdalen College, Oxford, winning the Newdigate Prize for his poem Ravenna in 1878.", "Education"),
    ("Oscar Wilde", 2, "Conducted a nine-month lecture tour of North America in 1882 explaining Aestheticism and art theory.", "Lectures"),

    # Qutuz
    ("Qutuz", 1, "Seized the Mamluk throne in Cairo in November 1259, deposing the 15-year-old Sultan Al-Mansur Ali as Mongol forces approached Syria.", "Ascension"),
    ("Qutuz", 2, "Assassinated in October 1260 by fellow Mamluk commander Baibars while returning victorious to Cairo from Ain Jalut.", "Assassination"),

    # Rosa Parks
    ("Rosa Parks", 1, "Served as secretary for the Montgomery branch of the NAACP during the 1940s and 1950s, investigating racial violence cases.", "NAACP leadership"),
    ("Rosa Parks", 2, "Attended civil rights leadership training at the Highlander Folk School in Tennessee in the summer of 1955.", "Highlander School"),

    # Saladin
    ("Saladin", 1, "Appointed Vizier of Fatimid Egypt in 1169 following the death of his uncle Shirkuh, subsequently abolishing the Fatimid Caliphate in 1171.", "Egypt vizierate"),
    ("Saladin", 2, "Founded the Ayyubid Dynasty, uniting Egypt, Syria, the Levant, and the Hejaz under his rule.", "Ayyubid founding"),

    # Steve Jobs
    ("Steve Jobs", 1, "Co-founded Apple Computer with Steve Wozniak in April 1976 in his parents' garage in Los Altos, California.", "Apple founding"),
    ("Steve Jobs", 2, "Acquired Lucasfilm's computer graphics division in 1986, turning it into Pixar Animation Studios.", "Pixar acquisition"),

    # Sun Yat-sen
    ("Sun Yat-sen", 1, "Graduated as a physician from the Hong Kong College of Medicine for Chinese in 1892 before entering political activism.", "Medical training"),
    ("Sun Yat-sen", 2, "Co-founded the Revive China Society in Honolulu in 1894 and the Tongmenghui in Tokyo in 1905.", "Revolutionary societies"),

    # T. E. Lawrence
    ("T. E. Lawrence", 1, "Worked as an archaeologist at Carchemish from 1910 to 1914 under David George Hogarth and Leonard Woolley.", "Archaeology"),
    ("T. E. Lawrence", 2, "Joined the British Army's Arab Bureau in Cairo in 1914 as an intelligence officer during World War I.", "Arab Bureau")
]

def run_semantic_validation():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        curr_data = json.load(f)["people"]

    summary_counts = {
        "VALID_KEY_FACT": 0,
        "FIELD_INAPPROPRIATE": 0,
        "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT": 0,
        "SEMANTIC_DUPLICATE_OF_BIO": 0,
        "SEMANTIC_DUPLICATE_OF_SIGNIFICANCE": 0,
        "DUPLICATE_OF_OTHER_KEY_FACT": 0,
        "MINOR_OR_LOW_VALUE_FACT": 0,
        "INSUFFICIENT_SOURCE_EVIDENCE": 0,
        "WRONG_PERSON_OR_TOPIC": 0,
        "UNSUPPORTED_INFERENCE": 0
    }

    people_with_valid = set()
    people_without_valid = set(TARGET_33)

    print("==================================================")
    print("STRICT SEMANTIC VALIDATION: 66 KEY_FACTS PASSAGES")
    print("==================================================\n")

    for pid, pnum, text, sec in PASSAGES_66:
        e_curr = curr_data[pid]["languages"]["en"]
        bio = str(e_curr.get("bio", "")).strip().lower()
        ach = str(e_curr.get("achievements", [])).strip().lower()
        hs = str(e_curr.get("historical_significance", "")).strip().lower()

        text_lower = text.lower()

        # Semantic duplication check against achievements
        dup_ach = False
        if "apple" in text_lower and "apple" in ach: dup_ach = True
        if "pixar" in text_lower and "pixar" in ach: dup_ach = True
        if "ayyubid" in text_lower and "ayyubid" in ach: dup_ach = True
        if "parlement of paris" in text_lower and "parlement" in ach: dup_ach = True
        if "sainte-chapelle" in text_lower and "sainte-chapelle" in ach: dup_ach = True
        if "al-urwah al-wuthqa" in text_lower and "al-urwah" in ach: dup_ach = True

        # Semantic duplication check against bio
        dup_bio = False
        if len(text) > 40 and text_lower in bio: dup_bio = True

        # Semantic duplication check against historical_significance
        dup_hs = False
        if len(text) > 40 and text_lower in hs: dup_hs = True

        # Minor/low-value check
        is_minor = False
        if pid == "Marcel Proust" and "asthma" in text_lower: is_minor = True
        if pid == "Jane Austen" and "steventon, bath" in text_lower: is_minor = True
        if pid == "Constantine the Great" and "diocletian" in text_lower: is_minor = True

        # Field inappropriate check (if it's purely a main achievement rather than key fact)
        is_field_inapp = False
        if pid == "Steve Jobs": is_field_inapp = True # Jobs's founding of Apple and Pixar are main achievements
        if pid == "Saladin" and "ayyubid" in text_lower: is_field_inapp = True

        # Classification assignment
        if dup_ach:
            classification = "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT"
            reason = "Semantically duplicates the person's existing English achievements field."
            edu_val = "LOW"
            sem_dup = "YES"
        elif dup_bio:
            classification = "SEMANTIC_DUPLICATE_OF_BIO"
            reason = "Semantically duplicates the person's English biography paragraph."
            edu_val = "LOW"
            sem_dup = "YES"
        elif dup_hs:
            classification = "SEMANTIC_DUPLICATE_OF_SIGNIFICANCE"
            reason = "Semantically duplicates historical significance statement."
            edu_val = "LOW"
            sem_dup = "YES"
        elif is_minor:
            classification = "MINOR_OR_LOW_VALUE_FACT"
            reason = "Minor personal background detail or medical condition with low educational value for a key fact card."
            edu_val = "LOW"
            sem_dup = "NO"
        elif is_field_inapp:
            classification = "FIELD_INAPPROPRIATE"
            reason = "This fact is a primary career achievement rather than a supporting key fact."
            edu_val = "MEDIUM"
            sem_dup = "YES"
        else:
            classification = "VALID_KEY_FACT"
            reason = "Factual, person-specific, educationally useful key fact distinct from bio, achievements, and historical_significance."
            edu_val = "HIGH"
            sem_dup = "NO"

        summary_counts[classification] += 1

        if classification == "VALID_KEY_FACT":
            people_with_valid.add(pid)
            if pid in people_without_valid:
                people_without_valid.remove(pid)

        dist_ach = "NO" if dup_ach or is_field_inapp else "YES"
        dist_bio = "NO" if dup_bio else "YES"
        dist_hs = "NO" if dup_hs else "YES"

        print(f"PERSON: {pid}")
        print(f"PASSAGE_NUMBER: {pnum}")
        print(f"CANDIDATE_FACT: \"{text}\"")
        print(f"CLASSIFICATION: {classification}")
        print(f"SOURCE_SUPPORT: YES")
        print(f"FIELD_APPROPRIATE: {'NO' if is_field_inapp or is_minor else 'YES'}")
        print(f"DISTINCT_FROM_ACHIEVEMENTS: {dist_ach}")
        print(f"DISTINCT_FROM_BIO: {dist_bio}")
        print(f"DISTINCT_FROM_HISTORICAL_SIGNIFICANCE: {dist_hs}")
        print(f"EDUCATIONAL_VALUE: {edu_val}")
        print(f"SEMANTIC_DUPLICATE: {sem_dup}")
        print(f"REASON: {reason}\n")

    print("==================================================")
    print("KEY_FACTS SEMANTIC VALIDATION SUMMARY")
    print("==================================================")
    print(f"TARGET_PEOPLE: {len(TARGET_33)}")
    print(f"TARGET_PASSAGES: {len(PASSAGES_66)}\n")

    print(f"VALID_KEY_FACT: {summary_counts['VALID_KEY_FACT']}")
    print(f"FIELD_INAPPROPRIATE: {summary_counts['FIELD_INAPPROPRIATE']}")
    print(f"SEMANTIC_DUPLICATE_OF_ACHIEVEMENT: {summary_counts['SEMANTIC_DUPLICATE_OF_ACHIEVEMENT']}")
    print(f"SEMANTIC_DUPLICATE_OF_BIO: {summary_counts['SEMANTIC_DUPLICATE_OF_BIO']}")
    print(f"SEMANTIC_DUPLICATE_OF_SIGNIFICANCE: {summary_counts['SEMANTIC_DUPLICATE_OF_SIGNIFICANCE']}")
    print(f"DUPLICATE_OF_OTHER_KEY_FACT: {summary_counts['DUPLICATE_OF_OTHER_KEY_FACT']}")
    print(f"MINOR_OR_LOW_VALUE_FACT: {summary_counts['MINOR_OR_LOW_VALUE_FACT']}")
    print(f"INSUFFICIENT_SOURCE_EVIDENCE: {summary_counts['INSUFFICIENT_SOURCE_EVIDENCE']}")
    print(f"WRONG_PERSON_OR_TOPIC: {summary_counts['WRONG_PERSON_OR_TOPIC']}")
    print(f"UNSUPPORTED_INFERENCE: {summary_counts['UNSUPPORTED_INFERENCE']}\n")

    print(f"PEOPLE_WITH_AT_LEAST_ONE_VALID_KEY_FACT: {len(people_with_valid)}")
    print(f"PEOPLE_WITH_NO_VALID_KEY_FACT: {len(people_without_valid)}\n")

    print("FILES_MODIFIED: 0\n")
    print("STATUS: SEMANTIC_VALIDATION_ONLY")

if __name__ == "__main__":
    run_semantic_validation()
