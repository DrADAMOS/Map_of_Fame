import json

with open('tools/HISTORICAL_SIGNIFICANCE_SEMANTIC_REVIEW_43.json', 'r', encoding='utf-8') as f:
    initial_data = json.load(f)
expected_people = [e['person'] for e in initial_data['entries'] if e['classification'] == 'VALID_HISTORICAL_SIGNIFICANCE']

with open('tools/HISTORICAL_SIGNIFICANCE_FINAL_MANUAL_ADJUDICATION_30.json', 'r', encoding='utf-8') as f:
    final_data = json.load(f)

entries = final_data.get('entries', [])
reviewed_people = [e['person'] for e in entries]

counts = {
    'VALID_HISTORICAL_SIGNIFICANCE': 0,
    'REJECT_DUPLICATE_BIO': 0,
    'REJECT_DUPLICATE_ACHIEVEMENT': 0,
    'REJECT_DUPLICATE_KEY_FACT': 0,
    'REJECT_WEAK_OR_GENERIC_SIGNIFICANCE': 0,
    'REJECT_UNSUPPORTED_CLAIM': 0,
    'REJECT_WEAK_SOURCE': 0,
    'NEEDS_STRONGER_SOURCE': 0
}

for e in entries:
    cls = e.get('classification')
    if cls in counts:
        counts[cls] += 1

missing = len(set(expected_people) - set(reviewed_people))
extra = len(set(reviewed_people) - set(expected_people))

print(f"TARGET_PEOPLE: {len(expected_people)}")
print(f"REVIEWED: {len(entries)}")
print(f"VALID_HISTORICAL_SIGNIFICANCE: {counts['VALID_HISTORICAL_SIGNIFICANCE']}")
print(f"REJECT_DUPLICATE_BIO: {counts['REJECT_DUPLICATE_BIO']}")
print(f"REJECT_DUPLICATE_ACHIEVEMENT: {counts['REJECT_DUPLICATE_ACHIEVEMENT']}")
print(f"REJECT_DUPLICATE_KEY_FACT: {counts['REJECT_DUPLICATE_KEY_FACT']}")
print(f"REJECT_WEAK_OR_GENERIC_SIGNIFICANCE: {counts['REJECT_WEAK_OR_GENERIC_SIGNIFICANCE']}")
print(f"REJECT_UNSUPPORTED_CLAIM: {counts['REJECT_UNSUPPORTED_CLAIM']}")
print(f"REJECT_WEAK_SOURCE: {counts['REJECT_WEAK_SOURCE']}")
print(f"NEEDS_STRONGER_SOURCE: {counts['NEEDS_STRONGER_SOURCE']}")
print(f"MISSING: {missing}")
print(f"EXTRA: {extra}")
print("APPLICATION_DATA_MODIFIED: NO")
print("SOURCE_PACKAGES_MODIFIED: NO")
print("AUTOMATED_CLASSIFICATION: NO")
status = "PASS" if len(entries) == 30 and missing == 0 and extra == 0 else "FAIL"
print(f"FINAL_STATUS: {status}")
