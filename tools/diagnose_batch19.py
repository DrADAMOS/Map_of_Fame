import json
from collections import Counter

P = 'app/src/main/assets/person_i18n.json'

TARGETS = {
    'AR_WRITER_ACH': ('ar', 'achievements', '\\u062d\\u0642\\u0642\\u062a \\u0623\\u062b\\u0631\\u0627\\u064b \\u0643\\u0628\\u064a\\u0631\\u0627\\u064b \\u0648\\u0625\\u0646\\u062c\\u0627\\u0632\\u0627\\u062a \\u062a\\u0627\\u0631\\u064a\\u062e\\u064a\\u0629 \\u0643\\u0640 \\u0623\\u062f\\u064a\\u0628'),
    'PT_WRITER_SIG': ('pt', 'historical_significance', 'Lembrado por moldar desenvolvimentos hist\\u00f3ricos como escritor.'),
    'PT_MUSICIAN_SIG': ('pt', 'historical_significance', 'Lembrado por moldar desenvolvimentos hist\\u00f3ricos como m\\u00fasico.'),
    'TR_WRITER_SIG': ('tr', 'historical_significance', 'Yazar olarak tarihsel geli\\u015fmelere y\\u00f6n vermesiyle hat\\u0131rlanmaktad\\u0131r.'),
    'JA_WRITER_SIG': ('ja', 'historical_significance', '\\u4f5c\\u5bb6\\u3068\\u3057\\u3066\\u306e\\u6b74\\u53f2\\u7684\\u767a\\u5c55\\u306b\\u5927\\u304d\\u304f\\u8ca2\\u732e\\u3057\\u305f\\u4eba\\u7269\\u3068\\u3057\\u3066\\u8a18\\u61b6\\u3055\\u308c\\u3066\\u3044\\u308b\\u3002'),
}

with open(P, encoding='utf-8') as f:
    data = json.load(f)

for label, (lang, field, target) in TARGETS.items():
    target = target.encode().decode('unicode_escape')
    matches = []
    for name, person in data['people'].items():
        value = person.get('languages', {}).get(lang, {}).get(field)
        if value == target:
            matches.append(name)

    print()
    print('=' * 90)
    print(label)
    print('LANG =', lang, 'FIELD =', field)
    print('COUNT =', len(matches))
    for name in matches:
        print('  -', name)
