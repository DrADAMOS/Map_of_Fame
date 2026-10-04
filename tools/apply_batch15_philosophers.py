from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"

TARGET_HINTS = {
    "en": "Renowned Philosopher",
    "es": "Renombrado filósofo",
    "fr": "Philosophe renommé",
    "ru": "Знаменитый философ",
}

PEOPLE = {
    "Cicero": {
        "en": ("Roman statesman and orator", "Cicero shaped Roman political thought and Latin prose through his speeches, philosophical works, and defense of republican government."),
        "es": ("Estadista y orador romano", "Cicerón influyó en el pensamiento político romano y en la prosa latina mediante sus discursos, obras filosóficas y defensa del gobierno republicano."),
        "fr": ("Homme d'État et orateur romain", "Cicéron a marqué la pensée politique romaine et la prose latine par ses discours, ses œuvres philosophiques et sa défense de la république."),
        "ru": ("Римский государственный деятель и оратор", "Цицерон оказал большое влияние на римскую политическую мысль и латинскую прозу своими речами, философскими сочинениями и защитой республиканского строя."),
    },
    "Al-Farabi": {
        "en": ("Islamic philosopher of the classical age", "Al-Farabi integrated Greek philosophical traditions with Islamic intellectual thought and wrote influential works on logic, ethics, politics, and music."),
        "es": ("Filósofo islámico de la época clásica", "Al-Farabi integró tradiciones filosóficas griegas con el pensamiento islámico y escribió obras influyentes sobre lógica, ética, política y música."),
        "fr": ("Philosophe islamique de l'époque classique", "Al-Farabi a rapproché les traditions philosophiques grecques de la pensée islamique et a produit des œuvres majeures sur la logique, l'éthique, la politique et la musique."),
        "ru": ("Исламский философ классической эпохи", "Аль-Фараби соединил греческие философские традиции с исламской мыслью и создал влиятельные труды по логике, этике, политике и музыке."),
    },
    "Ibn Hazm": {
        "en": ("Andalusian theologian and philosopher", "Ibn Hazm was a major Andalusian intellectual whose writings ranged across theology, law, philosophy, history, and comparative religion."),
        "es": ("Teólogo y filósofo andalusí", "Ibn Hazm fue un destacado intelectual andalusí cuyos escritos abarcaron la teología, el derecho, la filosofía, la historia y la religión comparada."),
        "fr": ("Théologien et philosophe andalou", "Ibn Hazm fut un intellectuel majeur d'al-Andalus dont les écrits couvrent la théologie, le droit, la philosophie, l'histoire et la comparaison des religions."),
        "ru": ("Андалусский богослов и философ", "Ибн Хазм был выдающимся интеллектуалом Андалусии, писавшим о богословии, праве, философии, истории и сравнительном изучении религий."),
    },
    "Averroes": {
        "en": ("Andalusian philosopher and jurist", "Averroes wrote extensive commentaries on Aristotle and became one of the most influential interpreters of Aristotelian philosophy in the medieval world."),
        "es": ("Filósofo y jurista andalusí", "Averroes escribió amplios comentarios sobre Aristóteles y se convirtió en uno de los intérpretes medievales más influyentes de la filosofía aristotélica."),
        "fr": ("Philosophe et juriste andalou", "Averroès rédigea de nombreux commentaires d'Aristote et devint l'un des interprètes médiévaux les plus influents de la philosophie aristotélicienne."),
        "ru": ("Андалусский философ и правовед", "Аверроэс создал обширные комментарии к Аристотелю и стал одним из наиболее влиятельных средневековых толкователей аристотелевской философии."),
    },
    "Ibn Arabi": {
        "en": ("Andalusian mystic and philosopher", "Ibn Arabi developed a vast body of mystical and philosophical writing that profoundly influenced later Islamic thought, especially Sufi intellectual traditions."),
        "es": ("Místico y filósofo andalusí", "Ibn Arabi desarrolló una extensa obra mística y filosófica que influyó profundamente en el pensamiento islámico posterior, especialmente en las tradiciones intelectuales sufíes."),
        "fr": ("Mystique et philosophe andalou", "Ibn Arabi développa une vaste œuvre mystique et philosophique qui influença profondément la pensée islamique ultérieure, notamment les traditions intellectuelles soufies."),
        "ru": ("Андалусский мистик и философ", "Ибн Араби создал обширное мистическое и философское наследие, оказавшее глубокое влияние на последующую исламскую мысль, особенно на интеллектуальные традиции суфизма."),
    },
    "Francis Bacon": {
        "en": ("English philosopher and statesman", "Francis Bacon promoted a systematic approach to empirical inquiry and became an important early advocate of methods associated with modern scientific investigation."),
        "es": ("Filósofo y estadista inglés", "Francis Bacon impulsó un enfoque sistemático de la investigación empírica y fue uno de los primeros defensores de métodos vinculados con la ciencia moderna."),
        "fr": ("Philosophe et homme d'État anglais", "Francis Bacon défendit une approche systématique de l'enquête empirique et fut un précurseur important des méthodes associées à la recherche scientifique moderne."),
        "ru": ("Английский философ и государственный деятель", "Фрэнсис Бэкон отстаивал систематическое эмпирическое исследование и стал одним из важных ранних сторонников методов, связанных с современной научной практикой."),
    },
    "Thomas Hobbes": {
        "en": ("English political philosopher", "Thomas Hobbes developed a powerful theory of political authority and social order in Leviathan, arguing for a strong sovereign as a remedy for civil conflict."),
        "es": ("Filósofo político inglés", "Thomas Hobbes desarrolló una influyente teoría de la autoridad política y el orden social en Leviatán, defendiendo un soberano fuerte como respuesta al conflicto civil."),
        "fr": ("Philosophe politique anglais", "Thomas Hobbes développa dans le Léviathan une théorie influente de l'autorité politique et de l'ordre social, en défendant un souverain fort face aux conflits civils."),
        "ru": ("Английский политический философ", "Томас Гоббс разработал влиятельную теорию политической власти и общественного порядка в «Левиафане», защищая сильную верховную власть как средство против гражданского конфликта."),
    },
    "René Descartes": {
        "en": ("French philosopher and mathematician", "René Descartes helped establish modern rationalist philosophy and made major contributions to mathematics, including the development of analytic geometry."),
        "es": ("Filósofo y matemático francés", "René Descartes contribuyó decisivamente al racionalismo moderno y realizó importantes aportes a las matemáticas, incluido el desarrollo de la geometría analítica."),
        "fr": ("Philosophe et mathématicien français", "René Descartes contribua de façon décisive à la philosophie rationaliste moderne et apporta des innovations majeures aux mathématiques, notamment à la géométrie analytique."),
        "ru": ("Французский философ и математик", "Рене Декарт сыграл ключевую роль в развитии современного рационализма и внёс важный вклад в математику, включая развитие аналитической геометрии."),
    },
    "John Locke": {
        "en": ("English philosopher of liberal thought", "John Locke developed influential ideas about natural rights, government by consent, and the formation of knowledge through experience."),
        "es": ("Filósofo inglés del pensamiento liberal", "John Locke desarrolló ideas influyentes sobre los derechos naturales, el gobierno basado en el consentimiento y la formación del conocimiento mediante la experiencia."),
        "fr": ("Philosophe anglais de la pensée libérale", "John Locke développa des idées majeures sur les droits naturels, le gouvernement fondé sur le consentement et la formation des connaissances par l'expérience."),
        "ru": ("Английский философ либеральной мысли", "Джон Локк сформулировал влиятельные идеи о естественных правах, правлении на основе согласия и формировании знания через опыт."),
    },
    "Jean-Jacques Rousseau": {
        "en": ("Genevan philosopher and political thinker", "Jean-Jacques Rousseau transformed debates about political legitimacy, education, and society through works including The Social Contract and Emile."),
        "es": ("Filósofo y pensador político ginebrino", "Jean-Jacques Rousseau transformó los debates sobre la legitimidad política, la educación y la sociedad mediante obras como El contrato social y Emilio."),
        "fr": ("Philosophe et penseur politique genevois", "Jean-Jacques Rousseau transforma les débats sur la légitimité politique, l'éducation et la société avec des œuvres comme Du contrat social et Émile."),
        "ru": ("Женевский философ и политический мыслитель", "Жан-Жак Руссо изменил представления о политической легитимности, воспитании и обществе в таких трудах, как «Об общественном договоре» и «Эмиль»."),
    },
    "Auguste Comte": {
        "en": ("French philosopher and founder of positivism", "Auguste Comte formulated positivism and argued that society could be studied systematically, helping establish sociology as a distinct field of inquiry."),
        "es": ("Filósofo francés y fundador del positivismo", "Auguste Comte formuló el positivismo y sostuvo que la sociedad podía estudiarse de forma sistemática, contribuyendo a consolidar la sociología como campo propio."),
        "fr": ("Philosophe français et fondateur du positivisme", "Auguste Comte formula le positivisme et soutint que la société pouvait être étudiée systématiquement, contribuant à établir la sociologie comme domaine distinct."),
        "ru": ("Французский философ и основатель позитивизма", "Огюст Конт сформулировал позитивизм и утверждал, что общество можно изучать систематически, способствуя становлению социологии как самостоятельной области."),
    },
    "Karl Marx": {
        "en": ("German philosopher and political economist", "Karl Marx developed a major critique of capitalism and historical materialism, profoundly influencing political theory, economics, and socialist movements."),
        "es": ("Filósofo y economista político alemán", "Karl Marx desarrolló una influyente crítica del capitalismo y del materialismo histórico, con un profundo impacto en la teoría política, la economía y los movimientos socialistas."),
        "fr": ("Philosophe et économiste politique allemand", "Karl Marx développa une critique majeure du capitalisme et le matérialisme historique, influençant profondément la théorie politique, l'économie et les mouvements socialistes."),
        "ru": ("Немецкий философ и политический экономист", "Карл Маркс разработал влиятельную критику капитализма и концепцию исторического материализма, оказав глубокое воздействие на политическую теорию, экономику и социалистические движения."),
    },
    "Friedrich Nietzsche": {
        "en": ("German philosopher and cultural critic", "Friedrich Nietzsche challenged established moral and philosophical assumptions through works that explored values, power, culture, and the crisis of traditional beliefs."),
        "es": ("Filósofo y crítico cultural alemán", "Friedrich Nietzsche cuestionó supuestos morales y filosóficos establecidos mediante obras que exploraron los valores, el poder, la cultura y la crisis de las creencias tradicionales."),
        "fr": ("Philosophe et critique culturel allemand", "Friedrich Nietzsche remit en question des présupposés moraux et philosophiques établis à travers des œuvres consacrées aux valeurs, au pouvoir, à la culture et à la crise des croyances traditionnelles."),
        "ru": ("Немецкий философ и критик культуры", "Фридрих Ницше подвергал сомнению устоявшиеся моральные и философские представления, исследуя ценности, власть, культуру и кризис традиционных убеждений."),
    },
    "Bertrand Russell": {
        "en": ("British philosopher and logician", "Bertrand Russell made foundational contributions to analytic philosophy and mathematical logic and became a prominent public advocate for peace and social reform."),
        "es": ("Filósofo y lógico británico", "Bertrand Russell realizó aportes fundamentales a la filosofía analítica y la lógica matemática y fue un destacado defensor público de la paz y la reforma social."),
        "fr": ("Philosophe et logicien britannique", "Bertrand Russell apporta des contributions fondamentales à la philosophie analytique et à la logique mathématique et devint un défenseur public de la paix et des réformes sociales."),
        "ru": ("Британский философ и логик", "Бертран Рассел внёс фундаментальный вклад в аналитическую философию и математическую логику, а также стал заметным общественным сторонником мира и социальных реформ."),
    },
    "Malek Bennabi": {
        "en": ("Algerian thinker on civilization and society", "Malek Bennabi developed a distinctive analysis of civilization, cultural renewal, and the conditions he believed were necessary for societies to overcome decline and regain creative capacity."),
        "es": ("Pensador argelino sobre civilización y sociedad", "Malek Bennabi desarrolló un análisis propio de la civilización, la renovación cultural y las condiciones que consideraba necesarias para que las sociedades superaran el declive y recuperaran su capacidad creadora."),
        "fr": ("Penseur algérien de la civilisation et de la société", "Malek Bennabi développa une analyse originale de la civilisation, du renouveau culturel et des conditions qu'il jugeait nécessaires pour que les sociétés dépassent le déclin et retrouvent leur capacité créatrice."),
        "ru": ("Алжирский мыслитель о цивилизации и обществе", "Малек Беннаби разработал самобытный анализ цивилизации, культурного обновления и условий, которые, по его мнению, необходимы обществам для преодоления упадка и восстановления созидательной способности."),
    },
}


def rebuild_js(data: dict) -> None:
    JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    JS_PATH.write_text(
        "window.PERSON_I18N = " + payload + ";\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"Missing: {JSON_PATH}")

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"person_i18n_before_batch15_philosophers_{timestamp}.json"
    shutil.copy2(JSON_PATH, backup_path)

    changes = 0
    missing_people: list[str] = []

    for person_name, translations in PEOPLE.items():
        person = people.get(person_name)
        if person is None:
            missing_people.append(person_name)
            continue

        languages = person.get("languages", {})
        for lang, (hint, significance) in translations.items():
            entry = languages.get(lang)
            if not isinstance(entry, dict):
                continue

            # Only replace the exact generic hint/significance values.
            # Existing person-specific content is never overwritten.
            if entry.get("hint") == TARGET_HINTS.get(lang):
                entry["hint"] = hint
                changes += 1

            generic_significance = {
                "en": "Remembered for shaping historical developments in philosopher.",
                "es": "Recordado por impulsar el desarrollo histórico como filósofo.",
                "fr": "Mémorable pour avoir marqué les développements historiques en tant que philosophe.",
                "ru": "Запомнился тем, что оказал значительное влияние на историческое развитие в качестве философа.",
            }[lang]

            if entry.get("historical_significance") == generic_significance:
                entry["historical_significance"] = significance
                changes += 1

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rebuild_js(data)

    # Semantic equality check between JSON and generated JS payload.
    js_text = JS_PATH.read_text(encoding="utf-8")
    prefix = "window.PERSON_I18N = "
    if not js_text.startswith(prefix):
        raise RuntimeError("Generated JS prefix is invalid.")
    js_data = json.loads(js_text[len(prefix):].rstrip().rstrip(";").strip())
    if js_data != data:
        raise RuntimeError("JSON↔JS semantic equality failed.")

    print(f"Batch 15 philosopher cleanup: {changes} field changes.")
    print(f"Backup JSON: {backup_path}")
    if missing_people:
        print("Missing people:")
        for name in missing_people:
            print(f"  - {name}")
    print("JSON↔JS semantic equality: PASS")


if __name__ == "__main__":
    main()
