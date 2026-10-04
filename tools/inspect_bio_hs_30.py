import json

with open('tools/REMAINING_DUPLICATE_FIELDS_INVENTORY.json', 'r', encoding='utf-8') as f:
    inv = json.load(f)

pairs = [p for p in inv['duplicate_pairs'] if {p['field_a'], p['field_b']} == {'bio', 'historical_significance'}]
by_person = {}
for p in pairs:
    pid = p['person']
    if pid not in by_person:
        by_person[pid] = {'languages': [], 'text': p['exact_text']}
    by_person[pid]['languages'].append(p['language'])

print("Total people:", len(by_person))
print("Total records:", len(pairs))
for pid, d in sorted(by_person.items()):
    print(f"- {pid} ({len(d['languages'])} langs): {d['languages']}")
    print(f"  Text: {d['text'][:120]}...")
