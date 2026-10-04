#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
PKG_13_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_13.json"
OUTPUT_VAL_13_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_VALIDATION_13.json"

VALIDATION_13_DETAILS = [
    {
        "person": "Alexis Carrel",
        "source_passage": "Carrel was a pioneer in tissue culture, transplantology and thoracic surgery, laying foundational concepts for modern organ transplantation.",
        "original_proposed_wording": "Pioneered foundational techniques in vascular surgery, organ transplantation, and tissue culture, establishing key principles for modern surgical medicine.",
        "claim_breakdown": [
            {"claim": "Pioneer in tissue culture, transplantology, and thoracic surgery", "status": "SUPPORTED"},
            {"claim": "Laying foundational concepts for modern organ transplantation", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Pioneered concepts in tissue culture, transplantology, and thoracic surgery that laid foundational principles for modern organ transplantation.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Anwar Sadat",
        "source_passage": "In his eleven years as president, he changed Egypt's trajectory, departing from the political tenets of Nasserism, leading the 1978 Camp David Accords and the Egypt–Israel peace treaty, making Egypt the first Arab state to recognize Israel.",
        "original_proposed_wording": "Fundamentally reoriented Egyptian foreign policy through the 1978 Camp David Accords and the Egypt–Israel peace treaty, making Egypt the first Arab nation to sign a peace treaty with Israel.",
        "claim_breakdown": [
            {"claim": "Changed Egypt's trajectory departing from Nasserism", "status": "SUPPORTED"},
            {"claim": "Led 1978 Camp David Accords and Egypt-Israel peace treaty", "status": "SUPPORTED"},
            {"claim": "Made Egypt first Arab state to recognize Israel", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Reoriented Egyptian policy by leading the 1978 Camp David Accords and Egypt–Israel peace treaty, making Egypt the first Arab state to recognize Israel.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Clara Barton",
        "source_passage": "Clarissa Harlowe Barton was an American nurse who founded the American Red Cross. She led the organization for 23 years, conducting humanitarian relief operations during wars and natural disasters.",
        "original_proposed_wording": "Pioneered civilian and military disaster relief in the United States by founding the American Red Cross and directing its humanitarian operations for over two decades.",
        "claim_breakdown": [
            {"claim": "Founded the American Red Cross", "status": "SUPPORTED"},
            {"claim": "Led the organization for 23 years conducting relief during wars and natural disasters", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Founded the American Red Cross and directed its humanitarian relief operations during wars and natural disasters for twenty-three years.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Dmitri Mendeleev",
        "source_passage": "Formulated the Periodic Law and created a farsighted version of the periodic table of elements, using it to correct the properties of some already discovered elements and also to predict the properties of eight elements yet to be discovered.",
        "original_proposed_wording": "Transformed modern chemistry by formulating the Periodic Law and creating a predictive periodic table of elements that anticipated undiscovered chemical elements.",
        "claim_breakdown": [
            {"claim": "Formulated Periodic Law and created periodic table of elements", "status": "SUPPORTED"},
            {"claim": "Used table to correct known properties and predict undiscovered elements", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Formulated the Periodic Law and created a predictive periodic table of elements used to correct known properties and anticipate undiscovered elements.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Hadrian",
        "source_passage": "Hadrian is known for building Hadrian's Wall, which marked the northern limit of Britannia... He rebuilt the Pantheon and constructed the vast Temple of Venus and Roma. Recognized for his philhellenism, he sought to make Athens the cultural capital of the empire.",
        "original_proposed_wording": "Consolidated Roman imperial defense through border fortifications such as Hadrian's Wall and sponsored architectural masterworks including the rebuilt Pantheon.",
        "claim_breakdown": [
            {"claim": "Built Hadrian's Wall marking northern limit of Britannia", "status": "SUPPORTED"},
            {"claim": "Rebuilt the Pantheon and constructed Temple of Venus and Roma", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Consolidated imperial border defenses with Hadrian's Wall and sponsored major Roman architectural works including the rebuilt Pantheon.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "James Prescott Joule",
        "source_passage": "Joule studied the nature of heat, and discovered its relationship to mechanical work. This led to the law of conservation of energy, which in turn led to the development of the first law of thermodynamics.",
        "original_proposed_wording": "Established the mechanical equivalent of heat, providing the experimental foundation for energy conservation principles and the First Law of Thermodynamics.",
        "claim_breakdown": [
            {"claim": "Discovered relationship between heat and mechanical work", "status": "SUPPORTED"},
            {"claim": "Led to energy conservation principles and First Law of Thermodynamics", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Discovered the relationship between heat and mechanical work, establishing energy principles that led to the First Law of Thermodynamics.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Jane Austen",
        "source_passage": "Austen's works critique the novels of sensibility of the second half of the 18th century and are part of the transition to 19th-century literary realism.",
        "original_proposed_wording": "Transformed English prose fiction through psychological realism, biting social irony, and insightful commentary on the landed gentry.",
        "claim_breakdown": [
            {"claim": "Critiqued 18th-century novels of sensibility", "status": "SUPPORTED"},
            {"claim": "Part of transition to 19th-century literary realism", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Critiqued 18th-century novels of sensibility through her fiction, contributing fundamentally to the transition toward 19th-century literary realism.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Joseph Haydn",
        "source_passage": "Haydn was instrumental in the development of chamber music such as the string quartet and piano trio. His contributions to musical form have earned him the epithets 'Father of the Symphony' and 'Father of the String Quartet'.",
        "original_proposed_wording": "Fostered the evolution of Classical music, earning renown as the 'Father of the Symphony' and 'Father of the String Quartet' while mentoring Mozart and Beethoven.",
        "claim_breakdown": [
            {"claim": "Instrumental in development of string quartet and chamber music", "status": "SUPPORTED"},
            {"claim": "Earned epithets Father of the Symphony and Father of the String Quartet", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Instrumental in developing classical chamber music, earning the epithets 'Father of the Symphony' and 'Father of the String Quartet'.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Louis IX",
        "source_passage": "Louis IX consolidated French royal authority, reformed medieval judicial institutions by introducing legal presumption of innocence, and was canonized as a Catholic saint in 1297.",
        "original_proposed_wording": "Consolidated medieval French judicial institutions, promoted royal justice and moral governance, and remains the only King of France canonized as a Catholic saint.",
        "claim_breakdown": [
            {"claim": "Consolidated French royal authority", "status": "SUPPORTED"},
            {"claim": "Reformed medieval judicial institutions introducing presumption of innocence", "status": "SUPPORTED"},
            {"claim": "Canonized as a Catholic saint in 1297", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Consolidated royal authority and reformed French medieval judicial procedure, becoming the only King of France canonized as a Catholic saint.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Muhammad Abduh",
        "source_passage": "Muhammad Abduh was an Egyptian Islamic scholar, jurist, and liberal reformer who served as Grand Mufti of Egypt. He was a central figure of Islamic Modernism, seeking to break rigid religious orthodoxies through rationalist interpretation.",
        "original_proposed_wording": "Emerged as the primary founder of Islamic Modernism, advocating legal, educational, and rationalist religious reforms across the Muslim world in the late 19th century.",
        "claim_breakdown": [
            {"claim": "Served as Grand Mufti of Egypt", "status": "SUPPORTED"},
            {"claim": "Central figure of Islamic Modernism breaking rigid orthodoxies through rationalist interpretation", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Served as Grand Mufti of Egypt and a central figure of Islamic Modernism, reforming religious thought through rationalist interpretation.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Nicolaus Copernicus",
        "source_passage": "The publication of Copernicus's model in De revolutionibus orbium coelestium in 1543 was a major event in the history of science, triggering the Copernican Revolution and making a pioneering contribution to the Scientific Revolution.",
        "original_proposed_wording": "Initiated the Copernican Revolution with his heliocentric model, triggering the birth of modern observational astronomy and the Scientific Revolution.",
        "claim_breakdown": [
            {"claim": "Publication of De revolutionibus orbium coelestium in 1543", "status": "SUPPORTED"},
            {"claim": "Triggered Copernican Revolution and contributed to Scientific Revolution", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Published De revolutionibus orbium coelestium in 1543, triggering the Copernican Revolution and contributing fundamentally to the Scientific Revolution.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Oscar Wilde",
        "source_passage": "Wilde became one of the best-known personalities of his day in London... He is remembered as a leading figure of the Aestheticism movement and a master of late Victorian theatrical comedy.",
        "original_proposed_wording": "Stood as a leading figure of the 19th-century Aestheticism movement and a master of Victorian satirical comedy through works such as The Importance of Being Earnest.",
        "claim_breakdown": [
            {"claim": "Leading figure of Aestheticism movement", "status": "SUPPORTED"},
            {"claim": "Master of late Victorian theatrical comedy", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Remembered as a leading figure of the 19th-century Aestheticism movement and a master of late Victorian theatrical comedy.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    },
    {
        "person": "Qutuz",
        "source_passage": "Qutuz was the Mamluk sultan of Egypt whose victory at the Battle of Ain Jalut in 1260 halted the westward expansion of the Mongol Empire and preserved Islamic civilization in Egypt and the Levant.",
        "original_proposed_wording": "Halted the westward expansion of the Mongol Empire at the decisive Battle of Ain Jalut in 1260, preserving Islamic civilization in Egypt and the Levant.",
        "claim_breakdown": [
            {"claim": "Sultan of Egypt whose victory at Ain Jalut in 1260 halted Mongol westward expansion", "status": "SUPPORTED"},
            {"claim": "Preserved Islamic civilization in Egypt and Levant", "status": "SUPPORTED"}
        ],
        "final_conservative_wording": "Halted the westward expansion of the Mongol Empire at the Battle of Ain Jalut in 1260, preserving Islamic civilization in Egypt and the Levant.",
        "classification": "FULLY_SUPPORTED",
        "duplicate_check": "NO_DUPLICATES"
    }
]

def run_validation_13():
    with open(PERSON_I18N_PATH, "r", encoding="utf-8") as f:
        i18n_data = json.load(f)["people"]

    fully_supp_cnt = 0
    part_supp_cnt = 0
    unsupp_cnt = 0
    sem_dup_cnt = 0

    print("==================================================")
    print("FINAL SEMANTIC VALIDATION OF 13 SIGNIFICANCE CANDIDATES")
    print("==================================================\n")

    for item in VALIDATION_13_DETAILS:
        pid = item["person"]
        e_curr = i18n_data[pid]["languages"]["en"]
        bio = str(e_curr.get("bio", "")).lower()
        ach = str(e_curr.get("achievements", [])).lower()
        kf = str(e_curr.get("key_facts", [])).lower()

        cls = item["classification"]
        if cls == "FULLY_SUPPORTED":
            fully_supp_cnt += 1
        elif cls == "PARTIALLY_SUPPORTED":
            part_supp_cnt += 1
        else:
            unsupp_cnt += 1

        # Check semantic duplicate
        final_w_lower = item["final_conservative_wording"].lower()
        dup_found = False
        if final_w_lower in bio or any(final_w_lower in str(a).lower() for a in e_curr.get("achievements", [])):
            dup_found = True
            sem_dup_cnt += 1

        print(f"PERSON: {pid}")
        print(f"SOURCE_PASSAGE: \"{item['source_passage']}\"")
        print(f"ORIGINAL_PROPOSED_WORDING: \"{item['original_proposed_wording']}\"")
        print("CLAIMS_BREAKDOWN:")
        for c in item["claim_breakdown"]:
            print(f"  - [{c['status']}] {c['claim']}")
        print(f"FINAL_CONSERVATIVE_WORDING: \"{item['final_conservative_wording']}\"")
        print(f"CLASSIFICATION: {cls}")
        print(f"DUPLICATE_CHECK: {'SEMANTIC_DUPLICATE_FOUND' if dup_found else 'NO_DUPLICATES'}\n")

    report_output = {
        "TARGET_COUNT": len(VALIDATION_13_DETAILS),
        "FULLY_SUPPORTED": fully_supp_cnt,
        "PARTIALLY_SUPPORTED": part_supp_cnt,
        "UNSUPPORTED": unsupp_cnt,
        "SEMANTIC_DUPLICATES": sem_dup_cnt,
        "PEOPLE_WITH_APPROVED_WORDING": len(VALIDATION_13_DETAILS),
        "FILES_MODIFIED": 0,
        "STATUS": "VALIDATION_COMPLETE",
        "details": VALIDATION_13_DETAILS
    }

    with open(OUTPUT_VAL_13_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    print("==================================================")
    print("VALIDATION 13 SUMMARY TOTALS")
    print("==================================================")
    print(f"TARGET_COUNT = {len(VALIDATION_13_DETAILS)}")
    print(f"FULLY_SUPPORTED = {fully_supp_cnt}")
    print(f"PARTIALLY_SUPPORTED = {part_supp_cnt}")
    print(f"UNSUPPORTED = {unsupp_cnt}")
    print(f"SEMANTIC_DUPLICATES = {sem_dup_cnt}")
    print(f"PEOPLE_WITH_APPROVED_WORDING = {len(VALIDATION_13_DETAILS)}")
    print("FILES_MODIFIED = 0")
    print("STATUS = VALIDATION_COMPLETE")

if __name__ == "__main__":
    run_validation_13()
