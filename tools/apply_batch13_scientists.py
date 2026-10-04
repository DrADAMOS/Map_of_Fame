from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"

TARGET_LANGS = ("en", "es", "fr", "ru")
PEOPLE = {'Al-Biruni': 'his measurements of Earth, astronomy and comparative study of cultures', 'Nicolaus Copernicus': 'the heliocentric model presented in De revolutionibus', 'Johannes Kepler': 'his three laws of planetary motion', 'Benjamin Franklin': 'his electrical experiments, lightning research and scientific societies', 'James Watt': 'major improvements to the steam engine and industrial power', 'Georg Ohm': "Ohm's law relating voltage, current and resistance", 'Michael Faraday': 'electromagnetic induction and the foundations of electric motor and generator technology', 'James Prescott Joule': 'the mechanical equivalent of heat and the quantitative study of energy', 'Gregor Mendel': 'his pea experiments and the statistical foundations of heredity', 'James Clerk Maxwell': "Maxwell's equations and the electromagnetic theory of light", 'Alfred Nobel': 'dynamite and the creation of the Nobel Prizes', 'Dmitri Mendeleev': 'the periodic table and prediction of undiscovered elements', 'Ernest Rutherford': 'the nuclear model of the atom and experimental studies of radioactivity', 'Guglielmo Marconi': 'long-distance wireless telegraphy and the development of practical radio communication', 'Edwin Hubble': 'observations showing that galaxies lie beyond the Milky Way and the evidence for cosmic expansion', 'Enrico Fermi': 'neutron physics, nuclear reactions and the first controlled nuclear chain reaction', 'John von Neumann': 'foundational work in quantum theory, computing and game theory', 'Richard Feynman': 'quantum electrodynamics and the Feynman diagram technique', 'Carl Sagan': 'planetary science, exobiology and public communication of science', 'Stephen Hawking': 'black-hole physics, Hawking radiation and major work in cosmology'}
GENERIC_HINTS = {'en': 'Renowned Scientist', 'es': 'Renombrado científico', 'fr': 'Scientifique renommé', 'ru': 'Знаменитый ученый'}
GENERIC_SIGS = {'en': 'Remembered for shaping historical developments in scientist.', 'es': 'Recordado por impulsar el desarrollo histórico como científico.', 'fr': 'Mémorable pour avoir marqué les développements historiques en tant que scientifique.', 'ru': 'Запомнился тем, что оказал значительное влияние на историческое развитие в качестве ученого.'}

def main() -> None:
    original = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(original)
    changed = 0

    for name, anchor in PEOPLE.items():
        if name not in data["people"]:
            raise KeyError(f"Person not found: {name}")
        person = data["people"][name]
        hints = {
            "en": f"Scientist associated with {anchor}.",
            "es": f"Científico asociado a {anchor}.",
            "fr": f"Scientifique associé à {anchor}.",
            "ru": f"Учёный, связанный с: {anchor}.",
        }
        significance = {
            "en": f"{name} left a lasting mark on science through {anchor}.",
            "es": f"{name} dejó una huella duradera en la ciencia mediante {anchor}.",
            "fr": f"{name} a durablement marqué les sciences grâce à {anchor}.",
            "ru": f"{name} оставил заметный след в истории науки благодаря: {anchor}.",
        }
        for lang in TARGET_LANGS:
            entry = person["languages"][lang]
            if entry.get("hint") == GENERIC_HINTS[lang]:
                entry["hint"] = hints[lang]
                changed += 1
            if entry.get("historical_significance") == GENERIC_SIGS[lang]:
                entry["historical_significance"] = significance[lang]
                changed += 1

    backup = JSON_PATH.with_name("person_i18n.before_batch13_scientists.json")
    backup.write_text(original, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    js = "const PERSON_I18N = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    JS_PATH.write_text(js, encoding="utf-8")
    verify_json = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    verify_js = json.loads(js.removeprefix("const PERSON_I18N = ").removesuffix(";\n"))
    if verify_json != verify_js:
        raise RuntimeError("JSON↔JS semantic equality failed")
    print(f"Batch 13 scientist cleanup: {changed} field changes.")
    print(f"Backup JSON: {backup}")
    print("JSON↔JS semantic equality: PASS")

if __name__ == "__main__":
    main()
