from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"

TARGET_LANGS = ("en", "es", "fr", "ru")
PEOPLE = {'Trajan': ("Dacian Wars and Trajan's Column", 'Expanded Rome to its greatest territorial extent under an emperor and commemorated the Dacian campaigns in monumental art.'), 'Augustus': ('the settlement of the Roman principate', 'Established the political order that followed the Roman Republic and inaugurated the long Julio-Claudian imperial succession.'), 'Hadrian': ("Hadrian's Wall and his consolidation policy", 'Shifted Roman imperial policy toward consolidation and left major architectural monuments across the empire.'), 'Marcus Aurelius': ('Meditations and the Marcomannic Wars', 'Combined Stoic philosophy with imperial rule during prolonged frontier wars, leaving the Meditations as a major work of ancient philosophy.'), 'Tughril Beg': ('the Seljuk capture of Baghdad in 1055', 'Founded the Great Seljuk political ascendancy and entered Baghdad as protector of the Abbasid caliphate.'), 'Malik-Shah I': ('the Great Seljuk Empire and the reforms of Nizam al-Mulk', 'Presided over the high point of Great Seljuk power while administration, scholarship and the Nizamiyya institutions expanded.'), 'Frederick Barbarossa': ('the imperial campaigns in Italy and the Third Crusade', 'Sought to strengthen imperial authority in Italy and later became the most prominent German ruler of the Third Crusade.'), 'Frederick II': ('the Kingdom of Sicily and the Sixth Crusade', 'Ruled a Mediterranean-centered empire and achieved the recovery of Jerusalem through negotiation during the Sixth Crusade.'), 'Louis IX': ('the Seventh and Eighth Crusades and royal justice', 'Strengthened French royal administration and personally led two crusades, becoming the only French king canonized in the Middle Ages.'), 'Edward III': ("the opening of the Hundred Years' War and English victories in France", 'Asserted an English claim to the French crown and presided over major victories including Crécy and Poitiers.'), 'Timur': ('the Timurid conquests across Central Asia, Persia and the Middle East', 'Built a vast conquest state from Central Asia and established the Timurid dynasty whose cultural legacy later flourished in Samarkand and Herat.'), 'Mehmed II': ('the Ottoman conquest of Constantinople in 1453', 'Captured Constantinople, ended the Byzantine Empire and transformed the city into the political center of the Ottoman state.'), 'Isabella I': ('the conquest of Granada and the 1492 Atlantic expedition', "Completed the conquest of Granada with Ferdinand II and sponsored Christopher Columbus's 1492 voyage."), 'Selim I': ('the Ottoman conquest of Syria, Egypt and the Hejaz', "Rapidly expanded Ottoman power into the Arab lands and brought the caliphate's major centers under Ottoman rule."), 'Henry VIII': ('the English Reformation and the break with papal authority', 'Separated the English church from papal jurisdiction and reshaped the English monarchy and religious institutions.'), 'Elizabeth I': ('the Elizabethan settlement and the defeat of the Spanish Armada', "Stabilized England's religious settlement and ruled during the 1588 defeat of the Spanish Armada and a major cultural flowering."), 'Louis XIV': ('Versailles and the centralization of French monarchy', 'Strengthened royal centralization, made Versailles a symbol of Bourbon power and dominated European diplomacy during a long reign.'), 'Peter the Great': ('the Great Northern War and the founding of Saint Petersburg', "Expanded Russia's Baltic access through the Great Northern War and pursued sweeping military, administrative and cultural reforms."), 'Catherine the Great': ('Russian expansion and the annexation of Crimea', 'Expanded the Russian Empire, annexed Crimea and promoted administrative, educational and cultural reforms during the Enlightenment.'), 'Marie Antoinette': ("the French Revolution and the monarchy's crisis", "Became a central public symbol of the French monarchy's final years and was executed during the French Revolution."), 'Muhammad Ali Pasha': ('the modernization of Egypt and the Greek campaign', 'Built a powerful semi-autonomous Egyptian state through military and administrative reforms and expanded its influence in the eastern Mediterranean.'), 'Otto von Bismarck': ('German unification and the founding of the German Empire in 1871', "Engineered the political and diplomatic process that unified most German states under Prussian leadership and became the empire's first chancellor."), 'Queen Victoria': ('the British Empire and the Victorian age', "Reigned during Britain's industrial expansion and imperial growth, giving her name to a defining period of 19th-century British history."), 'Ibn Saud': ('the establishment of the Kingdom of Saudi Arabia in 1932', 'Unified much of the Arabian Peninsula under his rule and founded the modern Kingdom of Saudi Arabia.')}
GENERIC_HINTS = {'en': 'Renowned Ruler', 'es': 'Renombrado gobernante', 'fr': 'Souverain renommé', 'ru': 'Знаменитый правитель'}
GENERIC_SIGS = {'en': 'Remembered for shaping historical developments in ruler.', 'es': 'Recordado por impulsar el desarrollo histórico como gobernante.', 'fr': 'Mémorable pour avoir marqué les développements historiques en tant que souverain.', 'ru': 'Запомнился тем, что оказал значительное влияние на историческое развитие в качестве правителя.'}

def main() -> None:
    original = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(original)
    changed = 0

    for name, (anchor, significance_en) in PEOPLE.items():
        if name not in data["people"]:
            raise KeyError(f"Person not found: {name}")
        person = data["people"][name]
        hints = {
            "en": f"Key ruler associated with {anchor}.",
            "es": f"Figura clave del poder político asociada a {anchor}.",
            "fr": f"Figure majeure du pouvoir politique associée à {anchor}.",
            "ru": f"Ключевая фигура власти, связанная с: {anchor}.",
        }
        sigs = {
            "en": significance_en,
            "es": {
                "Trajan": "Trajano quedó asociado a la expansión romana en las guerras dacias y a un programa monumental que incluye la Columna de Trajano.",
                "Augustus": "Augusto estableció el orden político del principado y convirtió su largo gobierno en el modelo inicial del Imperio romano.",
                "Hadrian": "Adriano es recordado por consolidar las fronteras del Imperio y por monumentos como el Muro de Adriano.",
                "Marcus Aurelius": "Marco Aurelio unió el gobierno imperial con la filosofía estoica y dirigió Roma durante las guerras marcomanas.",
                "Tughril Beg": "Tugril Beg fundó la ascendencia política selyúcida y consolidó su posición en Bagdad junto al califato abasí.",
                "Malik-Shah I": "Malik Shah I presidió el apogeo del poder selyúcida y una etapa de expansión administrativa y cultural.",
                "Frederick Barbarossa": "Federico Barbarroja marcó la política imperial del siglo XII con sus campañas italianas y su participación en la Tercera Cruzada.",
                "Frederick II": "Federico II destacó por su reino siciliano y por recuperar Jerusalén mediante negociación durante la Sexta Cruzada.",
                "Louis IX": "Luis IX reforzó la administración real francesa y dirigió las Séptima y Octava Cruzadas.",
                "Edward III": "Eduardo III impulsó la reclamación inglesa al trono francés y obtuvo importantes victorias al comienzo de la Guerra de los Cien Años.",
                "Timur": "Timur creó un gran estado conquistador desde Asia Central y sentó las bases de la dinastía timúrida.",
                "Mehmed II": "Mehmed II conquistó Constantinopla en 1453 y convirtió la ciudad en el centro político del Imperio otomano.",
                "Isabella I": "Isabel I de Castilla completó la conquista de Granada y patrocinó el viaje atlántico de 1492 junto con Fernando.",
                "Selim I": "Selim I extendió rápidamente el poder otomano a Siria, Egipto y el Hiyaz.",
                "Henry VIII": "Enrique VIII rompió la jurisdicción papal sobre la Iglesia inglesa y transformó la relación entre monarquía y religión.",
                "Elizabeth I": "Isabel I estabilizó el acuerdo religioso inglés y gobernó durante la derrota de la Armada española en 1588.",
                "Louis XIV": "Luis XIV centralizó la monarquía francesa y convirtió Versalles en un símbolo duradero del poder borbónico.",
                "Peter the Great": "Pedro el Grande amplió el acceso ruso al Báltico y emprendió profundas reformas militares y administrativas.",
                "Catherine the Great": "Catalina la Grande expandió el Imperio ruso, incluida Crimea, y promovió reformas culturales y educativas.",
                "Marie Antoinette": "María Antonieta se convirtió en un símbolo de la crisis de la monarquía francesa y fue ejecutada durante la Revolución.",
                "Muhammad Ali Pasha": "Muhammad Ali Pasha construyó un Estado egipcio poderoso mediante reformas militares y administrativas y amplió su influencia regional.",
                "Otto von Bismarck": "Bismarck dirigió el proceso diplomático y político que culminó en la unificación alemana y el Imperio de 1871.",
                "Queen Victoria": "Victoria reinó durante la expansión industrial e imperial británica y dio nombre a una etapa decisiva de la historia británica.",
                "Ibn Saud": "Ibn Saud unificó gran parte de la península arábiga y fundó el Reino de Arabia Saudí en 1932.",
            }[name],
            "fr": {
                "Trajan": "Trajan est associé à l’expansion romaine durant les guerres daciques et à un programme monumental dont témoigne la colonne Trajane.",
                "Augustus": "Auguste établit l’ordre politique du principat et fournit le modèle initial du gouvernement impérial romain.",
                "Hadrian": "Hadrien est surtout associé à la consolidation des frontières de l’Empire et à des monuments comme le mur d’Hadrien.",
                "Marcus Aurelius": "Marc Aurèle combina le pouvoir impérial et la philosophie stoïcienne tout en dirigeant Rome pendant les guerres marcomanes.",
                "Tughril Beg": "Tughril Beg fonda la prééminence politique seldjoukide et s’imposa à Bagdad comme protecteur du califat abbasside.",
                "Malik-Shah I": "Malik-Shah Ier régna à l’apogée de la puissance seldjoukide et d’un important développement administratif et culturel.",
                "Frederick Barbarossa": "Frédéric Barberousse domina la politique impériale du XIIe siècle par ses campagnes en Italie et sa participation à la troisième croisade.",
                "Frederick II": "Frédéric II se distingua par son royaume de Sicile et par la récupération négociée de Jérusalem durant la sixième croisade.",
                "Louis IX": "Louis IX renforça l’administration royale française et conduisit les septième et huitième croisades.",
                "Edward III": "Édouard III affirma la revendication anglaise sur la couronne de France et remporta plusieurs victoires au début de la guerre de Cent Ans.",
                "Timur": "Timur bâtit un vaste État de conquête en Asie centrale et fonda la dynastie timouride.",
                "Mehmed II": "Mehmed II conquit Constantinople en 1453 et en fit le centre politique de l’Empire ottoman.",
                "Isabella I": "Isabelle de Castille acheva la conquête de Grenade et soutint le voyage transatlantique de 1492 avec Ferdinand.",
                "Selim I": "Selim Ier étendit rapidement la puissance ottomane à la Syrie, à l’Égypte et au Hedjaz.",
                "Henry VIII": "Henri VIII rompit la juridiction pontificale sur l’Église anglaise et transforma les institutions religieuses du royaume.",
                "Elizabeth I": "Élisabeth I stabilisa le règlement religieux anglais et régna lors de la défaite de l’Armada espagnole en 1588.",
                "Louis XIV": "Louis XIV renforça la centralisation monarchique et fit de Versailles un symbole durable du pouvoir bourbonien.",
                "Peter the Great": "Pierre le Grand donna à la Russie un accès accru à la Baltique et lança de profondes réformes militaires et administratives.",
                "Catherine the Great": "Catherine II agrandit considérablement l’Empire russe, notamment avec l’annexion de la Crimée, et soutint les réformes culturelles.",
                "Marie Antoinette": "Marie-Antoinette devint un symbole de la crise de la monarchie française et fut exécutée pendant la Révolution.",
                "Muhammad Ali Pasha": "Méhémet Ali construisit un État égyptien puissant grâce à des réformes militaires et administratives et étendit son influence régionale.",
                "Otto von Bismarck": "Bismarck dirigea le processus politique et diplomatique qui aboutit à l’unification allemande et à l’Empire de 1871.",
                "Queen Victoria": "Victoria régna pendant l’expansion industrielle et impériale britannique et donna son nom à une période majeure du XIXe siècle.",
                "Ibn Saud": "Ibn Saoud unifia une grande partie de la péninsule Arabique et fonda le royaume d’Arabie saoudite en 1932.",
            }[name],
            "ru": {
                "Trajan": "Траян вошёл в историю благодаря расширению Римской империи в Дакийских войнах и монументам вроде Колонны Траяна.",
                "Augustus": "Август создал политический порядок принципата и заложил модель ранней императорской власти Рима.",
                "Hadrian": "Адриан известен укреплением границ империи и масштабными сооружениями, включая стену Адриана.",
                "Marcus Aurelius": "Марк Аврелий сочетал императорскую власть со стоической философией и руководил Римом во время Маркоманских войн.",
                "Tughril Beg": "Тогрул-бек основал политическое превосходство сельджуков и утвердился в Багдаде как защитник Аббасидского халифата.",
                "Malik-Shah I": "Малик-шах I правил в период наивысшего могущества Великих Сельджуков и развития их администрации и культуры.",
                "Frederick Barbarossa": "Фридрих Барбаросса определял имперскую политику XII века походами в Италию и участием в Третьем крестовом походе.",
                "Frederick II": "Фридрих II прославился сицилийским королевством и дипломатическим возвращением Иерусалима во время Шестого крестового похода.",
                "Louis IX": "Людовик IX укрепил французскую королевскую администрацию и лично возглавил Седьмой и Восьмой крестовые походы.",
                "Edward III": "Эдуард III отстаивал притязания Англии на французскую корону и одержал важные победы в начале Столетней войны.",
                "Timur": "Тимур создал обширное завоевательное государство в Центральной Азии и основал династию Тимуридов.",
                "Mehmed II": "Мехмед II захватил Константинополь в 1453 году и превратил его в политический центр Османской империи.",
                "Isabella I": "Изабелла Кастильская завершила завоевание Гранады и поддержала атлантическую экспедицию 1492 года вместе с Фердинандом.",
                "Selim I": "Селим I быстро расширил Османскую державу на Сирию, Египет и Хиджаз.",
                "Henry VIII": "Генрих VIII разорвал юрисдикционную связь английской церкви с папством и изменил религиозные институты королевства.",
                "Elizabeth I": "Елизавета I укрепила религиозное устройство Англии и правила во время разгрома Испанской армады в 1588 году.",
                "Louis XIV": "Людовик XIV усилил централизацию французской монархии и превратил Версаль в символ власти Бурбонов.",
                "Peter the Great": "Пётр I расширил доступ России к Балтике и провёл глубокие военные, административные и культурные реформы.",
                "Catherine the Great": "Екатерина II значительно расширила Российскую империю, включая присоединение Крыма, и поддерживала культурные реформы.",
                "Marie Antoinette": "Мария-Антуанетта стала одним из символов кризиса французской монархии и была казнена во время революции.",
                "Muhammad Ali Pasha": "Мухаммед Али-паша создал сильное египетское государство с помощью военных и административных реформ и расширил его региональное влияние.",
                "Otto von Bismarck": "Бисмарк руководил политическим и дипломатическим процессом, завершившимся объединением Германии и созданием империи в 1871 году.",
                "Queen Victoria": "Виктория правила в эпоху промышленного и имперского расширения Британии, определившей значительную часть истории XIX века.",
                "Ibn Saud": "Ибн Сауд объединил значительную часть Аравийского полуострова и основал Королевство Саудовская Аравия в 1932 году.",
            }[name],
        }
        for lang in TARGET_LANGS:
            entry = person["languages"][lang]
            if entry.get("hint") == GENERIC_HINTS[lang]:
                entry["hint"] = hints[lang]
                changed += 1
            if entry.get("historical_significance") == GENERIC_SIGS[lang]:
                entry["historical_significance"] = sigs[lang]
                changed += 1

    backup = JSON_PATH.with_name("person_i18n.before_batch12_rulers.json")
    backup.write_text(original, encoding="utf-8")
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    js = "const PERSON_I18N = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    JS_PATH.write_text(js, encoding="utf-8")
    verify_json = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    verify_js = json.loads(js.removeprefix("const PERSON_I18N = ").removesuffix(";\n"))
    if verify_json != verify_js:
        raise RuntimeError("JSON↔JS semantic equality failed")
    print(f"Batch 12 ruler cleanup: {changed} field changes.")
    print(f"Backup JSON: {backup}")
    print("JSON↔JS semantic equality: PASS")

if __name__ == "__main__":
    main()
