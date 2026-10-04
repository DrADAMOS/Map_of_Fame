from __future__ import annotations
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
JP=ROOT/'app/src/main/assets/person_i18n.json'
JSP=ROOT/'app/src/main/assets/js/person_i18n.js'

data=json.loads(JP.read_text(encoding='utf-8-sig'))
people=data['people']
changes=[]

def setv(person, field, value):
    old=people[person]['languages']['en'].get(field)
    if old != value:
        people[person]['languages']['en'][field]=value
        changes.append((person,field))

def strip_wiki_heading(v):
    if isinstance(v,str):
        return re.sub(r'^===\s*[^=]+?\s*===\.\s*','',v, count=1).strip()
    return v

# Remove copied Wikipedia section-heading artifacts while preserving the factual text.
for person in ['Saladin','Hannibal Barca','Marcus Aurelius','Michael Faraday','James Clerk Maxwell','Caravaggio','Bob Marley','Giuseppe Verdi','Gustav Mahler']:
    en=people[person]['languages']['en']
    for field in ['bio','historical_significance','achievements','key_facts']:
        if field in en:
            new=strip_wiki_heading(en[field])
            if new != en[field]:
                en[field]=new; changes.append((person,field))

# Replace achievement/key-fact copies with distinct, fact-based key facts.
setv('Frederick Barbarossa','key_facts',[
    'He was elected King of Germany in Frankfurt on 4 March 1152 and crowned in Aachen on 9 March 1152.',
    'He was crowned King of Italy in Pavia in 1155 and crowned Holy Roman Emperor in Rome that same year.'
])
setv('El Greco','key_facts',[
    'He moved to Toledo in 1577, where he established his mature career and received major religious commissions.',
    'He developed a distinctive style that combined Byzantine traditions with Venetian color and intense spiritual expression.'
])
setv('Frederick II','key_facts',[
    'He was crowned Holy Roman Emperor in 1220 and ruled a realm centered on the Kingdom of Sicily.',
    'During the Sixth Crusade, he negotiated the 1229 Treaty of Jaffa, which returned Jerusalem to the Crusader Kingdom without a major battle.'
])
setv('Wassily Kandinsky','key_facts',[
    'He published Concerning the Spiritual in Art in 1911, setting out an influential theoretical case for abstraction.',
    'He joined the Bauhaus in 1922 and taught there until the school was closed by the Nazi government in 1933.'
])

# Distinguish duplicated historical-significance narratives across alias records.
setv('Napoleon Bonaparte','historical_significance',
     'Napoleon transformed European politics through military conquest and administrative reform, most enduringly through the Napoleonic Code and the institutions of the French state.')
setv('Martin Luther King Jr.','historical_significance',
     'King became a central leader of the U.S. civil rights movement, helping turn nonviolent protest into a national campaign for voting rights and desegregation.')
setv('Omar Mukhtar','historical_significance',
     'Mukhtar became a lasting symbol of Libyan resistance to Italian colonial rule, combining local knowledge with mobile guerrilla tactics in Cyrenaica.')

# Replace a raw Russian citation/list accidentally embedded in English achievements.
setv('Dmitri Mendeleev','achievements',[
    'Formulated the periodic law and published the first widely successful periodic table in 1869, leaving gaps for elements not yet discovered.',
    'His predictions for elements such as gallium, scandium, and germanium were later confirmed, strengthening the scientific acceptance of the periodic system.'
])

# Rebuild the runtime mirror exactly from the corrected JSON.
JP.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
JSP.write_text('window.PERSON_I18N = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print('CHANGES',len(changes))
for c in changes: print(c[0],c[1])
