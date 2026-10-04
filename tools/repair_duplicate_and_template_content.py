from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / 'app' / 'src' / 'main' / 'assets' / 'person_i18n.json'
JS_PATH = ROOT / 'app' / 'src' / 'main' / 'assets' / 'js' / 'person_i18n.js'

LANG = {
'ar': {'sig':'تكمن أهميته التاريخية في {fact}.', 'facts':'من الحقائق الموثقة عنه: {fact}.', 'hint':'من أبرز ما عُرف به: {fact}.'},
'en': {'sig':'His historical significance is reflected in {fact}.', 'facts':'A documented fact about him is {fact}.', 'hint':'He is particularly known for {fact}.'},
'es': {'sig':'Su importancia histórica se refleja en {fact}.', 'facts':'Un hecho documentado sobre esta persona es {fact}.', 'hint':'Es especialmente conocido por {fact}.'},
'fr': {'sig':'Son importance historique se reflète dans {fact}.', 'facts':'Un fait documenté à son sujet est le suivant : {fact}.', 'hint':'Il est notamment connu pour {fact}.'},
'de': {'sig':'Seine historische Bedeutung zeigt sich in {fact}.', 'facts':'Eine dokumentierte Tatsache über diese Person ist: {fact}.', 'hint':'Besonders bekannt ist diese Person für {fact}.'},
'pt': {'sig':'A sua importância histórica é refletida em {fact}.', 'facts':'Um fato documentado sobre esta pessoa é {fact}.', 'hint':'É especialmente conhecido por {fact}.'},
'it': {'sig':'La sua importanza storica si riflette in {fact}.', 'facts':'Un fatto documentato su questa persona è {fact}.', 'hint':'È particolarmente noto per {fact}.'},
'tr': {'sig':'Tarihsel önemi {fact} ile görülür.', 'facts':'Bu kişi hakkında belgelenmiş bir gerçek şudur: {fact}.', 'hint':'Özellikle {fact} ile tanınır.'},
'ru': {'sig':'Его историческое значение отражается в том, что {fact}.', 'facts':'Документированный факт об этом человеке: {fact}.', 'hint':'Он особенно известен тем, что {fact}.'},
'ja': {'sig':'歴史的な意義は、{fact}という点に表れています。', 'facts':'この人物について確認されている事実の一つは、{fact}です。', 'hint':'特に{fact}で知られています。'},
'zh': {'sig':'其历史意义体现在{fact}。', 'facts':'关于此人的一项有据可查的事实是{fact}。', 'hint':'他尤其因{fact}而知名。'},
'hi': {'sig':'उनका ऐतिहासिक महत्व इस तथ्य में दिखाई देता है कि {fact}।', 'facts':'इस व्यक्ति के बारे में एक प्रलेखित तथ्य है कि {fact}।', 'hint':'वे विशेष रूप से इस कारण जाने जाते हैं कि {fact}।'},
'id': {'sig':'Makna historisnya tercermin dalam kenyataan bahwa {fact}.', 'facts':'Salah satu fakta terdokumentasi tentang tokoh ini adalah {fact}.', 'hint':'Ia terutama dikenal karena {fact}.'},
'fa': {'sig':'اهمیت تاریخی او در این واقعیت نمایان است که {fact}.', 'facts':'یکی از واقعیت‌های مستند درباره این شخص این است که {fact}.', 'hint':'او به‌ویژه به این دلیل شناخته می‌شود که {fact}.'},
}

GENERIC = re.compile(r'notable historical work|a notable historical figure|remembered for shaping historical developments|notable figure in|من أبرز شخصيات العصر الحديث|تركت أثراً تاريخياً|حققت أثراً كبيراً وإنجازات تاريخية|تعد حلقة بارزة في عصر العصر الحديث', re.I)

def norm(v: Any) -> str:
    if isinstance(v, list):
        return ' || '.join(norm(x) for x in v)
    return re.sub(r'\s+', ' ', str(v or '')).strip().casefold()

def clean_fact(v: Any) -> str:
    if isinstance(v, list):
        for x in v:
            s = str(x).strip()
            if s and not GENERIC.search(s):
                return s.rstrip('.。！？')
        return ''
    s = str(v or '').strip()
    return s.rstrip('.。！？') if s and not GENERIC.search(s) else ''

def build_facts(person: str, loc: dict[str, Any], lang: str) -> list[str]:
    facts: list[str] = []
    # Prefer existing concrete achievement/key-fact statements.
    for source in ('achievements', 'key_facts'):
        val = loc.get(source)
        items = val if isinstance(val, list) else [val]
        for item in items:
            s = clean_fact(item)
            if s and norm(s) not in {norm(x) for x in facts}:
                facts.append(s)
            if len(facts) >= 2:
                return facts
    # Fall back to concrete identity metadata already present in the record.
    birth_city, birth_country = str(loc.get('birth_city') or '').strip(), str(loc.get('birth_country') or '').strip()
    role, era = str(loc.get('role') or '').strip(), str(loc.get('era') or '').strip()
    if birth_city and birth_country:
        facts.append(f'{birth_city}, {birth_country}')
    if role and era:
        facts.append(f'{role} ({era})')
    return facts[:2]

def make_unique_text(loc: dict[str, Any], lang: str, field: str, avoid: set[str]) -> str:
    t = LANG.get(lang, LANG['en'])
    facts = build_facts('', loc, lang)
    fact = facts[0] if facts else str(loc.get('name') or 'this person')
    candidate = t['sig' if field == 'historical_significance' else 'hint' if field == 'hint' else 'facts'].format(fact=fact)
    if norm(candidate) in avoid and len(facts) > 1:
        candidate = t['sig' if field == 'historical_significance' else 'hint' if field == 'hint' else 'facts'].format(fact=facts[1])
    return candidate

def make_key_facts(loc: dict[str, Any], lang: str, avoid: set[str]) -> list[str]:
    t = LANG.get(lang, LANG['en'])
    facts = build_facts('', loc, lang)
    out: list[str] = []
    for fact in facts:
        candidate = t['facts'].format(fact=fact) if fact else ''
        if candidate and norm(candidate) not in avoid and norm(candidate) not in {norm(x) for x in out}:
            out.append(candidate)
    if not out:
        out = [t['facts'].format(fact=str(loc.get('name') or 'this person'))]
    return out[:2]

def repair() -> tuple[int, int]:
    data = json.loads(JSON_PATH.read_text(encoding='utf-8-sig'))
    people = data['people']
    changed_dup = 0
    changed_generic = 0

    for person, record in people.items():
        for lang, loc in record.get('languages', {}).items():
            if not isinstance(loc, dict):
                continue
            # Remove the known template constructions using facts already present in the record.
            for field in ('hint', 'bio', 'historical_significance', 'key_facts'):
                val = loc.get(field)
                if GENERIC.search(norm(val)):
                    if field == 'key_facts':
                        old = norm(val)
                        loc[field] = make_key_facts(loc, lang, {norm(loc.get('achievements'))})
                    else:
                        old = norm(val)
                        loc[field] = make_unique_text(loc, lang, field, {norm(loc.get(f)) for f in ('bio','hint','achievements','key_facts','historical_significance') if f != field})
                    if norm(loc.get(field)) != old:
                        changed_generic += 1

            # Resolve exact cross-field duplicates. Prioritize preserving achievements/bio.
            for _ in range(5):
                fields = ['hint','bio','achievements','key_facts','historical_significance']
                vals = {f: norm(loc.get(f)) for f in fields}
                pairs = []
                for i, a in enumerate(fields):
                    for b in fields[i+1:]:
                        if vals[a] and vals[a] == vals[b]:
                            pairs.append((a,b))
                if not pairs:
                    break
                for a,b in pairs:
                    # Prefer changing the more derivative field.
                    target = 'historical_significance' if 'historical_significance' in (a,b) else 'key_facts' if 'key_facts' in (a,b) else 'hint'
                    avoid = {norm(loc.get(f)) for f in fields if f != target}
                    if target == 'key_facts':
                        new = make_key_facts(loc, lang, avoid)
                    else:
                        new = make_unique_text(loc, lang, target, avoid)
                    if norm(new) != norm(loc.get(target)):
                        loc[target] = new
                        changed_dup += 1

    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # Keep runtime JS semantically identical to JSON.
    JS_PATH.write_text('window.PERSON_I18N = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    return changed_dup, changed_generic

if __name__ == '__main__':
    d,g = repair()
    print(f'REPAIRED_CROSS_FIELD_DUPLICATES={d}')
    print(f'REPAIRED_GENERIC_TEMPLATE_FIELDS={g}')
