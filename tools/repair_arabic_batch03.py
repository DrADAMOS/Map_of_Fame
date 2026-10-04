from pathlib import Path
import json, shutil, sys
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/"app/src/main/assets/person_i18n.json"; JS=ROOT/"app/src/main/assets/js/person_i18n.js"; SRC=ROOT/"tools/canonical/arabic_batch03.json"; BACK=ROOT/"tools/backups"
def main():
 apply="--apply" in sys.argv; d=json.loads(DATA.read_text(encoding="utf-8")); c=json.loads(SRC.read_text(encoding="utf-8"))["people"]; changes=[]
 for k,fields in c.items():
  if k not in d["people"]: raise SystemExit(f"Missing person: {k}")
  ar=d["people"][k].get("languages",{}).get("ar")
  if not isinstance(ar,dict): raise SystemExit(f"Missing Arabic: {k}")
  for f,n in fields.items():
   if ar.get(f)!=n: changes.append((k,f,n))
 print(f"Mode: {'APPLY' if apply else 'DRY-RUN'}"); print(f"People: {len(c)} | Changes: {len(changes)}")
 for k,f,_ in changes: print(f"  UPDATE {k} [ar] {f}")
 if not apply:return 0
 stamp=datetime.now().strftime("%Y%m%d_%H%M%S"); BACK.mkdir(parents=True,exist_ok=True); shutil.copy2(DATA,BACK/f"arabic_batch03_{stamp}.json"); shutil.copy2(JS,BACK/f"arabic_batch03_{stamp}.js")
 for k,f,n in changes:d["people"][k]["languages"]["ar"][f]=n
 DATA.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); JS.write_text("window.PERSON_I18N = "+json.dumps(d,ensure_ascii=False,indent=2)+";\n",encoding="utf-8"); print("APPLIED")
if __name__=="__main__": raise SystemExit(main())
