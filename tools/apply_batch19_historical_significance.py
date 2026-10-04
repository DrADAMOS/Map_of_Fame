from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"


PT = {
"Johann Wolfgang von Goethe": "Sua obra reuniu poesia, teatro, romance e reflexأ£o intelectual, tornando-o uma figura central da literatura alemأ£ e do classicismo de Weimar.",
"Alexandre Dumas": "Seus romances histأ³ricos popularizaram personagens e episأ³dios do passado europeu e fizeram dele um dos grandes nomes da narrativa de aventura do sأ©culo XIX.",
"Victor Hugo": "Sua poesia, seus romances e seu teatro marcaram profundamente a literatura francesa, enquanto sua atuaأ§أ£o pأ؛blica o tornou uma voz importante contra a pena de morte e pela justiأ§a social.",
"Fyodor Dostoevsky": "Seus romances exploraram conflitos morais, psicolأ³gicos e religiosos com profundidade incomum, influenciando decisivamente a literatura moderna e a psicologia da ficأ§أ£o.",
"Gustave Flaubert": "Sua busca por precisأ£o estilأ­stica e observaأ§أ£o social fez de Madame Bovary um marco do realismo e exerceu grande influأھncia sobre a narrativa moderna.",
"Leo Tolstoy": "Romances como Guerra e Paz e Anna Kariأھnina combinaram anأ،lise histأ³rica, psicolأ³gica e moral em uma das obras mais influentes da literatura mundial.",
"Oscar Wilde": "Seu humor, aforismos e crأ­tica das convenأ§أµes sociais fizeram dele uma figura marcante da literatura e da cultura britأ¢nicas do fim do sأ©culo XIX.",
"George Bernard Shaw": "Suas peأ§as uniram sأ،tira, debate polأ­tico e crأ­tica social, ajudando a renovar o teatro de lأ­ngua inglesa e influenciando o pensamento pأ؛blico sobre reformas sociais.",
"Anton Chekhov": "Seus contos e peأ§as transformaram a representaأ§أ£o da vida cotidiana, dos conflitos interiores e das relaأ§أµes humanas, tornando-se fundamentais para o teatro moderno.",
"Rudyard Kipling": "Sua poesia e sua ficأ§أ£o ajudaram a definir parte da literatura britأ¢nica do perأ­odo imperial, enquanto obras como O Livro da Selva alcanأ§aram projeأ§أ£o mundial.",
"H. G. Wells": "Seus romances ajudaram a estabelecer a ficأ§أ£o cientأ­fica moderna ao imaginar viagens no tempo, invasأµes extraterrestres e transformaأ§أµes tecnolأ³gicas com forte crأ­tica social.",
"Marcel Proust": "Em Em Busca do Tempo Perdido, desenvolveu uma exploraأ§أ£o inovadora da memأ³ria, da percepأ§أ£o e da passagem do tempo que redefiniu possibilidades do romance moderno.",
"James Joyce": "Suas experiأھncias com linguagem, fluxo de consciأھncia e estrutura narrativa, especialmente em Ulisses, tiveram impacto decisivo na literatura modernista.",
"Kahlil Gibran": "Sua poesia e prosa, sobretudo O Profeta, aproximaram tradiأ§أµes literأ،rias orientais e ocidentais e alcanأ§aram enorme circulaأ§أ£o internacional.",
"Franz Kafka": "Sua ficأ§أ£o apresentou situaأ§أµes de alienaأ§أ£o, burocracia e absurdo que se tornaram referأھncias centrais para a literatura moderna e para a cultura do sأ©culo XX.",
"Abbas al-Aqqad": "Sua extensa produأ§أ£o literأ،ria e intelectual contribuiu para a renovaأ§أ£o da literatura أ،rabe moderna, especialmente por meio da crأ­tica, da biografia e da poesia.",
"Ernest Hemingway": "Seu estilo conciso e sua tأ©cnica narrativa influenciaram profundamente a prosa do sأ©culo XX, com obras como O Velho e o Mar e Adeus أ s Armas.",
"Jorge Luis Borges": "Seus contos sobre labirintos, tempo, identidade e livros imaginأ،rios ampliaram as possibilidades da ficأ§أ£o e exerceram influأھncia mundial sobre a literatura contemporأ¢nea.",
"George Orwell": "Suas obras de crأ­tica polأ­tica, especialmente 1984 e A Revoluأ§أ£o dos Bichos, tornaram-se referأھncias duradouras para o debate sobre totalitarismo, propaganda e liberdade.",
"Pablo Neruda": "Sua poesia combinou amor, natureza, polأ­tica e experiأھncia histأ³rica e teve grande impacto na literatura hispano-americana e mundial.",
"Albert Camus": "Seus romances, ensaios e peأ§as exploraram o absurdo, a liberdade e a responsabilidade moral, tornando-o uma das principais vozes intelectuais da Franأ§a do pأ³s-guerra.",
"Badr Shakir al-Sayyab": "Sua renovaأ§أ£o da poesia أ،rabe por meio do verso livre fez dele uma das figuras fundamentais do movimento poأ©tico moderno no mundo أ،rabe.",
"Gabriel García Márquez": "Sua fusأ£o de histأ³ria, mito e cotidiano em obras como Cem Anos de Solidأ£o tornou-se um dos sأ­mbolos do realismo mأ،gico e da literatura latino-americana.",
"Mahmoud Darwish": "Sua poesia articulou identidade, exأ­lio, memأ³ria e experiأھncia palestina, tornando-se uma das vozes mais influentes da poesia أ،rabe contemporأ¢nea.",
"Joseph Haydn": "Sua longa produأ§أ£o sinfأ´nica e camerأ­stica ajudou a consolidar formas do perأ­odo clأ،ssico, influenciando diretamente Mozart e Beethoven.",
"Wolfgang Amadeus Mozart": "Sua produأ§أ£o em أ³pera, sinfonia, concerto e mأ؛sica de cأ¢mara tornou-se um dos pilares do repertأ³rio clأ،ssico e permanece central na histأ³ria da mأ؛sica ocidental.",
"Ludwig van Beethoven": "Suas sinfonias e sonatas ampliaram a escala expressiva da mأ؛sica clأ،ssica e abriram caminho para o romantismo musical.",
"Gioachino Rossini": "Suas أ³peras, especialmente O Barbeiro de Sevilha e Guilherme Tell, marcaram a أ³pera italiana do sأ©culo XIX e consolidaram seu domأ­nio da escrita vocal e cأ´mica.",
"Frédéric Chopin": "Suas obras para piano elevaram o instrumento a um novo nأ­vel de expressأ£o e tornaram-se fundamentais para o repertأ³rio romأ¢ntico.",
"Richard Wagner": "Suas أ³peras e sua concepأ§أ£o de drama musical transformaram o teatro lأ­rico europeu e influenciaram profundamente a mأ؛sica do final do sأ©culo XIX.",
"Giuseppe Verdi": "Suas أ³peras combinaram forأ§a dramأ،tica, caracterizaأ§أ£o vocal e melodias memorأ،veis, tornando-o uma das figuras decisivas da أ³pera italiana.",
"Johannes Brahms": "Sua mأ؛sica conciliou tradiأ§أ£o clأ،ssica e linguagem romأ¢ntica, produzindo sinfonias, concertos e mأ؛sica de cأ¢mara que se tornaram pilares do repertأ³rio ocidental.",
"Pyotr Tchaikovsky": "Suas sinfonias, concertos e balأ©s, incluindo O Lago dos Cisnes e O Quebra-Nozes, tornaram-se obras centrais do romantismo musical russo e internacional.",
"Gustav Mahler": "Suas sinfonias ampliaram dramaticamente a escala e a ambiأ§أ£o da forma sinfأ´nica, ligando o romantismo tardio أ s transformaأ§أµes musicais do sأ©culo XX.",
"Sergei Rachmaninoff": "Sua escrita pianأ­stica e suas obras orquestrais combinaram virtuosismo, lirismo e tradiأ§أ£o romأ¢ntica, mantendo forte presenأ§a no repertأ³rio concertأ­stico.",
"Igor Stravinsky": "Obras como A Sagraأ§أ£o da Primavera revolucionaram o ritmo e a linguagem musical do sأ©culo XX e fizeram dele uma figura central do modernismo.",
"Sergei Prokofiev": "Sua mأ؛sica combinou ritmos incisivos, melodias marcantes e experimentaأ§أ£o harmأ´nica em obras que atravessaram a mأ؛sica soviأ©tica e o repertأ³rio internacional.",
"Dmitri Shostakovich": "Suas sinfonias e quartetos refletiram as tensأµes polأ­ticas e pessoais da vida soviأ©tica e tornaram-se testemunhos importantes da mأ؛sica do sأ©culo XX.",
"Elvis Presley": "Sua combinaأ§أ£o de country, blues e ritmo e blues ajudou a popularizar o rock and roll e transformou a mأ؛sica popular e a cultura de massas do sأ©culo XX.",
"John Lennon": "Como integrante dos Beatles e posteriormente artista solo, combinou composiأ§أ£o popular e ativismo pela paz, deixando forte impacto cultural alأ©m da mأ؛sica.",
"Jim Morrison": "Como vocalista e letrista do The Doors, contribuiu para definir a estأ©tica do rock psicodأ©lico e tornou-se um أ­cone da contracultura dos anos 1960.",
"Bob Marley": "Sua mأ؛sica levou o reggae a uma audiأھncia global e associou canأ§أµes de forte dimensأ£o social e espiritual أ  identidade cultural jamaicana.",
"Freddie Mercury": "Sua voz, presenأ§a de palco e composiأ§أ£o ajudaram a transformar o Queen em uma das bandas mais influentes do rock, com impacto duradouro na mأ؛sica popular.",
"Michael Jackson": "Sua combinaأ§أ£o de canto, danأ§a, videoclipes e produأ§أ£o transformou a mأ؛sica pop mundial e estabeleceu novos padrأµes de espetأ،culo na indأ؛stria fonogrأ،fica.",
}

TR = {
"Johann Wolfgang von Goethe": "إ‍iir, tiyatro, roman ve dأ¼إںأ¼nceyi bir araya getiren eserleri Goethe'yi Alman edebiyatؤ±nؤ±n ve Weimar Klasisizminin temel figأ¼rlerinden biri yaptؤ±.",
"Jane Austen": "Romanlarؤ± sؤ±nؤ±f, evlilik, toplumsal beklentiler ve kadؤ±nlarؤ±n konumunu inceleyerek ؤ°ngiliz romanؤ±nؤ±n kalؤ±cؤ± klasiklerinden biri haline geldi.",
"Alexandre Dumas": "Tarihsel romanlarؤ± Avrupa geأ§miإںinden olaylarؤ± ve karakterleri geniإں okur kitlelerine taإںؤ±yarak on dokuzuncu yأ¼zyؤ±l macera edebiyatؤ±nؤ±n baإںlؤ±ca adlarؤ±ndan biri oldu.",
"Victor Hugo": "إ‍iir, roman ve tiyatro eserleri Fransؤ±z edebiyatؤ±nؤ± derinden etkiledi; kamu yaإںamؤ±ndaki tutumu da أ¶lأ¼m cezasؤ±na ve toplumsal adaletsizliؤںe karإںؤ± gأ¼أ§lأ¼ bir ses oluإںturdu.",
"Fyodor Dostoevsky": "Romanlarؤ± ahlaki, psikolojik ve dinsel أ§atؤ±إںmalarؤ± derinlemesine iإںleyerek modern edebiyatؤ±n ve psikolojik romanؤ±n geliإںimini gأ¼أ§lأ¼ biأ§imde etkiledi.",
"Gustave Flaubert": "أœsluptaki titizliؤںi ve toplum gأ¶zlemi, Madame Bovary'yi realizmin dأ¶nأ¼m noktalarؤ±ndan biri yaptؤ± ve modern anlatؤ± أ¼zerinde bأ¼yأ¼k etki bؤ±raktؤ±.",
"Leo Tolstoy": "Savaإں ve Barؤ±إں ile Anna Karenina gibi eserleri tarih, psikoloji ve ahlakؤ± birleإںtirerek dأ¼nya edebiyatؤ±nؤ±n en etkili romanlarؤ± arasؤ±nda yer aldؤ±.",
"Oscar Wilde": "Nأ¼ktesi, aforizmalarؤ± ve toplumsal geleneklere yأ¶nelik eleإںtirileri onu on dokuzuncu yأ¼zyؤ±l sonu ؤ°ngiliz edebiyatؤ±nؤ±n ayؤ±rt edici figأ¼rlerinden biri yaptؤ±.",
"George Bernard Shaw": "Oyunlarؤ±nda hiciv, siyasal tartؤ±إںma ve toplumsal eleإںtiriyi birleإںtirerek ؤ°ngiliz tiyatrosunun yenilenmesine ve reform tartؤ±إںmalarؤ±na katkؤ±da bulundu.",
"Anton Chekhov": "أ–ykأ¼leri ve oyunlarؤ± gأ¼ndelik hayatؤ±, iأ§ أ§atؤ±إںmalarؤ± ve insan iliإںkilerini yeni bir incelikle iإںleyerek modern tiyatronun temel kaynaklarؤ±ndan biri oldu.",
"Rudyard Kipling": "إ‍iir ve أ¶ykأ¼leri Britanya ؤ°mparatorluؤںu dأ¶neminin edebiyatؤ±nؤ± etkiledi; أ¶zellikle Orman Kitabؤ± gibi eserleri dأ¼nya أ§apؤ±nda kalؤ±cؤ± أ¼n kazandؤ±.",
"H. G. Wells": "Zaman yolculuؤںu, uzaylؤ± istilasؤ± ve teknolojik dأ¶nأ¼إںأ¼m gibi fikirleri toplumsal eleإںtiriyle birleإںtirerek modern bilimkurgunun geliإںmesinde أ¶ncأ¼ rol oynadؤ±.",
"Marcel Proust": "Kayؤ±p Zamanؤ±n ؤ°zinde'de hafؤ±za, algؤ± ve zamanؤ±n geأ§iإںini yenilikأ§i biأ§imde inceleyerek modern romanؤ±n anlatؤ±m olanaklarؤ±nؤ± geniإںletti.",
"James Joyce": "Dil, bilinأ§ akؤ±إںؤ± ve anlatؤ± yapؤ±sؤ± أ¼zerindeki deneyleri, أ¶zellikle Ulysses, modernist edebiyatؤ±n yأ¶nأ¼nأ¼ belirleyen أ§alؤ±إںmalar arasؤ±nda yer aldؤ±.",
"Virginia Woolf": "Bilinأ§ akؤ±إںؤ±, iأ§ monolog ve kadؤ±nlarؤ±n toplumsal konumu أ¼zerine yenilikأ§i yazؤ±mؤ± modernist ؤ°ngiliz edebiyatؤ±nؤ±n geliإںiminde belirleyici oldu.",
"Kahlil Gibran": "إ‍iir ve dأ¼zyazؤ±sؤ±, أ¶zellikle Ermiإں, Doؤںu ve Batؤ± edebi gelenekleri arasؤ±nda kأ¶prأ¼ kurarak uluslararasؤ± أ¶lأ§ekte geniإں bir okur kitlesine ulaإںtؤ±.",
"Franz Kafka": "Yabancؤ±laإںma, bأ¼rokrasi ve absأ¼rt durumlarؤ± iإںleyen kurgusu modern edebiyatؤ±n temel referanslarؤ±ndan biri haline geldi.",
"May Ziadeh": "Arap edebiyatؤ±nda kadؤ±n yazarlarؤ±n ve entelektأ¼el tartؤ±إںmanؤ±n gأ¶rأ¼nأ¼rlأ¼ؤںأ¼nأ¼ artؤ±ran yazؤ±larؤ±, denemeleri ve edebiyat salonlarؤ±yla modern Arap kأ¼ltأ¼rأ¼nde أ¶nemli bir yer edindi.",
"Abbas al-Aqqad": "Geniإں edebi ve dأ¼إںأ¼nsel أ¼retimi, eleإںtiri, biyografi ve إںiir alanlarؤ±nda modern Arap edebiyatؤ±nؤ±n yenilenmesine أ¶nemli katkؤ±lar saؤںladؤ±.",
}

JA = {
"Johann Wolfgang von Goethe": "è©©م€پوˆ¯و›²م€په°ڈèھ¬م€پو€‌وƒ³م‚’و¨ھو–­مپ—مپںن½œه“پç¾¤مپ«م‚ˆمپ£مپ¦م€پم‚²مƒ¼مƒ†مپ¯مƒ‰م‚¤مƒ„و–‡ه­¦مپ¨مƒ¯م‚¤مƒ‍مƒ¼مƒ«هڈ¤ه…¸ن¸»ç¾©م‚’ن»£è،¨مپ™م‚‹ن¸­ه؟ƒن؛؛ç‰©مپ¨مپھمپ£مپںم€‚",
"Jane Austen": "çµگه©ڑم€پéڑژç´ڑم€پç¤¾ن¼ڑçڑ„وœںه¾…م€په¥³و€§مپ®ç«‹ه ´م‚’é‹­مپڈوڈڈمپ„مپںه°ڈèھ¬مپ«م‚ˆمپ£مپ¦م€پم‚ھمƒ¼م‚¹مƒ†م‚£مƒ³مپ¯è‹±و–‡ه­¦م‚’ن»£è،¨مپ™م‚‹هڈ¤ه…¸ن½œه®¶مپ¨مپھمپ£مپںم€‚",
"Alexandre Dumas": "و­´هڈ²ن¸ٹمپ®ن؛‹ن»¶م‚„ن؛؛ç‰©م‚’ç”ںمپچç”ںمپچمپ¨وڈڈمپڈو­´هڈ²ه°ڈèھ¬مپ«م‚ˆمپ£مپ¦م€پمƒ‡مƒ¥مƒ‍مپ¯19ن¸–ç´€مپ®ه†’é™؛و–‡ه­¦م‚’ن»£è،¨مپ™م‚‹ن½œه®¶مپ®ن¸€ن؛؛مپ¨مپھمپ£مپںم€‚",
"Gustave Flaubert": "و–‡ن½“مپ¸مپ®ه¾¹ه؛•مپ—مپںمپ“مپ م‚ڈم‚ٹمپ¨ç¤¾ن¼ڑè¦³ه¯ںمپ«م‚ˆمپ£مپ¦م€پم€ژمƒœمƒ´م‚،مƒھمƒ¼ه¤«ن؛؛م€ڈم‚’ه†™ه®ںن¸»ç¾©مپ®é‡چè¦پن½œمپ«مپ—م€پè؟‘ن»£ه°ڈèھ¬مپ¸ه¤§مپچمپھه½±éں؟م‚’ن¸ژمپˆمپںم€‚",
"Oscar Wilde": "و©ںçں¥مپ«ه¯Œم‚€è­¦هڈ¥مپ¨ç¤¾ن¼ڑو…£ç؟’مپ¸مپ®و‰¹هˆ¤مپ«م‚ˆمپ£مپ¦م€پمƒ¯م‚¤مƒ«مƒ‰مپ¯19ن¸–ç´€وœ«مپ®è‹±و–‡ه­¦م‚’è±،ه¾´مپ™م‚‹ن½œه®¶مپ®ن¸€ن؛؛مپ¨مپھمپ£مپںم€‚",
"George Bernard Shaw": "é¢¨هˆ؛مپ¨ç¤¾ن¼ڑو‰¹هˆ¤م‚’هٹ‡ن½œمپ«çµگمپ³مپ¤مپ‘م€پè‹±èھ‍هœڈمپ®è؟‘ن»£و¼”هٹ‡مپ¨ç¤¾ن¼ڑو”¹é‌©م‚’م‚پمپگم‚‹ه…¬ه…±çڑ„è­°è«–مپ«ه¤§مپچمپھه½±éں؟م‚’ن¸ژمپˆمپںم€‚",
"Anton Chekhov": "و—¥ه¸¸ç”ںو´»م‚„ه†…é‌¢مپ®è‘›è—¤م€پن؛؛é–“é–¢ن؟‚م‚’ç¹ٹç´°مپ«وڈڈمپ„مپںçں­ç·¨مپ¨وˆ¯و›²مپ¯م€پè؟‘ن»£و¼”هٹ‡مپ¨çں­ç·¨ه°ڈèھ¬مپ®ç™؛ه±•مپ«و±؛ه®ڑçڑ„مپھه½±éں؟م‚’ن¸ژمپˆمپںم€‚",
"Rudyard Kipling": "è©©م‚„ç‰©èھ‍مپ«م‚ˆمپ£مپ¦ه¸‌ه›½وœںمپ®م‚¤م‚®مƒھم‚¹و–‡ه­¦م‚’ن»£è،¨مپ—م€پم€ژم‚¸مƒ£مƒ³م‚°مƒ«مƒ»مƒ–مƒƒم‚¯م€ڈمپھمپ©م‚’é€ڑمپکمپ¦ن¸–ç•Œçڑ„مپھèھ­è€…م‚’çچ²ه¾—مپ—مپںم€‚",
"H. G. Wells": "م‚؟م‚¤مƒ مƒˆمƒ©مƒ™مƒ«م€په®‡ه®™مپ‹م‚‰مپ®ن¾µç•¥م€پوٹ€è،“مپ«م‚ˆم‚‹ç¤¾ن¼ڑه¤‰هŒ–م‚’وڈڈمپچم€پè؟‘ن»£SFمپ®ن¸»è¦پمپھه½¢ه¼ڈمپ¨وƒ³هƒڈهٹ›م‚’ه½¢مپ¥مپڈمپ£مپںم€‚",
"Marcel Proust": "م€ژه¤±م‚ڈم‚Œمپںو™‚م‚’و±‚م‚پمپ¦م€ڈمپ§è¨کو†¶م€پçں¥è¦ڑم€پو™‚é–“مپ®وµپم‚Œم‚’é‌©و–°çڑ„مپ«وڈڈمپچم€پè؟‘ن»£ه°ڈèھ¬مپ®è،¨çڈ¾هڈ¯èƒ½و€§م‚’ه¤§مپچمپڈه؛ƒمپ’مپںم€‚",
"James Joyce": "è¨€èھ‍م€پو„ڈè­کمپ®وµپم‚Œم€پç‰©èھ‍و§‹é€ م‚’ه¤§èƒ†مپ«ه®ںé¨“مپ—م€پمپ¨م‚ٹم‚ڈمپ‘م€ژمƒ¦مƒھم‚·مƒ¼م‚؛م€ڈمپ«م‚ˆمپ£مپ¦مƒ¢مƒ€مƒ‹م‚؛مƒ و–‡ه­¦مپ®و–¹هگ‘و€§م‚’ه¤‰مپˆمپںم€‚",
"Virginia Woolf": "و„ڈè­کمپ®وµپم‚Œم‚„ه†…é‌¢وڈڈه†™م€په¥³و€§مپ®ç¤¾ن¼ڑçڑ„ن½چç½®م‚’é‌©و–°çڑ„مپ«و‰±مپ„م€پè‹±èھ‍هœڈمƒ¢مƒ€مƒ‹م‚؛مƒ و–‡ه­¦مپ®ç™؛ه±•مپ«ه¤§مپچمپڈه¯„ن¸ژمپ—مپںم€‚",
"Kahlil Gibran": "م€ژé گè¨€è€…م€ڈم‚’مپ¯مپکم‚پمپ¨مپ™م‚‹ن½œه“پمپ«م‚ˆمپ£مپ¦و‌±è¥؟مپ®و–‡ه­¦çڑ„ن¼‌çµ±م‚’çµگمپ³مپ¤مپ‘م€په›½éڑ›çڑ„مپ«ه؛ƒمپڈèھ­مپ¾م‚Œم‚‹ن½œه®¶مپ¨مپھمپ£مپںم€‚",
"Franz Kafka": "ç–ژه¤–م€په®کهƒڑهˆ¶م€پن¸چو‌،çگ†م‚’وڈڈمپڈç‹¬ç‰¹مپ®ن½œه“پن¸–ç•Œمپ¯م€پ20ن¸–ç´€و–‡ه­¦مپ®é‡چè¦پمپھهں؛و؛–ç‚¹مپ¨مپھم‚ٹم€په¾Œن¸–مپ®ن½œه®¶مپ«ه؛ƒمپڈه½±éں؟مپ—مپںم€‚",
"May Ziadeh": "è©•è«–م€پéڑڈç­†م€پو–‡ه­¦و´»ه‹•م‚’é€ڑمپکمپ¦è؟‘ن»£م‚¢مƒ©مƒ–و–‡هŒ–مپ«مپٹمپ‘م‚‹ه¥³و€§çں¥è­کن؛؛مپ®ه­کهœ¨و„ںم‚’é«کم‚پم€پو–‡ه­¦çڑ„ن؛¤وµپمپ®é‡چè¦پمپھه ´م‚’ç¯‰مپ„مپںم€‚",
"Abbas al-Aqqad": "و‰¹è©•م€پن¼‌è¨کم€پè©©مپھمپ©ه¹…ه؛ƒمپ„è‘—ن½œمپ«م‚ˆمپ£مپ¦è؟‘ن»£م‚¢مƒ©مƒ–و–‡ه­¦مپ®çں¥çڑ„هں؛ç›¤م‚’ç™؛ه±•مپ•مپ›مپںن»£è،¨çڑ„مپھو–‡ç­†ه®¶مپ®ن¸€ن؛؛مپ§مپ‚م‚‹م€‚",
}

MAPS = {"pt": PT, "tr": TR, "ja": JA}


def main() -> None:
    if not JSON_PATH.exists():
        raise FileNotFoundError(JSON_PATH)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]

    backup_dir = BACKUP_DIR
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = backup_dir / f"person_i18n_before_batch19_{stamp}.json"
    shutil.copy2(JSON_PATH, backup)

    changed = 0
    missing = []

    for lang, mapping in MAPS.items():
        for name, value in mapping.items():
            person = next((p for p in people.values() if isinstance(p, dict) and isinstance(p.get("languages"), dict) and any(isinstance(v, dict) and v.get("name") == name for v in p["languages"].values())), None)
            if person is None:
                missing.append(f"{lang}: {name}")
                continue
            localized = person.setdefault("languages", {}).setdefault(lang, {})
            if localized.get("historical_significance") != value:
                localized["historical_significance"] = value
                changed += 1

    if missing:
        raise RuntimeError("Missing people:\n" + "\n".join(missing))

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Preserve the project's JSON -> JS mirror convention.
    js_text = (
        "/* Auto-generated from person_i18n.json. Do not edit manually. */\n"
        "window.PERSON_I18N = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    )
    JS_PATH.write_text(js_text, encoding="utf-8")

    # Semantic equality check.
    marker = "window.PERSON_I18N = "
    js_data = json.loads(
        JS_PATH.read_text(encoding="utf-8").split(marker, 1)[1].rsplit(";", 1)[0]
    )
    if js_data != data:
        raise RuntimeError("JSON<->JS semantic equality FAILED")

    print(f"Batch 19 applied: {changed} field changes.")
    print(f"Backup JSON: {backup}")
    print("JSON<->JS semantic equality: PASS")
    print(f"PT targets: {len(PT)}")
    print(f"TR targets: {len(TR)}")
    print(f"JA targets: {len(JA)}")


if __name__ == "__main__":
    main()


