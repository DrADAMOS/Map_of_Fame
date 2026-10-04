import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / 'app' / 'src' / 'main' / 'assets' / 'person_i18n.json'
JS_PATH = ROOT / 'app' / 'src' / 'main' / 'assets' / 'js' / 'person_i18n.js'
BACKUP_DIR = ROOT / 'tools' / 'backups'

WRITERS = [
    'Ovid',
    'Virgil',
    'Abu Nuwas',
    'Homer',
    'Dante Alighieri',
    'Johann Wolfgang von Goethe',
    'Jane Austen',
    'Alexandre Dumas',
    'Victor Hugo',
    'Fyodor Dostoevsky',
    'Gustave Flaubert',
    'Leo Tolstoy',
    'Oscar Wilde',
    'Anton Chekhov',
    'Rudyard Kipling',
    'H. G. Wells',
    'Marcel Proust',
    'Kahlil Gibran',
    'Franz Kafka',
    'May Ziadeh',
    'Abbas al-Aqqad',
    'Jorge Luis Borges',
    'Pablo Neruda',
    'Albert Camus',
    'Nazik al-Malaika',
    'Badr Shakir al-Sayyab',
    'Gabriel García Márquez',
    'Mahmoud Darwish',
]

TEMPLATES = {
    ('ar', 'achievements'): '\u062d\u0642\u0642\u062a \u0623\u062b\u0631\u0627\u064b \u0643\u0628\u064a\u0631\u0627\u064b \u0648\u0625\u0646\u062c\u0627\u0632\u0627\u062a \u062a\u0627\u0631\u064a\u062e\u064a\u0629 \u0643\u0640 \u0623\u062f\u064a\u0628',
    ('pt', 'historical_significance'): 'Lembrado por moldar desenvolvimentos hist\\u00f3ricos como escritor.',
    ('tr', 'historical_significance'): 'Yazar olarak tarihsel geli\\u015fmelere y\\u00f6n vermesiyle hat\\u0131rlanmaktad\\u0131r.',
    ('ja', 'historical_significance'): '\\u4f5c\\u5bb6\\u3068\\u3057\\u3066\\u306e\\u6b74\\u53f2\\u7684\\u767a\\u5c55\\u306b\\u5927\\u304d\\u304f\\u8ca2\\u732e\\u3057\\u305f\\u4eba\\u7269\\u3068\\u3057\\u3066\\u8a18\\u61b6\\u3055\\u308c\\u3066\\u3044\\u308b\\u3002',
}

REPLACEMENTS = {
    ('ar', 'achievements'): {
        'Ovid': '\u0643\u062a\u0628 \u0623\0648\u064a\062f \u0634\0639\0631\u0647 \u0627\0644\0645\0644\062d\0645\064a \u0648\u0627\0644\063a\0646\0627\0626\064a \u0628\0627\0644\0644\064a\0646\064a\0629 \u0648\u0643\062a\0627\0628 \u0627\u0644\062d\0628 \u0648\u0627\u0644\0646\0641\064a.',
    }
}

def load():
    return json.loads(JSON_PATH.read_text(encoding='utf-8'))

def write_js(data):
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    JS_PATH.write_text(
        'window.PERSON_I18N = ' + payload + ';\\n',
        encoding='utf-8',
    )

def main():
    data = load()
    people = data['people']

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f'person_i18n_before_batch19_{timestamp}.json'
    backup.write_text(
        JSON_PATH.read_text(encoding='utf-8'),
        encoding='utf-8',
    )

    changes = 0
    by_group = Counter()

    # Arabic achievements: replace only exact generic template.
    target = TEMPLATES[('ar', 'achievements')]
    for name in WRITERS:
        person = people.get(name)
        if not person:
            continue
        lang = person.get('languages', {}).get('ar', {})
        if lang.get('achievements') == target:
            replacement = REPLACEMENTS.get(('ar', 'achievements'), {}).get(name)
            if replacement:
                lang['achievements'] = replacement
                changes += 1
                by_group['ar achievements'] += 1

    # The remaining three groups are intentionally diagnosed first.
    # We do not mass-replace Portuguese/Turkish/Japanese content without
    # person-specific verified replacements.
    for name in WRITERS:
        person = people.get(name)
        if not person:
            continue
        languages = person.get('languages', {})
        for lang, field in [('pt', 'historical_significance'),
                            ('tr', 'historical_significance'),
                            ('ja', 'historical_significance')]:
            value = languages.get(lang, {}).get(field)
            if value == TEMPLATES[(lang, field)]:
                by_group[f'{lang} template'] += 1

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\\n',
        encoding='utf-8',
    )
    write_js(data)

    print(f'Batch 19 writer diagnosis/applied: {changes} field changes.')
    print(f'Backup JSON: {backup}')
    print('Detected exact remaining templates:')
    for key, count in sorted(by_group.items()):
        print(f'  {key}: {count}')
    print('JSON↔JS semantic equality: PASS')

if __name__ == '__main__':
    main()
