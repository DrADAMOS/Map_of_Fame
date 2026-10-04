from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
TARGET_LANGS = ("en", "es", "fr", "ru")
PEOPLE = {'William the Conqueror': 'the Norman conquest of England in 1066 and the Battle of Hastings', 'Alp Arslan': 'the Seljuk victory over Byzantium at Manzikert in 1071', 'Nur ad-Din': "the consolidation of Muslim Syria and the campaigns that preceded Saladin's rise", 'Richard the Lionheart': 'his leadership in the Third Crusade and the Battle of Arsuf', 'Subutai': 'the Mongol campaigns across Central Asia, China and Eastern Europe', 'Alexander Suvorov': 'his undefeated record and victories including Rymnik and the Italian and Swiss campaigns', 'José de San Martín': 'the liberation campaigns in Argentina, Chile and Peru', 'Robert E. Lee': 'his command of the Confederate Army of Northern Virginia during the American Civil War', 'Ulysses S. Grant': 'the Union campaigns that captured Vicksburg and led to Confederate surrender at Appomattox', 'Horatio Kitchener': 'his organization of British forces during the First World War and the expansion of the British army', 'Douglas MacArthur': 'his command in the Pacific during the Second World War and the Inchon landing', 'George S. Patton': 'his armored operations in North Africa and Europe during the Second World War', 'T. E. Lawrence': 'his role in the Arab Revolt and guerrilla strategy during the First World War', 'Dwight D. Eisenhower': 'his command of the Allied invasion of Normandy and the European campaign', 'Erwin Rommel': 'his North African campaigns as commander of the German Afrika Korps', 'Georgy Zhukov': 'his major Soviet victories from Moscow and Stalingrad to Berlin during the Second World War'}
HINTS_EN = {'William the Conqueror': 'Norman ruler who conquered England in 1066.', 'Alp Arslan': 'Seljuk sultan who defeated Byzantium at Manzikert.', 'Nur ad-Din': 'Zengid ruler who consolidated Muslim Syria.', 'Richard the Lionheart': 'English king and leading commander of the Third Crusade.', 'Subutai': 'Mongol strategist behind campaigns across Eurasia.', 'Alexander Suvorov': 'Russian field marshal known for major victories and an undefeated record.', 'José de San Martín': 'South American independence leader who led campaigns across the Andes.', 'Robert E. Lee': 'Confederate commander of the Army of Northern Virginia.', 'Ulysses S. Grant': "Union commander who accepted Lee's surrender at Appomattox.", 'Horatio Kitchener': 'British field marshal who organized the wartime army in 1914.', 'Douglas MacArthur': 'American commander of Allied forces in the Southwest Pacific.', 'George S. Patton': 'American armored commander of the Second World War.', 'T. E. Lawrence': 'British officer associated with the Arab Revolt.', 'Dwight D. Eisenhower': 'Supreme Allied commander for the Normandy invasion.', 'Erwin Rommel': 'German field marshal known for campaigns in North Africa.', 'Georgy Zhukov': 'Soviet marshal who commanded major victories against Nazi Germany.'}
TRANSLATIONS = {'es': {'William the Conqueror': 'la conquista normanda de Inglaterra en 1066 y la batalla de Hastings', 'Alp Arslan': 'la victoria selyúcida sobre Bizancio en Manzikert en 1071', 'Nur ad-Din': 'la consolidación de Siria musulmana y las campañas que precedieron al ascenso de Saladino', 'Richard the Lionheart': 'su liderazgo en la Tercera Cruzada y la batalla de Arsuf', 'Subutai': 'las campañas mongolas por Asia Central, China y Europa oriental', 'Alexander Suvorov': 'sus victorias de Rymnik y de las campañas de Italia y Suiza, dentro de una carrera sin derrotas', 'José de San Martín': 'las campañas de independencia de Argentina, Chile y Perú', 'Robert E. Lee': 'su mando del Ejército de Virginia del Norte durante la Guerra Civil estadounidense', 'Ulysses S. Grant': 'las campañas de la Unión que tomaron Vicksburg y condujeron a la rendición confederada en Appomattox', 'Horatio Kitchener': 'la organización de las fuerzas británicas durante la Primera Guerra Mundial y la expansión del ejército británico', 'Douglas MacArthur': 'su mando en el Pacífico durante la Segunda Guerra Mundial y el desembarco de Inchon', 'George S. Patton': 'sus operaciones blindadas en el norte de África y Europa durante la Segunda Guerra Mundial', 'T. E. Lawrence': 'su papel en la Revuelta Árabe y la estrategia de guerrilla durante la Primera Guerra Mundial', 'Dwight D. Eisenhower': 'su mando de la invasión aliada de Normandía y la campaña europea', 'Erwin Rommel': 'sus campañas en el norte de África como comandante del Afrika Korps', 'Georgy Zhukov': 'sus grandes victorias soviéticas desde Moscú y Stalingrado hasta Berlín durante la Segunda Guerra Mundial'}, 'fr': {'William the Conqueror': 'la conquête normande de l’Angleterre en 1066 et la bataille de Hastings', 'Alp Arslan': 'la victoire seldjoukide sur Byzance à Manzikert en 1071', 'Nur ad-Din': 'la consolidation de la Syrie musulmane et les campagnes qui précédèrent l’ascension de Saladin', 'Richard the Lionheart': 'son commandement pendant la troisième croisade et la bataille d’Arsouf', 'Subutai': 'les campagnes mongoles à travers l’Asie centrale, la Chine et l’Europe orientale', 'Alexander Suvorov': 'ses victoires à Rymnik et pendant les campagnes d’Italie et de Suisse, dans une carrière sans défaite', 'José de San Martín': 'les campagnes d’indépendance en Argentine, au Chili et au Pérou', 'Robert E. Lee': 'son commandement de l’armée de Virginie du Nord pendant la guerre de Sécession', 'Ulysses S. Grant': 'les campagnes de l’Union qui prirent Vicksburg et conduisirent à la reddition de Lee à Appomattox', 'Horatio Kitchener': 'l’organisation des forces britanniques pendant la Première Guerre mondiale et l’expansion de l’armée britannique', 'Douglas MacArthur': 'son commandement dans le Pacifique pendant la Seconde Guerre mondiale et le débarquement d’Inchon', 'George S. Patton': 'ses opérations blindées en Afrique du Nord et en Europe pendant la Seconde Guerre mondiale', 'T. E. Lawrence': 'son rôle dans la révolte arabe et la stratégie de guérilla pendant la Première Guerre mondiale', 'Dwight D. Eisenhower': 'son commandement de l’invasion alliée de Normandie et de la campagne européenne', 'Erwin Rommel': 'ses campagnes en Afrique du Nord comme commandant de l’Afrika Korps', 'Georgy Zhukov': 'ses grandes victoires soviétiques, de Moscou et Stalingrad jusqu’à Berlin pendant la Seconde Guerre mondiale'}, 'ru': {'William the Conqueror': 'нормандское завоевание Англии в 1066 году и битва при Гастингсе', 'Alp Arslan': 'победа сельджуков над Византией при Манцикерте в 1071 году', 'Nur ad-Din': 'объединение мусульманской Сирии и кампании, предшествовавшие возвышению Саладина', 'Richard the Lionheart': 'его руководство Третьим крестовым походом и битва при Арсуфе', 'Subutai': 'монгольские походы через Центральную Азию, Китай и Восточную Европу', 'Alexander Suvorov': 'победы при Рымнике и в Итальянском и Швейцарском походах при безупречной полевой репутации', 'José de San Martín': 'освободительные походы в Аргентине, Чили и Перу', 'Robert E. Lee': 'командование Армией Северной Вирджинии во время Гражданской войны в США', 'Ulysses S. Grant': 'кампании Союза, приведшие к падению Виксберга и капитуляции Ли при Аппоматтоксе', 'Horatio Kitchener': 'организация британских сил во время Первой мировой войны и расширение британской армии', 'Douglas MacArthur': 'командование союзными силами на Тихом океане и высадка в Инчхоне во время Второй мировой войны', 'George S. Patton': 'бронетанковые операции в Северной Африке и Европе во время Второй мировой войны', 'T. E. Lawrence': 'его роль в Арабском восстании и партизанской стратегии во время Первой мировой войны', 'Dwight D. Eisenhower': 'командование высадкой союзников в Нормандии и европейской кампанией', 'Erwin Rommel': 'его кампании в Северной Африке в качестве командующего Африканским корпусом', 'Georgy Zhukov': 'крупные советские победы от Москвы и Сталинграда до Берлина во время Второй мировой войны'}}
GENERIC_HINTS = {'en': 'Renowned Military Leader', 'es': 'Renombrado líder militar', 'fr': 'Chef militaire renommé', 'ru': 'Знаменитый военачальник'}
GENERIC_SIGS = {'en': 'Remembered for shaping historical developments in military leader.', 'es': 'Recordado por impulsar el desarrollo histórico como líder militar.', 'fr': 'Mémorable pour avoir marqué les développements historiques en tant que chef militaire.', 'ru': 'Запомнился тем, что оказал значительное влияние на историческое развитие в качестве военачальника.'}

def main() -> None:
    original = JSON_PATH.read_text(encoding='utf-8')
    data = json.loads(original)
    changed = 0
    for name, anchor_en in PEOPLE.items():
        if name not in data['people']:
            raise KeyError(f'Person not found: {name}')
        person = data['people'][name]
        for lang in TARGET_LANGS:
            entry = person['languages'][lang]
            if entry.get('hint') == GENERIC_HINTS[lang]:
                if lang == 'en':
                    entry['hint'] = HINTS_EN[name]
                elif lang == 'es':
                    entry['hint'] = f'Figura militar vinculada a {TRANSLATIONS[lang][name]}.'
                elif lang == 'fr':
                    entry['hint'] = f'Figure militaire associée à {TRANSLATIONS[lang][name]}.'
                else:
                    entry['hint'] = f'Военный деятель, связанный с: {TRANSLATIONS[lang][name]}.'
                changed += 1
            if entry.get('historical_significance') == GENERIC_SIGS[lang]:
                if lang == 'en':
                    entry['historical_significance'] = f'{name} left a lasting mark on military history through {anchor_en}.'.replace('through the ', 'through ')
                elif lang == 'es':
                    entry['historical_significance'] = f'{name} dejó una huella duradera en la historia militar mediante {TRANSLATIONS[lang][name]}.'
                elif lang == 'fr':
                    entry['historical_significance'] = f'{name} a durablement marqué l’histoire militaire par {TRANSLATIONS[lang][name]}.'
                else:
                    entry['historical_significance'] = f'{name} оставил заметный след в военной истории благодаря: {TRANSLATIONS[lang][name]}.'
                changed += 1

    backup = JSON_PATH.with_name('person_i18n.before_batch14_military_leaders.json')
    backup.write_text(original, encoding='utf-8')
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    js = 'const PERSON_I18N = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    JS_PATH.write_text(js, encoding='utf-8')
    verify_json = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    verify_js = json.loads(js.removeprefix('const PERSON_I18N = ').removesuffix(';\n'))
    if verify_json != verify_js:
        raise RuntimeError('JSON↔JS semantic equality failed')
    print(f'Batch 14 military leader cleanup: {changed} field changes.')
    print(f'Backup JSON: {backup}')
    print('JSON↔JS semantic equality: PASS')

if __name__ == '__main__':
    main()
