from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"

TARGET_HINT = "من أبرز شخصيات العصر الحديث في مجال فنان"
TARGET_SIG = "تركت أثراً تاريخياً كـ فنان في عصر العصر الحديث."

# Person-specific Arabic content. Only the exact generic Arabic values above
# are replaced; existing person-specific content is preserved.
CONTENT = {
    "Francisco Goya": (
        "رسام إسباني رائد في الانتقال إلى الفن الحديث",
        "يُعد غويا من أهم الرسامين الإسبان، وقد وثّق في أعماله أهوال الحرب والمجتمع الإسباني، ومهّد بأسلوبه الجريء لبعض اتجاهات الفن الحديث."
    ),
    "Eugène Delacroix": (
        "رائد الرومانسية في الرسم الفرنسي",
        "كان ديلاكروا أبرز وجوه الرومانسية الفرنسية، واشتهر بالتكوينات الدرامية والألوان القوية، وأثر في أجيال لاحقة من الرسامين، ومنهم الانطباعيون."
    ),
    "Claude Monet": (
        "رائد الانطباعية الفرنسية",
        "كان مونيه أحد مؤسسي الانطباعية، وطوّر أسلوباً يعتمد على دراسة الضوء واللون واللحظة العابرة، كما أصبحت سلسلتا زنابق الماء وكاتدرائية روان من أشهر أعماله."
    ),
    "Henri Rousseau": (
        "رسام فرنسي عصامي اشتهر بمشاهد الغابات",
        "اشتهر هنري روسو بلوحاته ذات الغابات والنباتات والحيوانات المتخيلة، وأصبح أسلوبه البسيط والمميز مؤثراً في الفن الحديث رغم أنه كان عصامياً خارج الأوساط الأكاديمية."
    ),
    "Paul Gauguin": (
        "رائد ما بعد الانطباعية والفن الرمزي",
        "طوّر غوغان أسلوباً يعتمد على الألوان المسطحة والأشكال المبسطة والرمزية، وارتبطت أعماله في بريتاني وتاهيتي بتحول مهم في مسار الفن الحديث."
    ),
    "Vincent van Gogh": (
        "رسام هولندي رائد في ما بعد الانطباعية",
        "أحدث فان غوخ أثراً كبيراً في الفن الحديث من خلال ضربات الفرشاة التعبيرية والألوان القوية، ومن أشهر أعماله ليلة النجوم وعباد الشمس وسلسلة بورتريهاته الذاتية."
    ),
    "Alphonse Mucha": (
        "رائد الفن الزخرفي وفن الآرت نوفو",
        "أصبح ألفونس موخا من أبرز رموز الآرت نوفو، واشتهر بملصقاته ورسوماته الزخرفية ذات الخطوط المنحنية والشخصيات الأنثوية، كما ترك أثراً واسعاً في التصميم الغرافيكي."
    ),
    "Edvard Munch": (
        "رسام نرويجي رائد في التعبيرية",
        "استكشف مونك في أعماله القلق والحب والموت والوحدة، وأصبحت لوحة الصرخة من أشهر رموز الفن الحديث وأكثرها ارتباطاً بالتعبيرية."
    ),
    "Wassily Kandinsky": (
        "رائد الفن التجريدي الحديث",
        "كان كاندينسكي من رواد التجريد، وطوّر لوحات تعتمد على اللون والخط والشكل بوصفها عناصر مستقلة نسبياً عن التمثيل الواقعي، كما درّس في مدرسة باوهاوس."
    ),
    "Henri Matisse": (
        "رائد الوحشية وأحد كبار رسامي القرن العشرين",
        "كان ماتيس من أبرز قادة الوحشية، واشتهر باستخدام الألوان الصريحة والأشكال المبسطة، وأسهم في توسيع إمكانات الرسم الحديث والتصميم الورقي."
    ),
    "Kazimir Malevich": (
        "مؤسس المدرسة التفوقية في الفن",
        "أسس ماليفيتش التفوقية ودفع التجريد إلى أشكال هندسية شديدة الاختزال، وتُعد لوحة المربع الأسود من أبرز أعماله وأكثرها تأثيراً في تاريخ الفن الطليعي."
    ),
    "Pablo Picasso": (
        "شريك مؤسس التكعيبية وأحد أبرز فناني القرن العشرين",
        "شارك بيكاسو في تأسيس التكعيبية وغيّر أساليب تمثيل الشكل والفضاء في الفن الحديث، ومن أعماله المحورية غيرنيكا وآنسات أفينيون."
    ),
    "Amedeo Modigliani": (
        "رسام إيطالي اشتهر بالصور ذات الوجوه والأعناق الممدودة",
        "اشتهر موديلياني بصوره الشخصية والعارية ذات الوجوه والأعناق الممدودة، وأصبح أسلوبه المميز جزءاً بارزاً من المشهد الفني في باريس خلال بدايات القرن العشرين."
    ),
    "Marc Chagall": (
        "رسام حداثي مزج الذاكرة والخيال والرمزية",
        "طوّر شاغال لغة بصرية تجمع بين الذكريات اليهودية والريفية والرموز والأحلام، وامتد إنتاجه بين الرسم والطباعة وتصميم الزجاج الملون والمسرح."
    ),
    "Joan Miró": (
        "فنان إسباني رائد في السريالية والتجريد",
        "طوّر ميرو أسلوباً شخصياً يجمع الأشكال العضوية والرموز والألوان الصافية، وكان من الفنانين المؤثرين في السريالية والفن التجريدي خلال القرن العشرين."
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
    backup = BACKUP_DIR / f"person_i18n_before_batch16_ar_artists_{stamp}.json"
    shutil.copy2(JSON_PATH, backup)

    changes = 0
    missing = []

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

    print(f"Batch 16 Arabic artists: {changes} field changes.")
    print(f"Backup JSON: {backup}")
    if missing:
        print("Missing records:")
        for item in missing:
            print(f"  - {item}")
    print("JSON↔JS semantic equality: PASS")


if __name__ == "__main__":
    main()
