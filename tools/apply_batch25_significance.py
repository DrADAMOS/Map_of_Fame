from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"


# Batch 25: largest remaining historical-significance template groups.
# Only historical_significance is changed. Every replacement is person-specific.
TARGETS: dict[str, str] = {
    # Arabic politicians — 11
    "Thomas Jefferson|ar": "ارتبط إرث جيفرسون بصياغة إعلان الاستقلال وبناء النظام الجمهوري الأميركي المبكر، كما كان لسياساته الرئاسية، ومنها شراء لويزيانا، أثر طويل في توسع الولايات المتحدة.",
    "Alexander Hamilton|ar": "كان هاملتون من أبرز مهندسي النظام المالي الأميركي المبكر، ودافع عن إنشاء بنك وطني وتوحيد الديون وتعزيز الحكومة الفدرالية، وأسهم في تأسيس البرنامج الفدرالي.",
    "Joseph Stalin|ar": "غيّر ستالين بنية الاتحاد السوفيتي عبر التصنيع السريع والتجميع الزراعي القسري وتركيز السلطة، وقاد الدولة خلال الجزء الأكبر من الحرب السوفيتية ضد ألمانيا النازية.",
    "Mustafa Kemal Atatürk|ar": "أسس أتاتورك الجمهورية التركية وقاد إصلاحات واسعة في القانون والتعليم واللغة ومؤسسات الدولة، واضعاً أسس النظام الجمهوري الحديث بعد سقوط الدولة العثمانية.",
    "Franklin D. Roosevelt|ar": "أعاد روزفلت تشكيل دور الحكومة الأميركية عبر برامج الصفقة الجديدة، ثم قاد الولايات المتحدة خلال معظم الحرب العالمية الثانية، فترك أثراً عميقاً في السياسة الاقتصادية والاجتماعية الأميركية.",
    "Harry S. Truman|ar": "قاد ترومان الولايات المتحدة في نهاية الحرب العالمية الثانية وبداية الحرب الباردة، وارتبط عهده بمبدأ ترومان وخطة مارشال وتأسيس حلف الناتو.",
    "Adolf Hitler|ar": "قاد هتلر ألمانيا النازية نحو التوسع والحرب في أوروبا، وكان نظامه مسؤولاً عن الهولوكوست والاضطهاد الجماعي، مما جعله محوراً أساسياً في تاريخ الاستبداد والإبادة الجماعية في القرن العشرين.",
    "Jawaharlal Nehru|ar": "كان نهرو أول رئيس وزراء للهند المستقلة، وأسهم في ترسيخ مؤسساتها البرلمانية وتوجهها العلماني وسياسة عدم الانحياز في السنوات الأولى من الحرب الباردة.",
    "Charles de Gaulle|ar": "قاد ديغول فرنسا الحرة خلال الحرب العالمية الثانية، ثم أسس الجمهورية الخامسة، وأثر بصورة حاسمة في المؤسسات السياسية الفرنسية ودور فرنسا الدولي بعد الحرب.",
    "Rosa Parks|ar": "أصبحت روزا باركس رمزاً لحركة الحقوق المدنية الأميركية بعد رفضها التخلي عن مقعدها في حافلة بمدينة مونتغومري عام 1955، وهو الحدث الذي ساعد على إطلاق مقاطعة حافلات مونتغومري.",
    "Eva Perón|ar": "كان لإيفا بيرون حضور بارز في الحياة العامة الأرجنتينية من خلال دعم العمال والنساء، والمساهمة في حملة حق المرأة في التصويت، وبرامج مؤسسة إيفا بيرون الاجتماعية.",

    # Portuguese military leaders — 11
    "Alexander Suvorov|pt": "Suvorov destacou-se pelas campanhas russas contra o Império Otomano e pelas operações na Itália e nos Alpes em 1799, tornando-se uma das figuras militares mais célebres da Rússia imperial.",
    "José de San Martín|pt": "San Martín foi decisivo nas guerras de independência sul-americanas, organizando o Exército dos Andes e conduzindo as campanhas que contribuíram para a independência da Argentina, do Chile e do Peru.",
    "Robert E. Lee|pt": "Lee comandou o Exército da Virgínia do Norte durante grande parte da Guerra Civil Americana e tornou-se o principal comandante militar da Confederação, rendendo-se em Appomattox em 1865.",
    "Ulysses S. Grant|pt": "Grant comandou as forças da União nas fases decisivas da Guerra Civil Americana, coordenando campanhas que levaram à rendição de Robert E. Lee em Appomattox; depois tornou-se presidente dos Estados Unidos.",
    "Horatio Kitchener|pt": "Kitchener foi uma figura central na organização militar britânica durante a Primeira Guerra Mundial, especialmente na expansão do Exército britânico e na mobilização de voluntários em larga escala.",
    "Douglas MacArthur|pt": "MacArthur comandou forças aliadas no Pacífico durante a Segunda Guerra Mundial e depois liderou a ocupação do Japão, desempenhando também um papel central nas primeiras fases da Guerra da Coreia.",
    "George S. Patton|pt": "Patton destacou-se pelo comando de forças blindadas norte-americanas no Norte da África, na Sicília e na Europa durante a Segunda Guerra Mundial, especialmente em operações de rápida mobilidade.",
    "T. E. Lawrence|pt": "Lawrence ficou conhecido pelo papel que desempenhou na Revolta Árabe durante a Primeira Guerra Mundial, ajudando forças árabes a combater o Império Otomano e tornando-se posteriormente uma figura célebre da literatura e da história militar.",
    "Dwight D. Eisenhower|pt": "Eisenhower foi o comandante supremo aliado na Europa durante a Segunda Guerra Mundial e coordenou o desembarque da Normandia; depois tornou-se presidente dos Estados Unidos.",
    "Erwin Rommel|pt": "Rommel ganhou notoriedade pelo comando de forças alemãs no Norte da África durante a Segunda Guerra Mundial, onde sua atuação lhe valeu o apelido de Raposa do Deserto, antes de sua participação final na Alemanha em 1944.",
    "Georgy Zhukov|pt": "Jukov foi um dos principais comandantes soviéticos da Segunda Guerra Mundial, desempenhando papéis decisivos na defesa de Moscou e Stalingrado e na ofensiva que culminou na tomada de Berlim.",

    # Arabic military leaders — 10
    "José de San Martín|ar": "كان سان مارتين من القادة الرئيسيين في حروب استقلال أميركا الجنوبية، ونظّم جيش الأنديز وقاد حملات أسهمت في استقلال الأرجنتين وتشيلي وبيرو.",
    "Robert E. Lee|ar": "قاد لي جيش فرجينيا الشمالية خلال معظم الحرب الأهلية الأميركية، وأصبح أبرز قادة الكونفدرالية قبل استسلامه لقوات الاتحاد في أبوماتوكس عام 1865.",
    "Ulysses S. Grant|ar": "قاد غرانت قوات الاتحاد في المراحل الحاسمة من الحرب الأهلية الأميركية، ونسّق حملات انتهت باستسلام روبرت لي في أبوماتوكس، ثم أصبح رئيساً للولايات المتحدة.",
    "Horatio Kitchener|ar": "كان كيتشنر من أبرز المسؤولين عن التوسع العسكري البريطاني خلال الحرب العالمية الأولى، وأسهم في تعبئة أعداد كبيرة من المتطوعين وتوسيع الجيش البريطاني.",
    "Douglas MacArthur|ar": "قاد ماك آرثر قوات الحلفاء في جنوب غرب المحيط الهادئ خلال الحرب العالمية الثانية، ثم أشرف على احتلال اليابان، ولعب دوراً مهماً في المراحل الأولى من الحرب الكورية.",
    "George S. Patton|ar": "برز باتون في قيادة القوات المدرعة الأميركية في شمال أفريقيا وصقلية وأوروبا خلال الحرب العالمية الثانية، واشتهر بسرعة تحرك قواته في العمليات الهجومية.",
    "T. E. Lawrence|ar": "اشتهر لورنس بدوره في الثورة العربية خلال الحرب العالمية الأولى، حيث تعاون مع القوات العربية ضد الدولة العثمانية، ثم أصبح لاحقاً شخصية بارزة في الأدب والتاريخ العسكري.",
    "Dwight D. Eisenhower|ar": "كان أيزنهاور القائد الأعلى لقوات الحلفاء في أوروبا خلال الحرب العالمية الثانية، وأشرف على التخطيط لعملية إنزال نورماندي، ثم أصبح رئيساً للولايات المتحدة.",
    "Erwin Rommel|ar": "اشتهر رومل بقيادة القوات الألمانية في شمال أفريقيا خلال الحرب العالمية الثانية، واكتسب لقب ثعلب الصحراء، ثم ارتبط اسمه بالمؤامرات العسكرية والسياسية داخل ألمانيا عام 1944.",
    "Georgy Zhukov|ar": "كان جوكوف من أبرز القادة السوفيت في الحرب العالمية الثانية، وشارك في الدفاع عن موسكو وستالينغراد ثم في الهجوم الذي انتهى بسقوط برلين عام 1945.",
}


def split_key(key: str) -> tuple[str, str]:
    name, lang = key.rsplit("|", 1)
    return name, lang


def rebuild_js(data: dict) -> None:
    JS_PATH.write_text(
        "window.PERSON_I18N = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data.get("people")
    if not isinstance(people, dict):
        raise TypeError("Expected top-level 'people' object.")

    index: dict[str, dict] = {}
    for person in people.values():
        if not isinstance(person, dict):
            continue
        languages = person.get("languages", {})
        if not isinstance(languages, dict):
            continue
        for lang_data in languages.values():
            if isinstance(lang_data, dict) and isinstance(lang_data.get("name"), str):
                index.setdefault(lang_data["name"], person)
                break

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"person_i18n_before_batch25_{timestamp}.json"
    shutil.copy2(JSON_PATH, backup)

    missing: list[str] = []
    changed = 0

    for raw_key, value in TARGETS.items():
        name, lang = split_key(raw_key)
        person = index.get(name)
        if person is None:
            missing.append(raw_key)
            continue

        languages = person.get("languages", {})
        lang_data = languages.get(lang) if isinstance(languages, dict) else None
        if not isinstance(lang_data, dict):
            missing.append(raw_key)
            continue

        if lang_data.get("historical_significance") != value:
            lang_data["historical_significance"] = value
            changed += 1

    if missing:
        raise RuntimeError("Missing targets:\n" + "\n".join(missing))

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    rebuild_js(data)

    marker = "window.PERSON_I18N = "
    js = JS_PATH.read_text(encoding="utf-8")
    if not js.startswith(marker):
        raise RuntimeError("Unexpected JS format.")
    payload = js[len(marker):].strip()
    if payload.endswith(";"):
        payload = payload[:-1].rstrip()
    if json.loads(payload) != data:
        raise RuntimeError("JSON<->JS semantic equality FAILED.")

    print(f"Batch 25 applied: {changed} fields across 32 people.")
    print("AR politicians: 11 | PT military: 11 | AR military: 10")
    print(f"Backup JSON: {backup}")
    print("JSON<->JS semantic equality: PASS")


if __name__ == "__main__":
    main()
