import json

def load_pkg(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f).get('entries', [])

e43 = load_pkg('tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json')
e5 = load_pkg('tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json')
e3 = load_pkg('tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_3_REPAIR.json')

all_sources = {}
for e in e43 + e5 + e3:
    p = e['person']
    if p not in all_sources:
        all_sources[p] = []
    all_sources[p].append(e)

with open('tools/DUPLICATE_FIELD_ADJUDICATION_FINAL_43.json', 'r', encoding='utf-8') as f:
    adjudication = json.load(f)

people = [c['person'] for c in adjudication['clusters']]

for p in people:
    sources = all_sources.get(p, [])
    print(f"=== {p} ===")
    for s in sources:
        print(f"  [{s.get('source_title')}] ({s.get('source_section')}): {s.get('exact_source_passage')}")
