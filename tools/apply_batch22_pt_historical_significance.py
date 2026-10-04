from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"

# Batch 22 intentionally targets the two largest exact duplicate groups:
# Portuguese artist significance (15) and Portuguese scientist significance (15).
# Each replacement is person-specific; no generic role template is used.
TARGETS: dict[str, str] = {
    # Artists
    "Francisco Goya": "Reconhecido pelas pinturas que documentaram a violência da guerra e pela transformação da arte espanhola no início da modernidade.",
    "Eugène Delacroix": "Reconhecido como uma figura central do romantismo francês, sobretudo por obras que combinaram cor intensa, movimento e temas históricos.",
    "Claude Monet": "Reconhecido como um dos principais fundadores do impressionismo, pela investigação contínua da luz, da cor e das mudanças atmosféricas.",
    "Henri Rousseau": "Reconhecido por cenas de selva imaginárias e por uma linguagem pictórica autodidata que influenciou artistas modernos.",
    "Paul Gauguin": "Reconhecido por romper com a representação naturalista e explorar cores intensas e formas simplificadas que influenciaram a arte moderna.",
    "Vincent van Gogh": "Reconhecido pela força expressiva das suas cores e pinceladas e pelo impacto duradouro da sua obra na pintura moderna.",
    "Alphonse Mucha": "Reconhecido por estabelecer uma linguagem gráfica emblemática da Art Nouveau através de cartazes, ilustrações e desenhos ornamentais.",
    "Edvard Munch": "Reconhecido por transformar experiências de ansiedade, amor e morte em uma linguagem expressionista de grande influência.",
    "Wassily Kandinsky": "Reconhecido como pioneiro da abstração, ao explorar relações entre cor, forma e expressão espiritual na pintura.",
    "Henri Matisse": "Reconhecido por revolucionar o uso da cor e da forma e por uma obra que atravessou pintura, escultura e recortes de papel.",
    "Kazimir Malevich": "Reconhecido por fundar o suprematismo e levar a pintura abstrata a uma linguagem baseada em formas geométricas elementares.",
    "Pablo Picasso": "Reconhecido por cofundar o cubismo e transformar radicalmente a representação visual através de sucessivas experiências artísticas.",
    "Amedeo Modigliani": "Reconhecido pelos retratos e nus de formas alongadas, que se tornaram uma das linguagens figurativas mais distintas da arte moderna.",
    "Marc Chagall": "Reconhecido por combinar memória, símbolos, cores intensas e imagens oníricas em uma linguagem visual pessoal.",
    "Joan Miró": "Reconhecido por desenvolver uma linguagem poética de formas orgânicas e símbolos que marcou a pintura moderna e o surrealismo.",

    # Scientists
    "James Watt": "Reconhecido pelas melhorias decisivas no motor a vapor, especialmente o condensador separado, que aumentou sua eficiência industrial.",
    "Georg Ohm": "Reconhecido por formular a relação matemática entre tensão, corrente e resistência que passou a ser conhecida como lei de Ohm.",
    "Michael Faraday": "Reconhecido pela descoberta da indução eletromagnética e por trabalhos fundamentais sobre eletrólise e campos magnéticos.",
    "James Prescott Joule": "Reconhecido por demonstrar quantitativamente a relação entre trabalho e calor e por contribuições fundamentais à conservação da energia.",
    "Gregor Mendel": "Reconhecido pelos experimentos com ervilhas que revelaram padrões regulares de hereditariedade e lançaram as bases da genética.",
    "James Clerk Maxwell": "Reconhecido por unificar matematicamente eletricidade e magnetismo e prever a natureza eletromagnética das ondas luminosas.",
    "Alfred Nobel": "Reconhecido pela invenção da dinamite e por estabelecer, por meio de seu legado, os Prêmios Nobel.",
    "Dmitri Mendeleev": "Reconhecido por organizar a tabela periódica e prever propriedades de elementos que ainda não haviam sido descobertos.",
    "Ernest Rutherford": "Reconhecido por demonstrar a existência do núcleo atômico e por pesquisas fundamentais sobre radioatividade e desintegração.",
    "Edwin Hubble": "Reconhecido por demonstrar a existência de galáxias além da Via Láctea e por estabelecer evidências da expansão do universo.",
    "Enrico Fermi": "Reconhecido por contribuições decisivas à física nuclear e por liderar a construção do primeiro reator nuclear autossustentável.",
    "John von Neumann": "Reconhecido por contribuições fundamentais à arquitetura dos computadores, à teoria dos jogos e à matemática aplicada.",
    "Richard Feynman": "Reconhecido por contribuições decisivas à eletrodinâmica quântica e por métodos que transformaram a física teórica.",
    "Carl Sagan": "Reconhecido por pesquisas planetárias e por tornar a astronomia e a ciência acessíveis a milhões de pessoas.",
    "Stephen Hawking": "Reconhecido por trabalhos sobre buracos negros e cosmologia teórica e por sua divulgação científica para o grande público.",
}


def normalize_name(value: str) -> str:
    try:
        return value.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value


def find_person(people: dict, target: str) -> dict | None:
    for person in people.values():
        if not isinstance(person, dict):
            continue
        languages = person.get("languages")
        if not isinstance(languages, dict):
            continue
        en = languages.get("en")
        if not isinstance(en, dict):
            continue
        name = en.get("name")
        if isinstance(name, str) and (
            name == target or normalize_name(name) == target
        ):
            return person
    return None


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"person_i18n_before_batch22_pt_significance_{stamp}.json"
    shutil.copy2(JSON_PATH, backup)

    missing: list[str] = []
    changed = 0

    for name, significance in TARGETS.items():
        person = find_person(people, name)
        if person is None:
            missing.append(name)
            continue
        languages = person.setdefault("languages", {})
        pt = languages.setdefault("pt", {})
        if pt.get("historical_significance") != significance:
            pt["historical_significance"] = significance
            changed += 1

    if missing:
        raise RuntimeError("Missing people:\n" + "\n".join(missing))

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    JS_PATH.write_text(
        "/* Auto-generated from person_i18n.json. Do not edit manually. */\n"
        "window.PERSON_I18N = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    js_payload = JS_PATH.read_text(encoding="utf-8").split(
        "window.PERSON_I18N = ", 1
    )[1].rsplit(";", 1)[0]
    if json.loads(js_payload) != data:
        raise RuntimeError("JSON<->JS semantic equality FAILED")

    print(f"Batch 22 applied: {changed} fields across {len(TARGETS)} people.")
    print(f"Backup JSON: {backup}")
    print("JSON<->JS semantic equality: PASS")
    print("Language: pt")
    print("Target groups: 15 artists + 15 scientists")


if __name__ == "__main__":
    main()
