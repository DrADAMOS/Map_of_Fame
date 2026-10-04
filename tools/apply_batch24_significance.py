from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"


TARGETS: dict[str, dict[str, str]] = {
    # English politician significance
    "Thomas Jefferson": {
        "en": "Jefferson shaped the early United States through the Declaration of Independence, the Virginia Statute for Religious Freedom, and the Louisiana Purchase, while his presidency helped define the republic's early political direction."
    },
    "Alexander Hamilton": {
        "en": "Hamilton was central to the creation of the U.S. financial system, advocating a national bank, federal assumption of state debts, and a strong federal government through the Federalist program."
    },
    "Joseph Stalin": {
        "en": "Stalin transformed the Soviet Union through forced collectivization, rapid industrialization, and centralized rule, while his leadership was decisive in the Soviet war effort against Nazi Germany."
    },
    "Mustafa Kemal Atatürk": {
        "en": "Atatürk founded the Republic of Turkey and led sweeping reforms in law, education, language, and government that replaced much of the Ottoman political and institutional order."
    },
    "Franklin D. Roosevelt": {
        "en": "Roosevelt reshaped the American state through the New Deal and led the United States through most of World War II, establishing a lasting model of expanded federal economic and social intervention."
    },
    "Harry S. Truman": {
        "en": "Truman presided over the final phase of World War II and the opening of the Cold War, including the Marshall Plan, the Truman Doctrine, and the creation of NATO during his presidency."
    },
    "Adolf Hitler": {
        "en": "Hitler's dictatorship drove Nazi Germany's expansion and the outbreak of World War II in Europe and was responsible for the Holocaust, making his regime central to the history of twentieth-century totalitarianism and genocide."
    },
    "Jawaharlal Nehru": {
        "en": "Nehru became independent India's first prime minister and helped establish its parliamentary institutions, secular political framework, and policy of non-alignment during the early Cold War."
    },
    "Charles de Gaulle": {
        "en": "De Gaulle led Free France during World War II and later founded the Fifth Republic, leaving a decisive mark on modern French institutions and France's postwar international role."
    },
    "Rosa Parks": {
        "en": "Parks became a major symbol of the U.S. civil rights movement after her 1955 refusal to surrender her bus seat helped trigger the Montgomery Bus Boycott."
    },
    "Eva Perón": {
        "en": "Eva Perón became a powerful figure in Argentine public life through her advocacy for workers and women, her role in the campaign for women's suffrage, and the social programs associated with the Eva Perón Foundation."
    },
    "Malcolm X": {
        "en": "Malcolm X became an influential voice for Black self-determination and racial justice in the United States, and his later shift toward broader international human-rights advocacy expanded his political legacy."
    },

    # French versions of the same 12
    "Thomas Jefferson|fr": "Jefferson a marqué les débuts des États-Unis par la Déclaration d'indépendance, le Virginia Statute for Religious Freedom et l'achat de la Louisiane, tandis que sa présidence a contribué à définir l'orientation politique de la jeune république.",
    "Alexander Hamilton|fr": "Hamilton a joué un rôle central dans la création du système financier américain en défendant une banque nationale, la prise en charge fédérale des dettes des États et un gouvernement fédéral fort.",
    "Joseph Stalin|fr": "Staline a transformé l'Union soviétique par la collectivisation forcée, l'industrialisation accélérée et un pouvoir fortement centralisé, tandis que sa direction a été déterminante dans l'effort de guerre soviétique contre l'Allemagne nazie.",
    "Mustafa Kemal Atatürk|fr": "Atatürk a fondé la République de Turquie et conduit de profondes réformes du droit, de l'éducation, de la langue et des institutions, rompant avec une grande partie de l'ordre politique et institutionnel ottoman.",
    "Franklin D. Roosevelt|fr": "Roosevelt a profondément transformé l'État américain avec le New Deal et dirigé les États-Unis pendant l'essentiel de la Seconde Guerre mondiale, durablement l'action fédérale dans les domaines économique et social.",
    "Harry S. Truman|fr": "Truman a dirigé les États-Unis durant la fin de la Seconde Guerre mondiale et les débuts de la guerre froide, notamment avec la doctrine Truman, le plan Marshall et la création de l'OTAN.",
    "Adolf Hitler|fr": "Hitler a dirigé l'Allemagne nazie dans son expansion territoriale et dans le déclenchement de la Seconde Guerre mondiale en Europe; son régime fut aussi responsable de la Shoah, qui en fait une figure centrale de l'histoire du totalitarisme et du génocide au XXe siècle.",
    "Jawaharlal Nehru|fr": "Nehru fut le premier Premier ministre de l'Inde indépendante et contribua à établir ses institutions parlementaires, son cadre politique séculier et sa politique de non-alignement au début de la guerre froide.",
    "Charles de Gaulle|fr": "De Gaulle a dirigé la France libre pendant la Seconde Guerre mondiale puis fondé la Ve République, laissant une empreinte décisive sur les institutions françaises modernes et le rôle international de la France après-guerre.",
    "Rosa Parks|fr": "Parks est devenue un symbole majeur du mouvement américain des droits civiques après son refus, en 1955, de céder sa place dans un autobus, événement qui contribua au déclenchement du boycott des bus de Montgomery.",
    "Eva Perón|fr": "Eva Perón a joué un rôle majeur dans la vie publique argentine par son soutien aux travailleurs et aux femmes, sa participation à la campagne pour le suffrage féminin et les programmes sociaux liés à la Fondation Eva Perón.",
    "Malcolm X|fr": "Malcolm X fut une voix influente de l'autodétermination noire et de la justice raciale aux États-Unis; son évolution vers une approche plus internationale des droits humains a élargi la portée de son héritage politique.",

    # Turkish musician significance
    "Joseph Haydn|tr": "Haydn, senfoni ve yaylı çalgılar dörtlüsü repertuvarının gelişiminde belirleyici rol oynayarak Klasik dönem müziğinin temel biçimlerinin yerleşmesine katkıda bulundu.",
    "Wolfgang Amadeus Mozart|tr": "Mozart, senfoni, konçerto, oda müziği ve opera alanındaki eserleriyle Klasik dönemin ifade gücünü genişletti; özellikle opera repertuvarı üzerindeki etkisi kalıcı oldu.",
    "Ludwig van Beethoven|tr": "Beethoven, Klasik dönem ile Romantik dönem arasındaki geçişi belirleyen eserleriyle senfoni, sonat ve oda müziğinin kapsamını ve ifade olanaklarını köklü biçimde genişletti.",
    "Gioachino Rossini|tr": "Rossini, özellikle opera buffa ve opera seria alanındaki eserleriyle on dokuzuncu yüzyıl İtalyan operasının gelişiminde önemli bir rol oynadı ve bel canto geleneğini etkiledi.",
    "Frédéric Chopin|tr": "Chopin, piyano için yazdığı mazurkalar, noktürnler, baladlar ve etütlerle romantik piyano müziğinin dilini dönüştürdü ve piyano repertuvarının kalıcı bestecilerinden biri oldu.",
    "Richard Wagner|tr": "Wagner, müzik dramı anlayışı, leitmotif kullanımı ve gelişmiş armonik diliyle opera tarihini dönüştürdü; Bayreuth Festivali de onun sahneleme ve repertuvar anlayışının kalıcı mirası oldu.",
    "Giuseppe Verdi|tr": "Verdi, Rigoletto, La traviata ve Aida gibi operalarıyla İtalyan opera geleneğinin gelişimine yön verdi ve on dokuzuncu yüzyılın en etkili opera bestecilerinden biri oldu.",
    "Johannes Brahms|tr": "Brahms, senfoni, konçerto, oda müziği ve piyano eserlerinde klasik biçimlerle Romantik dönemin ifade anlayışını birleştirerek Alman müzik geleneğinin önemli temsilcilerinden biri oldu.",
    "Pyotr Tchaikovsky|tr": "Çaykovski, senfonileri, konçertoları, operaları ve bale müzikleriyle Rus bestecilik geleneğini Avrupa repertuvarıyla buluşturdu; Kuğu Gölü ve Fındıkkıran özellikle kalıcı bir sahne mirası bıraktı.",
    "Gustav Mahler|tr": "Mahler, senfoni ve lied türlerini geniş ölçekli orkestral anlatımla birleştirerek geç Romantizmin müzik dilini dönüştürdü ve yirminci yüzyıl besteciliğine güçlü bir geçiş noktası oluşturdu.",
    "Sergei Rachmaninoff|tr": "Rahmaninov, özellikle piyano konçertoları, senfonileri ve solo piyano eserleriyle geç Romantik üslubun en tanınan temsilcilerinden biri oldu ve piyano repertuvarını zenginleştirdi.",
    "Igor Stravinsky|tr": "Stravinsky, Bahar Ayini başta olmak üzere eserleriyle ritim, orkestrasyon ve biçim anlayışını dönüştürdü; Rus döneminden neoklasik ve seri müziğe uzanan kariyeri yirminci yüzyıl müziğini derinden etkiledi.",
}


def split_target_key(key: str) -> tuple[str, str]:
    if "|" in key:
        name, lang = key.rsplit("|", 1)
        return name, lang
    return key, "en"


def rebuild_js(data: dict) -> None:
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    JS_PATH.write_text(
        "window.PERSON_I18N = " + payload + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"Missing: {JSON_PATH}")

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data.get("people")
    if not isinstance(people, dict):
        raise TypeError("Expected top-level 'people' object.")

    by_name: dict[str, tuple[str, dict]] = {}
    for person_id, person in people.items():
        if not isinstance(person, dict):
            continue
        languages = person.get("languages", {})
        if not isinstance(languages, dict):
            continue
        for lang_data in languages.values():
            if isinstance(lang_data, dict) and isinstance(lang_data.get("name"), str):
                by_name.setdefault(lang_data["name"], (person_id, person))
                break

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"person_i18n_before_batch24_{timestamp}.json"
    shutil.copy2(JSON_PATH, backup)

    changed = 0
    missing: list[str] = []

    for raw_key, value in TARGETS.items():
        name, lang = split_target_key(raw_key)
        match = by_name.get(name)
        if match is None:
            missing.append(f"{name} [{lang}]")
            continue

        _, person = match
        languages = person.setdefault("languages", {})
        if lang not in languages or not isinstance(languages[lang], dict):
            missing.append(f"{name} [{lang}]")
            continue

        old = languages[lang].get("historical_significance")
        if old != value:
            languages[lang]["historical_significance"] = value
            changed += 1

    if missing:
        raise RuntimeError("Missing targets:\n" + "\n".join(missing))

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    rebuild_js(data)

    # Semantic equality check between JSON and the JS assignment.
    js = JS_PATH.read_text(encoding="utf-8")
    marker = "window.PERSON_I18N = "
    if not js.startswith(marker):
        raise RuntimeError("Unexpected JS format after rebuild.")
    js_payload = js[len(marker):].strip()
    if js_payload.endswith(";"):
        js_payload = js_payload[:-1].rstrip()
    js_data = json.loads(js_payload)
    if js_data != data:
        raise RuntimeError("JSON<->JS semantic equality FAILED.")

    print(f"Batch 24 applied: {changed} fields across 24 people.")
    print("EN: 12 | FR: 12 | TR: 12")
    print(f"Backup JSON: {backup}")
    print("JSON<->JS semantic equality: PASS")


if __name__ == "__main__":
    main()
