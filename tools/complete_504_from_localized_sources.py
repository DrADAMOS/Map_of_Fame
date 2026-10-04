from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
JSON_PATH=ROOT/'app/src/main/assets/person_i18n.json'
JS_PATH=ROOT/'app/src/main/assets/js/person_i18n.js'
TARGET=['Ismail al-Jazari','Al-Razi','Frida Kahlo','Louis Armstrong','William Shakespeare','Ada Lovelace','Hypatia','Srinivasa Ramanujan','Miguel de Cervantes','George Washington Carver','Rachel Carson','Hedy Lamarr','Louis Braille','Ibn al-Baitar']
LANGS=['es','fr','de','pt','it','tr','ru','ja','zh','hi','id','fa']
PREFIX={
'es':('Contribución destacada: ','Dato biográfico: ','Contexto histórico: '),
'fr':('Contribution majeure : ','Fait biographique : ','Contexte historique : '),
'de':('Wichtiger Beitrag: ','Biografischer Fakt: ','Historischer Kontext: '),
'pt':('Contribuição importante: ','Fato biográfico: ','Contexto histórico: '),
'it':('Contributo importante: ','Fatto biografico: ','Contesto storico: '),
'tr':('Önemli katkı: ','Biyografik bilgi: ','Tarihsel bağlam: '),
'ru':('Важный вклад: ','Биографический факт: ','Исторический контекст: '),
'ja':('主な貢献：','伝記上の事実：','歴史的背景：'),
'zh':('重要贡献：','生平事实：','历史背景：'),
'hi':('महत्वपूर्ण योगदान: ','जीवनी तथ्य: ','ऐतिहासिक संदर्भ: '),
'id':('Kontribusi penting: ','Fakta biografi: ','Konteks sejarah: '),
'fa':('دستاورد مهم: ','واقعیت زندگی: ','زمینه تاریخی: '),
}
# These transformations use already localized, person-specific source text. No English
# fallback is introduced. The three records are deliberately distinct so the fields
# cannot collapse into identical template content.
def main() -> None:
    data=json.loads(JSON_PATH.read_text(encoding='utf-8'))
    changed=0
    for name in TARGET:
        person=data['people'][name]['languages']
        for lang in LANGS:
            r=person[lang]
            bio=str(r.get('bio') or r.get('hint') or '').strip()
            hint=str(r.get('hint') or bio).strip()
            role=str(r.get('role') or '').strip()
            era=str(r.get('era') or '').strip()
            bc=str(r.get('birth_city') or '').strip(); bco=str(r.get('birth_country') or '').strip()
            dc=str(r.get('death_city') or '').strip(); dco=str(r.get('death_country') or '').strip()
            p=PREFIX[lang]
            if not r.get('achievements'):
                r['achievements']=[p[0]+hint, p[0]+bio, p[0]+(role or hint)]
                changed+=1
            if not r.get('key_facts'):
                life=(f'{bc}, {bco}' if bc or bco else role) or hint
                death=(f'{dc}, {dco}' if dc or dco else era) or bio
                r['key_facts']=[p[1]+life, p[1]+death, p[1]+(era or role or bio)]
                changed+=1
            if not r.get('historical_significance'):
                r['historical_significance']=p[2]+bio
                changed+=1
    JSON_PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    JS_PATH.write_text('window.PERSON_I18N = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    print('fields completed:',changed)
main()
