from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'app/src/main/assets/person_i18n.json'; J=ROOT/'app/src/main/assets/js/person_i18n.js'
GEN=re.compile(r'notable historical work|a notable historical figure|remembered for shaping historical developments|notable figure in|من أبرز شخصيات العصر الحديث|تركت أثراً تاريخياً|حققت أثراً كبيراً وإنجازات تاريخية|تعد حلقة بارزة في عصر العصر الحديث',re.I)
SIG={
'ar':'تظهر أهميته التاريخية بوضوح في أن {fact}.','en':'His historical significance is evident in the fact that {fact}.','es':'Su importancia histórica se refleja en el hecho de que {fact}.','fr':'Son importance historique se reflète notamment par le fait que {fact}.','de':'Seine historische Bedeutung zeigt sich insbesondere darin, dass {fact}.','pt':'A sua importância histórica é evidente no facto de que {fact}.','it':'La sua importanza storica emerge dal fatto che {fact}.','tr':'Tarihsel önemi, {fact} gerçeğinde açıkça görülür.','ru':'Его историческое значение особенно заметно в том, что {fact}.','ja':'歴史的な意義は、{fact}という点に表れています。','zh':'其历史意义尤其体现在{fact}。','hi':'उनका ऐतिहासिक महत्व इस तथ्य में स्पष्ट होता है कि {fact}।','id':'Makna historisnya terlihat jelas dari kenyataan bahwa {fact}.','fa':'اهمیت تاریخی او به‌ویژه در این واقعیت آشکار است که {fact}.'}
HINT={'ar':'يُعرف خصوصاً بـ {fact}.','en':'Best known for {fact}.','es':'Es especialmente conocido por {fact}.','fr':'Il est notamment connu pour {fact}.','de':'Besonders bekannt ist er für {fact}.','pt':'É especialmente conhecido por {fact}.','it':'È particolarmente noto per {fact}.','tr':'Özellikle {fact} ile tanınır.','ru':'Особенно известен тем, что {fact}.','ja':'特に{fact}で知られています。','zh':'尤其因{fact}而知名。','hi':'वे विशेष रूप से {fact} के लिए जाने जाते हैं।','id':'Ia terutama dikenal karena {fact}.','fa':'او به‌ویژه به دلیل {fact} شناخته می‌شود.'}

def norm(v):
 if isinstance(v,list): return ' || '.join(norm(x) for x in v)
 return re.sub(r'\s+',' ',str(v or '')).strip().casefold()
def fact_items(loc):
 out=[]
 for src in ('achievements','key_facts','bio'):
  v=loc.get(src); items=v if isinstance(v,list) else [v]
  for x in items:
   s=re.sub(r'\s+',' ',str(x or '')).strip().rstrip('.。！？')
   if s and not GEN.search(s) and norm(s) not in {norm(y) for y in out}:
    out.append(s)
 return out

def rebuild(loc,lang,target,avoid):
 facts=fact_items(loc)
 if target=='key_facts':
  # Use concise source facts without templated wrapper; prefer items not equal to achievements.
  ach={norm(x) for x in (loc.get('achievements') if isinstance(loc.get('achievements'),list) else [loc.get('achievements')])}
  chosen=[x for x in facts if norm(x) not in ach and norm(x) not in avoid][:3]
  if not chosen: chosen=[x for x in facts if norm(x) not in avoid][:3]
  return chosen
 fact=next((x for x in facts if norm(x) not in avoid), facts[0] if facts else str(loc.get('name') or 'this person'))
 return (SIG if target=='historical_significance' else HINT).get(lang,SIG['en']).format(fact=fact)

def main():
 d=json.loads(P.read_text(encoding='utf8')); changes=0
 fields=['hint','bio','achievements','key_facts','historical_significance']
 for person,r in d['people'].items():
  for lang,loc in r['languages'].items():
   # Fix all generic values first.
   for f in fields:
    if GEN.search(norm(loc.get(f))):
     old=norm(loc.get(f)); loc[f]=rebuild(loc,lang,'key_facts' if f=='key_facts' else f,{norm(loc.get(x)) for x in fields if x!=f}); changes += norm(loc.get(f))!=old
   # Resolve exact duplicate pairs iteratively, preserving bio/achievements where possible.
   for _ in range(8):
    vals={f:norm(loc.get(f)) for f in fields}; pair=None
    for i,a in enumerate(fields):
     for b in fields[i+1:]:
      if vals[a] and vals[a]==vals[b]: pair=(a,b); break
     if pair: break
    if not pair: break
    a,b=pair
    target='historical_significance' if 'historical_significance' in pair else 'key_facts' if 'key_facts' in pair else 'hint'
    new=rebuild(loc,lang,target,{norm(loc.get(x)) for x in fields if x!=target})
    if norm(new)==norm(loc.get(target)):
     # deterministic fallback: use a different concrete fact and mark the field semantically.
     facts=fact_items(loc); alt=next((x for x in facts if norm(x) not in {norm(loc.get(f)) for f in fields}), None)
     if alt:
      new=(SIG if target=='historical_significance' else HINT).get(lang,SIG['en']).format(fact=alt)
    if norm(new)!=norm(loc.get(target)):
     loc[target]=new; changes+=1
    else: break
 P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); J.write_text('window.PERSON_I18N = '+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
 print('REFINED_CHANGES',changes)
main()
