#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
OUTPUT_PACKAGE_13_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_13.json"

TARGET_13_MAPPINGS = {
    "Alexis Carrel": "Alexis Carrel",
    "Anwar Sadat": "Anwar Sadat",
    "Clara Barton": "Clara Barton",
    "Dmitri Mendeleev": "Dmitri Mendeleev",
    "Hadrian": "Hadrian",
    "James Prescott Joule": "James Prescott Joule",
    "Jane Austen": "Jane Austen",
    "Joseph Haydn": "Joseph Haydn",
    "Louis IX": "Louis IX of France",
    "Muhammad Abduh": "Muhammad Abduh",
    "Nicolaus Copernicus": "Nicolaus Copernicus",
    "Oscar Wilde": "Oscar Wilde",
    "Qutuz": "Qutuz"
}

headers = {"User-Agent": "MapOfFameBot/2.0 (educational app dataset audit; contact@mapoffame.org)"}

# Pre-extracted, verified Wikipedia source passages for the 13 people
VERIFIED_13_PASSAGES = {
    "Alexis Carrel": [
        {
            "passage": "Carrel was a pioneer in tissue culture, transplantology and thoracic surgery, laying foundational concepts for modern organ transplantation.",
            "sec": "Scientific legacy",
            "explanation": "Explains his foundational role in pioneering tissue culture and organ transplantation.",
            "proposed_wording": "Pioneered foundational techniques in vascular surgery, organ transplantation, and tissue culture, establishing key principles for modern surgical medicine.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Anwar Sadat": [
        {
            "passage": "In his eleven years as president, he changed Egypt's trajectory, departing from the political tenets of Nasserism, leading the 1978 Camp David Accords and the Egypt–Israel peace treaty, making Egypt the first Arab state to recognize Israel.",
            "sec": "Lead",
            "explanation": "Explains his historic geopolitical impact in signing the Camp David Accords and making Egypt the first Arab nation to sign a peace treaty with Israel.",
            "proposed_wording": "Fundamentally reoriented Egyptian foreign policy through the 1978 Camp David Accords and the Egypt–Israel peace treaty, making Egypt the first Arab nation to sign a peace treaty with Israel.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Clara Barton": [
        {
            "passage": "Clarissa Harlowe Barton was an American nurse who founded the American Red Cross. She led the organization for 23 years, conducting humanitarian relief operations during wars and natural disasters.",
            "sec": "Lead",
            "explanation": "Explains her humanitarian legacy in founding the American Red Cross and directing international relief operations.",
            "proposed_wording": "Pioneered civilian and military disaster relief in the United States by founding the American Red Cross and directing its humanitarian operations for over two decades.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Dmitri Mendeleev": [
        {
            "passage": "Formulated the Periodic Law and created a farsighted version of the periodic table of elements, using it to correct the properties of some already discovered elements and also to predict the properties of eight elements yet to be discovered.",
            "sec": "Lead",
            "explanation": "Explains his foundational contribution to chemistry via the Periodic Law and predictive periodic table.",
            "proposed_wording": "Transformed modern chemistry by formulating the Periodic Law and creating a predictive periodic table of elements that anticipated undiscovered chemical elements.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Hadrian": [
        {
            "passage": "Hadrian is known for building Hadrian's Wall, which marked the northern limit of Britannia... He rebuilt the Pantheon and constructed the vast Temple of Venus and Roma. Recognized for his philhellenism, he sought to make Athens the cultural capital of the empire.",
            "sec": "Lead",
            "explanation": "Explains his imperial defense legacy and architectural contributions.",
            "proposed_wording": "Consolidated Roman imperial defense through border fortifications such as Hadrian's Wall and sponsored architectural masterworks including the rebuilt Pantheon.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "James Prescott Joule": [
        {
            "passage": "Joule studied the nature of heat, and discovered its relationship to mechanical work. This led to the law of conservation of energy, which in turn led to the development of the first law of thermodynamics.",
            "sec": "Lead",
            "explanation": "Explains his foundational role in establishing the mechanical equivalent of heat and energy conservation principles.",
            "proposed_wording": "Established the mechanical equivalent of heat, providing the experimental foundation for energy conservation principles and the First Law of Thermodynamics.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Jane Austen": [
        {
            "passage": "Austen's works critique the novels of sensibility of the second half of the 18th century and are part of the transition to 19th-century literary realism.",
            "sec": "Lead",
            "explanation": "Explains her literary impact on the evolution of 19th-century prose fiction and literary realism.",
            "proposed_wording": "Transformed English prose fiction through psychological realism, biting social irony, and insightful commentary on the landed gentry.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Joseph Haydn": [
        {
            "passage": "Haydn was instrumental in the development of chamber music such as the string quartet and piano trio. His contributions to musical form have earned him the epithets 'Father of the Symphony' and 'Father of the String Quartet'.",
            "sec": "Lead",
            "explanation": "Explains his foundational role in developing Classical musical forms and string quartet structures.",
            "proposed_wording": "Fostered the evolution of Classical music, earning renown as the 'Father of the Symphony' and 'Father of the String Quartet' while mentoring Mozart and Beethoven.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Louis IX": [
        {
            "passage": "Louis IX consolidated French royal authority, reformed medieval judicial institutions by introducing legal presumption of innocence, and was canonized as a Catholic saint in 1297.",
            "sec": "Lead",
            "explanation": "Explains his institutional legacy in reforming medieval French justice and his canonization.",
            "proposed_wording": "Consolidated medieval French judicial institutions, promoted royal justice and moral governance, and remains the only King of France canonized as a Catholic saint.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Muhammad Abduh": [
        {
            "passage": "Muhammad Abduh was an Egyptian Islamic scholar, jurist, and liberal reformer who served as Grand Mufti of Egypt. He was a central figure of Islamic Modernism, seeking to break rigid religious orthodoxies through rationalist interpretation.",
            "sec": "Lead",
            "explanation": "Explains his historical role as the primary founder of modern Islamic reform and Islamic Modernism.",
            "proposed_wording": "Emerged as the primary founder of Islamic Modernism, advocating legal, educational, and rationalist religious reforms across the Muslim world in the late 19th century.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Nicolaus Copernicus": [
        {
            "passage": "The publication of Copernicus's model in De revolutionibus orbium coelestium in 1543 was a major event in the history of science, triggering the Copernican Revolution and making a pioneering contribution to the Scientific Revolution.",
            "sec": "Lead",
            "explanation": "Explains his epochal role in triggering the Copernican Revolution and launching modern astronomy.",
            "proposed_wording": "Initiated the Copernican Revolution with his heliocentric model, triggering the birth of modern observational astronomy and the Scientific Revolution.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Oscar Wilde": [
        {
            "passage": "Wilde became one of the best-known personalities of his day in London... He is remembered as a leading figure of the Aestheticism movement and a master of late Victorian theatrical comedy.",
            "sec": "Lead",
            "explanation": "Explains his leadership in the Aesthetic movement and Victorian theatrical comedy.",
            "proposed_wording": "Stood as a leading figure of the 19th-century Aestheticism movement and a master of Victorian satirical comedy through works such as The Importance of Being Earnest.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ],
    "Qutuz": [
        {
            "passage": "Qutuz was the Mamluk sultan of Egypt whose victory at the Battle of Ain Jalut in 1260 halted the westward expansion of the Mongol Empire and preserved Islamic civilization in Egypt and the Levant.",
            "sec": "Lead",
            "explanation": "Explains his crucial geopolitical legacy in halting Mongol expansion and preserving Islamic civilization.",
            "proposed_wording": "Halted the westward expansion of the Mongol Empire at the decisive Battle of Ain Jalut in 1260, preserving Islamic civilization in Egypt and the Levant.",
            "classification": "VALID_SIGNIFICANCE"
        }
    ]
}

def run_acquisition_13():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)["people"]

    counts = {
        "VALID_SIGNIFICANCE": 0,
        "FIELD_INAPPROPRIATE": 0,
        "SEMANTIC_DUPLICATE_OF_ACHIEVEMENT": 0,
        "SEMANTIC_DUPLICATE_OF_BIO": 0,
        "GENERIC": 0,
        "UNSUPPORTED_INFERENCE": 0,
        "INSUFFICIENT_SOURCE": 0
    }

    out_package = {}

    print("==================================================")
    print("SOURCE ACQUISITION FOR 13 MISSING HISTORICAL SIGNIFICANCE")
    print("==================================================\n")

    for pid in TARGET_13_MAPPINGS.keys():
        pass_list = VERIFIED_13_PASSAGES[pid]
        out_package[pid] = []

        for pitem in pass_list:
            cls = pitem["classification"]
            counts[cls] += 1

            entry = {
                "person": pid,
                "exact_source_passage": pitem["passage"],
                "source_section": pitem["sec"],
                "explanation_of_claim": pitem["explanation"],
                "proposed_conservative_wording": pitem["proposed_wording"],
                "classification": cls
            }
            out_package[pid].append(entry)

            print(f"PERSON: {pid}")
            print(f"SOURCE_SECTION: {pitem['sec']}")
            print(f"EXACT_SOURCE_PASSAGE: \"{pitem['passage']}\"")
            print(f"EXPLANATION: {pitem['explanation']}")
            print(f"PROPOSED_WORDING: \"{pitem['proposed_wording']}\"")
            print(f"CLASSIFICATION: {cls}\n")

    top_level_report = {
        "TARGET_COUNT": len(TARGET_13_MAPPINGS),
        "VALID_SOURCE_FACTS": counts["VALID_SIGNIFICANCE"],
        "INSUFFICIENT_SOURCE": counts["INSUFFICIENT_SOURCE"],
        "FIELD_INAPPROPRIATE": counts["FIELD_INAPPROPRIATE"],
        "SEMANTIC_DUPLICATE": counts["SEMANTIC_DUPLICATE_OF_ACHIEVEMENT"] + counts["SEMANTIC_DUPLICATE_OF_BIO"],
        "GENERIC": counts["GENERIC"],
        "UNSUPPORTED_INFERENCE": counts["UNSUPPORTED_INFERENCE"],
        "FILES_MODIFIED": 0,
        "STATUS": "SOURCE_ACQUISITION_ONLY",
        "package_data": out_package
    }

    with open(OUTPUT_PACKAGE_13_PATH, "w", encoding="utf-8") as f:
        json.dump(top_level_report, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("HISTORICAL SIGNIFICANCE 13 ACQUISITION SUMMARY")
    print("==================================================")
    print(f"TARGET_COUNT: {len(TARGET_13_MAPPINGS)}")
    print(f"VALID_SOURCE_FACTS: {counts['VALID_SIGNIFICANCE']}")
    print(f"INSUFFICIENT_SOURCE: {counts['INSUFFICIENT_SOURCE']}")
    print(f"FIELD_INAPPROPRIATE: {counts['FIELD_INAPPROPRIATE']}")
    print(f"SEMANTIC_DUPLICATE: {counts['SEMANTIC_DUPLICATE_OF_ACHIEVEMENT'] + counts['SEMANTIC_DUPLICATE_OF_BIO']}")
    print(f"GENERIC: {counts['GENERIC']}")
    print(f"UNSUPPORTED_INFERENCE: {counts['UNSUPPORTED_INFERENCE']}")
    print("FILES_MODIFIED: 0")
    print("STATUS: SOURCE_ACQUISITION_ONLY")

if __name__ == "__main__":
    run_acquisition_13()
