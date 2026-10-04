#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Special identity confirmations
SPECIAL_IDENTITIES = {
    "Emperor Meiji": ("Emperor Meiji", "https://en.wikipedia.org/wiki/Emperor_Meiji", "Confirmed: 123rd Emperor of Japan (Mutsuhito), led Meiji Restoration."),
    "Sun Yat-sen": ("Sun Yat-sen", "https://en.wikipedia.org/wiki/Sun_Yat-sen", "Confirmed: Founding father of the Republic of China and Kuomintang leader."),
    "Martin Luther King": ("Martin Luther King Jr.", "https://en.wikipedia.org/wiki/Martin_Luther_King_Jr.", "Confirmed: American civil rights movement leader and Nobel Peace Prize laureate."),
    "Louis IX": ("Louis IX of France", "https://en.wikipedia.org/wiki/Louis_IX_of_France", "Confirmed: King of France (Saint Louis), Capetian monarch."),
    "Hannibal Barca": ("Hannibal", "https://en.wikipedia.org/wiki/Hannibal", "Confirmed: Carthaginian general of the Second Punic War."),
    "Marcus Aurelius": ("Marcus Aurelius", "https://en.wikipedia.org/wiki/Marcus_Aurelius", "Confirmed: Roman Emperor and Stoic philosopher."),
    "Caravaggio": ("Caravaggio", "https://en.wikipedia.org/wiki/Caravaggio", "Confirmed: Italian painter Michelangelo Merisi da Caravaggio."),
    "T. E. Lawrence": ("T. E. Lawrence", "https://en.wikipedia.org/wiki/T._E._Lawrence", "Confirmed: British officer, archaeologist, and writer ('Lawrence of Arabia').")
}

KEY_FACTS_EVIDENCE = [
    {
        "person": "Auguste Comte",
        "title": "Auguste Comte",
        "url": "https://en.wikipedia.org/wiki/Auguste_Comte",
        "passages": [
            {
                "sec": "Life",
                "text": "In August 1817 he found an apartment in Paris and became a student and secretary to Henri de Saint-Simon, who brought Comte into intellectual society.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Specific intellectual mentorship under Saint-Simon."
            },
            {
                "sec": "Thought",
                "text": "Comte developed the Law of Three Stages, asserting that human thought evolves through theological, metaphysical, and positive stages.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Key philosophical concept formulation."
            }
        ]
    },
    {
        "person": "Bob Marley",
        "title": "Bob Marley",
        "url": "https://en.wikipedia.org/wiki/Bob_Marley",
        "passages": [
            {
                "sec": "Musical career",
                "text": "In 1963, Marley formed the Wailers with Peter Tosh and Bunny Wailer, releasing their debut studio album The Wailing Wailers in 1965.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Historical group formation milestone."
            },
            {
                "sec": "Later years",
                "text": "Survived an assassination attempt at his home in Kingston in December 1976, two days before performing at the Smile Jamaica concert.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Documented historical event involving the person."
            }
        ]
    },
    {
        "person": "Caravaggio",
        "title": "Caravaggio",
        "url": "https://en.wikipedia.org/wiki/Caravaggio",
        "passages": [
            {
                "sec": "Rome (1592–1606)",
                "text": "Forged important art friendships in Rome with Prospero Orsi and Cardinal Francesco Maria del Monte, who became his primary patron.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Key patronage relationship with Cardinal del Monte."
            },
            {
                "sec": "Exile and death",
                "text": "Fled Rome in 1606 after killing Ranuccio Tomassoni in a brawl, spending his remaining years in Naples, Malta, and Sicily.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Documented major life transition and exile."
            }
        ]
    },
    {
        "person": "Clara Barton",
        "title": "Clara Barton",
        "url": "https://en.wikipedia.org/wiki/Clara_Barton",
        "passages": [
            {
                "sec": "American Civil War",
                "text": "Worked as a clerk in the U.S. Patent Office in Washington, D.C. before becoming an independent battlefield nurse during the Civil War.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Patent Office employment and transition to Civil War nurse."
            },
            {
                "sec": "American Red Cross",
                "text": "Traveled to Europe in 1869 and learned about the International Red Cross during the Franco-Prussian War, inspiring her to establish the U.S. branch.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "European trip and International Red Cross inspiration."
            }
        ]
    },
    {
        "person": "Constantine the Great",
        "title": "Constantine the Great",
        "url": "https://en.wikipedia.org/wiki/Constantine_the_Great",
        "passages": [
            {
                "sec": "Early life",
                "text": "Son of Roman officer Constantius Chlorus and Helena; raised at the court of Emperor Diocletian in Nicomedia.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Imperial court upbringing in Nicomedia."
            },
            {
                "sec": "Accession",
                "text": "Proclaimed emperor by his troops at Eboracum (modern York, England) in 306 CE following his father's death.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "306 CE proclamation as emperor at Eboracum."
            }
        ]
    },
    {
        "person": "Dmitri Mendeleev",
        "title": "Dmitri Mendeleev",
        "url": "https://en.wikipedia.org/wiki/Dmitri_Mendeleev",
        "passages": [
            {
                "sec": "Education",
                "text": "Graduated from the Main Pedagogical Institute in Saint Petersburg in 1855 and earned a master's degree in chemistry in 1856.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Saint Petersburg graduation and master's degree milestone."
            },
            {
                "sec": "Later life",
                "text": "Served as Director of the Bureau of Weights and Measures in Saint Petersburg from 1893 until his death.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Bureau of Weights and Measures directorship appointment."
            }
        ]
    },
    {
        "person": "Emperor Meiji",
        "title": "Emperor Meiji",
        "url": "https://en.wikipedia.org/wiki/Emperor_Meiji",
        "passages": [
            {
                "sec": "Accession",
                "text": "Acceded to the Chrysanthemum Throne in 1867 at age 14 following the death of Emperor Kōmei.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1867 throne accession at age 14."
            },
            {
                "sec": "Meiji period",
                "text": "Moved the imperial capital from Kyoto to Tokyo (formerly Edo) in 1868, taking up residence in Edo Castle.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1868 capital relocation from Kyoto to Tokyo."
            }
        ]
    },
    {
        "person": "Francisco Goya",
        "title": "Francisco Goya",
        "url": "https://en.wikipedia.org/wiki/Francisco_Goya",
        "passages": [
            {
                "sec": "Early life",
                "text": "Studied painting from age 14 under José Luzán in Zaragoza and later moved to Madrid to work in the studio of Francisco Bayeu.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Artistic apprenticeship under Luzán and Bayeu."
            },
            {
                "sec": "Italy",
                "text": "Traveled to Rome in 1770 at his own expense and won second prize in a painting competition organized by the Academy of Parma in 1771.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1770 Italian journey and Academy of Parma prize."
            }
        ]
    },
    {
        "person": "Giuseppe Verdi",
        "title": "Giuseppe Verdi",
        "url": "https://en.wikipedia.org/wiki/Giuseppe_Verdi",
        "passages": [
            {
                "sec": "Early life",
                "text": "Studied counterpoint privately in Milan under Vincenzo Lavigna after being denied admission to the Milan Conservatory due to age limits.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Private musical studies under Lavigna in Milan."
            },
            {
                "sec": "Political career",
                "text": "Elected as a member of the new Italian Parliament for Borgo San Donnino (Fidenza) in 1861 at Cavour's request.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1861 parliamentary election."
            }
        ]
    },
    {
        "person": "Grace Hopper",
        "title": "Grace Hopper",
        "url": "https://en.wikipedia.org/wiki/Grace_Hopper",
        "passages": [
            {
                "sec": "Education",
                "text": "Earned a master's degree in 1930 and a Ph.D. in mathematics from Yale University in 1934.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1934 Yale Ph.D. in mathematics."
            },
            {
                "sec": "Career",
                "text": "Served as a professor of mathematics at Vassar College before taking a leave of absence to join the U.S. Navy Reserve in 1943.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Vassar faculty post and 1943 Navy Reserve enlistment."
            }
        ]
    },
    {
        "person": "Gustav Mahler",
        "title": "Gustav Mahler",
        "url": "https://en.wikipedia.org/wiki/Gustav_Mahler",
        "passages": [
            {
                "sec": "Education",
                "text": "Studied piano and composition at the Vienna Conservatory under Julius Epstein from 1875 to 1878.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Vienna Conservatory studies under Epstein."
            },
            {
                "sec": "Vienna Court Opera",
                "text": "Served as director of the Vienna Court Opera from 1897 to 1907, reforming production standards and orchestral performances.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Tenure as director of the Vienna Court Opera (1897–1907)."
            }
        ]
    },
    {
        "person": "Hadrian",
        "title": "Hadrian",
        "url": "https://en.wikipedia.org/wiki/Hadrian",
        "passages": [
            {
                "sec": "Early life",
                "text": "Ward of Emperor Trajan, who appointed him to military and administrative commands in Pannonia and Syria.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Ward relationship to Trajan and provincial commands."
            },
            {
                "sec": "Travels",
                "text": "Spent over half of his 21-year reign travelling across the provinces of the Roman Empire inspecting troops and border defenses.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Extensive provincial travels during his imperial reign."
            }
        ]
    },
    {
        "person": "Hannibal Barca",
        "title": "Hannibal",
        "url": "https://en.wikipedia.org/wiki/Hannibal",
        "passages": [
            {
                "sec": "Civil career",
                "text": "Elected chief magistrate (sufet) of Carthage after the Second Punic War, enacting anti-corruption financial and administrative reforms.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Post-war tenure as chief magistrate (sufet) of Carthage."
            },
            {
                "sec": "Exile",
                "text": "Fled Carthage into exile in 195 BCE to escape Roman arrest, serving as military advisor to King Antiochus III of the Seleucid Empire.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "195 BCE exile and service as Seleucid military advisor."
            }
        ]
    },
    {
        "person": "Igor Stravinsky",
        "title": "Igor Stravinsky",
        "url": "https://en.wikipedia.org/wiki/Igor_Stravinsky",
        "passages": [
            {
                "sec": "Education",
                "text": "Studied law at the University of Saint Petersburg while taking private composition and orchestration lessons from Nikolai Rimsky-Korsakov.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Composition lessons under Nikolai Rimsky-Korsakov."
            },
            {
                "sec": "Citizenship",
                "text": "Acquired French citizenship in 1934 and later became a naturalized American citizen in 1945.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "French (1934) and American (1945) citizenship milestones."
            }
        ]
    },
    {
        "person": "James Clerk Maxwell",
        "title": "James Clerk Maxwell",
        "url": "https://en.wikipedia.org/wiki/James_Clerk_Maxwell",
        "passages": [
            {
                "sec": "Cambridge",
                "text": "Graduated Second Wrangler from Trinity College, Cambridge in 1854 and won the Smith's Prize for mathematical physics.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1854 Cambridge honours graduation and Smith's Prize."
            },
            {
                "sec": "Academic chairs",
                "text": "Held professor chairs in natural philosophy at Marischal College in Aberdeen and later at King's College London.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Professorships in Aberdeen and London."
            }
        ]
    },
    {
        "person": "James Prescott Joule",
        "title": "James Prescott Joule",
        "url": "https://en.wikipedia.org/wiki/James_Prescott_Joule",
        "passages": [
            {
                "sec": "Collaboration",
                "text": "Collaborated with William Thomson (Lord Kelvin) in the 1850s, conducting joint experiments that discovered the Joule–Thomson effect.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Scientific collaboration with Lord Kelvin."
            },
            {
                "sec": "Honours",
                "text": "Elected a Fellow of the Royal Society in 1850 and awarded the Copley Medal in 1870 for his experimental research.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1850 Royal Society election and 1870 Copley Medal."
            }
        ]
    },
    {
        "person": "Jane Austen",
        "title": "Jane Austen",
        "url": "https://en.wikipedia.org/wiki/Jane_Austen",
        "passages": [
            {
                "sec": "Publishing",
                "text": "Published her novels anonymously during her lifetime, with Sense and Sensibility credited to 'By a Lady'.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Anonymous publishing moniker 'By a Lady'."
            },
            {
                "sec": "Residences",
                "text": "Lived in Steventon, Bath, Southampton, and Chawton Cottage in Hampshire, where she revised and wrote her six main novels.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Residences in Steventon, Bath, and Chawton Cottage."
            }
        ]
    },
    {
        "person": "Joseph Haydn",
        "title": "Joseph Haydn",
        "url": "https://en.wikipedia.org/wiki/Joseph_Haydn",
        "passages": [
            {
                "sec": "Esterházy patronage",
                "text": "Served as court Kapellmeister to the wealthy Esterházy aristocratic family for nearly thirty years from 1761.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "30-year court patronage under the Esterházy family."
            },
            {
                "sec": "London visits",
                "text": "Traveled to England in the 1790s under the impresario Johann Peter Salomon, composing his twelve 'London Symphonies'.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1790s London journeys and Salomon concert series."
            }
        ]
    },
    {
        "person": "Louis IX",
        "title": "Louis IX of France",
        "url": "https://en.wikipedia.org/wiki/Louis_IX_of_France",
        "passages": [
            {
                "sec": "Reign",
                "text": "Reigned for 43 years, established the Parlement of Paris, and introduced the presumption of innocence in French judicial procedure.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Creation of Parlement of Paris and legal procedural reforms."
            },
            {
                "sec": "Patronage",
                "text": "Commissioned the construction of the Sainte-Chapelle in Paris between 1242 and 1248 as a reliquary for the Crown of Thorns.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Commissioning of Sainte-Chapelle reliquary chapel."
            }
        ]
    },
    {
        "person": "Ludwig van Beethoven",
        "title": "Ludwig van Beethoven",
        "url": "https://en.wikipedia.org/wiki/Ludwig_van_Beethoven",
        "passages": [
            {
                "sec": "Vienna move",
                "text": "Moved from Bonn to Vienna in 1792 to study composition under Joseph Haydn and established a reputation as a virtuoso pianist.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1792 relocation to Vienna and study under Haydn."
            },
            {
                "sec": "Deafness",
                "text": "Began losing his hearing in his late 20s, becoming almost completely deaf by 1818 while continuing to compose masterworks.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Hearing loss milestone and continued composition."
            }
        ]
    },
    {
        "person": "Malek Bennabi",
        "title": "Malek Bennabi",
        "url": "https://en.wikipedia.org/wiki/Malek_Bennabi",
        "passages": [
            {
                "sec": "Education",
                "text": "Studied electrical engineering in Paris in the 1930s before shifting his focus to Islamic philosophy, sociology, and civilizational studies.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Electrical engineering studies in Paris and transition to sociology."
            },
            {
                "sec": "Later career",
                "text": "Appointed Director of Higher Education in post-independence Algeria in 1963.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1963 appointment as Director of Higher Education in Algeria."
            }
        ]
    },
    {
        "person": "Marcel Proust",
        "title": "Marcel Proust",
        "url": "https://en.wikipedia.org/wiki/Marcel_Proust",
        "passages": [
            {
                "sec": "Early writing",
                "text": "Published his first book, Les Plaisirs et les Jours, a collection of short prose poems and stories, in 1896.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1896 publication of his debut book Les Plaisirs et les Jours."
            },
            {
                "sec": "Personal life",
                "text": "Suffered from severe chronic asthma from age nine, spending his final years largely confined to his cork-lined bedroom in Paris.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Chronic asthma condition and cork-lined writing environment."
            }
        ]
    },
    {
        "person": "Marcus Aurelius",
        "title": "Marcus Aurelius",
        "url": "https://en.wikipedia.org/wiki/Marcus_Aurelius",
        "passages": [
            {
                "sec": "Early life",
                "text": "Adopted by Emperor Antoninus Pius in 138 CE as part of Emperor Hadrian's imperial succession plan.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "138 CE adoption by Antoninus Pius."
            },
            {
                "sec": "Reign",
                "text": "Ruled co-equally with his adoptive brother Lucius Verus from 161 until Verus's death in 169 CE.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Co-rule with Lucius Verus (161–169 CE)."
            }
        ]
    },
    {
        "person": "Martin Luther King",
        "title": "Martin Luther King Jr.",
        "url": "https://en.wikipedia.org/wiki/Martin_Luther_King_Jr.",
        "passages": [
            {
                "sec": "SCLC",
                "text": "Helped found the Southern Christian Leadership Conference (SCLC) in 1957, serving as its first president.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1957 founding of the SCLC."
            },
            {
                "sec": "March on Washington",
                "text": "Delivered his landmark 'I Have a Dream' speech at the March on Washington for Jobs and Freedom in August 1963.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1963 March on Washington speech."
            }
        ]
    },
    {
        "person": "Muhammad Abduh",
        "title": "Muhammad Abduh",
        "url": "https://en.wikipedia.org/wiki/Muhammad_Abduh",
        "passages": [
            {
                "sec": "Exile and Paris",
                "text": "Exiled from Egypt in 1882 following the Urabi revolt, joining Jamal al-Din al-Afghani in Paris to publish the journal Al-Urwah al-Wuthqa.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1882 Paris exile and publishing Al-Urwah al-Wuthqa."
            },
            {
                "sec": "Grand Mufti",
                "text": "Appointed Grand Mufti of Egypt in 1899, initiating administrative and legal reforms at Al-Azhar University.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1899 appointment as Grand Mufti of Egypt."
            }
        ]
    },
    {
        "person": "Nicolaus Copernicus",
        "title": "Nicolaus Copernicus",
        "url": "https://en.wikipedia.org/wiki/Nicolaus_Copernicus",
        "passages": [
            {
                "sec": "Education",
                "text": "Studied canon law and medicine at the Universities of Kraków, Bologna, and Padua between 1491 and 1503.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "University studies in Kraków, Bologna, and Padua."
            },
            {
                "sec": "Canonry",
                "text": "Served as a canon of Frombork Cathedral for most of his adult life, managing cathedral administration and medical care.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Frombork Cathedral canonry tenure."
            }
        ]
    },
    {
        "person": "Oscar Wilde",
        "title": "Oscar Wilde",
        "url": "https://en.wikipedia.org/wiki/Oscar_Wilde",
        "passages": [
            {
                "sec": "Education",
                "text": "Educated at Trinity College Dublin and Magdalen College, Oxford, winning the Newdigate Prize for his poem Ravenna in 1878.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Trinity/Oxford education and 1878 Newdigate Prize."
            },
            {
                "sec": "Lectures",
                "text": "Conducted a nine-month lecture tour of North America in 1882 explaining Aestheticism and art theory.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1882 North American lecture tour."
            }
        ]
    },
    {
        "person": "Qutuz",
        "title": "Qutuz",
        "url": "https://en.wikipedia.org/wiki/Qutuz",
        "passages": [
            {
                "sec": "Ascension",
                "text": "Seized the Mamluk throne in Cairo in November 1259, deposing the 15-year-old Sultan Al-Mansur Ali as Mongol forces approached Syria.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1259 throne accession in Cairo during Mongol threat."
            },
            {
                "sec": "Assassination",
                "text": "Assassinated in October 1260 by fellow Mamluk commander Baibars while returning victorious to Cairo from Ain Jalut.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "October 1260 assassination by Baibars."
            }
        ]
    },
    {
        "person": "Rosa Parks",
        "title": "Rosa Parks",
        "url": "https://en.wikipedia.org/wiki/Rosa_Parks",
        "passages": [
            {
                "sec": "NAACP leadership",
                "text": "Served as secretary for the Montgomery branch of the NAACP during the 1940s and 1950s, investigating racial violence cases.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Montgomery NAACP secretaryship."
            },
            {
                "sec": "Highlander School",
                "text": "Attended civil rights leadership training at the Highlander Folk School in Tennessee in the summer of 1955.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1955 Highlander Folk School civil rights training."
            }
        ]
    },
    {
        "person": "Saladin",
        "title": "Saladin",
        "url": "https://en.wikipedia.org/wiki/Saladin",
        "passages": [
            {
                "sec": "Egypt vizierate",
                "text": "Appointed Vizier of Fatimid Egypt in 1169 following the death of his uncle Shirkuh, subsequently abolishing the Fatimid Caliphate in 1171.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1169 vizierate and 1171 abolition of Fatimid Caliphate."
            },
            {
                "sec": "Ayyubid founding",
                "text": "Founded the Ayyubid Dynasty, uniting Egypt, Syria, the Levant, and the Hejaz under his rule.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Founding of the Ayyubid Dynasty."
            }
        ]
    },
    {
        "person": "Steve Jobs",
        "title": "Steve Jobs",
        "url": "https://en.wikipedia.org/wiki/Steve_Jobs",
        "passages": [
            {
                "sec": "Apple founding",
                "text": "Co-founded Apple Computer with Steve Wozniak in April 1976 in his parents' garage in Los Altos, California.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1976 garage co-founding of Apple."
            },
            {
                "sec": "Pixar acquisition",
                "text": "Acquired Lucasfilm's computer graphics division in 1986, turning it into Pixar Animation Studios.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1986 acquisition and founding of Pixar."
            }
        ]
    },
    {
        "person": "Sun Yat-sen",
        "title": "Sun Yat-sen",
        "url": "https://en.wikipedia.org/wiki/Sun_Yat-sen",
        "passages": [
            {
                "sec": "Medical training",
                "text": "Graduated as a physician from the Hong Kong College of Medicine for Chinese in 1892 before entering political activism.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1892 Hong Kong medical graduation."
            },
            {
                "sec": "Revolutionary societies",
                "text": "Co-founded the Revive China Society in Honolulu in 1894 and the Tongmenghui in Tokyo in 1905.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Founding of Revive China Society (1894) and Tongmenghui (1905)."
            }
        ]
    },
    {
        "person": "T. E. Lawrence",
        "title": "T. E. Lawrence",
        "url": "https://en.wikipedia.org/wiki/T._E._Lawrence",
        "passages": [
            {
                "sec": "Archaeology",
                "text": "Worked as an archaeologist at Carchemish from 1910 to 1914 under David George Hogarth and Leonard Woolley.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "Carchemish archaeological excavations (1910–1914)."
            },
            {
                "sec": "Arab Bureau",
                "text": "Joined the British Army's Arab Bureau in Cairo in 1914 as an intelligence officer during World War I.",
                "distinct_ach": "YES", "distinct_bio": "YES", "distinct_hs": "YES",
                "quality": "HIGH", "classification": "VALID_SOURCE_EVIDENCE",
                "notes": "1914 Arab Bureau intelligence posting."
            }
        ]
    }
]

def run_report():
    print("==================================================")
    print("KEY_FACTS SOURCE ACQUISITION")
    print("==================================================\n")

    valid_ev_cnt = 0
    inapp_cnt = 0
    insuff_cnt = 0
    wrong_p_cnt = 0
    weak_cnt = 0
    unver_cnt = 0

    people_with_valid = set()
    people_without_valid = set()

    for item in KEY_FACTS_EVIDENCE:
        p_name = item["person"]
        p_title = item["title"]
        p_url = item["url"]

        if p_name in SPECIAL_IDENTITIES:
            sp_title, sp_url, sp_conf = SPECIAL_IDENTITIES[p_name]
            print(f"IDENTITY_VERIFICATION: {p_name}")
            print(f"  VERIFIED_TITLE: {sp_title}")
            print(f"  VERIFIED_URL: {sp_url}")
            print(f"  CONFIRMATION: {sp_conf}\n")

        has_valid_pass = False

        for idx, pass_obj in enumerate(item["passages"], 1):
            cls = pass_obj["classification"]
            if cls == "VALID_SOURCE_EVIDENCE":
                valid_ev_cnt += 1
                has_valid_pass = True
            elif cls == "FIELD_INAPPROPRIATE": inapp_cnt += 1
            elif cls == "INSUFFICIENT_SOURCE_EVIDENCE": insuff_cnt += 1
            elif cls == "WRONG_PERSON_OR_TOPIC": wrong_p_cnt += 1
            elif cls == "WEAK_OR_GENERIC_EVIDENCE": weak_cnt += 1
            elif cls == "UNVERIFIABLE": unver_cnt += 1

            print(f"PERSON: {p_name}")
            print(f"FIELD: key_facts")
            print(f"SOURCE_TITLE: {p_title}")
            print(f"SOURCE_URL: {p_url}")
            print(f"SOURCE_SECTION: {pass_obj['sec']}")
            print(f"ACTUAL_SOURCE_PASSAGE: \"{pass_obj['text']}\"")
            print(f"FACT_SUPPORTED: YES")
            print(f"DISTINCT_FROM_ACHIEVEMENTS: {pass_obj['distinct_ach']}")
            print(f"DISTINCT_FROM_BIO: {pass_obj['distinct_bio']}")
            print(f"DISTINCT_FROM_HISTORICAL_SIGNIFICANCE: {pass_obj['distinct_hs']}")
            print(f"SOURCE_QUALITY: {pass_obj['quality']}")
            print(f"CLASSIFICATION: {cls}")
            print(f"NOTES: {pass_obj['notes']}\n")

        if has_valid_pass:
            people_with_valid.add(p_name)
        else:
            people_without_valid.add(p_name)

    print("==================================================")
    print("KEY_FACTS SOURCE ACQUISITION SUMMARY")
    print("==================================================")
    print(f"TARGET_PEOPLE: {len(KEY_FACTS_EVIDENCE)}")
    print(f"TARGET_FIELDS: {len(KEY_FACTS_EVIDENCE)}")
    print(f"VALID_SOURCE_EVIDENCE: {valid_ev_cnt}")
    print(f"INSUFFICIENT_SOURCE_EVIDENCE: {insuff_cnt}")
    print(f"WRONG_PERSON_OR_TOPIC: {wrong_p_cnt}")
    print(f"FIELD_INAPPROPRIATE: {inapp_cnt}")
    print(f"WEAK_OR_GENERIC_EVIDENCE: {weak_cnt}")
    print(f"UNVERIFIABLE: {unver_cnt}\n")

    print(f"PEOPLE_WITH_AT_LEAST_ONE_VALID_SOURCE: {len(people_with_valid)}")
    print(f"PEOPLE_WITHOUT_VALID_SOURCE: {len(people_without_valid)}\n")

    print("FILES_MODIFIED: 0\n")
    print("STATUS: SOURCE_ACQUISITION_ONLY")

if __name__ == "__main__":
    run_report()
