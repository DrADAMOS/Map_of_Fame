from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"

TARGET_HINT = "من أبرز شخصيات العصر الحديث في مجال عالم"
TARGET_SIG = "تركت أثراً تاريخياً كـ عالم في عصر العصر الحديث."

CONTENT = {
    "James Watt": (
        "مهندس اسكتلندي ارتبط بتطوير المحرك البخاري",
        "أدخل جيمس واط تحسينات جوهرية على المحرك البخاري، وأسهمت ابتكاراته في جعل الطاقة البخارية أكثر كفاءة ودعمت توسع الثورة الصناعية."
    ),
    "Georg Ohm": (
        "فيزيائي ألماني اكتشف العلاقة بين الجهد والتيار والمقاومة",
        "وضع جورج أوم العلاقة الأساسية بين الجهد والتيار والمقاومة، والتي أصبحت تعرف بقانون أوم وتشكل أساساً مهماً في دراسة الدوائر الكهربائية."
    ),
    "Michael Faraday": (
        "فيزيائي وكيميائي إنجليزي رائد في الكهرومغناطيسية",
        "اكتشف فاراداي الحث الكهرومغناطيسي وأسهم في تأسيس علم الكهروكيمياء، وكانت تجاربه أساساً مهماً لتطوير المولدات والمحركات الكهربائية."
    ),
    "James Prescott Joule": (
        "فيزيائي إنجليزي درس العلاقة بين الحرارة والطاقة",
        "أثبت جيمس جول العلاقة بين الشغل والحرارة وقدم إسهامات أساسية في فهم حفظ الطاقة، وحملت وحدة الطاقة في النظام الدولي اسمه."
    ),
    "Gregor Mendel": (
        "مؤسس علم الوراثة الحديث",
        "أجرى غريغور مندل تجاربه الشهيرة على نبات البازلاء، واكتشف أنماطاً أساسية لانتقال الصفات أصبحت أساساً لعلم الوراثة الحديث."
    ),
    "James Clerk Maxwell": (
        "فيزيائي اسكتلندي وحّد نظريات الكهرباء والمغناطيسية",
        "صاغ جيمس كليرك ماكسويل معادلات الكهرومغناطيسية التي وحدت الكهرباء والمغناطيسية والضوء ضمن إطار نظري واحد، وكان لعمله أثر عميق في الفيزياء الحديثة."
    ),
    "Alfred Nobel": (
        "كيميائي ومخترع ومؤسس جوائز نوبل",
        "طوّر ألفرد نوبل الديناميت وسجّل عدداً كبيراً من براءات الاختراع، وأسس وصيته المؤسسة التي أنشأت جوائز نوبل لتكريم الإنجازات البارزة."
    ),
    "Ernest Rutherford": (
        "فيزيائي نيوزيلندي رائد في فيزياء النواة",
        "قاد إرنست رذرفورد أبحاثاً حاسمة حول النشاط الإشعاعي وبنية الذرة، وأدى تفسيره لتجربة رقائق الذهب إلى النموذج النووي للذرة."
    ),
    "Edwin Hubble": (
        "فلكي أمريكي وسّع فهمنا للكون",
        "أثبت إدوين هابل أن مجرة درب التبانة ليست وحدها في الكون، وربط قياسات المجرات بسرعات ابتعادها، مما أسهم في ترسيخ فهم الكون المتوسع."
    ),
    "Enrico Fermi": (
        "فيزيائي إيطالي أمريكي رائد في الفيزياء النووية",
        "قدم إنريكو فيرمي إسهامات مهمة في الفيزياء النووية وميكانيكا الكم، وقاد الفريق الذي أنشأ أول مفاعل نووي ذاتي الاستدامة في شيكاغو."
    ),
    "John von Neumann": (
        "عالم رياضيات أسهم في تأسيس علوم الحاسوب الحديثة",
        "قدم جون فون نيومان إسهامات بارزة في الرياضيات والفيزياء والحوسبة، وارتبط اسمه ببنية الحاسوب ذات البرنامج المخزن وبالتطور المبكر للحوسبة الإلكترونية."
    ),
    "Carl Sagan": (
        "فلكي أمريكي ومروج بارز للعلم",
        "جمع كارل ساغان بين البحث الفلكي والتواصل العلمي، وأسهم في دراسة الكواكب ودعم استكشاف الفضاء، واشتهر بقدرته على تقديم العلم لجمهور واسع."
    ),
    "Stephen Hawking": (
        "فيزيائي بريطاني اشتهر بأبحاث الثقوب السوداء",
        "قدم ستيفن هوكينغ إسهامات مؤثرة في الفيزياء النظرية، ولا سيما في دراسة الثقوب السوداء وإشعاعها، كما أصبح من أشهر المفسرين العلميين في عصره."
    ),
    "Ahmed Zewail": (
        "كيميائي مصري أمريكي رائد في كيمياء الفيمتو",
        "أسس أحمد زويل مجال كيمياء الفيمتو باستخدام نبضات الليزر فائقة السرعة لرصد التفاعلات الكيميائية على مقياس زمني بالغ القصر، وحصل على نوبل في الكيمياء عام 1999."
    ),
}


def rebuild_js(data: dict) -> None:
    JS_PATH.parent.mkdir(parents=True, exist_ok=True)
    JS_PATH.write_text(
        "window.PERSON_I18N = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"person_i18n_before_batch17_ar_scientists_{stamp}.json"
    shutil.copy2(JSON_PATH, backup)

    changes = 0
    missing: list[str] = []

    for name, (hint, significance) in CONTENT.items():
        person = people.get(name)
        if person is None:
            missing.append(name)
            continue

        ar = person.get("languages", {}).get("ar")
        if not isinstance(ar, dict):
            missing.append(f"{name} [ar]")
            continue

        if ar.get("hint") == TARGET_HINT:
            ar["hint"] = hint
            changes += 1

        if ar.get("historical_significance") == TARGET_SIG:
            ar["historical_significance"] = significance
            changes += 1

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rebuild_js(data)

    prefix = "window.PERSON_I18N = "
    js_text = JS_PATH.read_text(encoding="utf-8")
    if not js_text.startswith(prefix):
        raise RuntimeError("Invalid generated JS prefix.")
    js_data = json.loads(js_text[len(prefix):].rstrip().rstrip(";").strip())
    if js_data != data:
        raise RuntimeError("JSON↔JS semantic equality failed.")

    print(f"Batch 17 Arabic scientists: {changes} field changes.")
    print(f"Backup JSON: {backup}")
    if missing:
        print("Missing records:")
        for item in missing:
            print(f"  - {item}")
    print("JSON↔JS semantic equality: PASS")


if __name__ == "__main__":
    main()
