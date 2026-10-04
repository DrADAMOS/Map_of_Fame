from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"


TARGETS: dict[tuple[str, str], str] = {
    # Arabic — politicians
    ("Thomas Jefferson", "ar"): "أصبح توماس جيفرسون أحد أبرز مهندسي الجمهورية الأمريكية المبكرة؛ صاغ إعلان الاستقلال وتولى الرئاسة وقاد شراء لويزيانا الذي وسّع أراضي الولايات المتحدة بصورة كبيرة.",
    ("Alexander Hamilton", "ar"): "كان ألكسندر هاملتون من أهم مؤسسي النظام المالي الأمريكي، فدافع عن إنشاء بنك وطني وعن توحيد الديون العامة، وأسهم في بناء الحكومة الفدرالية الجديدة.",
    ("Joseph Stalin", "ar"): "حوّل جوزيف ستالين الاتحاد السوفيتي عبر التصنيع السريع والتجميع القسري للزراعة وترسيخ الحكم المركزي، وقاد البلاد خلال الجزء الأكبر من الحرب ضد ألمانيا النازية.",
    ("Mustafa Kemal Atatürk", "ar"): "أسس مصطفى كمال أتاتورك جمهورية تركيا وقاد إصلاحات واسعة في القانون والتعليم واللغة ومؤسسات الدولة، واضعاً أسس النظام الجمهوري التركي الحديث.",
    ("Franklin D. Roosevelt", "ar"): "أعاد فرانكلين روزفلت تشكيل دور الحكومة الأمريكية من خلال الصفقة الجديدة، وقاد الولايات المتحدة خلال معظم الحرب العالمية الثانية، ورسّخ توسع الدولة الفدرالية في الاقتصاد والمجتمع.",
    ("Harry S. Truman", "ar"): "قاد هاري ترومان الولايات المتحدة في نهاية الحرب العالمية الثانية وبداية الحرب الباردة، وارتبط عهده بمبدأ ترومان وخطة مارشال وتأسيس حلف الناتو.",
    ("Adolf Hitler", "ar"): "قاد أدولف هتلر ألمانيا النازية في التوسع العسكري الذي أشعل الحرب العالمية الثانية في أوروبا، وكان نظامه مسؤولاً عن الهولوكوست وعن واحدة من أكثر الدكتاتوريات تدميراً في القرن العشرين.",
    ("Jawaharlal Nehru", "ar"): "كان جواهر لال نهرو أول رئيس وزراء للهند المستقلة، وأسهم في بناء مؤسساتها البرلمانية وتوجهها العلماني وفي ترسيخ سياسة عدم الانحياز خلال بدايات الحرب الباردة.",
    ("Charles de Gaulle", "ar"): "قاد شارل ديغول فرنسا الحرة خلال الحرب العالمية الثانية، ثم أسس الجمهورية الخامسة، وكان له دور حاسم في تشكيل المؤسسات الفرنسية الحديثة ومكانة فرنسا الدولية بعد الحرب.",
    ("Rosa Parks", "ar"): "أصبحت روزا باركس رمزاً بارزاً لحركة الحقوق المدنية الأمريكية بعد رفضها عام 1955 التخلي عن مقعدها في حافلة، وهو الحدث الذي ساعد في إطلاق مقاطعة حافلات مونتغومري.",
    ("Eva Perón", "ar"): "برزت إيفا بيرون في الحياة العامة الأرجنتينية من خلال دعم العمال والنساء، ودورها في الحملة من أجل حق المرأة في التصويت، وبرامج المساعدة الاجتماعية التي ارتبطت بمؤسستها.",

    # Portuguese — military leaders
    ("Alexander Suvorov", "pt"): "Suvorov destacou-se como comandante russo por suas vitórias em campanhas contra o Império Otomano e na Itália e Suíça, tornando-se uma referência duradoura da tradição militar russa.",
    ("José de San Martín", "pt"): "José de San Martín foi um dos principais líderes das guerras de independência sul-americanas, conduzindo a campanha dos Andes e contribuindo para a independência da Argentina, do Chile e do Peru.",
    ("Robert E. Lee", "pt"): "Robert E. Lee comandou o Exército da Virgínia do Norte durante grande parte da Guerra Civil Americana e tornou-se a principal figura militar da Confederação, antes de se render em Appomattox em 1865.",
    ("Ulysses S. Grant", "pt"): "Ulysses S. Grant dirigiu importantes campanhas da União na Guerra Civil Americana, aceitou a rendição de Robert E. Lee em Appomattox e depois tornou-se presidente dos Estados Unidos.",
    ("Horatio Kitchener", "pt"): "Horatio Kitchener foi uma figura central do esforço militar britânico na Primeira Guerra Mundial, sobretudo na expansão do exército voluntário e na organização da mobilização britânica.",
    ("Douglas MacArthur", "pt"): "Douglas MacArthur comandou forças aliadas no Pacífico durante a Segunda Guerra Mundial, liderou a campanha de retorno às Filipinas e exerceu papel decisivo na ocupação do Japão após 1945.",
    ("George S. Patton", "pt"): "George S. Patton destacou-se como comandante blindado americano na Segunda Guerra Mundial, especialmente nas campanhas do Norte da África, Sicília e Europa Ocidental.",
    ("T. E. Lawrence", "pt"): "T. E. Lawrence ganhou destaque ao atuar com forças árabes durante a Revolta Árabe na Primeira Guerra Mundial, ajudando a coordenar operações contra o Império Otomano e tornando-se uma figura histórica controversa.",
    ("Dwight D. Eisenhower", "pt"): "Dwight D. Eisenhower comandou as forças aliadas na Europa durante a Segunda Guerra Mundial e supervisionou o desembarque da Normandia, tornando-se depois presidente dos Estados Unidos.",
    ("Erwin Rommel", "pt"): "Erwin Rommel comandou forças alemãs no Norte da África durante a Segunda Guerra Mundial e tornou-se conhecido por suas operações móveis, embora tenha terminado a guerra implicado na conspiração contra Hitler.",
    ("Georgy Zhukov", "pt"): "Georgy Zhukov foi um dos principais comandantes soviéticos na Segunda Guerra Mundial, participando da defesa de Moscou, da vitória em Stalingrado e da ofensiva que culminou na tomada de Berlim.",

    # Arabic — military leaders
    ("José de San Martín", "ar"): "كان خوسيه دي سان مارتين من أبرز قادة حروب استقلال أمريكا الجنوبية، وقاد عبور جبال الأنديز وحملات أسهمت في استقلال الأرجنتين وتشيلي وبيرو.",
    ("Robert E. Lee", "ar"): "قاد روبرت إي. لي جيش فرجينيا الشمالية في معظم مراحل الحرب الأهلية الأمريكية، وكان أبرز القادة العسكريين الكونفدراليين قبل استسلامه في أبوماتوكس عام 1865.",
    ("Ulysses S. Grant", "ar"): "قاد يوليسيس س. غرانت حملات حاسمة للاتحاد خلال الحرب الأهلية الأمريكية، وقبل استسلام روبرت إي. لي في أبوماتوكس، ثم أصبح رئيساً للولايات المتحدة.",
    ("Horatio Kitchener", "ar"): "كان هوراشيو كيتشنر من أبرز منظمي الجهد العسكري البريطاني في الحرب العالمية الأولى، وأسهم في توسيع الجيش وتنظيم التعبئة البريطانية على نطاق واسع.",
    ("Douglas MacArthur", "ar"): "قاد دوغلاس ماك آرثر قوات الحلفاء في جنوب غرب المحيط الهادئ خلال الحرب العالمية الثانية، وقاد حملة العودة إلى الفلبين ثم لعب دوراً رئيسياً في احتلال اليابان بعد الحرب.",
    ("George S. Patton", "ar"): "برز جورج س. باتون قائداً للقوات المدرعة الأمريكية في الحرب العالمية الثانية، وشارك في حملات شمال أفريقيا وصقلية وأوروبا الغربية.",
    ("T. E. Lawrence", "ar"): "اشتهر ت. إي. لورنس بدوره في الثورة العربية خلال الحرب العالمية الأولى، حيث تعاون مع القوات العربية ضد الدولة العثمانية، وأصبح لاحقاً شخصية تاريخية مثيرة للجدل.",
    ("Dwight D. Eisenhower", "ar"): "قاد دوايت د. أيزنهاور قوات الحلفاء في أوروبا خلال الحرب العالمية الثانية وأشرف على إنزال نورماندي، ثم انتقل إلى العمل السياسي وأصبح رئيساً للولايات المتحدة.",
    ("Erwin Rommel", "ar"): "قاد إرفين رومل القوات الألمانية في شمال أفريقيا خلال الحرب العالمية الثانية واشتهر بالمناورة السريعة، ثم ارتبط في نهاية الحرب بالمؤامرة ضد هتلر وأُجبر على الانتحار.",
    ("Georgy Zhukov", "ar"): "كان غيورغي جوكوف من أهم القادة السوفيت في الحرب العالمية الثانية، وشارك في الدفاع عن موسكو والانتصار في ستالينغراد والهجوم الأخير الذي انتهى بسقوط برلين.",
}


def find_people(people: dict) -> dict[str, dict]:
    # Index EVERY localized name. The previous batches failed because a person
    # may have been encountered first under a non-English localized name.
    index: dict[str, dict] = {}
    for person in people.values():
        if not isinstance(person, dict):
            continue
        languages = person.get("languages")
        if not isinstance(languages, dict):
            continue
        for lang_data in languages.values():
            if not isinstance(lang_data, dict):
                continue
            name = lang_data.get("name")
            if isinstance(name, str) and name.strip():
                index.setdefault(name.strip(), person)
    return index


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

    index = find_people(people)
    missing: list[str] = []

    for (name, lang) in TARGETS:
        if name not in index:
            missing.append(f"{name} [{lang}]")

    if missing:
        raise RuntimeError(
            "Could not resolve localized names:\n" + "\n".join(missing)
        )

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"person_i18n_before_batch26_{timestamp}.json"
    shutil.copy2(JSON_PATH, backup)

    changed = 0
    for (name, lang), value in TARGETS.items():
        person = index[name]
        languages = person.get("languages")
        if not isinstance(languages, dict):
            raise TypeError(f"Invalid languages object for {name}")
        lang_data = languages.get(lang)
        if not isinstance(lang_data, dict):
            raise RuntimeError(f"Missing language {lang} for {name}")
        if lang_data.get("historical_significance") != value:
            lang_data["historical_significance"] = value
            changed += 1

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

    print(f"Batch 26 applied: {changed} fields.")
    print("AR politicians: 11 | PT military: 11 | AR military: 10")
    print(f"Backup JSON: {backup}")
    print("JSON<->JS semantic equality: PASS")


if __name__ == "__main__":
    main()
