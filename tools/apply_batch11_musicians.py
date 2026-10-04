from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"

TARGET_LANGS = ("en", "es", "fr", "ru")
GENERIC_HINTS = {
    "en": "Renowned Musician",
    "es": "Renombrado músico",
    "fr": "Musicien renommé",
    "ru": "Знаменитый музыкант",
}

ANCHORS = {'Claudio Monteverdi': "L'Orfeo and his madrigals", 'Antonio Vivaldi': 'The Four Seasons and his concertos', 'Johann Sebastian Bach': 'the Brandenburg Concertos and The Well-Tempered Clavier', 'George Frideric Handel': 'Messiah and the English oratorio', 'Joseph Haydn': 'his London Symphonies and string quartets', 'Wolfgang Amadeus Mozart': 'Don Giovanni, The Magic Flute and his piano concertos', 'Ludwig van Beethoven': 'his Fifth and Ninth Symphonies', 'Gioachino Rossini': 'The Barber of Seville and bel canto opera', 'Frédéric Chopin': 'his mazurkas, polonaises and piano études', 'Richard Wagner': 'The Ring cycle and leitmotif technique', 'Giuseppe Verdi': 'La traviata, Aida and Otello', 'Johannes Brahms': 'his four symphonies and A German Requiem', 'Pyotr Tchaikovsky': 'Swan Lake, The Nutcracker and the Pathétique', 'Gustav Mahler': 'his large-scale symphonies and Das Lied von der Erde', 'Sergei Rachmaninoff': 'his Piano Concertos Nos. 2 and 3', 'Igor Stravinsky': 'The Firebird, Petrushka and The Rite of Spring', 'Sergei Prokofiev': 'Peter and the Wolf and Romeo and Juliet', 'Dmitri Shostakovich': 'his fifteen symphonies and fifteen string quartets', 'Elvis Presley': 'his early rock recordings and landmark live performances', 'John Lennon': 'the Beatles and Imagine', 'Jim Morrison': 'the Doors and his poetic rock lyrics', 'Bob Marley': 'Exodus and the international spread of reggae', 'Freddie Mercury': 'Queen and Bohemian Rhapsody', 'Michael Jackson': 'Thriller and his integrated music-video performances'}

def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    changed = 0
    for name, anchor in ANCHORS.items():
        person = data["people"][name]
        hints = {
            "en": f"Key figure associated with {anchor}.",
            "es": f"Figura clave de la música asociada a {anchor}.",
            "fr": f"Figure majeure de la musique associée à {anchor}.",
            "ru": f"Ключевая фигура музыкальной истории, связанная с {anchor}.",
        }
        significance = {
            "en": f"{name} left a lasting mark on music through {anchor}.",
            "es": f"{name} dejó una huella duradera en la música mediante {anchor}.",
            "fr": f"{name} a durablement marqué la musique grâce à {anchor}.",
            "ru": f"{name} оставил заметный след в истории музыки благодаря: {anchor}.",
        }
        for lang in TARGET_LANGS:
            entry = person["languages"][lang]
            if entry.get("hint") == GENERIC_HINTS[lang]:
                entry["hint"] = hints[lang]
                changed += 1
            old_sig = str(entry.get("historical_significance", ""))
            generic_markers = (
                "Remembered for shaping historical developments in musician.",
                "Recordado por impulsar el desarrollo histórico como músico.",
                "Mémorable pour avoir marqué les développements historiques en tant que musicien.",
                "Запомнился тем, что оказал значительное влияние на историческое развитие в качестве музыканта.",
            )
            if old_sig in generic_markers:
                entry["historical_significance"] = significance[lang]
                changed += 1

    backup = JSON_PATH.with_name("person_i18n.before_batch11_musicians.json")
    backup.write_text(JSON_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    js = "const PERSON_I18N = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    JS_PATH.write_text(js, encoding="utf-8")
    verify_json = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    verify_js = json.loads(js.removeprefix("const PERSON_I18N = ").removesuffix(";\n"))
    if verify_json != verify_js:
        raise RuntimeError("JSON↔JS semantic equality failed")
    print(f"Batch 11 musician cleanup: {changed} field changes.")
    print(f"Backup JSON: {backup}")
    print("JSON↔JS semantic equality: PASS")

if __name__ == "__main__":
    main()
