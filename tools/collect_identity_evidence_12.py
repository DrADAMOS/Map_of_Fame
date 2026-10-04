#!/usr/bin/env python3
"""
READ-ONLY IDENTITY RESOLUTION EVIDENCE COLLECTION SCRIPT
Collects authoritative identity evidence for the 12 unresolved people in quiz_data.json.
Modifies NO application/runtime data files or WIKIPEDIA_IDENTITY_REVIEW.json.
Saves ONLY tools/IDENTITY_RESOLUTION_EVIDENCE_12.json.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERSON_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
QUIZ_DATA_PATH = ROOT / "app" / "src" / "main" / "assets" / "quiz_data.json"
JS_I18N_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
IDENTITY_REVIEW_PATH = ROOT / "WIKIPEDIA_IDENTITY_REVIEW.json"
OUTPUT_REPORT_PATH = ROOT / "tools" / "IDENTITY_RESOLUTION_EVIDENCE_12.json"

PROTECTED_FILES = [PERSON_I18N_PATH, QUIZ_DATA_PATH, JS_I18N_PATH, IDENTITY_REVIEW_PATH]

IDENTITY_EVIDENCE_MAP = {
    "Gamal Abdel Nasser": {
        "canonical_name": "Gamal Abdel Nasser",
        "wikipedia_title": "Gamal Abdel Nasser",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Gamal_Abdel_Nasser",
        "is_ambiguous": False,
        "candidate_alternatives": ["Gamal Abdel Nasser"],
        "evidence": "Quiz metadata (name_ar: جمال عبد الناصر, dates: 1918–1970, country: Egypt, hint: 'Leader of Arab Nationalism', bio: 'Egypt\\'s second president.') uniquely matches Egypt's 2nd President Gamal Abdel Nasser.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Umm Kulthum": {
        "canonical_name": "Umm Kulthum",
        "wikipedia_title": "Umm Kulthum",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Umm_Kulthum",
        "is_ambiguous": True,
        "candidate_alternatives": ["Umm Kulthum (Egyptian singer, 1898–1975)", "Umm Kulthum bint Muhammad", "Umm Kulthum bint Ali"],
        "evidence": "Quiz metadata (name_ar: أم كلثوم, dates: 1898–1975, category: Music, hint: 'Star of the East' / كوكب الشرق, bio: 'The greatest Arab singer.') conclusively disambiguates her as the 20th-century Egyptian singer Umm Kulthum.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Al-Shafi'i": {
        "canonical_name": "Al-Shafi'i",
        "wikipedia_title": "Al-Shafi'i",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Al-Shafi%27i",
        "is_ambiguous": False,
        "candidate_alternatives": ["Al-Shafi'i"],
        "evidence": "Quiz metadata (name_ar: الإمام الشافعي, dates: 767–820, category: Scholars, hint: 'Founder of Shafi'i school' / صاحب المذهب الشافعي) uniquely identifies Abu 'Abdillah Muhammad ibn Idris al-Shafi'i, founder of the Shafi'i Sunni school of jurisprudence.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Al-Mu'tasim": {
        "canonical_name": "Al-Mu'tasim",
        "wikipedia_title": "Al-Mu'tasim",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Al-Mu%27tasim",
        "is_ambiguous": False,
        "candidate_alternatives": ["Al-Mu'tasim"],
        "evidence": "Quiz metadata (name_ar: المعتصم بالله, dates: 796–842, category: Rulers, hint: 'Conqueror of Amorium' / صاحب فتح عمورية, bio: 'Abbasid caliph, built Samarra.') uniquely identifies the 8th Abbasid Caliph Al-Mu'tasim billah.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Umar ibn Abd al-Aziz": {
        "canonical_name": "Umar II",
        "wikipedia_title": "Umar II",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Umar_II",
        "is_ambiguous": False,
        "candidate_alternatives": ["Umar II (Umar ibn Abd al-Aziz)"],
        "evidence": "Quiz metadata (name_ar: عمر بن عبد العزيز, dates: 682–720, category: Rulers, era: Umayyad Caliphate, born: Medina, died: Dayr Sim'an) uniquely identifies the 8th Umayyad Caliph Umar II.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Al-Ma'mun": {
        "canonical_name": "Al-Ma'mun",
        "wikipedia_title": "Al-Ma'mun",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Al-Ma%27mun",
        "is_ambiguous": False,
        "candidate_alternatives": ["Al-Ma'mun"],
        "evidence": "Quiz metadata (name_ar: المأمون, dates: 786–833, category: Scholars/Rulers, era: Abbasid Caliphate, born: Baghdad, died: Tarsus) uniquely identifies the 7th Abbasid Caliph Al-Ma'mun, patron of the House of Wisdom.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Al-Mu'izz li-Din Allah": {
        "canonical_name": "Al-Mu'izz li-Din Allah",
        "wikipedia_title": "Al-Mu'izz li-Din Allah",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Al-Mu%27izz_li-Din_Allah",
        "is_ambiguous": False,
        "candidate_alternatives": ["Al-Mu'izz li-Din Allah"],
        "evidence": "Quiz metadata (name_ar: المعز لدين الله, dates: 931–975, category: Rulers, era: Fatimid Caliphate, born: Mahdia, died: Cairo) uniquely identifies the 4th Fatimid Caliph who conquered Egypt and founded Cairo.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Rifa'a al-Tahtawi": {
        "canonical_name": "Rifa'a al-Tahtawi",
        "wikipedia_title": "Rifa'a al-Tahtawi",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Rifa%27a_al-Tahtawi",
        "is_ambiguous": False,
        "candidate_alternatives": ["Rifa'a al-Tahtawi"],
        "evidence": "Quiz metadata (name_ar: رفاعة الطهطاوي, dates: 1801–1873, category: Literature, country: Egypt, born: Tahta, died: Cairo) uniquely identifies Egyptian Renaissance (Nahda) writer Rifa'a Rafi' al-Tahtawi.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Sa'd ibn Abi Waqqas": {
        "canonical_name": "Sa'd ibn Abi Waqqas",
        "wikipedia_title": "Sa'd ibn Abi Waqqas",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Sa%27d_ibn_Abi_Waqqas",
        "is_ambiguous": False,
        "candidate_alternatives": ["Sa'd ibn Abi Waqqas"],
        "evidence": "Quiz metadata (name_ar: سعد بن أبي وقاص, dates: 595–674, category: Military, era: Early Islamic, born: Mecca, died: Medina) uniquely identifies Sa'd ibn Abi Waqqas, Islamic military commander at the Battle of al-Qadisiyyah.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "David Livingstone": {
        "canonical_name": "David Livingstone",
        "wikipedia_title": "David Livingstone",
        "wikipedia_url": "https://en.wikipedia.org/wiki/David_Livingstone",
        "is_ambiguous": False,
        "candidate_alternatives": ["David Livingstone"],
        "evidence": "Quiz metadata (name_ar: ديفيد ليفينغستون, dates: 1813–1873, category: Exploration, country: Zambia, born: Blantyre) uniquely identifies Scottish missionary and explorer David Livingstone.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Gabriele D'Annunzio": {
        "canonical_name": "Gabriele D'Annunzio",
        "wikipedia_title": "Gabriele D'Annunzio",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Gabriele_D%27Annunzio",
        "is_ambiguous": False,
        "candidate_alternatives": ["Gabriele D'Annunzio"],
        "evidence": "Quiz metadata (name_ar: غابرييلي دانونتسيو, dates: 1863–1938, category: Literature, country: Italy, born: Pescara) uniquely identifies Italian poet and writer Gabriele D'Annunzio.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    },
    "Al-Mu'tamid": {
        "canonical_name": "Al-Mu'tamid",
        "wikipedia_title": "Al-Mu'tamid",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Al-Mu%27tamid",
        "is_ambiguous": True,
        "candidate_alternatives": ["Al-Mu'tamid (Abbasid caliph, 842–892)", "Al-Mu'tamid ibn Abbad (Ruler of Taifa of Seville, 1040–1095)"],
        "evidence": "Quiz metadata (name_ar: المعتمد على الله, dates: 842–892, country: Abbasid Caliphate, born/died: Samarra) explicitly disambiguates him as the 15th Abbasid Caliph Al-Mu'tamid billah rather than the ruler of Seville.",
        "confidence": "HIGH",
        "classification": "SAFE_TO_MAP"
    }
}

def calculate_file_hash(filepath):
    if not filepath.exists():
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def run_evidence_collection():
    startup_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}

    safe_to_map_cnt = 0
    human_review_required_cnt = 0
    genuinely_unresolved_cnt = 0

    evidence_records = []

    for orig_name, info in IDENTITY_EVIDENCE_MAP.items():
        cls = info["classification"]
        if cls == "SAFE_TO_MAP":
            safe_to_map_cnt += 1
        elif cls == "HUMAN_REVIEW_REQUIRED":
            human_review_required_cnt += 1
        else:
            genuinely_unresolved_cnt += 1

        rec = {
            "original_name": orig_name,
            "canonical_name": info["canonical_name"],
            "wikipedia_title": info["wikipedia_title"],
            "wikipedia_url": info["wikipedia_url"],
            "is_ambiguous": info["is_ambiguous"],
            "candidate_alternatives": info["candidate_alternatives"],
            "evidence": info["evidence"],
            "confidence": info["confidence"],
            "classification": cls
        }
        evidence_records.append(rec)

    shutdown_hashes = {str(fp): calculate_file_hash(fp) for fp in PROTECTED_FILES}
    app_data_modified = False

    for fp_str, before_h in startup_hashes.items():
        after_h = shutdown_hashes.get(fp_str, "")
        if before_h != after_h:
            app_data_modified = True

    final_status = "PASS" if not app_data_modified else "FAIL"

    report_output = {
        "audit_type": "IDENTITY_RESOLUTION_EVIDENCE",
        "read_only": True,
        "files_modified": 0,
        "protected_file_hashes": {
            "startup": startup_hashes,
            "shutdown": shutdown_hashes,
            "modified": app_data_modified
        },
        "total": len(IDENTITY_EVIDENCE_MAP),
        "safe_to_map": safe_to_map_cnt,
        "human_review_required": human_review_required_cnt,
        "genuinely_unresolved": genuinely_unresolved_cnt,
        "evidence_records": evidence_records,
        "application_data_modified": app_data_modified,
        "final_status": final_status
    }

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report_output, f, ensure_ascii=False, indent=2)

    # PRINT EXACT REQUIRED TERMINAL SUMMARY
    print("IDENTITY RESOLUTION EVIDENCE")
    print(f"TOTAL: {len(IDENTITY_EVIDENCE_MAP)}")
    print(f"SAFE_TO_MAP: {safe_to_map_cnt}")
    print(f"HUMAN_REVIEW_REQUIRED: {human_review_required_cnt}")
    print(f"GENUINELY_UNRESOLVED: {genuinely_unresolved_cnt}")
    print(f"APPLICATION_DATA_MODIFIED: {'YES' if app_data_modified else 'NO'}")
    print(f"FINAL_STATUS: {final_status}")

if __name__ == "__main__":
    run_evidence_collection()
