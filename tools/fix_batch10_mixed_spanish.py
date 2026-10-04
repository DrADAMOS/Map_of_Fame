from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"


FIXES = {
    "El Greco": {
        "es": {
            "historical_significance": (
                "Desarrolló en España un estilo reconocible por sus figuras "
                "alargadas, colores intensos y profunda espiritualidad, "
                "especialmente en sus obras de Toledo."
            )
        }
    },
    "Kazimir Malevich": {
        "es": {
            "historical_significance": (
                "Llevó la pintura hacia la abstracción geométrica con el "
                "suprematismo y convirtió la forma y el color básicos en "
                "protagonistas de la composición."
            )
        }
    },
}


def main() -> None:
    original = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(original)

    changed = 0

    for person_name, languages in FIXES.items():
        if person_name not in data["people"]:
            raise KeyError(f"Person not found: {person_name}")

        person = data["people"][person_name]

        for language, fields in languages.items():
            if language not in person["languages"]:
                raise KeyError(
                    f"Language '{language}' not found for {person_name}"
                )

            entry = person["languages"][language]

            for field, value in fields.items():
                if entry.get(field) != value:
                    entry[field] = value
                    changed += 1

    backup = JSON_PATH.with_name(
        "person_i18n.before_batch10_language_fix.json"
    )

    if not backup.exists():
        backup.write_text(original, encoding="utf-8")

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    js = (
        "const PERSON_I18N = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    )

    JS_PATH.write_text(js, encoding="utf-8")

    verify_json = json.loads(
        JSON_PATH.read_text(encoding="utf-8")
    )

    js_payload = (
        js.removeprefix("const PERSON_I18N = ")
        .removesuffix(";\n")
    )

    verify_js = json.loads(js_payload)

    if verify_json != verify_js:
        raise RuntimeError("JSON↔JS semantic equality failed")

    print(f"Batch 10 language correction: {changed} field changes.")
    print(f"Backup JSON: {backup}")
    print("JSON↔JS semantic equality: PASS")


if __name__ == "__main__":
    main()
