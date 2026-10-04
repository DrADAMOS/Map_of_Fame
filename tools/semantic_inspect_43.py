import json

with open('tools/HISTORICAL_SIGNIFICANCE_DRAFT_43.json', 'r', encoding='utf-8') as f:
    draft = json.load(f)

with open('app/src/main/assets/person_i18n.json', 'r', encoding='utf-8') as f:
    i18n = json.load(f)

def load_pkg(path):
    if not Path(path).exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f).get('entries', [])

from pathlib import Path
all_sources = load_pkg('tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_43.json') + \
              load_pkg('tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_5_REPAIR.json') + \
              load_pkg('tools/HISTORICAL_SIGNIFICANCE_SOURCE_PACKAGE_3_REPAIR.json')

source_map = {}
for s in all_sources:
    p = s['person']
    if p not in source_map:
        source_map[p] = []
    source_map[p].append(s)

people_dict = i18n.get('people', {})

for entry in draft['entries']:
    p = entry['person']
    prop = entry['proposed_text']
    pdata = people_dict.get(p, {}).get('languages', {}).get('en', {})
    bio = pdata.get('bio', '')
    ach = pdata.get('achievements', [])
    kf = pdata.get('key_facts', [])
    sources = source_map.get(p, [])
    
    print(f"=== {p} ===")
    print(f"  Proposed: {prop}")
    print(f"  Bio:      {bio}")
    print(f"  Ach:      {ach}")
    print(f"  KeyFacts: {kf}")
    print(f"  Sources:  {len(sources)} records")
    for s in sources:
        print(f"    [{s.get('source_title')} / {s.get('source_section')}]: {s.get('exact_source_passage')[:150]}...")
    print()
