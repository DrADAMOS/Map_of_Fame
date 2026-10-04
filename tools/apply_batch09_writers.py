from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"

PEOPLE = {
    "Ovid": {
        "en": ("Roman poet of Metamorphoses", "Ovid transformed Greek and Roman mythology into influential Latin poetry, especially through the Metamorphoses."),
        "fr": ("Poète romain des Métamorphoses", "Ovide a transformé les mythes gréco-romains en une poésie latine majeure, surtout dans les Métamorphoses."),
        "ru": ("Римский поэт «Метаморфоз»", "Овидий превратил греко-римские мифы в выдающуюся латинскую поэзию, прежде всего в «Метаморфозах»."),
        "es": ("Poeta romano de las Metamorfosis", "Ovidio convirtió los mitos grecorromanos en una poesía latina de enorme influencia, especialmente en las Metamorfosis."),
    },
    "Virgil": {
        "en": ("Poet of the Aeneid", "Virgil shaped Latin epic poetry through the Aeneid, an enduring literary account of Rome's legendary origins."),
        "fr": ("Poète de l’Énéide", "Virgile a marqué l’épopée latine avec l’Énéide, récit littéraire durable des origines légendaires de Rome."),
        "ru": ("Автор «Энеиды»", "Вергилий сформировал латинскую эпическую традицию «Энеидой», рассказывающей о легендарных истоках Рима."),
        "es": ("Poeta de la Eneida", "Virgilio transformó la épica latina con la Eneida, relato literario perdurable de los orígenes legendarios de Roma."),
    },
    "Abu Nuwas": {
        "en": ("Abbasid poet of wine verse", "Abu Nuwas became a defining voice of Abbasid Arabic poetry, famous for wine poetry and bold urban themes."),
        "fr": ("Poète abbasside de la poésie bachique", "Abou Nouwas fut une voix majeure de la poésie arabe abbasside, célèbre pour ses poèmes sur le vin et ses thèmes urbains."),
        "ru": ("Аббасидский поэт винной лирики", "Абу Нувас стал одним из ярких голосов арабской поэзии эпохи Аббасидов, прославившись винной лирикой и смелыми городскими темами."),
        "es": ("Poeta abasí de la poesía del vino", "Abu Nuwas fue una voz decisiva de la poesía árabe abasí, célebre por sus versos sobre el vino y sus temas urbanos."),
    },
    "Homer": {
        "en": ("Traditional author of Iliad and Odyssey", "Homer is traditionally credited with the Iliad and Odyssey, foundational epics of Greek literature and Western literary tradition."),
        "fr": ("Auteur traditionnel de l’Iliade et de l’Odyssée", "Homère est traditionnellement considéré comme l’auteur de l’Iliade et de l’Odyssée, épopées fondatrices de la littérature grecque."),
        "ru": ("Традиционный автор «Илиады» и «Одиссеи»", "Гомеру традиционно приписывают «Илиаду» и «Одиссею», основополагающие эпосы греческой и западной литературы."),
        "es": ("Autor tradicional de la Ilíada y la Odisea", "A Homero se le atribuyen tradicionalmente la Ilíada y la Odisea, epopeyas fundamentales de la literatura griega y occidental."),
    },
    "Dante Alighieri": {
        "en": ("Poet of the Divine Comedy", "Dante's Divine Comedy became a foundational work of Italian literature and a major influence on European literary culture."),
        "fr": ("Poète de la Divine Comédie", "La Divine Comédie de Dante est devenue une œuvre fondatrice de la littérature italienne et une influence majeure en Europe."),
        "ru": ("Автор «Божественной комедии»", "«Божественная комедия» Данте стала основополагающим произведением итальянской литературы и оказала огромное влияние на Европу."),
        "es": ("Poeta de la Divina comedia", "La Divina comedia de Dante se convirtió en una obra fundacional de la literatura italiana y en una influencia decisiva en Europa."),
    },
    "Johann Wolfgang von Goethe": {
        "en": ("German author of Faust", "Goethe's Faust and his wider literary work became central to German literature and European Romantic-era culture."),
        "fr": ("Auteur allemand de Faust", "Le Faust de Goethe et son œuvre ont profondément marqué la littérature allemande et la culture européenne."),
        "ru": ("Немецкий автор «Фауста»", "«Фауст» Гёте и его творчество стали центральными явлениями немецкой литературы и европейской культуры."),
        "es": ("Autor alemán de Fausto", "Fausto y la obra de Goethe se convirtieron en pilares de la literatura alemana y de la cultura europea."),
    },
    "Jane Austen": {
        "en": ("Novelist of Regency society", "Jane Austen transformed the English novel through precise social observation, irony, and works such as Pride and Prejudice."),
        "fr": ("Romancière de la société de la Régence", "Jane Austen a renouvelé le roman anglais par son observation sociale, son ironie et des œuvres comme Orgueil et Préjugés."),
        "ru": ("Романистка эпохи Регентства", "Джейн Остин преобразила английский роман точным наблюдением за обществом, иронией и такими произведениями, как «Гордость и предубеждение»."),
        "es": ("Novelista de la sociedad de la Regencia", "Jane Austen transformó la novela inglesa mediante la observación social, la ironía y obras como Orgullo y prejuicio."),
    },
    "Alexandre Dumas": {
        "en": ("French author of The Three Musketeers", "Dumas helped define the historical adventure novel through The Three Musketeers and The Count of Monte Cristo."),
        "fr": ("Auteur français des Trois Mousquetaires", "Dumas a marqué le roman d’aventures historique avec Les Trois Mousquetaires et Le Comte de Monte-Cristo."),
        "ru": ("Французский автор «Трёх мушкетёров»", "Дюма прославил историко-приключенческий роман произведениями «Три мушкетёра» и «Граф Монте-Кристо»."),
        "es": ("Autor francés de Los tres mosqueteros", "Dumas definió la novela histórica de aventuras con Los tres mosqueteros y El conde de Montecristo."),
    },
    "Victor Hugo": {
        "en": ("French author of Les Misérables", "Victor Hugo combined literature and political engagement, leaving major works including Les Misérables and Notre-Dame de Paris."),
        "fr": ("Auteur français des Misérables", "Victor Hugo a uni création littéraire et engagement politique dans des œuvres majeures comme Les Misérables et Notre-Dame de Paris."),
        "ru": ("Французский автор «Отверженных»", "Виктор Гюго соединил литературу и общественно-политическую деятельность в таких произведениях, как «Отверженные» и «Собор Парижской Богоматери»."),
        "es": ("Autor francés de Los miserables", "Victor Hugo unió literatura y compromiso político en obras fundamentales como Los miserables y Nuestra Señora de París."),
    },
    "Fyodor Dostoevsky": {
        "en": ("Russian novelist of psychological fiction", "Dostoevsky explored guilt, faith, freedom, and morality in psychologically intense novels such as Crime and Punishment."),
        "fr": ("Romancier russe de la psychologie", "Dostoïevski a exploré la culpabilité, la foi, la liberté et la morale dans des romans comme Crime et Châtiment."),
        "ru": ("Русский романист психологической прозы", "Достоевский исследовал вину, веру, свободу и нравственность в психологически насыщенных романах, включая «Преступление и наказание»."),
        "es": ("Novelista ruso de la ficción psicológica", "Dostoievski exploró la culpa, la fe, la libertad y la moral en novelas de gran intensidad psicológica como Crimen y castigo."),
    },
    "Gustave Flaubert": {
        "en": ("French realist author of Madame Bovary", "Flaubert reshaped realist prose through rigorous style and Madame Bovary, a landmark of nineteenth-century fiction."),
        "fr": ("Auteur réaliste de Madame Bovary", "Flaubert a renouvelé la prose réaliste par son exigence stylistique et Madame Bovary, œuvre majeure du XIXe siècle."),
        "ru": ("Французский реалист, автор «Мадам Бовари»", "Флобер преобразил реалистическую прозу строгим стилем и романом «Мадам Бовари», ставшим классикой XIX века."),
        "es": ("Autor realista de Madame Bovary", "Flaubert renovó la prosa realista mediante su rigor estilístico y Madame Bovary, obra clave de la narrativa del siglo XIX."),
    },
    "Leo Tolstoy": {
        "en": ("Russian author of War and Peace", "Tolstoy combined vast historical scope with moral and psychological analysis in War and Peace and Anna Karenina."),
        "fr": ("Auteur russe de Guerre et Paix", "Tolstoï a uni fresque historique et analyse morale dans Guerre et Paix et Anna Karénine."),
        "ru": ("Русский автор «Войны и мира»", "Толстой соединил исторический размах с нравственным и психологическим анализом в «Войне и мире» и «Анне Карениной»."),
        "es": ("Autor ruso de Guerra y paz", "Tolstói combinó la amplitud histórica con el análisis moral y psicológico en Guerra y paz y Anna Karénina."),
    },
    "Oscar Wilde": {
        "en": ("Irish author of The Picture of Dorian Gray", "Wilde became a major figure of aestheticism through witty drama, criticism, and The Picture of Dorian Gray."),
        "fr": ("Auteur irlandais du Portrait de Dorian Gray", "Wilde fut une figure majeure de l’esthétisme grâce à son théâtre, sa critique et Le Portrait de Dorian Gray."),
        "ru": ("Ирландский автор «Портрета Дориана Грея»", "Уайльд стал выдающимся представителем эстетизма благодаря пьесам, критике и роману «Портрет Дориана Грея»."),
        "es": ("Autor irlandés de El retrato de Dorian Gray", "Wilde fue una figura central del esteticismo gracias a su teatro, crítica y novela El retrato de Dorian Gray."),
    },
    "George Bernard Shaw": {
        "en": ("Irish playwright and social critic", "Shaw used comedy and drama to challenge social conventions, becoming one of the most influential English-language playwrights."),
        "fr": ("Dramaturge irlandais et critique social", "Shaw a utilisé la comédie et le théâtre pour remettre en cause les conventions sociales et marquer durablement la scène anglophone."),
        "ru": ("Ирландский драматург и социальный критик", "Шоу использовал комедию и драму для критики общественных норм и стал одним из самых влиятельных англоязычных драматургов."),
        "es": ("Dramaturgo irlandés y crítico social", "Shaw utilizó la comedia y el teatro para cuestionar las convenciones sociales y se convirtió en una figura decisiva del teatro en inglés."),
    },
    "Anton Chekhov": {
        "en": ("Russian master of short fiction and drama", "Chekhov transformed short fiction and modern drama through understated characterization and works such as The Cherry Orchard."),
        "fr": ("Maître russe de la nouvelle et du théâtre", "Tchekhov a transformé la nouvelle et le théâtre modernes par ses personnages subtils et des œuvres comme La Cerisaie."),
        "ru": ("Русский мастер рассказа и драмы", "Чехов преобразил малую прозу и современную драму тонкой психологией персонажей и такими пьесами, как «Вишнёвый сад»."),
        "es": ("Maestro ruso del relato y el teatro", "Chéjov transformó el relato breve y el teatro moderno mediante personajes sutiles y obras como El jardín de los cerezos."),
    },
    "Rudyard Kipling": {
        "en": ("British author of The Jungle Book", "Kipling shaped English-language literature with The Jungle Book, Kim, and poems reflecting the British imperial era."),
        "fr": ("Auteur britannique du Livre de la jungle", "Kipling a marqué la littérature anglophone avec Le Livre de la jungle, Kim et une poésie liée à l’époque impériale britannique."),
        "ru": ("Британский автор «Книги джунглей»", "Киплинг оказал влияние на англоязычную литературу произведениями «Книга джунглей», «Ким» и поэзией эпохи Британской империи."),
        "es": ("Autor británico de El libro de la selva", "Kipling marcó la literatura en inglés con El libro de la selva, Kim y una poesía vinculada a la época imperial británica."),
    },
    "H. G. Wells": {
        "en": ("British pioneer of science fiction", "Wells helped establish modern science fiction through The Time Machine, The War of the Worlds, and other speculative novels."),
        "fr": ("Pionnier britannique de la science-fiction", "Wells a contribué à fonder la science-fiction moderne avec La Machine à explorer le temps et La Guerre des mondes."),
        "ru": ("Британский пионер научной фантастики", "Уэллс помог сформировать современную научную фантастику романами «Машина времени» и «Война миров»."),
        "es": ("Pionero británico de la ciencia ficción", "Wells contribuyó a fundar la ciencia ficción moderna con La máquina del tiempo y La guerra de los mundos."),
    },
    "Marcel Proust": {
        "en": ("French author of In Search of Lost Time", "Proust transformed modern fiction through In Search of Lost Time and its exploration of memory, time, and consciousness."),
        "fr": ("Auteur français d’À la recherche du temps perdu", "Proust a transformé le roman moderne avec À la recherche du temps perdu et son exploration de la mémoire et du temps."),
        "ru": ("Французский автор «В поисках утраченного времени»", "Пруст преобразил современную прозу циклом «В поисках утраченного времени», исследуя память, время и сознание."),
        "es": ("Autor francés de En busca del tiempo perdido", "Proust transformó la narrativa moderna con En busca del tiempo perdido y su exploración de la memoria, el tiempo y la conciencia."),
    },
    "James Joyce": {
        "en": ("Irish modernist author of Ulysses", "Joyce revolutionized modernist literature through Ulysses, Dubliners, and experimental approaches to language and consciousness."),
        "fr": ("Auteur irlandais moderniste d’Ulysse", "Joyce a révolutionné la littérature moderniste avec Ulysse, Dubliners et ses expérimentations sur le langage et la conscience."),
        "ru": ("Ирландский модернист, автор «Улисса»", "Джойс преобразил модернистскую литературу романом «Улисс», сборником «Дублинцы» и экспериментами с языком и сознанием."),
        "es": ("Autor irlandés modernista de Ulises", "Joyce revolucionó la literatura modernista con Ulises, Dublineses y sus experimentos sobre el lenguaje y la conciencia."),
    },
    "Virginia Woolf": {
        "en": ("English modernist novelist", "Woolf became a central modernist writer through novels such as Mrs Dalloway and To the Lighthouse and influential feminist essays."),
        "fr": ("Romancière moderniste anglaise", "Virginia Woolf fut une figure centrale du modernisme avec Mrs Dalloway, Vers le phare et des essais féministes influents."),
        "ru": ("Английская писательница-модернистка", "Вирджиния Вулф стала центральной фигурой модернизма благодаря романам «Миссис Дэллоуэй», «На маяк» и феминистским эссе."),
        "es": ("Novelista modernista inglesa", "Virginia Woolf fue una figura central del modernismo con novelas como La señora Dalloway y Al faro y ensayos feministas influyentes."),
    },
    "Kahlil Gibran": {
        "en": ("Lebanese-American author of The Prophet", "Gibran reached a global audience through The Prophet, combining poetic prose with themes of love, spirituality, and human life."),
        "fr": ("Auteur libano-américain du Prophète", "Gibran a touché un public mondial avec Le Prophète, mêlant prose poétique, spiritualité, amour et réflexion sur la vie."),
        "ru": ("Ливано-американский автор «Пророка»", "Джибран получил мировую известность благодаря «Пророку», соединяя поэтическую прозу с темами любви, духовности и человеческой жизни."),
        "es": ("Autor libanés-estadounidense de El profeta", "Gibran alcanzó fama mundial con El profeta, combinando prosa poética con reflexiones sobre el amor, la espiritualidad y la vida."),
    },
    "Franz Kafka": {
        "en": ("Prague modernist author of The Trial", "Kafka's unsettling fiction, including The Trial and The Metamorphosis, became a defining influence on twentieth-century literature."),
        "fr": ("Auteur moderniste de Prague", "Les récits de Kafka, notamment Le Procès et La Métamorphose, ont profondément influencé la littérature du XXe siècle."),
        "ru": ("Пражский писатель-модернист", "Проза Кафки, включая «Процесс» и «Превращение», стала одним из важнейших источников литературы XX века."),
        "es": ("Autor modernista de Praga", "La narrativa inquietante de Kafka, incluida El proceso y La metamorfosis, se convirtió en una influencia decisiva del siglo XX."),
    },
    "May Ziadeh": {
        "en": ("Lebanese-Palestinian writer and intellectual", "May Ziadeh was a pioneering Arab intellectual who promoted literature, education, and women's cultural participation in the early twentieth century."),
        "fr": ("Écrivaine et intellectuelle libano-palestinienne", "May Ziadeh fut une intellectuelle arabe pionnière qui défendit la littérature, l’éducation et la participation culturelle des femmes."),
        "ru": ("Ливано-палестинская писательница и интеллектуалка", "Май Зиаде была выдающейся арабской интеллектуалкой, поддерживавшей литературу, образование и культурное участие женщин."),
        "es": ("Escritora e intelectual libanesa-palestina", "May Ziadeh fue una intelectual árabe pionera que impulsó la literatura, la educación y la participación cultural de las mujeres."),
    },
    "Abbas al-Aqqad": {
        "en": ("Egyptian writer and literary critic", "Al-Aqqad helped shape modern Arabic literary criticism and wrote influential studies of literature, thought, and historical figures."),
        "fr": ("Écrivain et critique littéraire égyptien", "Al-Aqqad a contribué à la critique littéraire arabe moderne par ses études de littérature, de pensée et de grandes figures historiques."),
        "ru": ("Египетский писатель и литературный критик", "Аль-Аккад сыграл важную роль в современной арабской критике, создавая исследования литературы, мысли и исторических деятелей."),
        "es": ("Escritor y crítico literario egipcio", "Al-Aqqad contribuyó decisivamente a la crítica literaria árabe moderna con estudios sobre literatura, pensamiento y figuras históricas."),
    },
    "Ernest Hemingway": {
        "en": ("American author of The Old Man and the Sea", "Hemingway's restrained prose and novels such as The Sun Also Rises influenced twentieth-century fiction and journalism."),
        "fr": ("Auteur américain du Vieil Homme et la Mer", "La prose dépouillée de Hemingway et des œuvres comme Le Soleil se lève aussi ont marqué la fiction et le journalisme du XXe siècle."),
        "ru": ("Американский автор «Старика и моря»", "Сдержанная проза Хемингуэя и такие произведения, как «И восходит солнце», оказали влияние на литературу и журналистику XX века."),
        "es": ("Autor estadounidense de El viejo y el mar", "La prosa contenida de Hemingway y obras como Fiesta influyeron profundamente en la narrativa y el periodismo del siglo XX."),
    },
    "Jorge Luis Borges": {
        "en": ("Argentine master of labyrinthine fiction", "Borges transformed modern literature through stories and essays built around mirrors, labyrinths, infinity, and imagined books."),
        "fr": ("Maître argentin de la fiction labyrinthique", "Borges a transformé la littérature moderne par des récits et essais consacrés aux labyrinthes, aux miroirs, à l’infini et aux livres imaginaires."),
        "ru": ("Аргентинский мастер лабиринтной прозы", "Борхес преобразил современную литературу рассказами и эссе о лабиринтах, зеркалах, бесконечности и вымышленных книгах."),
        "es": ("Maestro argentino de la ficción laberíntica", "Borges transformó la literatura moderna con relatos y ensayos sobre laberintos, espejos, el infinito y libros imaginarios."),
    },
    "George Orwell": {
        "en": ("British author of Nineteen Eighty-Four", "Orwell used fiction and political writing to examine authoritarianism, propaganda, and the corruption of language in the modern age."),
        "fr": ("Auteur britannique de 1984", "Orwell a utilisé la fiction et l’essai politique pour analyser l’autoritarisme, la propagande et la manipulation du langage."),
        "ru": ("Британский автор «1984»", "Оруэлл исследовал авторитаризм, пропаганду и искажение языка в романах и политической публицистике."),
        "es": ("Autor británico de 1984", "Orwell utilizó la ficción y el ensayo político para analizar el autoritarismo, la propaganda y la corrupción del lenguaje."),
    },
    "Pablo Neruda": {
        "en": ("Chilean poet and Nobel laureate", "Neruda became one of Latin America's best-known poets, combining intimate lyricism with political and historical themes."),
        "fr": ("Poète chilien et prix Nobel", "Neruda fut l’un des poètes latino-américains les plus connus, mêlant lyrisme intime, engagement politique et thèmes historiques."),
        "ru": ("Чилийский поэт и лауреат Нобелевской премии", "Неруда стал одним из самых известных поэтов Латинской Америки, соединяя личную лирику с политическими и историческими темами."),
        "es": ("Poeta chileno y premio Nobel", "Neruda fue uno de los poetas más importantes de América Latina, combinando lirismo íntimo con temas políticos e históricos."),
    },
    "Albert Camus": {
        "en": ("French-Algerian writer of The Stranger", "Camus developed influential reflections on absurdity, freedom, and moral responsibility through fiction and essays."),
        "fr": ("Écrivain franco-algérien de L’Étranger", "Camus a développé une réflexion majeure sur l’absurde, la liberté et la responsabilité morale dans ses romans et essais."),
        "ru": ("Франко-алжирский автор «Постороннего»", "Камю развил влиятельное осмысление абсурда, свободы и нравственной ответственности в романах и эссе."),
        "es": ("Autor franco-argelino de El extranjero", "Camus desarrolló una reflexión influyente sobre el absurdo, la libertad y la responsabilidad moral en sus novelas y ensayos."),
    },
    "Nazik al-Malaika": {
        "en": ("Iraqi pioneer of free verse", "Nazik al-Malaika was a pioneering Iraqi poet who helped introduce and theorize free verse in modern Arabic poetry."),
        "fr": ("Pionnière irakienne du vers libre", "Nazik al-Malaika fut une poétesse irakienne pionnière qui contribua à introduire et théoriser le vers libre arabe moderne."),
        "ru": ("Иракская пионерка свободного стиха", "Назик аль-Малаика была одной из основательниц современного арабского свободного стиха и его теоретического осмысления."),
        "es": ("Pionera iraquí del verso libre", "Nazik al-Malaika fue una poeta iraquí pionera en la introducción y teorización del verso libre en la poesía árabe moderna."),
    },
    "Badr Shakir al-Sayyab": {
        "en": ("Iraqi pioneer of modern Arabic poetry", "Al-Sayyab helped establish modern Arabic free verse, bringing personal, political, and mythic imagery into a new poetic form."),
        "fr": ("Pionnier irakien de la poésie arabe moderne", "Al-Sayyab a contribué à établir le vers libre arabe moderne en mêlant expérience personnelle, politique et images mythiques."),
        "ru": ("Иракский пионер современной арабской поэзии", "Аль-Сайяб сыграл ключевую роль в развитии арабского свободного стиха, соединяя личные, политические и мифологические образы."),
        "es": ("Pionero iraquí de la poesía árabe moderna", "Al-Sayyab ayudó a establecer el verso libre árabe moderno, combinando imágenes personales, políticas y míticas."),
    },
    "Gabriel García Márquez": {
        "en": ("Colombian master of magical realism", "García Márquez brought magical realism to a global audience through One Hundred Years of Solitude and his wider fiction."),
        "fr": ("Maître colombien du réalisme magique", "García Márquez a fait connaître le réalisme magique dans le monde avec Cent ans de solitude et son œuvre romanesque."),
        "ru": ("Колумбийский мастер магического реализма", "Габриэль Гарсиа Маркес познакомил мировую аудиторию с магическим реализмом романом «Сто лет одиночества» и другими произведениями."),
        "es": ("Maestro colombiano del realismo mágico", "García Márquez llevó el realismo mágico a un público mundial con Cien años de soledad y el resto de su narrativa."),
    },
    "Mahmoud Darwish": {
        "en": ("Palestinian poet of exile and identity", "Darwish became a central voice of modern Arabic poetry, exploring exile, identity, homeland, and memory in lyrical verse."),
        "fr": ("Poète palestinien de l’exil et de l’identité", "Darwich fut une voix centrale de la poésie arabe moderne, explorant l’exil, l’identité, la patrie et la mémoire."),
        "ru": ("Палестинский поэт изгнания и идентичности", "Махмуд Дарвиш стал одной из центральных фигур современной арабской поэзии, исследуя изгнание, идентичность, родину и память."),
        "es": ("Poeta palestino del exilio y la identidad", "Darwish fue una voz central de la poesía árabe moderna, explorando el exilio, la identidad, la patria y la memoria."),
    },
}

def main() -> None:
    if not JSON_PATH.exists():
        raise FileNotFoundError(JSON_PATH)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(JSON_PATH, BACKUP_DIR / f"person_i18n_batch09_{stamp}.json")
    if JS_PATH.exists():
        shutil.copy2(JS_PATH, BACKUP_DIR / f"person_i18n_batch09_{stamp}.js")

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]
    changed = 0

    for person, langs in PEOPLE.items():
        if person not in people:
            raise KeyError(f"Missing person: {person}")
        for lang, (hint, significance) in langs.items():
            entry = people[person]["languages"].get(lang)
            if not entry:
                raise KeyError(f"Missing language {lang!r} for {person}")
            old_hint = entry.get("hint")
            old_sig = entry.get("historical_significance")
            if old_hint in {
                "Renowned Writer", "Écrivain renommé",
                "Renombrado escritor",
            } or old_hint is not None:
                if old_hint != hint:
                    entry["hint"] = hint
                    changed += 1
            if old_sig is not None and old_sig != significance:
                entry["historical_significance"] = significance
                changed += 1

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Keep the existing JS contract: JSON payload exported as a JS constant.
    if JS_PATH.exists():
        JS_PATH.write_text(
            "const PERSON_I18N = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
            encoding="utf-8",
        )

    print(f"Batch 09 applied: {len(PEOPLE)} people, {changed} field changes.")
    print(f"Backup JSON: {BACKUP_DIR / f'person_i18n_batch09_{stamp}.json'}")
    print(f"Backup JS:   {BACKUP_DIR / f'person_i18n_batch09_{stamp}.js'}")

if __name__ == "__main__":
    main()
