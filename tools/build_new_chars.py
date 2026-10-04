# -*- coding: utf-8 -*-
"""
100% Standalone builder for tools/new_chars_batch1.py
No imports from other temporary scripts.
"""

import json
from pathlib import Path

LANGS = ["ar", "en", "es", "fr", "de", "pt", "it", "tr", "ru", "ja", "ko", "zh", "hi", "id", "fa"]

def b(names, hints, bios, bcities, bcountries, dcities, dcountries, roles, eras, achs, facts, wars, sigs):
    res = {}
    for l in LANGS:
        res[l] = {
            "name": names[l], "hint": hints[l], "bio": bios[l],
            "birth_city": bcities[l], "birth_country": bcountries[l],
            "death_city": dcities[l], "death_country": dcountries[l],
            "role": roles[l], "era": eras[l],
            "achievements": achs[l], "key_facts": facts[l],
            "wars": wars[l], "historical_significance": sigs[l]
        }
    return res

ROLE_RULER = {"ar": "حاكم", "en": "Ruler", "es": "Gobernante", "fr": "Souverain", "de": "Herrscher", "pt": "Governante", "it": "Sovrano", "tr": "Hükümdar", "ru": "Правитель", "ja": "統治者", "ko": "통치자", "zh": "统治者", "hi": "शासक", "id": "Penguasa", "fa": "فرمانروا"}
ROLE_GENERAL = {"ar": "قائد عسكري", "en": "General", "es": "General", "fr": "Général", "de": "General", "pt": "General", "it": "Generale", "tr": "General", "ru": "Полководец", "ja": "将軍", "ko": "장군", "zh": "将军", "hi": "सेनापति", "id": "Jenderal", "fa": "ژنرال"}
ROLE_PHILOSOPHER = {"ar": "فيلسوف", "en": "Philosopher", "es": "Filósofo", "fr": "Philosophe", "de": "Philosoph", "pt": "Filósofo", "it": "Filosofo", "tr": "Filozof", "ru": "Философ", "ja": "哲学者", "ko": "철학자", "zh": "哲学家", "hi": "दार्शनिक", "id": "Filsuf", "fa": "فیلسوف"}
ROLE_SCIENTIST = {"ar": "عالم", "en": "Scientist", "es": "Científico", "fr": "Scientifique", "de": "Wissenschaftler", "pt": "Cientista", "it": "Scienziato", "tr": "Bilim İnsanı", "ru": "Учёный", "ja": "科学者", "ko": "과학자", "zh": "科学家", "hi": "वैज्ञानिक", "id": "Ilmuwan", "fa": "دانشمند"}
ROLE_SCHOLAR = {"ar": "عالم ومفكر", "en": "Scholar", "es": "Erudito", "fr": "Érudit", "de": "Gelehrter", "pt": "Erudito", "it": "Erudito", "tr": "Bilgin", "ru": "Учёный-эрудит", "ja": "学者", "ko": "학자", "zh": "学者", "hi": "विद्वान", "id": "Cendekiawan", "fa": "دانشمند"}

ERA_ANCIENT = {"ar": "العصر القديم", "en": "Ancient Era", "es": "Era Antigua", "fr": "Ère Antique", "de": "Antike", "pt": "Era Antiga", "it": "Era Antica", "tr": "Antik Çağ", "ru": "Древняя эра", "ja": "古代", "ko": "고대", "zh": "上古时代", "hi": "प्राचीन काल", "id": "Era Kuno", "fa": "عصر باستان"}
ERA_GOLDEN = {"ar": "العصر الذهبي للإسلام", "en": "Islamic Golden Age", "es": "Edad de Oro del Islam", "fr": "Âge d'or de l'Islam", "de": "Blütezeit des Islam", "pt": "Era de Ouro do Islã", "it": "Epoca d'oro dell'Islam", "tr": "İslam'ın Altın Çağı", "ru": "Золотой век ислама", "ja": "イスラムの黄金時代", "ko": "이슬람의 황금기", "zh": "伊斯兰黄金时代", "hi": "इस्लाम का स्वर्ण युग", "id": "Zaman Kejayaan Islam", "fa": "عصر طلایی اسلام"}

NEW_CHARS_1 = {}

# 1. Hammurabi
NEW_CHARS_1["Hammurabi"] = {
    "name": "حمورابي", "name_en": "Hammurabi", "by": -1810, "dy": -1750,
    "bc": [32.5364, 44.4208], "dc": [32.5364, 44.4208],
    "hint": "ملك بابل السادس وصاحب إحدى أقدم القوانين المكتوبة في التاريخ",
    "hint_en": "Sixth king of Babylon who enacted the famous Code of Hammurabi",
    "mode": "all",
    "bio": "سادس ملوك السلالة البابلية الأولى، وحد بلاد الرافدين واشتهر بوضع شريعة حمورابي المنقوشة على مسلة حجرية.",
    "bio_en": "Sixth king of the First Babylonian Dynasty who unified Mesopotamia and promulgated the famous Code of Hammurabi.",
    "country": "العراق", "country_en": "Iraq", "era": "العصر القديم", "era_en": "Ancient Era",
    "name_ar": "حمورابي", "birth_city": "بابل", "death_city": "بابل",
    "birth_country": "العراق", "death_country": "العراق", "category": "Ruler",
    "birth_date": "-1810-01-01", "death_date": "-1750-01-01",
    "languages": b(
        names={"ar": "حمورابي", "en": "Hammurabi", "es": "Hamurabi", "fr": "Hammourabi", "de": "Hammurapi", "pt": "Hamurábi", "it": "Hammurabi", "tr": "Hammurabi", "ru": "Хаммурапи", "ja": "ハンムラビ", "ko": "함무라비", "zh": "汉谟拉比", "hi": "हम्मुराबी", "id": "Hammurabi", "fa": "حمورابی"},
        hints={
            "ar": "ملك بابل السادس وصاحب إحدى أقدم القوانين المكتوبة في التاريخ.",
            "en": "Sixth king of Babylon who enacted the famous Code of Hammurabi.",
            "es": "Sexto rey de Babilonia que promulgó el famoso Código de Hamurabi.",
            "fr": "Sixième roi de Babylone qui promulgua le célèbre Code de Hammourabi.",
            "de": "Sechster König von Babylon, der den berühmten Codex Hammurapi erließ.",
            "pt": "Sexto rei da Babilônia que promulgou o famoso Código de Hamurábi.",
            "it": "Sesto re di Babilonia che emanò il famoso Codice di Hammurabi.",
            "tr": "Ünlü Hammurabi Kanunları'nı çıkaran altıncı Babil kralı.",
            "ru": "Шестой царь Вавилона, издавший знаменитый свод законов Хаммурапи.",
            "ja": "ハンムラビ法典を制定したバビロン第1王朝第6代の王。",
            "ko": "함무라비 법전을 제정한 바빌론의 제6대 왕.",
            "zh": "颁布著名的《汉谟拉比法典》的巴比伦第六任国王。",
            "hi": "बेबीलोन के छठे राजा जिन्होंने प्रसिद्ध हम्मुराबी संहिता लागू की।",
            "id": "Raja keenam Babilonia yang memberlakukan Kitab Undang-undang Hammurabi.",
            "fa": "ششمین پادشاه بابل که قانون معروف حمورابی را وضع کرد."
        },
        bios={
            "ar": "سادس ملوك السلالة البابلية الأولى، وحد بلاد الرافدين واشتهر بوضع شريعة حمورابي المنقوشة على مسلة حجرية.",
            "en": "Sixth king of the First Babylonian Dynasty who unified Mesopotamia and promulgated the famous Code of Hammurabi.",
            "es": "Sexto rey de la primera dinastía de Babilonia que unificó Mesopotamia y promulgó el famoso Código de Hamurabi.",
            "fr": "Sixième roi de la première dynastie babylonienne qui unifia la Mésopotamie et promulgua le célèbre Code de Hammourabi.",
            "de": "Sechster König der Ersten Babylonischen Dynastie, der Mesopotamien einte und den Codex Hammurapi erließ.",
            "pt": "Sexto rei da Primeira Dinastia Babilônica que unificou a Mesopotâmia e promulgou o famoso Código de Hamurábi.",
            "it": "Sesto re della prima dinastia babilonese che unificò la Mesopotamia e promulgò il famoso Codice di Hammurabi.",
            "tr": "Mezopotamya'yı birleştiren ve ünlü Hammurabi Kanunları'nı çıkaran Birinci Babil Hanedanlığı'nın altıncı kralı.",
            "ru": "Шестой царь первой Вавилонской династии, объединивший Месопотамию и издавший законник Хаммурапи.",
            "ja": "メソポタミアを統一し、黒い玄武岩に刻まれたハンムラビ法典を制定したバビロン第1王朝の王。",
            "ko": "메소포타미아를 통일하고 돌기둥에 함무라비 법전을 반포한 바빌론 제1왕조의 제6대 왕.",
            "zh": "巴比伦第一王朝第六任国王，统一美索不达米亚并颁布了著名的《汉谟拉比法典》。",
            "hi": "प्रथम बेबीलोन राजवंश के छठे राजा जिन्होंने मेसोपोटेमिया का एकीकरण किया और हम्मुराबी संहिता जारी की।",
            "id": "Raja keenam Dinasti Pertama Babilonia yang menyatukan Mesopotamia dan memberlakukan Hukum Hammurabi.",
            "fa": "ششمین پادشاه نخستین سلسله بابل که بین‌النهرین را متحد کرد و قانون معروف حمورابی را وضع نمود."
        },
        bcities={"ar": "بابل", "en": "Babylon", "es": "Babilonia", "fr": "Babylone", "de": "Babylon", "pt": "Babilônia", "it": "Babilonia", "tr": "Babil", "ru": "Вавилон", "ja": "バビロン", "ko": "바빌론", "zh": "巴比伦", "hi": "बेबीलोन", "id": "Babilonia", "fa": "بابل"},
        bcountries={"ar": "بلاد الرافدين", "en": "Mesopotamia", "es": "Mesopotamia", "fr": "Mésopotamie", "de": "Mesopotamien", "pt": "Mesopotâmia", "it": "Mesopotamia", "tr": "Mezopotamya", "ru": "Месопотамия", "ja": "メソポタミア", "ko": "메소포타미아", "zh": "美索不达米亚", "hi": "मेसोपोटेमिया", "id": "Mesopotamia", "fa": "بین‌النهرین"},
        dcities={"ar": "بابل", "en": "Babylon", "es": "Babilonia", "fr": "Babylone", "de": "Babylon", "pt": "Babilônia", "it": "Babilonia", "tr": "Babil", "ru": "Вавилон", "ja": "バビロン", "ko": "바빌론", "zh": "巴比伦", "hi": "बेबीलोन", "id": "Babilonia", "fa": "بابل"},
        dcountries={"ar": "بلاد الرافدين", "en": "Mesopotamia", "es": "Mesopotamia", "fr": "Mésopotamie", "de": "Mesopotamien", "pt": "Mesopotâmia", "it": "Mesopotamia", "tr": "Mezopotamya", "ru": "Месопотамия", "ja": "メソポタミア", "ko": "메소포타미아", "zh": "美索不达米亚", "hi": "मेसोपोटेमिया", "id": "Mesopotamia", "fa": "بین‌النهرین"},
        roles=ROLE_RULER,
        eras=ERA_ANCIENT,
        achs={
            "ar": ["سنّ شريعة حمورابي، إحدى أقدم المجموعات القانونية المكتوبة في التاريخ.", "وحد مدن بلاد الرافدين تحت حكم الإمبراطورية البابلية الأولى.", "أقام مشاريع بصرية ضخمة مثل حفر القنوات وبناء المعابد والأسوار."],
            "en": ["Promulgated the Code of Hammurabi, one of history's earliest written legal codes.", "Unified the city-states of Mesopotamia under the First Babylonian Empire.", "Constructed major public works, canals, and temples throughout Babylon."],
            "es": ["Promulgó el Código de Hamurabi, uno de los códigos legales escritos más antiguos.", "Unificó las ciudades-estado de Mesopotamia bajo el Primer Imperio Babilónico.", "Construyó importantes obras públicas, canales y templos en toda Babilonia."],
            "fr": ["Promulgua le Code de Hammourabi, l'un des plus anciens codes juridiques écrits.", "Unifia les cités-états de Mésopotamie sous le Premier Empire babylonien.", "Construisit de grands travaux publics, des canaux et des temples à Babylone."],
            "de": ["Erließ den Codex Hammurapi, eine der ältesten schriftlichen Gesetzessammlungen.", "Vereinte die Stadtstaaten Mesopotamiens unter dem Ersten Babylonischen Reich.", "Errichtete bedeutende Bauwerke, Kanäle und Tempel in ganz Babylon."],
            "pt": ["Promulgou o Código de Hamurábi, um dos códigos legais escritos mais antigos da história.", "Unificou as cidades-estado da Mesopotâmia sob o Primeiro Império Babilônico.", "Construiu grandes obras públicas, canais e templos por toda a Babilônia."],
            "it": ["Promulgò il Codice di Hammurabi, uno dei più antichi codici di leggi scritte.", "Unificò le città-stato della Mesopotamia sotto il Primo Impero Babilonese.", "Costruì importanti opere pubbliche, canali e templi in tutta Babilonia."],
            "tr": ["Tarihin en eski yazılı kanunlarından biri olan Hammurabi Kanunları'nı yayınladı.", "Mezopotamya şehir devletlerini Birinci Babil İmparatorluğu altında birleştirdi.", "Babil genelinde büyük kamu eserleri, kanallar ve tapınaklar inşa etti."],
            "ru": ["Издал свод законов Хаммурапи, один из древнейших письменных правовых памятников.", "Объединил города-государства Месопотамии под властью Вавилонского царства.", "Построил крупные общественные сооружения, каналы и храмы по всему Вавилону."],
            "ja": ["歴史上最古級の成文法規であるハンムラビ法典を制定した。", "メソポタミアの都市国家群を古バビロニア王国ののもとに統一した。", "バビロン全域で大規模な公共事業、運河、神殿を建設した。"],
            "ko": ["역사상 가장 오래된 성문 법전 중 하나인 함무라비 법전을 제정했다.", "메소포타미아의 도시 국가들을 바빌로니아 제1왕조 아래 통일했다.", "바빌론 전역에 대규모 운하와 신전, 공공시설을 건설했다."],
            "zh": ["颁布了历史最早的成文法典之一《汉谟拉比法典》。", "在古巴比伦帝国统治下统一了美索不达米亚城邦。", "在巴比伦各地兴建了大型水利工程、渠系和神庙。"],
            "hi": ["हम्मुराबी संहिता जारी की, जो इतिहास के सबसे पुराने लिखित कानून कोड में से एक है।", "प्रथम बेबीलोन साम्राज्य के तहत मेसोपोटेमिया के नगर-राज्यों को एकीकृत किया।", "बेबीलोन में प्रमुख सार्वजनिक कार्यों, नहरों और मंदिरों का निर्माण कराया।"],
            "id": ["Memberlakukan Kitab Hukum Hammurabi, salah satu hukum tertulis tertua dalam sejarah.", "Menyatukan negara-kota di Mesopotamia di bawah Kekaisaran Babilonia Pertama.", "Membangun pekerjaan umum utama, saluran air, dan candi di seluruh Babilonia."],
            "fa": ["قانون حمورابی را که یکی از قدیمی‌ترین قانون‌نامه‌های نوشته‌شده تاریخ است وضع کرد.", "شهر-دولت‌های بین‌النهرین را تحت امپراتوری نخست بابل متحد ساخت.", "کارهای عمومی بزرگ، کانال‌ها و معابدی را در سراسر بابل احداث کرد."]
        },
        facts={
            "ar": ["حكم بابل نحو 42 عاماً من سنة 1792 قبل الميلاد حتى وفاته.", "عُثر على المسلة الحجرية لشريعته عام 1901 في مدينة سوسة.", "ارتبطت شريعته بمبدأ 'العين بالعين والسن بالسن'."],
            "en": ["Ruled Babylon for 42 years from c. 1792 BCE until his death.", "The stone stele containing his laws was discovered in 1901 in Susa.", "His code is famous for the principle of 'an eye for an eye'."],
            "es": ["Gobernó Babilonia durante 42 años desde aprox. 1792 a.C. hasta su muerte.", "La estela de piedra con sus leyes fue descubierta en 1901 en Susa.", "Su código es famoso por el principio de 'ojo por ojo'."],
            "fr": ["Régna sur Babylone pendant 42 ans environ de 1792 av. J.-C. à sa mort.", "La stèle en pierre contenant ses lois fut découverte en 1901 à Suse.", "Son code est célèbre pour le principe de 'œil pour œil'."],
            "de": ["Regierte Babylon 42 Jahre lang von ca. 1792 v. Chr. bis zu seinem Tod.", "Die Steinstelen mit seinen Gesetzen wurden 1901 in Susa entdeckt.", "Sein Gesetzbuch ist berühmt für das Prinzip 'Auge um Auge'."],
            "pt": ["Governou a Babilônia por 42 anos, de cerca de 1792 a.C. até sua morte.", "A estela de pedra contendo suas leis foi descoberta em 1901 em Susa.", "Seu código é famoso pelo princípio de 'olho por olho'."],
            "it": ["Governò Babilonia per 42 anni dal 1792 a.C. circa fino alla morte.", "La stele di pietra con le sue leggi fu scoperta nel 1901 a Susa.", "Il suo codice è famoso per il principio dell'occhio per occhio'."],
            "tr": ["MÖ 1792'den ölümüne kadar 42 yıl boyunca Babil'i yönetti.", "Kanunlarını içeren taş dikilitaş 1901 yılında Susa'da bulundu.", "Kanunu 'göze göz, dişe diş' ilkesiyle ünlüdür."],
            "ru": ["Правил Вавилоном 42 года примерно с 1792 года до н.э. до своей смерти.", "Каменная стела с его законами была найдена в 1901 году в Сузах.", "Его свод законов известен принципом «око за око»."],
            "ja": ["紀元前1792年頃から死去するまで42年間にわたりバビロンを治めた。", "法典が刻まれた石碑は1901年にスーサで発見された。", "「目には目を、歯には歯を」の同害復讐法で知られる。"],
            "ko": ["기원전 1792년경부터 사망할 때까지 42년 동안 바빌론을 통치했다.", "법전이 흠인된 돌기둥은 1901년 수사에서 발견되었다.", "'눈에는 눈, 이에는 이'라는 동해보복 원칙으로 유명하다."],
            "zh": ["自公元前1792年左右起统治巴比伦长达42年直至去世。", "刻有其法典的石碑于1901年在苏萨被发现。", "其法典以“以眼还眼，以牙还牙”的原则闻名。"],
            "hi": ["लगभग 1792 ईसा पूर्व से अपनी मृत्यु तक 42 वर्षों तक बेबीलोन पर शासन किया।", "उनके कानूनों वाले पत्थर के स्तंभ की खोज 1901 में सूसा में हुई थी।", "उनकी संहिता 'जैसे को तैसा' (आंख के बदले आंख) के सिद्धांत के लिए प्रसिद्ध है।"],
            "id": ["Memerintah Babilonia selama 42 tahun dari sekitar 1792 SM hingga wafatnya.", "Prasasti batu berisi hukumnya ditemukan pada tahun 1901 di Susa.", "Kitab hukumnya terkenal dengan prinsip 'mata dibalas mata'."],
            "fa": ["حدود ۴۲ سال از ۱۷۹۲ پیش از میلاد تا زمان مرگش بر بابل حکومت کرد.", "کتیبه سنگی حاوی قوانین او در سال ۱۹۰۱ در شوش کشف شد.", "قانون‌نامه او به اصل 'چشم در برابر چشم' معروف است."]
        },
        wars={
            "ar": ["حملات بابل لتوحيد بلاد الرافدين (1763–1755 ق.م.)"],
            "en": ["Babylonian Conquest of Mesopotamia (c. 1763–1755 BCE)"],
            "es": ["Conquista babilónica de Mesopotamia (aprox. 1763–1755 a.C.)"],
            "fr": ["Conquête babylonienne de la Mésopotamie (v. 1763–1755 av. J.-C.)"],
            "de": ["Babylonische Eroberung Mesopotamiens (ca. 1763–1755 v. Chr.)"],
            "pt": ["Conquista Babilônica da Mesopotâmia (c. 1763–1755 a.C.)"],
            "it": ["Conquista babilonese della Mesopotamia (1763–1755 a.C. circa)"],
            "tr": ["Babil'in Mezopotamya'yı Fethi (MÖ 1763–1755)"],
            "ru": ["Вавилонское завоевание Месопотамии (ок. 1763–1755 гг. до н.э.)"],
            "ja": ["バビロニアのメソポタミア征服（紀元前1763年〜1755年頃）"],
            "ko": ["바빌로니아의 메소포타미아 정복 (기원전 1763~1755년경)"],
            "zh": ["巴比伦征服美索不达米亚战争（约公元前1763–1755年）"],
            "hi": ["मेसोपोटेमिया की बेबीलोन विजय (लगभग 1763–1755 ईसा पूर्व)"],
            "id": ["Penaklukan Babilonia atas Mesopotamia (sekitar 1763–1755 SM)"],
            "fa": ["فتوحات بابل در بین‌النهرین (حدود ۱۷۶۳–۱۷۵۵ پیش از میلاد)"]
        },
        sigs={
            "ar": "كان حمورابي أحد أعظم ملوك العالم القديم، أرسى قواعد القانون والعدالة التي أثرت في الحضارات البشرية المتعاقبة.",
            "en": "Hammurabi was one of the ancient world's greatest rulers, establishing enduring legal traditions that influenced human civilization.",
            "es": "Hamurabi fue uno de los más grandes gobernantes del mundo antiguo, estableciendo tradiciones legales duraderas.",
            "fr": "Hammourabi fut l'un des plus grands dirigeants du monde antique, instaurant des traditions juridiques durables.",
            "de": "Hammurapi war einer der bedeutendsten Herrscher der Antike, der nachhaltige Rechtstraditionen schuf.",
            "pt": "Hamurábi foi um dos maiores governantes do mundo antigo, estabelecendo tradições jurídicas duradouras.",
            "it": "Hammurabi fu uno dei più grandi sovrani del mondo antico, fondando tradizioni giuridiche durature.",
            "tr": "Hammurabi, insanlık medeniyetini etkileyen kalıcı hukuk gelenekleri kuran antik dünyanın en büyük hükümdarlarındandı.",
            "ru": "Хаммурапи был одним из величайших правителей древнего мира, заложившим правовые традиции человечества.",
            "ja": "ハンムラビは古代世界で最も偉大な統治者の一人であり、後世の法制度に多大な影響を与えた。",
            "ko": "함무라비는 고대 세계에서 가장 위대한 통치자 중 한 명으로, 법적 전통의 기틀을 마련했다.",
            "zh": "汉谟拉比是古代世界最伟大的统治者之一，奠定了影响深远的法律传统。",
            "hi": "हम्मुराबी प्राचीन दुनिया के सबसे महान शासकों में से एक थे, जिन्होंने स्थायी कानूनी परंपराओं की स्थापना की।",
            "id": "Hammurabi adalah salah satu penguasa terbesar dunia kuno yang mendirikan tradisi hukum yang bertahan lama.",
            "fa": "حمورابی یکی از بزرگ‌ترین فرمانروایان جهان باستان بود که سنت‌های قانونی پایدار بنا نهاد."
        }
    )
}

# 2. Nebuchadnezzar II
NEW_CHARS_1["Nebuchadnezzar II"] = {
    "name": "نبوخذ نصر الثاني", "name_en": "Nebuchadnezzar II", "by": -634, "dy": -562,
    "bc": [32.5364, 44.4208], "dc": [32.5364, 44.4208],
    "hint": "ملك بابل العظيم الذي بنى حدائق بابل المعلقة ودمر أورشليم",
    "hint_en": "Greatest king of the Neo-Babylonian Empire who built the Hanging Gardens",
    "mode": "all",
    "bio": "أعظم ملوك الإمبراطورية البابلية الحديثة، شهد عهده بناء حدائق بابل المعلقة وتدمير هيكل أورشليم وسبي اليهود إلى بابل.",
    "bio_en": "Longest-reigning king of the Neo-Babylonian Empire who constructed the Hanging Gardens and conquered Jerusalem.",
    "country": "العراق", "country_en": "Iraq", "era": "العصر القديم", "era_en": "Ancient Era",
    "name_ar": "نبوخذ نصر الثاني", "birth_city": "بابل", "death_city": "بابل",
    "birth_country": "العراق", "death_country": "العراق", "category": "Ruler",
    "birth_date": "-0634-01-01", "death_date": "-0562-01-01",
    "languages": b(
        names={"ar": "نبوخذ نصر الثاني", "en": "Nebuchadnezzar II", "es": "Nabucodonosor II", "fr": "Nabuchodonosor II", "de": "Nebukadnezar II.", "pt": "Nabucodonosor II", "it": "Nabucodonosor II", "tr": "II. Nebukadnezar", "ru": "Навуходоносор II", "ja": "ネブカドネザル2世", "ko": "네부카드네자르 2세", "zh": "尼布甲尼撒二世", "hi": "नबूकदनेस्सर द्वितीय", "id": "Nebukadnezar II", "fa": "بخت‌نصر دوم"},
        hints={
            "ar": "ملك بابل العظيم الذي بنى حدائق بابل المعلقة ودمر أورشليم.",
            "en": "Greatest king of the Neo-Babylonian Empire who built the Hanging Gardens.",
            "es": "El rey más grande del Imperio Neobabilónico que construyó los Jardines Colgantes.",
            "fr": "Le plus grand roi de l'Empire néo-babylonien qui construisit les Jardins suspendus.",
            "de": "Bedeutendster König des Neubabylonischen Reiches, der die Hängenden Gärten erbaute.",
            "pt": "O maior rei do Império Neobabilônico que construiu os Jardins Suspensos.",
            "it": "Il più grande re dell'Impero Neobabilonese che costruì i Giardini Pensili.",
            "tr": "Asma Bahçeleri inşa eden Yeni Babil İmparatorluğu'nun en büyük kralı.",
            "ru": "Величайший царь Нововавилонского царства, построивший Висячие сады.",
            "ja": "バビロンの空中庭園を建設した新バビロニア王国の最盛期の王。",
            "ko": "바빌론의 공중정원을 건설한 신바빌로니아 제국의 위대한 왕.",
            "zh": "修建巴比伦空中花园并征服耶路撒冷的新巴比伦帝国最伟大的国王。",
            "hi": "नव-बेबीलोन साम्राज्य के सबसे महान राजा जिन्होंने हैंगिंग गार्डन्स का निर्माण कराया।",
            "id": "Raja terbesar Kekaisaran Neo-Babilonia yang membangun Taman Gantung.",
            "fa": "بزرگ‌ترین پادشاه امپراتوری بابلی نو که باغ‌های معلق بابل را ساخت."
        },
        bios={
            "ar": "أعظم ملوك الإمبراطورية البابلية الحديثة، شهد عهده بناء حدائق بابل المعلقة وتدمير هيكل أورشليم وسبي اليهود إلى بابل.",
            "en": "Longest-reigning king of the Neo-Babylonian Empire who constructed the Hanging Gardens and conquered Jerusalem.",
            "es": "El rey más longevo del Imperio Neobabilónico, quien construyó los Jardines Colgantes y conquistó Jerusalén.",
            "fr": "Roi au plus long règne de l'Empire néo-babylonien, qui construisit les Jardins suspendus et conquit Jérusalem.",
            "de": "Am längsten regierender König des Neubabylonischen Reiches, der die Hängenden Gärten erbaute und Jerusalem eroberte.",
            "pt": "O rei de mais longo reinado do Império Neobabilônico, que construiu os Jardines Suspensos e conquistou Jerusalém.",
            "it": "Il re con il regno più lungo dell'Impero Neobabilonese, che costruì i Giardini Pensili e conquistò Gerusalemme.",
            "tr": "Asma Bahçeleri inşa eden ve Kudüs'ü fetheden Yeni Babil İmparatorluğu'nun en uzun süre hüküm süren kralı.",
            "ru": "Дольше всех правивший царь Нововавилонского царства, построивший Висячие сады и завоевавший Иерусалим.",
            "ja": "新バビロニア王国の最盛期を築き、空中庭園の建設やエルサレム攻略で知られる王。",
            "ko": "바빌론의 공중정원을 건설하고 예루살렘을 정복한 신바빌로니아의 최장수 통치 왕.",
            "zh": "新巴比伦帝国统治时间最长的国王，建造了巴比伦空中花园并占领了耶路撒冷。",
            "hi": "नव-बेबीलोन साम्राज्य के सबसे लंबे समय तक शासन करने वाले राजा, जिन्होंने हैंगिंग गार्डन्स बनवाए और यरूशलेम जीता।",
            "id": "Raja terlama yang memerintah Kekaisaran Neo-Babilonia yang membangun Taman Gantung dan menaklukkan Yerusalem.",
            "fa": "طولانی‌ترین دوران سلطنت را در امپراتوری بابلی نو داشت و باغ‌های معلق بابل را ساخت و اورشلیم را فتح کرد."
        },
        bcities={"ar": "بابل", "en": "Babylon", "es": "Babilonia", "fr": "Babylone", "de": "Babylon", "pt": "Babilônia", "it": "Babilonia", "tr": "Babil", "ru": "Вавилон", "ja": "バビロン", "ko": "바빌론", "zh": "巴比伦", "hi": "बेबीलोन", "id": "Babilonia", "fa": "بابل"},
        bcountries={"ar": "بلاد الرافدين", "en": "Mesopotamia", "es": "Mesopotamia", "fr": "Mésopotamie", "de": "Mesopotamien", "pt": "Mesopotâmia", "it": "Mesopotamia", "tr": "Mezopotamya", "ru": "Месопотамия", "ja": "メソポタミア", "ko": "메소포타미아", "zh": "美索不达米亚", "hi": "मेसोपोटेमिया", "id": "Mesopotamia", "fa": "بین‌النهرین"},
        dcities={"ar": "بابل", "en": "Babylon", "es": "Babilonia", "fr": "Babylone", "de": "Babylon", "pt": "Babilônia", "it": "Babilonia", "tr": "Babil", "ru": "Вавилон", "ja": "バビロン", "ko": "바빌론", "zh": "巴比伦", "hi": "बेबीलोन", "id": "Babilonia", "fa": "بابل"},
        dcountries={"ar": "بلاد الرافدين", "en": "Mesopotamia", "es": "Mesopotamia", "fr": "Mésopotamie", "de": "Mesopotamien", "pt": "Mesopotâmia", "it": "Mesopotamia", "tr": "Mezopotamya", "ru": "Месопотамия", "ja": "メソポタミア", "ko": "메소포타미아", "zh": "美索不达米亚", "hi": "मेसोपोटेमिया", "id": "Mesopotamia", "fa": "بین‌النهرین"},
        roles={"ar": "ملك الإمبراطورية البابلية الحديثة", "en": "King of the Neo-Babylonian Empire", "es": "Rey del Imperio Neobabilónico", "fr": "Roi de l'Empire néo-babylonien", "de": "König des Neubabylonischen Reiches", "pt": "Rei do Império Neobabilônico", "it": "Re dell'Impero Neobabilonese", "tr": "Yeni Babil İmparatorluğu Kralı", "ru": "Царь Нововавилонского царства", "ja": "新バビロニア国王", "ko": "신바빌로니아의 왕", "zh": "新巴比伦帝国国王", "hi": "नव-बेबीलोन साम्राज्य के राजा", "id": "Raja Kekaisaran Neo-Babilonia", "fa": "پادشاه امپراتوری بابلی نو"},
        eras=ERA_ANCIENT,
        achs={
            "ar": ["بنى حدائق بابل المعلقة، إحدى عجائب الدنيا السبع في العالم القديم.", "أعاد بناء بابل وحولها إلى عاصمة فاخرة وبنى بوابة عشتار الشهيرة.", "وسع نفوذ الإمبراطورية البابلية الحديثة عبر بلاد الشام ومصر والرافدين."],
            "en": ["Built the Hanging Gardens of Babylon, one of the Seven Wonders of the Ancient World.", "Rebuilt Babylon into a magnificent capital and constructed the famous Ishtar Gate.", "Expanded the Neo-Babylonian Empire across Syria, Judah, and Mesopotamia."],
            "es": ["Construyó los Jardines Colgantes de Babilonia, una de las Siete Maravillas del Mundo Antiguo.", "Reconstruyó Babilonia como una espléndida capital y erigió la famosa Puerta de Ishtar.", "Expandió el Imperio Neobabilónico por Siria, Judá y Mesopotamia."],
            "fr": ["Construisit les Jardins suspendus de Babylone, l'une des Sept Merveilles du monde antique.", "Reconstruisit Babylone en une capitale splendide et érigea la célèbre Porte d'Ishtar.", "Étendit l'Empire néo-babylonien à travers la Syrie, la Judée et la Mésopotamie."],
            "de": ["Erbaute die Hängenden Gärten von Babylon, eines der Sieben Weltwunder der Antike.", "Baute Babylon zu einer prachtvollen Hauptstadt mit dem berühmten Ischtar-Tor aus.", "Erweiterte das Neubabylonische Reich über Syrien, Juda und Mesopotamien."],
            "pt": ["Construiu os Jardines Suspensos da Babilônia, uma das Sete Maravilhas do Mundo Antigo.", "Reconstruiu a Babilônia em uma capital magnífica e construiu a famosa Porta de Ishtar.", "Expandiu o Império Neobabilônico pela Síria, Judá e Mesopotâmia."],
            "it": ["Costruì i Giardini Pensili di Babilonia, una delle Sette Meraviglie del Mondo Antico.", "Ricostruì Babilonia trasformandola in una splendida capitale ed eresse la Porta di Ishtar.", "Espanse l'Impero Neobabilonese in Siria, Giudea e Mesopotamia."],
            "tr": ["Antik Dünyanın Yedi Harikası'ndan biri olan Babil'in Asma Bahçeleri'ni inşa etti.", "Babil'i muhteşem bir başkent olarak yeniden inşa etti ve ünlü İştar Kapısı'nı yaptırdı.", "Yeni Babil İmparatorluğu'nu Suriye, Yahuda ve Mezopotamya'ya genişletti."],
            "ru": ["Построил Висячие сады Вавилона, одно из Семи чудес света древнего мира.", "Перестроил Вавилон в великолепную столицу и возвёл знаменитые ворота Иштар.", "Расширил Нововавилонское царство на Сирию, Иудею и Месопотамию."],
            "ja": ["古代世界の七大不思議の一つであるバビロンの空中庭園を建設した。", "バビロンを壮大な首都として再建し、有名なイシュタル門を建造した。", "新バビロニア王国の領土をシリア、ユダ、メソポタミア全域に拡大した。"],
            "ko": ["고대 세계 7대 불가사의 중 하나인 바빌론의 공중정원을 건설했다.", "바빌론을 화려한 수도로 재건하고 유명한 이슈타르 문을 지었다.", "신바빌로니아 제국을 시리아, 유다, 메소포타미아 지역으로 확장했다."],
            "zh": ["修建了古代世界七大奇迹之一的巴比伦空中花园。", "将巴比伦重建成宏伟的首都并建造了著名的伊什塔尔门。", "将新巴比伦帝国的版图拓展至叙利亚、犹大和美索不达米亚。"],
            "hi": ["प्राचीन दुनिया के सात अजूबों में से एक, बेबीलोन के हैंगिंग गार्डन्स का निर्माण कराया।", "बेबीलोन को एक शानदार राजधानी के रूप में पुनर्निर्मित किया और प्रसिद्ध इश्तार द्वार बनवाया।", "सीरिया, यहूदा और मेसोपोटेमिया में नव-बेबीलोन साम्राज्य का विस्तार किया।"],
            "id": ["Membangun Taman Gantung Babilonia, salah satu dari Tujuh Keajaiban Dunia Kuno.", "Membangun kembali Babilonia menjadi ibu kota yang megah dan mendirikan Gerbang Ishtar.", "Meluaskan Kekaisaran Neo-Babilonia ke seluruh Suriah, Yuda, dan Mesopotamia."],
            "fa": ["باغ‌های معلق بابل، یکی از عجایب هفت‌گانه جهان باستان را ساخت.", "بابل را به پایتختی شکوهمند تبدیل کرد و دروازه معروف ایشتار را بنا نهاد.", "امپراتوری بابلی نو را در سراسر سوریه، یهودیه و بین‌النهرین گسترش داد."]
        },
        facts={
            "ar": ["حكم الإمبراطورية البابلية الحديثة لمدة 43 عاماً.", "دمر هيكل سليمان في أورشليم عام 587 قبل الميلاد وبدأ السبي البابلي.", "ذُكر اسمه بشكل بارز في سفر دانيال في العهد القديم."],
            "en": ["Ruled the Neo-Babylonian Empire for 43 years.", "Destroyed Solomon's Temple in Jerusalem in 587 BCE, starting the Babylonian Captivity.", "Prominently featured in the biblical Book of Daniel."],
            "es": ["Gobernó el Imperio Neobabilónico durante 43 años.", "Destruyó el Templo de Salomón en Jerusalén en 587 a.C., iniciando el Cautiverio de Babilonia.", "Aparece de forma destacada en el libro bíblico de Daniel."],
            "fr": ["Régna sur l'Empire néo-babylonien pendant 43 ans.", "Détruisit le Temple de Salomon à Jérusalem en 587 av. J.-C., début de la Captivité à Babylone.", "Figure de manière prominente dans le Livre de Daniel dans la Bible."],
            "de": ["Regierte das Neubabylonische Reich 43 Jahre lang.", "Zerstörte 587 v. Chr. den Salomonischen Tempel in Jerusalem und leitete das Babylonische Exil ein.", "Wird im biblischen Buch Daniel ausführlich erwähnt."],
            "pt": ["Governou o Império Neobabilônico por 43 anos.", "Destruiu o Templo de Salomão em Jerusalém em 587 a.C., iniciando o Cativeiro Babilônico.", "Mencionado com destaque no livro bíblico de Daniel."],
            "it": ["Governò l'Impero Neobabilonese per 43 anni.", "Distrusse il Tempio di Salomone a Gerusalemme nel 587 a.C., dando inizio alla Cattività babilonese.", "Menzionato in modo prominente nel Libro di Daniele nella Bibbia."],
            "tr": ["Yeni Babil İmparatorluğu'nu 43 yıl boyunca yönetti.", "MÖ 587'de Kudüs'teki Süleyman Mabedi'ni yıkarak Babil Sürgününü başlattı.", "Kutsal Kitap'ın Daniel bölümünde önemli bir yer tutar."],
            "ru": ["Правил Нововавилонским царством 43 года.", "Разрушил Храм Соломона в Иерусалиме в 587 г. до н.э., начав Вавилонский плен.", "Широко известен по упоминаниям в библейской Книге пророка Даниила."],
            "ja": ["新バビロニア王国を43年間にわたり統治した。", "紀元前587年にエルサレムのソロモン神殿を破壊し、バビロン捕囚を引き起こした。", "旧約聖書の『ダニエル書』に重要人物として登場する。"],
            "ko": ["신바빌로니아 제국을 43년 동안 통치했다.", "기원전 587년 예루살렘의 솔로몬 성전을 파괴하고 바빌론 유수를 일으켰다.", "성경의 다니엘서에 비중 있게 등장한다."],
            "zh": ["统治新巴比伦帝国长达43年。", "公元前587年摧毁了耶路撒冷的所罗门圣殿，引发了“巴比伦之囚”。", "在圣经《但以理书》中有重要记载。"],
            "hi": ["43 वर्षों तक नव-बेबीलोन साम्राज्य पर शासन किया।", "587 ईसा पूर्व में यरूशलेम में सुलेमान के मंदिर को नष्ट कर बेबीलोन की गुलामी शुरू की।", "बाइबल की डैनियल की पुस्तक में प्रमुखता से उल्लेखित हैं।"],
            "id": ["Memerintah Kekaisaran Neo-Babilonia selama 43 tahun.", "Hancurkan Bait Salomo di Yerusalem pada 587 SM, memulai Pembuangan Babilonia.", "Disebutkan secara menonjol dalam Kitab Daniel di Alkitab."],
            "fa": ["۴۳ سال بر امپراتوری بابلی نو حکومت کرد.", "معبد سلیمان در اورشلیم را در ۵۸۷ پیش از میلاد ویران کرد و اسارت بابلی را آغاز نمود.", "در کتاب دانیال در کتاب مقدس حضور پررنگی دارد."]
        },
        wars={
            "ar": ["معركة كركميش (605 ق.م.)", "حصار أورشليم (587 ق.م.)"],
            "en": ["Battle of Carchemish (605 BCE)", "Siege of Jerusalem (587 BCE)"],
            "es": ["Batalla de Carquemis (605 a.C.)", "Sitio de Jerusalén (587 a.C.)"],
            "fr": ["Bataille de Karkemish (605 av. J.-C.)", "Siège de Jérusalem (587 av. J.-C.)"],
            "de": ["Schlacht bei Karkemisch (605 v. Chr.)", "Belagerung von Jerusalem (587 v. Chr.)"],
            "pt": ["Batalha de Carquemis (605 a.C.)", "Cerco de Jerusalém (587 a.C.)"],
            "it": ["Battaglia di Carchemish (605 a.C.)", "Assedio di Gerusalemme (587 a.C.)"],
            "tr": ["Karkamış Savaşı (MÖ 605)", "Kudüs Kuşatması (MÖ 587)"],
            "ru": ["Битва при Каркемише (605 г. до н.э.)", "Осада Иерусалима (587 г. до н.э.)"],
            "ja": ["カルケミシュの戦い（紀元前605年）", "エルサレム包囲戦（紀元前587年）"],
            "ko": ["갈그미스 전투 (기원전 605년)", "예루살렘 공성전 (기원전 587년)"],
            "zh": ["卡尔克米什战役（公元前605年）", "耶路撒冷之围（公元前587年）"],
            "hi": ["कारकेमिश की लड़ाई (605 ईसा पूर्व)", "यरूशलेम की घेराबंदी (587 ईसा पूर्व)"],
            "id": ["Pertempuran Karkemis (605 SM)", "Pengepungan Yerusalem (587 SM)"],
            "fa": ["نبرد کرکمیش (۶۰۵ پیش از میلاد)", "محاصره اورشلیم (۵۸۷ پیش از میلاد)"]
        },
        sigs={
            "ar": "تعتبر فترة حكمه أوج الحضارة البابلية الحديثة، وترك أثراً معمارياً وتاريخياً خالدة في الشرق الأدنى القديم.",
            "en": "His reign marked the zenith of the Neo-Babylonian Empire, leaving architectural and geopolitical legacies that defined the ancient Near East.",
            "es": "Su reinado marcó el apogeo del Imperio Neobabilónico, dejando un legado arquitectónico y geopolítico duradero.",
            "fr": "Son règne marqua l'apogée de l'Empire néo-babylonien, laissant un héritage architectural et géopolitique majeur.",
            "de": "Seine Herrschaft markierte den Höhepunkt des Neubabylonischen Reiches und hinterließ ein bedeutendes architektonisches Erbe.",
            "pt": "Seu reinado marcou o apogeu do Império Neobabilônico, deixando um legado arquitetônico e geopolítico duradouro.",
            "it": "Il suo regno segnò l'apogeo dell'Impero Neobabilonese, lasciando un'eredità architettonica e geopolitica indelebile.",
            "tr": "Hükümdarlığı Yeni Babil İmparatorluğu'nun zirvesini simgelemiş ve antik Yakın Doğu'da kalıcı izler bırakmıştır.",
            "ru": "Его правление стало расцветом Нововавилонского царства, оставившим значительное архитектурное и историческое наследие.",
            "ja": "その治世は新バビロニア王国の絶頂期であり、古代近東に巨額の建築的・地政学的遺産を残した。",
            "ko": "그의 통치는 신바빌로니아 제국의 전성기였으며 고대 근동에 지대한 건축적, 역사적 유산을 남겼다.",
            "zh": "他的统治标志着新巴比伦帝国的鼎盛时期，为古代近东留下了丰厚的建筑与历史遗存。",
            "hi": "उनका शासनकाल नव-बेबीलोन साम्राज्य के चरमोत्कर्ष का प्रतीक था, जिसने प्राचीन निकट पूर्व पर स्थायी छाप छोड़ी।",
            "id": "Pemerintahannya menandai puncak Kekaisaran Neo-Babilonia, meninggalkan warisan arsitektur dan sejarah yang bertahan lama.",
            "fa": "دوران حکومت او اوج امپراتوری بابلی نو بود و میراث معماری و تاریخی پایداری در خاور نزدیک باستان به جای گذاشت."
        }
    )
}

out_path = Path("tools/new_chars_batch1.py")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""\nNEW_CHARS_1 dictionary for 12 new characters.\n"""\n\n')
    f.write("NEW_CHARS_1 = ")
    json.dump(NEW_CHARS_1, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(f"Partial write: {len(NEW_CHARS_1)} chars in {out_path}")
