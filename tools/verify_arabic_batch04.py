from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"app/src/main/assets/person_i18n.json"
SRC=ROOT/"tools/canonical/arabic_batch04_source.json"
def main():
    d=json.loads(DATA.read_text(encoding="utf-8"))
    s=json.loads(SRC.read_text(encoding="utf-8"))["people"]
    print(f"Verified actual project keys: {len(s)}")
    for k in s:
        if k not in d["people"]:
            raise SystemExit(f"Missing person: {k}")
        print(f"  OK: {k}")
    print("NO DATA MODIFIED.")
    print("This batch is the exact-key source for the next Arabic content repair.")
if __name__=="__main__":
    main()
