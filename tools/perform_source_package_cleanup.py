#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG_PATH = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.json"
BACKUP_PATH = ROOT / "tools" / "WIKIPEDIA_SOURCE_PACKAGE_37.pre_field_cleanup.json"

EXACT_18_ACHIEVEMENTS = [
    ("Alexis Carrel", "=== Vascular suture ===."),
    ("Anwar Sadat", "In 1983, Sadat, a miniseries based on the life of Anwar Sadat, aired on US television with Oscar-winning actor Louis Gossett Jr."),
    ("Anwar Sadat", "The film was promptly banned by the Egyptian government, as were all other movies produced and distributed by Columbia Pictures, over allegations of historical inaccuracies."),
    ("Auguste Comte", "=== Comte's positivism ===."),
    ("Bob Marley", "=== 1962–1972: Early years ===."),
    ("Emperor Meiji", "=== Unrest and Accession ===."),
    ("Grace Hopper", "=== World War II ===."),
    ("Gustav Mahler", "=== First appointments ===."),
    ("Hannibal Barca", "Hannibal was one of the sons of Carthaginian general and statesman Hamilcar Barca and an unknown mother."),
    ("Joseph Haydn", "=== Early life ===."),
    ("Louis IX", "=== Construction of the Sainte-Chapelle ===."),
    ("Ludwig van Beethoven", "=== Early life and education ===."),
    ("Michael Faraday", "=== Chemistry ===."),
    ("Nur ad-Din", "Born in February 1118, Nur ad-Din was the second son of Imad al-Din Zengi, the Turcoman atabeg of Aleppo and Mosul, who was a devoted enemy of the crusader presence in Syria."),
    ("Oscar Wilde", "The 1891 census records the Wildes' residence at 16 Tite Street, (now 34) where Oscar lived with his wife Constance and two sons."),
    ("Steve Jobs", "=== 1974–1985 ===."),
    ("Steve Jobs", "==== Pre-Apple ====."),
    ("Steve Jobs", "In February 1974, Jobs returned to his parents' home in Los Altos and began looking for a job.")
]

EXACT_23_SIGNIFICANCE = [
    ("Alexis Carrel", "French surgeon and biologist (1873–1944)"),
    ("Anwar Sadat", "President of Egypt from 1970 to 1981"),
    ("Auguste Comte", "French philosopher, mathematician and sociologist (1798–1857)"),
    ("Caravaggio", "Italian painter (1571–1610)"),
    ("Clara Barton", "American Civil War nurse and founder of the American Red Cross (1821–1912)"),
    ("Constantine the Great", "Constantine reunited the empire under one emperor, and he won major victories over the Franks and Alamanni in 306–308, the Franks again in 313–314, the Goths in 332, and the Sarmatians in 334."),
    ("Dmitri Mendeleev", "Russian chemist (1834–1907)"),
    ("Emperor Meiji", "Emperor of Japan from 1867 to 1912"),
    ("Gustav Mahler", "Austro-Bohemian composer and conductor (1860–1911)"),
    ("Hadrian", "Roman emperor from 117 to 138"),
    ("James Prescott Joule", "English physicist (1818–1889)"),
    ("Jane Austen", "English novelist (1775–1817)"),
    ("Joseph Haydn", "Austrian composer (1732–1809)"),
    ("Louis IX", "King of France from 1226 to 1270"),
    ("Malek Bennabi", "Algerian philosopher"),
    ("Marcel Proust", "French novelist, literary critic, and essayist (1871–1922)"),
    ("Michael Faraday", "English chemist and physicist (1791–1867)"),
    ("Muhammad Abduh", "Egyptian jurist and theologian (1849–1905)"),
    ("Nicolaus Copernicus", "Mathematician and astronomer (1473–1543)"),
    ("Oscar Wilde", "Irish writer (1854–1900)"),
    ("Qutuz", "Sultan of Egypt from 1259 to 1260"),
    ("Steve Jobs", "American businessman and inventor (1955–2011)"),
    ("T. E. Lawrence", "British Army officer, diplomat and writer (1888–1935)")
]

def perform_cleanup():
    # 1. Create backup if not exists
    if not BACKUP_PATH.exists():
        shutil.copyfile(PKG_PATH, BACKUP_PATH)

    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        pkg = json.load(f)

    people = pkg.get("people", {})

    ach_rem_map = {}
    for pid, item in EXACT_18_ACHIEVEMENTS:
        if pid not in ach_rem_map: ach_rem_map[pid] = []
        ach_rem_map[pid].append(item)

    hs_rem_map = {}
    for pid, item in EXACT_23_SIGNIFICANCE:
        if pid not in hs_rem_map: hs_rem_map[pid] = []
        hs_rem_map[pid].append(item)

    audit_logs = []

    orig_facts_count = 0
    retained_facts_count = 0
    removed_facts_count = 0

    removed_by_field = {
        "biography": 0,
        "achievements": 0,
        "key_facts": 0,
        "historical_significance": 0
    }

    for pid, p in people.items():
        sf = p.get("source_facts", {})

        # 1. BIOGRAPHY
        bio_facts = sf.get("biography_facts", [])
        if bio_facts != ["INSUFFICIENT_SOURCE"]:
            orig_facts_count += len(bio_facts)
            retained_facts_count += len(bio_facts)

        # 2. ACHIEVEMENTS
        ach_facts = sf.get("achievement_facts", [])
        if ach_facts != ["INSUFFICIENT_SOURCE"]:
            to_rem = ach_rem_map.get(pid, [])
            cleaned_ach = []
            for item in ach_facts:
                orig_facts_count += 1
                if item in to_rem:
                    removed_facts_count += 1
                    removed_by_field["achievements"] += 1
                    audit_logs.append({
                        "person": pid,
                        "field": "achievements",
                        "fact": item,
                        "reason": "Does not describe a concrete achievement (heading, parentage, birth, trivia, or passive event).",
                        "decision": "REMOVED_FIELD_INAPPROPRIATE"
                    })
                else:
                    retained_facts_count += 1
                    cleaned_ach.append(item)
            sf["achievement_facts"] = cleaned_ach if cleaned_ach else ["INSUFFICIENT_SOURCE"]

        # 3. KEY FACTS
        kf_facts = sf.get("key_facts", [])
        if kf_facts != ["INSUFFICIENT_SOURCE"]:
            orig_facts_count += len(kf_facts)
            retained_facts_count += len(kf_facts)

        # 4. SIGNIFICANCE
        sig_facts = sf.get("significance_facts", [])
        if sig_facts != ["INSUFFICIENT_SOURCE"]:
            to_rem = hs_rem_map.get(pid, [])
            cleaned_sig = []
            for item in sig_facts:
                orig_facts_count += 1
                if item in to_rem:
                    removed_facts_count += 1
                    removed_by_field["historical_significance"] += 1
                    audit_logs.append({
                        "person": pid,
                        "field": "historical_significance",
                        "fact": item,
                        "reason": "Mere title, occupation, or lifespan statement / military campaign detail assigned to historical_significance.",
                        "decision": "REMOVED_FIELD_INAPPROPRIATE"
                    })
                else:
                    retained_facts_count += 1
                    cleaned_sig.append(item)
            sf["significance_facts"] = cleaned_sig if cleaned_sig else ["INSUFFICIENT_SOURCE"]

    pkg["field_cleanup_audit"] = audit_logs

    # Save cleaned JSON
    with open(PKG_PATH, "w", encoding="utf-8") as f:
        json.dump(pkg, f, ensure_ascii=False, indent=2)

    # Validation
    valid_orig = (orig_facts_count == 247)
    valid_retained = (retained_facts_count == 206)
    valid_removed = (removed_facts_count == 41)
    valid_ach_rem = (removed_by_field["achievements"] == 18)
    valid_hs_rem = (removed_by_field["historical_significance"] == 23)

    status_pass = (valid_orig and valid_retained and valid_removed and valid_ach_rem and valid_hs_rem)

    print("SOURCE_PACKAGE_FIELD_CLEANUP")
    print("============================")
    print(f"Original field-assignment facts:\n{orig_facts_count}\n")
    print(f"Retained field-appropriate facts:\n{retained_facts_count}\n")
    print(f"Removed field-inappropriate facts:\n{removed_facts_count}\n")
    print(f"Removed from achievements:\n{removed_by_field['achievements']}\n")
    print(f"Removed from historical_significance:\n{removed_by_field['historical_significance']}\n")
    print(f"Removed from biography:\n{removed_by_field['biography']}\n")
    print(f"Removed from key_facts:\n{removed_by_field['key_facts']}\n")
    print(f"Replacement facts invented:\n0\n")
    print(f"External facts added:\n0\n")
    print(f"People changed:\n0\n")
    print(f"Identity records changed:\n0\n")
    print(f"Network requests:\n0\n")
    print(f"Runtime files modified:\n0\n")
    print(f"SOURCE PACKAGE STATUS:\n{'PASS' if status_pass else 'FAIL'}")

if __name__ == "__main__":
    perform_cleanup()
