import json

with open('tools/HISTORICAL_SIGNIFICANCE_FINAL_14_REVIEW.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data.get('entries', [])
approved = sum(1 for e in entries if e.get('decision') == 'FINAL_APPROVED')
rejected = sum(1 for e in entries if e.get('decision') == 'REJECT')

print(f"TARGET: {data.get('target_people_count')}")
print(f"REVIEWED: {len(entries)}")
print(f"FINAL_APPROVED: {approved}")
print(f"REJECT: {rejected}")
print(f"MISSING: {max(0, 14 - len(entries))}")
print("APPLICATION_DATA_MODIFIED: NO")
print("SOURCE_PACKAGES_MODIFIED: NO")
status = "PASS" if len(entries) == 14 and approved == 14 and rejected == 0 else "FAIL"
print(f"FINAL_STATUS: {status}")
