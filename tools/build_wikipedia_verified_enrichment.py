#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,time,sys
from pathlib import Path
from urllib.parse import quote,urljoin
import requests
from bs4 import BeautifulSoup

LANGS=['ar','en','es','fr','de','pt','it','tr','ru','ja','ko','zh','hi','id','fa']
ROOT=Path(__file__).resolve().parents[1]; ASSETS=ROOT/'app'/'src'/'main'/'assets'; QUIZ=ASSETS/'quiz_data.json'; OUT=ASSETS/'person_i18n.json'
CACHE=ROOT/'.wikipedia_cache'; CACHE.mkdir(exist_ok=True); STATE=ROOT/'WIKIPEDIA_ENRICHMENT_STATE.json'; REVIEW=ROOT/'WIKIPEDIA_IDENTITY_REVIEW.json'; AUDIT=ROOT/'WIKIPEDIA_ENRICHMENT_AUDIT.json'
UA='MapOfFame/1.0 (offline historical-data build; contact project maintainer)'
TIMEOUT=30
S=requests.Session(); S.headers.update({'User-Agent':UA,'Accept-Language':'en'})

def clean(x): return re.sub(r'\s+',' ',str(x or '')).strip()
def norm(x): return re.sub(r'[^\w\s]',' ',clean(x).casefold()).strip()
def parse_year(x):
    if isinstance(x,int): return x
    m=re.search(r'-?\d{1,4}',clean(x)); return int(m.group()) if m else None

def cache_key(url): return CACHE/(re.sub(r'[^A-Za-z0-9_.-]','_',url)+'.html')
def get(url,delay=1.0):
    p=cache_key(url)
    if p.exists(): return p.read_text(encoding='utf8')
    for attempt in range(7):
        try:
            r=S.get(url,timeout=TIMEOUT)
            if r.status_code==429:
                wait=int(r.headers.get('Retry-After','0') or 0) or min(60,5*(attempt+1)); time.sleep(wait); continue
            r.raise_for_status(); p.write_text(r.text,encoding='utf8'); time.sleep(delay); return r.text
        except requests.RequestException:
            if attempt==6: raise
            time.sleep(min(60,2**attempt))
    raise RuntimeError(url)

def page(title,lang='en',delay=1.0):
    url=f'https://{lang}.wikipedia.org/wiki/{quote(title.replace(" ","_"),safe="()!,'-:,")}'; html=get(url,delay); soup=BeautifulSoup(html,'html.parser'); h1=soup.find('h1');
    if not h1: return None
    lead=[]
    content=soup.select_one('.mw-parser-output')
    if content:
        for p in content.find_all('p',recursive=False):
            t=clean(p.get_text(' ',strip=True))
            if len(t)>=40: lead.append(t)
            if len(lead)>=8: break
    alts={}
    for link in soup.find_all('link',rel='alternate'):
        langcode=link.get('hreflang'); href=link.get('href')
        if langcode in LANGS and href: alts[langcode]=href
    return {'title':clean(h1.get_text(' ',strip=True)),'url':url,'lead':lead,'langs':alts}

def search(name,delay=1.0):
    url='https://en.wikipedia.org/w/index.php?search='+quote(name)
    html=get(url,delay); soup=BeautifulSoup(html,'html.parser'); out=[]
    for a in soup.select('.mw-search-result-heading a')[:8]:
        href=a.get('href',''); title=clean(a.get_text(' ',strip=True))
        if href.startswith('/wiki/') and title: out.append((title,urljoin('https://en.wikipedia.org',href)))
    return out

def score(person,p):
    name=clean(person.get('name_en') or person.get('name')); title=p['title']; s=0
    if norm(name)==norm(title): s+=70
    elif norm(name) in norm(title) or norm(title) in norm(name): s+=40
    else: s+=min(25,10*len(set(norm(name).split())&set(norm(title).split())))
    text=' '.join(p['lead']).casefold(); by=parse_year(person.get('by') or person.get('birth_date')); dy=parse_year(person.get('dy') or person.get('death_date'))
    if by is not None and str(abs(by)) in text: s+=10
    if dy is not None and str(abs(dy)) in text: s+=10
    for k in ('birth_city_en','death_city_en'):
        v=clean(person.get(k));
        if v and norm(v) in norm(text): s+=6
    return s

def resolve(person,delay):
    name=clean(person.get('name_en') or person.get('name')); candidates=[]
    # Try deterministic title first; this avoids search ambiguity for exact Wikipedia titles.
    guesses=[name]
    special={
        'Buddha':'The Buddha',
        'Hannibal Barca':'Hannibal',
        'Attila the Hun':'Attila',
        'Thabit ibn Qurra':'Thābit ibn Qurra',
        'Tughril Beg':'Tughril I',
        'Al-Idrisi':'Muhammad al-Idrisi',
        'Nur ad-Din':'Nur al-Din',
        'Richard the Lionheart':'Richard I of England',
        'Louis IX':'Louis IX of France',
        'Isabella I':'Isabella I of Castile',
        'Shah Abbas I':'Abbas the Great',
        'Mozart':'Wolfgang Amadeus Mozart',
        'Muhammad Ali Pasha':'Muhammad Ali of Egypt',
        'Beethoven':'Ludwig van Beethoven',
        'Pyotr Tchaikovsky':'Pyotr Ilyich Tchaikovsky',
        'Horatio Kitchener':'Herbert Kitchener, 1st Earl Kitchener',
        'King Abdulaziz':'Ibn Saud',
        'King Faisal I':'Faisal I',
        'Abbas al-Aqqad':'Abbas Mahmoud al-Aqqad',
        'Martin Luther King':'Martin Luther King Jr.',
        'Frederick II':'Frederick II, Holy Roman Emperor',
        'Henry V':'Henry V of England',
        'Tariq ibn Ziyad':'Tariq ibn Ziyad'
    }
    if name in special: guesses.insert(0,special[name])
    seen=set()
    for t in guesses:
        if t in seen: continue
        seen.add(t); p=page(t,'en',delay)
        if p:
            candidates.append(p)
    if not candidates:
        for _,u in search(name,delay):
            title=u.split('/wiki/',1)[-1].replace('_',' ')
            p=page(title,'en',delay)
            if p: candidates.append(p)
    scored=sorted(((score(person,p),p) for p in candidates),key=lambda x:x[0],reverse=True)
    if not scored: return None,{'status':'not_found','candidates':[]}
    best=scored[0]; second=scored[1][0] if len(scored)>1 else -1
    explicit = name in special
    # An explicit project mapping is accepted only if the requested article exists.
    # This avoids rejecting known aliases merely because the display name differs.
    if explicit and best[1]['title'] == special[name]:
        return best[1],{'status':'verified','title':best[1]['title'],'score':best[0],'match':'explicit_mapping'}
    ok=best[0]>=60 and best[0]-second>=12
    return (best[1],{'status':'verified','title':best[1]['title'],'score':best[0],'match':'scored'}) if ok else (None,{'status':'ambiguous','best':best[1]['title'],'score':best[0],'candidates':[{'title':p['title'],'score':s} for s,p in scored[:5]]})

def make_content(person,lang,p):
    lead=p['lead']; bio=' '.join(lead[:4]).strip(); facts=lead[:5]; ach=[x for x in lead if re.search(r'\b(founded|invented|discovered|developed|wrote|published|created|built|reformed|established|composed|painted|led|conquered|ruled|served|formulated|was|became)\b',x,re.I)][:4]
    if not ach: ach=lead[1:4]
    events=[x for x in lead if re.search(r'\b(war|battle|campaign|invasion|revolt|rebellion|siege|revolution|uprising)\b',x,re.I)][:4]
    qlang=person.get('name') if lang!='en' else person.get('name_en') or person.get('name')
    return {'name':clean(qlang),'hint':clean(lead[0])[:180] if lead else '','bio':bio,'birth_city':clean(person.get('birth_city_ar' if lang=='ar' else 'birth_city')),'birth_country':clean(person.get('birth_country_ar' if lang=='ar' else 'birth_country')),'death_city':clean(person.get('death_city_ar' if lang=='ar' else 'death_city')),'death_country':clean(person.get('death_country_ar' if lang=='ar' else 'death_country')),'role':clean(person.get('role_ar' if lang=='ar' else 'role_en' if lang=='en' else '')),'era':clean(person.get('era_en' if lang=='en' else 'era')),'achievements':ach,'key_facts':facts,'wars':events,'historical_significance':clean(lead[-1] if lead else ''),'source':{'type':'wikipedia','language':lang,'title':p['title'],'url':p['url']}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--delay',type=float,default=1.2); ap.add_argument('--limit',type=int,default=0); ap.add_argument('--review-only',action='store_true'); ap.add_argument('--recheck-unresolved',action='store_true'); args=ap.parse_args()
    people=json.loads(QUIZ.read_text(encoding='utf8')); people=people[:args.limit] if args.limit else people
    state=json.loads(STATE.read_text(encoding='utf8')) if STATE.exists() else {'schema':2,'completed':{},'output':{}}
    review=json.loads(REVIEW.read_text(encoding='utf8')) if REVIEW.exists() else {'schema':2,'people':{},'unresolved':[]}
    output=state.get('output') or {'schema':5,'languages':LANGS,'policy':'source-backed-no-placeholder-no-cross-language-fallback','people':{}}
    for i,person in enumerate(people,1):
        name=clean(person.get('name_en') or person.get('name'))
        if name in state['completed'] and (state['completed'][name] or not args.recheck_unresolved):
            print(f'[{i}/{len(people)}] CACHED: {name}'); continue
        p,res=resolve(person,args.delay); review['people'][name]=res
        if not p:
            if name not in review['unresolved']: review['unresolved'].append(name)
            state['completed'][name]=False; print(f'[{i}/{len(people)}] REVIEW REQUIRED: {name}')
        else:
            if args.review_only:
                state['completed'][name]=True
                print(f'[{i}/{len(people)}] VERIFIED: {name} -> {p["title"]}')
            else:
                titles=p['langs']; titles['en']=p['url']
                langs={}
                for lang in LANGS:
                    if lang=='en': lp=p
                    else:
                        href=titles.get(lang,'')
                        if not href: langs[lang]=None; continue
                        lp=page(href.rsplit('/wiki/',1)[-1],lang,args.delay) if '/wiki/' in href else None
                    langs[lang]=make_content(person,lang,lp) if lp else None
                output['people'][name]={'languages':langs}; state['completed'][name]=True; print(f'[{i}/{len(people)}] VERIFIED: {name} -> {p["title"]}')
        STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf8'); REVIEW.write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf8')
    verified_titles={}
    for n,r in review['people'].items():
        if r.get('status')=='verified':
            verified_titles.setdefault(r.get('title'),[]).append(n)
    duplicate_identities={k:v for k,v in verified_titles.items() if len(v)>1}
    AUDIT.write_text(json.dumps({'schema':3,'people_processed':len(people),'verified':sum(1 for v in state['completed'].values() if v),'unresolved':review['unresolved'],'duplicate_wikipedia_identities':duplicate_identities},ensure_ascii=False,indent=2),encoding='utf8')
    if args.review_only: return 0 if not review['unresolved'] else 2
    if review['unresolved']: print('STOP: unresolved identities remain; output not replaced.',file=sys.stderr); return 2
    OUT.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf8'); print(f'Wrote {OUT}'); return 0
if __name__=='__main__': raise SystemExit(main())
