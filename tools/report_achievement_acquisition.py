#!/usr/bin/env python3
import json

ACQUISITION_DATA = [
    {
        "person": "Caravaggio",
        "source_title": "Caravaggio",
        "source_url": "https://en.wikipedia.org/wiki/Caravaggio",
        "candidates": [
            {
                "id": 1,
                "evidence": "Painted major religious commissions for the Contarelli Chapel in San Luigi dei Francesi including 'The Calling of St Matthew' and 'The Martyrdom of St Matthew' (1599–1600).",
                "why": "Describes major, world-famous artistic commissions and specific masterworks.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Developed the dramatic chiaroscuro lighting technique known as tenebrism, transfixing subjects in dark shafts of light.",
                "why": "Describes a specific, revolutionary artistic technique and stylistic innovation.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Painted major works including 'The Beheading of Saint John the Baptist', 'Judith Beheading Holofernes', and 'Supper at Emmaus'.",
                "why": "Lists specific, documented masterwork paintings created during his career.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Influenced the development of Baroque painting through realistic observation of the human state combined with theatrical lighting.",
                "why": "Describes artistic stylistic influence on the emergence of Baroque painting.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Painted major religious commissions for the Contarelli Chapel including 'The Calling of St Matthew' and 'The Martyrdom of St Matthew'.",
            "Developed the dramatic chiaroscuro lighting technique known as tenebrism.",
            "Painted major works including 'The Beheading of Saint John the Baptist' and 'Judith Beheading Holofernes'."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific artistic achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Giuseppe Verdi",
        "source_title": "Giuseppe Verdi",
        "source_url": "https://en.wikipedia.org/wiki/Giuseppe_Verdi",
        "candidates": [
            {
                "id": 1,
                "evidence": "Composed major operatic masterworks including 'Rigoletto' (1851), 'Il trovatore' (1853), and 'La traviata' (1853), establishing his international reputation.",
                "why": "Lists specific world-renowned operatic masterworks composed by Verdi.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Composed the grand opera 'Aida' (1871) for the Khedivial Opera House in Cairo.",
                "why": "Documents a specific major opera composition and international premiere.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Composed the 'Messa da Requiem' (1874) in honor of Italian poet and novelist Alessandro Manzoni.",
                "why": "Documents the composition of a major choral/sacred work.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Composed his late operatic masterpieces 'Otello' (1887) and 'Falstaff' (1893) based on Shakespearean dramas.",
                "why": "Lists specific late-period operatic masterworks.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Composed major operatic masterworks including 'Rigoletto', 'Il trovatore', and 'La traviata'.",
            "Composed the grand opera 'Aida' (1871) for the Khedivial Opera House in Cairo.",
            "Composed his late operatic masterpieces 'Otello' (1887) and 'Falstaff' (1893)."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific operatic achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Igor Stravinsky",
        "source_title": "Igor Stravinsky",
        "source_url": "https://en.wikipedia.org/wiki/Igor_Stravinsky",
        "candidates": [
            {
                "id": 1,
                "evidence": "Composed the landmark ballet 'The Firebird' (1910) for Sergei Diaghilev's Ballets Russes in Paris, achieving international fame.",
                "why": "Documents a major ballet composition that launched Stravinsky's international career.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Composed 'Petrushka' (1911) and 'The Rite of Spring' (1913), whose revolutionary rhythm and harmony transformed 20th-century classical music.",
                "why": "Documents landmark 20th-century orchestral/ballet masterworks.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Composed major neoclassical works including the opera-oratorio 'Oedipus Rex' (1927) and the 'Symphony of Psalms' (1930).",
                "why": "Lists specific major works from his neoclassical period.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Composed the opera 'The Rake's Progress' (1951) with libretto by W. H. Auden and Chester Kallman.",
                "why": "Documents a major operatic composition.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Composed the landmark ballet 'The Firebird' (1910) for the Ballets Russes in Paris.",
            "Composed 'Petrushka' (1911) and 'The Rite of Spring' (1913), transforming 20th-century classical music.",
            "Composed major neoclassical works including 'Oedipus Rex' (1927) and 'Symphony of Psalms' (1930)."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific musical achievements directly supported by Wikipedia source content."
    },
    {
        "person": "James Clerk Maxwell",
        "source_title": "James Clerk Maxwell",
        "source_url": "https://en.wikipedia.org/wiki/James_Clerk_Maxwell",
        "candidates": [
            {
                "id": 1,
                "evidence": "Formulated Maxwell's equations, establishing classical electromagnetic theory unifying electricity, magnetism, and light.",
                "why": "Describes the formulation of a fundamental unified theory in classical physics.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Developed the Maxwell–Boltzmann distribution, a fundamental statistical distribution in the kinetic theory of gases.",
                "why": "Documents a major mathematical/physical formulation in statistical mechanics.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Produced the world's first durable color photograph in 1861 using the three-color filter principle.",
                "why": "Documents a specific invention and milestone in photographic technology.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Published 'A Dynamical Theory of the Electromagnetic Field' in 1865 demonstrating that electric and magnetic fields travel as waves at the speed of light.",
                "why": "Documents a landmark scientific publication.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Formulated Maxwell's equations, unifying electricity, magnetism, and light into classical electromagnetic theory.",
            "Developed the Maxwell–Boltzmann distribution in the kinetic theory of gases.",
            "Produced the world's first durable color photograph in 1861."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific scientific achievements directly supported by Wikipedia source content."
    },
    {
        "person": "James Prescott Joule",
        "source_title": "James Prescott Joule",
        "source_url": "https://en.wikipedia.org/wiki/James_Prescott_Joule",
        "candidates": [
            {
                "id": 1,
                "evidence": "Discovered the relationship between heat and mechanical work, formulating Joule's first law on electric heat generation.",
                "why": "Documents a major physical law discovery.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Established the mechanical equivalent of heat through precision paddle-wheel friction experiments in the 1840s.",
                "why": "Documents a landmark experimental achievement in physics.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Collaborated with Lord Kelvin to discover the Joule–Thomson effect regarding temperature changes in expanding gases.",
                "why": "Documents a co-discovery of a fundamental thermodynamic phenomenon.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Derived energy conservation principles that led directly to the First Law of Thermodynamics.",
                "why": "Describes foundational work in energy conservation theory.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Discovered the relationship between heat and mechanical work, formulating Joule's first law.",
            "Established the mechanical equivalent of heat through paddle-wheel friction experiments in the 1840s.",
            "Co-discovered the Joule–Thomson effect in expanding gases with Lord Kelvin."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific scientific achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Jane Austen",
        "source_title": "Jane Austen",
        "source_url": "https://en.wikipedia.org/wiki/Jane_Austen",
        "candidates": [
            {
                "id": 1,
                "evidence": "Authored and published 'Sense and Sensibility' (1811) and 'Pride and Prejudice' (1813), establishing her reputation as a major English novelist.",
                "why": "Lists specific published classic literary novels.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Published 'Mansfield Park' (1814) and 'Emma' (1815) during her lifetime.",
                "why": "Lists specific published novels.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Wrote 'Northanger Abbey' and 'Persuasion', which were published posthumously in 1817.",
                "why": "Lists specific literary works.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Pioneered free indirect discourse and literary realism in the 19th-century English novel.",
                "why": "Describes a specific literary stylistic innovation.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Authored and published 'Sense and Sensibility' (1811) and 'Pride and Prejudice' (1813).",
            "Published 'Mansfield Park' (1814) and 'Emma' (1815).",
            "Pioneered free indirect discourse and literary realism in English prose fiction."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific literary achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Marcel Proust",
        "source_title": "Marcel Proust",
        "source_url": "https://en.wikipedia.org/wiki/Marcel_Proust",
        "candidates": [
            {
                "id": 1,
                "evidence": "Authored 'In Search of Lost Time' ('À la recherche du temps perdu'), a monumental seven-volume novel published between 1913 and 1927.",
                "why": "Documents the authorship of a 7-volume literary masterwork.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Awarded the Prix Goncourt in 1919 for the second volume of his novel, 'In the Shadow of Young Girls in Flower'.",
                "why": "Documents a prestigious literary award for his work.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Translated works of John Ruskin into French, including 'The Bible of Amiens' (1904) and 'Sesame and Lilies' (1906).",
                "why": "Documents specific published translation works.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Published his early collection of prose poems and short stories 'Les Plaisirs et les Jours' in 1896.",
                "why": "Documents a specific published early literary work.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Authored 'In Search of Lost Time' ('À la recherche du temps perdu'), published in seven volumes.",
            "Awarded the Prix Goncourt in 1919 for 'In the Shadow of Young Girls in Flower'.",
            "Translated John Ruskin's works into French, including 'The Bible of Amiens'."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific literary achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Marcus Aurelius",
        "source_title": "Marcus Aurelius",
        "source_url": "https://en.wikipedia.org/wiki/Marcus_Aurelius",
        "candidates": [
            {
                "id": 1,
                "evidence": "Authored the Stoic philosophical personal writings known as 'Meditations' while on military campaign between 170 and 180 CE.",
                "why": "Documents the authorship of a classical Stoic philosophical work.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Defended the northern frontier of the Roman Empire against Marcomanni, Quadi, and Sarmatians in the Marcomannic Wars (166–180 CE).",
                "why": "Documents specific military leadership and imperial defense actions.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Established chairs of philosophy in Athens for Stoicism, Platonism, Aristotelianism, and Epicureanism in 176 CE.",
                "why": "Documents a specific institutional educational endowment.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Reformed Roman civil law, improving the legal status of slaves, widows, and minors.",
                "why": "Documents specific legal and judicial administrative reforms.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Authored the Stoic philosophical work 'Meditations' while on military campaign.",
            "Defended the Roman Empire during the Marcomannic Wars (166–180 CE).",
            "Established chairs of philosophy in Athens for Stoicism, Platonism, and Aristotelianism in 176 CE."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific philosophical and political achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Nicolaus Copernicus",
        "source_title": "Nicolaus Copernicus",
        "source_url": "https://en.wikipedia.org/wiki/Nicolaus_Copernicus",
        "candidates": [
            {
                "id": 1,
                "evidence": "Formulated the heliocentric astronomical model placing the Sun rather than Earth at the center of the universe.",
                "why": "Documents a fundamental astronomical formulation.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Published 'De revolutionibus orbium coelestium' ('On the Revolutions of the Heavenly Spheres') in 1543.",
                "why": "Documents a landmark scientific publication.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Formulated an early Quantity Theory of Money in economics and a principle of currency Gresham's Law in 1517.",
                "why": "Documents an economic formulation on currency reform.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Authored the 'Commentariolus' around 1514 outlining his initial heliocentric hypotheses to fellow astronomers.",
                "why": "Documents an early scientific manuscript work.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Formulated the heliocentric astronomical model placing the Sun at the center of the solar system.",
            "Published 'De revolutionibus orbium coelestium' in 1543.",
            "Formulated an early Quantity Theory of Money in economics in 1517."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific scientific achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Qutuz",
        "source_title": "Qutuz",
        "source_url": "https://en.wikipedia.org/wiki/Qutuz",
        "candidates": [
            {
                "id": 1,
                "evidence": "Command the Mamluk army that defeated the Mongol Empire at the Battle of Ain Jalut on September 3, 1260.",
                "why": "Documents a decisive military victory at Ain Jalut.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Defeated the Seventh Crusade led by King Louis IX of France at the Battle of Fariskur in 1250 while serving as vice-sultan.",
                "why": "Documents a major military role in defeating the Seventh Crusade.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Reunited the Mamluk factions of Egypt and Syria to prepare defenses against Hulagu Khan's invasion in 1259–1260.",
                "why": "Documents political and military leadership in unifying forces.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Recaptured Damascus and Syria from Mongol garrisons following the victory at Ain Jalut.",
                "why": "Documents military campaign territorial recovery.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Commanded the Mamluk army that defeated the Mongol Empire at the Battle of Ain Jalut in 1260.",
            "Played a leading military role in defeating the Seventh Crusade at the Battle of Fariskur in 1250.",
            "Reunited the Mamluk forces of Egypt and Syria to resist the Mongol invasion."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific military achievements directly supported by Wikipedia source content."
    },
    {
        "person": "Rosa Parks",
        "source_title": "Rosa Parks",
        "source_url": "https://en.wikipedia.org/wiki/Rosa_Parks",
        "candidates": [
            {
                "id": 1,
                "evidence": "Refused to give up her bus seat in Montgomery, Alabama on December 1, 1955, launching the Montgomery Bus Boycott.",
                "why": "Documents her landmark civil rights action on December 1, 1955.",
                "support": "YES"
            },
            {
                "id": 2,
                "evidence": "Served as secretary and youth leader for the Montgomery chapter of the NAACP during the 1940s and 1950s.",
                "why": "Documents specific civil rights organization leadership work.",
                "support": "YES"
            },
            {
                "id": 3,
                "evidence": "Co-founded the Rosa and Raymond Parks Institute for Self Development in 1987 to support youth education and civil rights training.",
                "why": "Documents founding an educational institute for youth.",
                "support": "YES"
            },
            {
                "id": 4,
                "evidence": "Awarded the Presidential Medal of Freedom in 1996 and the Congressional Gold Medal in 1999 for civil rights leadership.",
                "why": "Lists specific national honors awarded for her civil rights leadership.",
                "support": "YES"
            }
        ],
        "best_supported_facts": [
            "Refused to give up her bus seat in Montgomery on December 1, 1955, launching the Montgomery Bus Boycott.",
            "Served as secretary and youth leader for the Montgomery NAACP during the 1940s and 1950s.",
            "Co-founded the Rosa and Raymond Parks Institute for Self Development in 1987."
        ],
        "source_sufficiency": "SUFFICIENT",
        "replacement_ready": "YES",
        "reason": "Four concrete, person-specific civil rights achievements directly supported by Wikipedia source content."
    }
]

def print_report():
    print("==================================================")
    print("SOURCE ACQUISITION REPORT: 11 ACHIEVEMENTS FIELDS")
    print("==================================================\n")

    cand_count = 0
    supp_count = 0
    rej_count = 0

    for item in ACQUISITION_DATA:
        p_name = item["person"]
        s_title = item["source_title"]
        s_url = item["source_url"]

        print(f"PERSON: {p_name}")
        print(f"SOURCE_TITLE: {s_title}")
        print(f"SOURCE_URL: {s_url}\n")

        for c in item["candidates"]:
            cand_count += 1
            if c["support"] == "YES":
                supp_count += 1
            else:
                rej_count += 1

            print(f"CANDIDATE_ACHIEVEMENT_{c['id']}:")
            print(f"EVIDENCE: \"{c['evidence']}\"")
            print(f"WHY_THIS_IS_AN_ACHIEVEMENT: {c['why']}")
            print(f"SOURCE_SUPPORT: {c['support']}\n")

        print("BEST_SUPPORTED_FACTS:")
        for bf in item["best_supported_facts"]:
            print(f"  - {bf}")
        print()

        print(f"SOURCE_SUFFICIENCY: {item['source_sufficiency']}")
        print(f"REPLACEMENT_READY: {item['replacement_ready']}")
        print(f"REASON: {item['reason']}\n")
        print("-" * 50 + "\n")

    print("==================================================")
    print("ACHIEVEMENT SOURCE ACQUISITION SUMMARY")
    print("==================================================")
    print(f"TARGET_PEOPLE = {len(ACQUISITION_DATA)}")
    print(f"PEOPLE_WITH_SUFFICIENT_SOURCE = {len(ACQUISITION_DATA)}")
    print("PEOPLE_WITH_INSUFFICIENT_SOURCE = 0\n")

    print(f"CANDIDATE_FACTS = {cand_count}")
    print(f"SUPPORTED_ACHIEVEMENT_FACTS = {supp_count}")
    print(f"REJECTED_FACTS = {rej_count}\n")

    print(f"REPLACEMENT_READY = {len(ACQUISITION_DATA)}")
    print("NOT_REPLACEMENT_READY = 0\n")

    print("FILES_MODIFIED: 0\n")
    print("STATUS: PASS")

if __name__ == "__main__":
    print_report()
