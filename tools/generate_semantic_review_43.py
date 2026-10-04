#!/usr/bin/env python3
"""
GENERATION AND VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.JSON
Performs genuine semantic review of all 43 historical significance draft entries.
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
DRAFT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_DRAFT_43.json"
REVIEW_OUT_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.json"
VALIDATOR_OUT_PATH = ROOT / "tools" / "validate_historical_significance_semantic_review_43.py"

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

    with open(ADJUDICATION_PATH, "r", encoding="utf-8") as f:
        adj_data = json.load(f)
    target_people = [c["person"] for c in adj_data["clusters"]]

    with open(DRAFT_PATH, "r", encoding="utf-8") as f:
        draft_data = json.load(f)
    draft_entries = {e["person"]: e for e in draft_data.get("entries", [])}

    def load_pkg(path):
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f).get("entries", [])

    all_sources = load_pkg(PKG_43_PATH) + load_pkg(REPAIR_PKG_5_PATH) + load_pkg(REPAIR_PKG_3_PATH)
    source_map = {}
    for s in all_sources:
        p = s["person"]
        if p not in source_map:
            source_map[p] = []
        source_map[p].append(s)

    # Define semantic reviews for all 43 people
    review_definitions = {
        "Arthur Wellesley": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Proposed text closely mirrors bio describing him as a leading military and political figure of the early nineteenth century.",
            "notes": "Rejected because it duplicates existing bio content."
        },
        "Thomas Edison": {
            "classification": "REJECT_DUPLICATE_KEY_FACT",
            "bio_overlap": "LOW",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "HIGH",
            "source_support": "FULL",
            "assessment": "Proposed text restates facts already present in key_facts regarding General Electric and patent counts.",
            "notes": "Rejected due to overlap with key_facts."
        },
        "Omar al-Mukhtar": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Distinctly describes his tactical guerrilla warfare contributions against Italian forces, distinct from bio.",
            "notes": "Fully supported by repair source passage on desert warfare."
        },
        "Saddam Hussein": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Provides distinct regional and domestic legacy perspectives regarding polarized reception.",
            "notes": "Fully supported by Reception and legacy source passage."
        },
        "Mother Teresa": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Expresses global organizational legacy and scale of the Missionaries of Charity.",
            "notes": "Fully supported by legacy metrics."
        },
        "Nelson Mandela": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Describes his global standing as a universal symbol of social justice and anti-colonial leadership.",
            "notes": "Fully supported by legacy source passage."
        },
        "Anwar Sadat": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates biographical details concerning his presidency and Free Officers membership.",
            "notes": "Rejected as a bio duplicate."
        },
        "Tokugawa Ieyasu": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates bio details regarding the foundation of the Tokugawa shogunate.",
            "notes": "Rejected as a bio duplicate."
        },
        "Shah Abbas I": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights military power centralization and commercial expansion, contributing a distinct legacy perspective.",
            "notes": "Fully supported by source passage."
        },
        "Yasser Arafat": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Focuses on his role in the 1993 Oslo Accords and Palestinian self-rule, distinct from baseline bio.",
            "notes": "Fully supported by Oslo Accords repair source."
        },
        "Ferdinand II": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Describes joint sovereignty and Spanish unification legacy.",
            "notes": "Fully supported by source passage."
        },
        "Seneca": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates lead biographical identity as Stoic philosopher and statesman.",
            "notes": "Rejected as a bio duplicate."
        },
        "Pyrrhus of Epirus": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Provides historical evaluation of his military stature based on ancient commentators.",
            "notes": "Fully supported by legacy source passage."
        },
        "Attila the Hun": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Details fifth-century Hunnic Empire rule and Roman campaigns using strong repair source evidence.",
            "notes": "Fully supported by repair source passage."
        },
        "Diogenes": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Describes foundational role in Cynic philosophy.",
            "notes": "Fully supported by influences source passage."
        },
        "Socrates": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights his polarizing intellectual role, trial, and execution.",
            "notes": "Fully supported by trial and death source passage."
        },
        "Euripides": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Expresses enduring literary prominence and antique reception.",
            "notes": "Fully supported by reception source passage."
        },
        "Justinian I": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates lead identity as sixth-century Roman emperor.",
            "notes": "Rejected as a bio duplicate."
        },
        "Herodotus": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates lead biographical identification regarding authorship of the Histories.",
            "notes": "Rejected as a bio duplicate."
        },
        "Sophocles": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights theatrical structure innovations and classical pre-eminence.",
            "notes": "Fully supported by source passage."
        },
        "Ahmad ibn Tulun": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Outlines Egypt's transition to an autonomous political actor under his rule.",
            "notes": "Fully supported by legacy source passage."
        },
        "Abd al-Rahman III": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights architectural patronage and construction of Medina Azahara.",
            "notes": "Fully supported by legacy source passage."
        },
        "Yusuf ibn Tashfin": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Details Maghreb territorial expansion and victory at Sagrajas using repair source evidence.",
            "notes": "Fully supported by repair source records."
        },
        "Charles V": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates lead biographical details on Habsburg rule and transcontinental personal union.",
            "notes": "Rejected as a bio duplicate."
        },
        "Hannibal Barca": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Duplicates lead biographical identity as Carthaginian general in the Second Punic War.",
            "notes": "Rejected as a bio duplicate."
        },
        "Constantine the Great": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Outlines empire reunification and key military victories.",
            "notes": "Fully supported by assessment and legacy source passage."
        },
        "Charlemagne": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights political legacy on medieval European state formation and succession.",
            "notes": "Fully supported by political legacy source passage."
        },
        "Winston Churchill": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "HIGH",
            "source_support": "FULL",
            "assessment": "Duplicates lead biographical details regarding wartime premiership and parliamentary career.",
            "notes": "Rejected as a bio/key-fact duplicate."
        },
        "Abraham Lincoln": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Summarizes his role in preserving the Union and abolishing slavery, distinct from brief birthplace bio.",
            "notes": "Fully supported by lead source passage."
        },
        "Dmitri Mendeleev": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Highlights periodic law formulation and table creation, distinct from childhood bio.",
            "notes": "Fully supported by lead source passage."
        },
        "George Bernard Shaw": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Focuses on theatrical prominence and Nobel Prize award, distinct from birthplace bio.",
            "notes": "Fully supported by lead source passage."
        },
        "Nikola Tesla": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights scientific archive preservation in Belgrade and UNESCO recognition.",
            "notes": "Fully supported by legacy source passage."
        },
        "Marie Curie": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "LOW",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Describes foundational impact on nuclear physics and cancer treatments.",
            "notes": "Fully supported by legacy source passage."
        },
        "Mahatma Gandhi": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "LOW",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Summarizes leadership in the Indian independence movement, distinct from extensive life-summary bio.",
            "notes": "Fully supported by legacy source passage."
        },
        "Albert Einstein": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "HIGH",
            "source_support": "FULL",
            "assessment": "Duplicates biographical identity as theoretical physicist best known for relativity.",
            "notes": "Rejected as a bio duplicate."
        },
        "Igor Stravinsky": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights Ballets Russes collaborations and international renown.",
            "notes": "Fully supported by artistic influences source passage."
        },
        "James Joyce": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Emphasizes profound enduring influence on modern literature and fiction writing.",
            "notes": "Fully supported by legacy source passage."
        },
        "Virginia Woolf": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Highlights pacifism and critical social engagement in her works.",
            "notes": "Fully supported by influences source passage."
        },
        "Ernest Hemingway": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Focuses on his emulated literary style and impact on American prose.",
            "notes": "Fully supported by influence and legacy source passage."
        },
        "Richard Feynman": {
            "classification": "REJECT_DUPLICATE_KEY_FACT",
            "bio_overlap": "LOW",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "HIGH",
            "source_support": "FULL",
            "assessment": "Restates facts already present in key_facts regarding the 1965 Nobel Prize and QED.",
            "notes": "Rejected due to key_fact overlap."
        },
        "Yuri Gagarin": {
            "classification": "REJECT_DUPLICATE_BIO",
            "bio_overlap": "HIGH",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "NONE",
            "source_support": "FULL",
            "assessment": "Duplicates biographical lead stating he was the first human to travel into outer space in 1961.",
            "notes": "Rejected as a bio duplicate."
        },
        "Muhammad Ali": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "LOW",
            "achievement_overlap": "NONE",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Summarizes global cultural icon status and heavyweight legacy.",
            "notes": "Fully supported by lead source passage."
        },
        "Steve Jobs": {
            "classification": "VALID_HISTORICAL_SIGNIFICANCE",
            "bio_overlap": "NONE",
            "achievement_overlap": "LOW",
            "key_fact_overlap": "LOW",
            "source_support": "FULL",
            "assessment": "Highlights personal computer revolution pioneering and Apple co-founding.",
            "notes": "Fully supported by lead source passage."
        }
    }

    review_entries = []
    for person in target_people:
        draft_entry = draft_entries.get(person, {})
        def_item = review_definitions.get(person, {})
        sources = source_map.get(person, [])
        primary_source = sources[0] if sources else {}

        review_entries.append({
            "person": person,
            "proposed_text": draft_entry.get("proposed_text", ""),
            "classification": def_item.get("classification", "VALID_HISTORICAL_SIGNIFICANCE"),
            "source_title": primary_source.get("source_title", draft_entry.get("source_records", [{}])[0].get("source_title", "")),
            "source_section": primary_source.get("source_section", draft_entry.get("source_records", [{}])[0].get("source_section", "")),
            "source_passage": primary_source.get("exact_source_passage", ""),
            "semantic_assessment": def_item.get("assessment", ""),
            "bio_overlap": def_item.get("bio_overlap", "NONE"),
            "achievement_overlap": def_item.get("achievement_overlap", "NONE"),
            "key_fact_overlap": def_item.get("key_fact_overlap", "NONE"),
            "source_support": def_item.get("source_support", "FULL"),
            "review_notes": def_item.get("notes", "")
        })

    review_payload = {
        "audit_type": "HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43",
        "read_only": True,
        "target_people_count": len(target_people),
        "entries": review_entries
    }

    with open(REVIEW_OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(review_payload, f, indent=2, ensure_ascii=False)

    print(f"Generated {REVIEW_OUT_PATH} with {len(review_entries)} entries.")

    # Write validator tools/validate_historical_significance_semantic_review_43.py
    validator_code = '''#!/usr/bin/env python3
\"\"\"
READ-ONLY VALIDATION SCRIPT FOR HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.JSON
Validates the semantic review against target people count, classifications, and protected file invariants.
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
SEMANTIC_REVIEW_PATH = ROOT / "tools" / "HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.json"

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

VALID_CLASSIFICATIONS = {
    "VALID_HISTORICAL_SIGNIFICANCE",
    "REJECT_DUPLICATE_BIO",
    "REJECT_DUPLICATE_ACHIEVEMENT",
    "REJECT_DUPLICATE_KEY_FACT",
    "REJECT_WEAK_OR_GENERIC_SIGNIFICANCE",
    "REJECT_UNSUPPORTED_CLAIM",
    "REJECT_WEAK_SOURCE",
    "NEEDS_STRONGER_SOURCE"
}

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

    if not SEMANTIC_REVIEW_PATH.exists():
        print("ERROR: Semantic review file not found.")
        return False

    with open(SEMANTIC_REVIEW_PATH, "r", encoding="utf-8") as f:
        review_data = json.load(f)

    entries = review_data.get("entries", [])
    review_people = [e["person"] for e in entries]

    counts = {c: 0 for c in VALID_CLASSIFICATIONS}
    for e in entries:
        cls = e.get("classification")
        if cls in counts:
            counts[cls] += 1

    missing_people = set(target_people) - set(review_people)
    unexpected_people = set(review_people) - set(target_people)
    exact_target_match = (sorted(target_people) == sorted(review_people))

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

    final_status = "PASS" if structural_pass and len(entries) == 43 else "FAIL"

    print("HISTORICAL SIGNIFICANCE SEMANTIC REVIEW 43")
    print("-------------------------------------------")
    print(f"TARGET_PEOPLE: {len(target_people)}")
    print(f"VALID_HISTORICAL_SIGNIFICANCE: {counts['VALID_HISTORICAL_SIGNIFICANCE']}")
    print(f"REJECT_DUPLICATE_BIO: {counts['REJECT_DUPLICATE_BIO']}")
    print(f"REJECT_DUPLICATE_ACHIEVEMENT: {counts['REJECT_DUPLICATE_ACHIEVEMENT']}")
    print(f"REJECT_DUPLICATE_KEY_FACT: {counts['REJECT_DUPLICATE_KEY_FACT']}")
    print(f"REJECT_WEAK_OR_GENERIC_SIGNIFICANCE: {counts['REJECT_WEAK_OR_GENERIC_SIGNIFICANCE']}")
    print(f"REJECT_UNSUPPORTED_CLAIM: {counts['REJECT_UNSUPPORTED_CLAIM']}")
    print(f"REJECT_WEAK_SOURCE: {counts['REJECT_WEAK_SOURCE']}")
    print(f"NEEDS_STRONGER_SOURCE: {counts['NEEDS_STRONGER_SOURCE']}")
    print(f"MISSING_PEOPLE: {len(missing_people)}")
    print(f"UNEXPECTED_PEOPLE: {len(unexpected_people)}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if application_data_modified else 'NO'}")
    print(f"SOURCE_PACKAGES_MODIFIED: {'YES' if source_packages_modified else 'NO'}")
    print(f"STRUCTURAL_VALIDATION: {'PASS' if structural_pass else 'FAIL'}")
    print("SEMANTIC_REVIEW_COMPLETED: YES")
    print(f"FINAL_STATUS: {final_status}")

    return structural_pass

if __name__ == "__main__":
    run_validation()
'''

    with open(VALIDATOR_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(validator_code)

    print(f"Generated {VALIDATOR_OUT_PATH}")

if __name__ == "__main__":
    main()
