from __future__ import annotations
import json, shutil
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
JSON_PATH=ROOT/"app/src/main/assets/person_i18n.json"
JS_PATH=ROOT/"app/src/main/assets/js/person_i18n.js"
BACKUP_DIR=ROOT/"tools/backups"

TR={
"Francisco Goya":"İspanyol sanatında modern döneme geçişte belirleyici bir rol oynadı; savaşın ve toplumsal şiddetin etkilerini güçlü resimlerle belgeledi.",
"Eugène Delacroix":"Fransız romantizminin önde gelen ressamlarından biri olarak renk, hareket ve tarihsel konuları birleştiren etkili bir üslup geliştirdi.",
"Claude Monet":"İzlenimciliğin kurucu isimlerinden biri olarak ışığın ve atmosferin değişimini doğrudan gözleme dayalı resimlerle araştırdı.",
"Henri Rousseau":"Tropik ormanları ve düşsel sahneleri kendine özgü bir üslupla resmederek modern sanatın gelişiminde etkili oldu.",
"Paul Gauguin":"Doğalcı betimlemeden uzaklaşarak güçlü renkler ve sadeleştirilmiş biçimlerle modern sanatın yeni yönlerini etkiledi.",
"Vincent van Gogh":"Yoğun renkleri ve belirgin fırça darbeleriyle kişisel ve ifadeci bir resim dili geliştirdi; modern sanat üzerinde kalıcı etki bıraktı.",
"Alphonse Mucha":"Afiş, illüstrasyon ve dekoratif tasarımlarıyla Art Nouveau'nun en tanınabilir görsel dillerinden birini oluşturdu.",
"Edvard Munch":"Kaygı, aşk, hastalık ve ölüm gibi temaları ifadeci bir dille işleyerek modern sanatın gelişimine güçlü bir etki yaptı.",
"Wassily Kandinsky":"Soyut sanatın öncülerinden biri olarak renk ve biçimi doğrudan ruhsal ifade aracı olarak kullanan bir resim anlayışı geliştirdi.",
"Henri Matisse":"Güçlü renkleri ve sade biçimleriyle resimde yeni ifade olanakları açtı; Fauvism'in önde gelen isimlerinden oldu.",
"Kazimir Malevich":"Süprematizmi kurarak resmi temel geometrik biçimlere indirgeyen radikal bir soyutlama anlayışı geliştirdi.",
"Pablo Picasso":"Kübizmin kurucularından biri olarak biçimin parçalanması ve yeniden kurulması yoluyla modern sanatın yönünü değiştirdi.",
"Amedeo Modigliani":"Uzun yüzler ve bedenlerle karakterize edilen özgün portre ve nü anlayışıyla modern figüratif sanatın ayırt edici isimlerinden oldu.",
"Marc Chagall":"Anı, simge ve düşsel imgeleri yoğun renklerle birleştiren kişisel bir görsel dil geliştirdi.",
}

JA={
"Francisco Goya":"戦争の暴力を記録した作品や宮廷画家としての活動を通じて、スペイン絵画を近代へと導く重要な役割を果たした。",
"Eugène Delacroix":"強い色彩と動き、歴史的主題を結びつけ、フランス・ロマン主義を代表する画家となった。",
"Henri Rousseau":"想像上の熱帯風景と独自の素朴な画風によって、後の近代芸術家たちに影響を与えた。",
"Paul Gauguin":"自然主義的な描写から離れ、強い色彩と単純化された形によって近代絵画の新しい方向を示した。",
"Vincent van Gogh":"強烈な色彩と筆触による表現的な絵画を発展させ、近代美術に大きな影響を残した。",
"Alphonse Mucha":"劇場ポスターや装飾的な図案を通じて、アール・ヌーヴォーを象徴する独自のグラフィック様式を確立した。",
"Edvard Munch":"不安、愛、病、死などの心理的主題を表現主義的な画面に変換し、近代美術に強い影響を与えた。",
"Wassily Kandinsky":"色と形そのものを精神的表現の手段とする抽象絵画を発展させ、その先駆者の一人となった。",
"Henri Matisse":"鮮やかな色彩と単純化された形を大胆に用い、フォーヴィスムを代表する画家として近代絵画を刷新した。",
"Kazimir Malevich":"シュプレマティスムを創始し、基本的な幾何学形態による非具象絵画を推し進めた。",
"Pablo Picasso":"キュビスムを共同で発展させ、形態を分解して再構成する方法によって近代美術の方向を大きく変えた。",
"Amedeo Modigliani":"細長くデフォルメされた顔や身体を特徴とする肖像画と裸体画の独自の様式を確立した。",
"Marc Chagall":"記憶や象徴、夢のような人物像を鮮やかな色彩で結びつけ、独自の詩的な画風を築いた。",
}

def norm(s):
    try:return s.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError,UnicodeDecodeError):return s

def find(people,name):
    for p in people.values():
        if not isinstance(p,dict):continue
        en=p.get("languages",{}).get("en",{})
        if isinstance(en,dict) and isinstance(en.get("name"),str) and (en["name"]==name or norm(en["name"])==name):return p
    return None

def apply_group(data,group,lang):
    missing=[]; changed=0
    for name,value in group.items():
        p=find(data["people"],name)
        if p is None: missing.append(name); continue
        p["languages"].setdefault(lang,{})["historical_significance"]=value
        changed+=1
    return changed,missing

def main():
    data=json.loads(JSON_PATH.read_text(encoding="utf-8"))
    BACKUP_DIR.mkdir(parents=True,exist_ok=True)
    backup=BACKUP_DIR/f"person_i18n_before_batch23_tr_ja_significance_{datetime.now():%Y%m%d_%H%M%S}.json"
    shutil.copy2(JSON_PATH,backup)
    c1,m1=apply_group(data,TR,"tr"); c2,m2=apply_group(data,JA,"ja")
    if m1 or m2: raise RuntimeError("Missing people:\n"+"\n".join(m1+m2))
    JSON_PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    JS_PATH.write_text("/* Auto-generated from person_i18n.json. Do not edit manually. */\nwindow.PERSON_I18N = "+json.dumps(data,ensure_ascii=False,separators=(",",":"))+";\n",encoding="utf-8")
    payload=JS_PATH.read_text(encoding="utf-8").split("window.PERSON_I18N = ",1)[1].rsplit(";",1)[0]
    if json.loads(payload)!=data: raise RuntimeError("JSON<->JS semantic equality FAILED")
    print(f"Batch 23 applied: {c1+c2} fields across {len(TR)+len(JA)} people.")
    print(f"TR: {c1} | JA: {c2}")
    print(f"Backup JSON: {backup}")
    print("JSON<->JS semantic equality: PASS")

if __name__=="__main__":main()
