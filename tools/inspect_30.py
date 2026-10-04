import json

with open('tools/HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.json', 'r', encoding='utf-8') as f:
    sr43 = json.load(f)

with open('tools/HISTORICAL_SIGNIFICANCE_DRAFT_43.json', 'r', encoding='utf-8') as f:
    draft43 = json.load(f)

with open('app/src/main/assets/person_i18n.json', 'r', encoding='utf-8') as f:
    i18n = json.load(f)

people_dict = i18n.get('people', {})
draft_map = {e['person']: e for e in draft43['entries']}
sr_map = {e['person']: e for e in sr43['entries']}

valid_30 = [e['person'] for e in sr43['entries'] if e['classification'] == 'VALID_HISTORICAL_SIGNIFICANCE']

for p in valid_30:
    d = draft_map.get(p, {})
    s = sr_map.get(p, {})
    pdata = people_dict.get(p, {}).get('languages', {}).get('en', {})
    print(f"*** {p} ***")
    print(f"  Proposed: {d.get('proposed_text')}")
    print(f"  Bio:      {pdata.get('bio')}")
    print(f"  Ach:      {pdata.get('achievements')}")
    print(f"  KeyFacts: {pdata.get('key_facts')}")
    print(f"  Passage:  {s.get('source_passage')}")
    print("-" * 60)
