from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "app" / "src" / "main" / "assets" / "person_i18n.json"
JS_PATH = ROOT / "app" / "src" / "main" / "assets" / "js" / "person_i18n.js"
BACKUP_DIR = ROOT / "tools" / "backups"

# Batch 10: exact repeated Artist hint/significance values.
# Only the four languages explicitly identified in the direct audit are touched.
DATA = {
"Jan van Eyck": {
"en": ("Northern Renaissance pioneer of oil painting", "Van Eyck transformed Northern European painting through meticulous oil technique and works such as the Ghent Altarpiece and Arnolfini Portrait."),
"es": ("Pionero flamenco de la pintura al óleo", "Van Eyck transformó la pintura del norte de Europa mediante una técnica al óleo minuciosa y obras como el Políptico de Gante y el Retrato de Arnolfini."),
"fr": ("Pionnier flamand de la peinture à l’huile", "Van Eyck a transformé la peinture de l’Europe du Nord par sa maîtrise de l’huile, notamment dans le Retable de Gand et le Portrait des époux Arnolfini."),
"ru": ("Пионер Северного Возрождения в живописи", "Ян ван Эйк преобразил живопись Северной Европы виртуозной техникой масляной живописи, особенно в Гентском алтаре и портрете четы Арнольфини.")
},
"Michelangelo": {
"en": ("Renaissance master of sculpture and painting", "Michelangelo defined High Renaissance art through the David, the Sistine Chapel ceiling, and monumental works in sculpture, painting, and architecture."),
"es": ("Maestro del Renacimiento en escultura y pintura", "Miguel Ángel definió el Alto Renacimiento con el David, el techo de la Capilla Sixtina y obras monumentales de escultura, pintura y arquitectura."),
"fr": ("Maître de la Renaissance en sculpture et peinture", "Michel-Ange a marqué la Haute Renaissance avec le David, le plafond de la chapelle Sixtine et ses œuvres monumentales de sculpture, peinture et architecture."),
"ru": ("Мастер Высокого Возрождения в скульптуре и живописи", "Микеланджело определил искусство Высокого Возрождения скульптурой «Давидом», росписью потолка Сикстинской капеллы и архитектурными проектами.")
},
"Raphael": {
"en": ("Renaissance painter of the School of Athens", "Raphael became a defining High Renaissance painter through harmonious compositions such as the School of Athens and his Madonnas."),
"es": ("Pintor renacentista de La escuela de Atenas", "Rafael fue una figura esencial del Alto Renacimiento por composiciones como La escuela de Atenas y sus numerosas Madonnas."),
"fr": ("Peintre de la Renaissance auteur de L’École d’Athènes", "Raphaël fut une figure majeure de la Haute Renaissance grâce à des compositions comme L’École d’Athènes et ses Madones."),
"ru": ("Художник Высокого Возрождения, автор «Афинской школы»", "Рафаэль стал одним из главных мастеров Высокого Возрождения благодаря гармоничным композициям, включая «Афинскую школу», и образам Мадонн.")
},
"Titian": {
"en": ("Venetian master of color and portraiture", "Titian reshaped Venetian painting through rich color, expressive brushwork, portraits, mythological scenes, and religious compositions."),
"es": ("Maestro veneciano del color y el retrato", "Tiziano transformó la pintura veneciana mediante el color, la pincelada expresiva, los retratos y sus escenas mitológicas y religiosas."),
"fr": ("Maître vénitien de la couleur et du portrait", "Titien a renouvelé la peinture vénitienne par la richesse des couleurs, ses portraits et ses compositions mythologiques et religieuses."),
"ru": ("Венецианский мастер цвета и портрета", "Тициан преобразил венецианскую живопись богатством цвета, выразительной манерой, портретами и мифологическими и религиозными композициями.")
},
"El Greco": {
"en": ("Mannerist painter of Toledo", "El Greco developed a distinctive elongated style in Spain, combining Byzantine roots, Venetian color, and intense spiritual expression."),
"es": ("Pintor manierista de Toledo", "El Greco desarrolló en España un узнаваемый вытянутый стиль, сочетавший византийские истоки, венецианский колорит y una intensa expresión espiritual."),
"fr": ("Peintre maniériste de Tolède", "El Greco a développé en Espagne un style aux figures allongées, mêlant héritage byzantin, couleur vénitienne et forte expression spirituelle."),
"ru": ("Мастер маньеризма из Толедо", "Эль Греко выработал в Испании узнаваемый вытянутый стиль, соединив византийские истоки, венецианский колорит и сильную духовную выразительность.")
},
"Caravaggio": {
"en": ("Baroque master of dramatic light", "Caravaggio revolutionized European painting with stark chiaroscuro, naturalistic figures, and emotionally charged biblical scenes."),
"es": ("Maestro barroco de la luz dramática", "Caravaggio revolucionó la pintura europea con fuertes contrastes de luz y sombra, figuras naturalistas y escenas bíblicas de gran intensidad."),
"fr": ("Maître baroque du clair-obscur dramatique", "Caravage a révolutionné la peinture européenne par son clair-obscur marqué, ses figures naturalistes et ses scènes bibliques intensément dramatiques."),
"ru": ("Мастер барокко драматического света", "Караваджо преобразил европейскую живопись резким светотеневым контрастом, натуралистическими фигурами и эмоциональными библейскими сценами.")
},
"Peter Paul Rubens": {
"en": ("Flemish Baroque painter and diplomat", "Rubens became a leading Flemish Baroque painter through energetic compositions, monumental history paintings, portraits, and diplomatic service."),
"es": ("Pintor flamenco barroco y diplomático", "Rubens fue una figura central del barroco flamenco por sus composiciones dinámicas, pinturas históricas monumentales, retratos y actividad diplomática."),
"fr": ("Peintre baroque flamand et diplomate", "Rubens fut l’un des grands maîtres du baroque flamand par ses compositions dynamiques, ses peintures d’histoire monumentales et son activité diplomatique."),
"ru": ("Фламандский художник барокко и дипломат", "Рубенс стал ведущим мастером фламандского барокко благодаря динамичным композициям, монументальным историческим картинам, портретам и дипломатической деятельности.")
},
"Diego Velázquez": {
"en": ("Spanish court painter of Las Meninas", "Velázquez transformed Spanish court painting through naturalistic portraits, complex spatial compositions, and masterpieces such as Las Meninas."),
"es": ("Pintor de corte español de Las meninas", "Velázquez transformó la pintura de corte española mediante retratos naturalistas, complejas composiciones espaciales y obras como Las meninas."),
"fr": ("Peintre de cour espagnol des Ménines", "Vélasquez a renouvelé la peinture de cour espagnole par ses portraits naturalistes, ses espaces complexes et des œuvres comme Les Ménines."),
"ru": ("Испанский придворный художник, автор «Мени́н»", "Веласкес преобразил испанскую придворную живопись натуралистическими портретами, сложным построением пространства и картиной «Менины».")
},
"Rembrandt": {
"en": ("Dutch master of portraits and light", "Rembrandt transformed Dutch painting through psychologically intense portraits, self-portraits, biblical scenes, and expressive use of light and shadow."),
"es": ("Maestro neerlandés del retrato y la luz", "Rembrandt transformó la pintura neerlandesa mediante retratos de gran profundidad psicológica, autorretratos, escenas bíblicas y un uso expresivo de la luz."),
"fr": ("Maître néerlandais du portrait et de la lumière", "Rembrandt a marqué la peinture néerlandaise par ses portraits psychologiques, ses autoportraits, ses scènes bibliques et son usage expressif de la lumière."),
"ru": ("Нидерландский мастер портрета и света", "Рембрандт преобразил голландскую живопись психологически насыщенными портретами, автопортретами, библейскими сценами и выразительной светотенью.")
},
"Francisco Goya": {
"en": ("Spanish painter of court and war", "Goya bridged the Old Masters and modern art through court portraits, The Third of May 1808, and the dark imagery of the Black Paintings."),
"es": ("Pintor español de la corte y la guerra", "Goya unió la tradición de los grandes maestros con el arte moderno mediante retratos de corte, El 3 de mayo de 1808 y las Pinturas negras."),
"fr": ("Peintre espagnol de cour et de guerre", "Goya a fait le lien entre les anciens maîtres et l’art moderne avec ses portraits de cour, Le Trois Mai 1808 et les Peintures noires."),
"ru": ("Испанский художник двора и войны", "Гойя связал искусство старых мастеров с современным искусством придворными портретами, «Третьим мая 1808 года» и «Чёрными картинами».")
},
"Eugène Delacroix": {
"en": ("French Romantic painter of Liberty Leading the People", "Delacroix became a leading French Romantic through dynamic color, historical subjects, and Liberty Leading the People."),
"es": ("Pintor francés del Romanticismo", "Delacroix fue uno de los principales representantes del romanticismo francés благодаря al color dinámico, los temas históricos y La libertad guiando al pueblo."),
"fr": ("Peintre français du romantisme", "Delacroix fut l’un des grands représentants du romantisme français grâce à ses couleurs dynamiques, ses sujets historiques et La Liberté guidant le peuple."),
"ru": ("Французский художник романтизма, автор «Свободы, ведущей народ»", "Делакруа стал ведущим французским романтиком благодаря динамичному цвету, историческим сюжетам и картине «Свобода, ведущая народ».")
},
"Claude Monet": {
"en": ("Founder of French Impressionism", "Monet helped define Impressionism through serial studies of light, atmosphere, and changing perception, including his Water Lilies."),
"es": ("Fundador del impresionismo francés", "Monet fue uno de los fundadores del impresionismo y exploró la luz y la atmósfera en series como Nenúfares y las vistas de la catedral de Ruan."),
"fr": ("Fondateur de l’impressionnisme français", "Monet a contribué à définir l’impressionnisme par ses recherches sur la lumière et l’atmosphère, notamment dans les Nymphéas."),
"ru": ("Основатель французского импрессионизма", "Моне стал одним из основателей импрессионизма, исследуя свет и атмосферу в сериях картин, включая «Кувшинки».")
},
"Henri Rousseau": {
"en": ("Self-taught painter of jungle scenes", "Rousseau developed a distinctive self-taught style, best known for dreamlike jungle paintings despite never visiting the tropics."),
"es": ("Pintor autodidacta de escenas selváticas", "Rousseau desarrolló un estilo autodidacta inconfundible, célebre por sus escenas selváticas oníricas aunque nunca visitó los trópicos."),
"fr": ("Peintre autodidacte des jungles imaginaires", "Rousseau a développé un style autodidacte singulier, surtout connu pour ses jungles oniriques, bien qu’il n’ait jamais voyagé sous les tropiques."),
"ru": ("Самоучка, прославившийся сценами джунглей", "Руссо создал самобытный стиль художника-самоучки и прославился фантастическими сценами джунглей, хотя никогда не посещал тропики.")
},
"Paul Gauguin": {
"en": ("Post-Impressionist painter of Tahitian scenes", "Gauguin helped shape Post-Impressionism through simplified forms, strong colors, and paintings inspired by life in Tahiti."),
"es": ("Pintor posimpresionista de escenas tahitianas", "Gauguin contribuyó al posimpresionismo con formas simplificadas, colores intensos y obras inspiradas en su estancia en Tahití."),
"fr": ("Peintre postimpressionniste des scènes tahitiennes", "Gauguin a contribué au postimpressionnisme par ses formes simplifiées, ses couleurs intenses et ses œuvres inspirées de Tahiti."),
"ru": ("Постимпрессионист, писавший сцены Таити", "Гоген сыграл важную роль в постимпрессионизме упрощёнными формами, насыщенным цветом и картинами, вдохновлёнными Таити.")
},
"Vincent van Gogh": {
"en": ("Post-Impressionist master of expressive color", "Van Gogh transformed modern painting through intense color, energetic brushwork, and works such as The Starry Night and Sunflowers."),
"es": ("Maestro posimpresionista del color expresivo", "Van Gogh transformó la pintura moderna mediante colores intensos, pinceladas enérgicas y obras como La noche estrellada y Los girasoles."),
"fr": ("Maître postimpressionniste de la couleur expressive", "Van Gogh a transformé la peinture moderne par ses couleurs intenses, sa touche énergique et des œuvres comme La Nuit étoilée et Les Tournesols."),
"ru": ("Мастер постимпрессионизма выразительного цвета", "Ван Гог преобразил современную живопись интенсивным цветом, энергичной манерой и такими произведениями, как «Звёздная ночь» и «Подсолнухи».")
},
"Alphonse Mucha": {
"en": ("Art Nouveau illustrator and designer", "Mucha became a defining figure of Art Nouveau through elegant posters, decorative panels, typography, and commercial design."),
"es": ("Ilustrador y diseñador del Art Nouveau", "Mucha fue una figura esencial del modernismo europeo gracias a sus carteles, paneles decorativos, tipografía y diseño comercial."),
"fr": ("Illustrateur et designer de l’Art nouveau", "Mucha fut une figure majeure de l’Art nouveau grâce à ses affiches, panneaux décoratifs, créations typographiques et travaux commerciaux."),
"ru": ("Иллюстратор и дизайнер модерна", "Муха стал одним из главных представителей модерна благодаря изящным плакатам, декоративным панно, типографике и коммерческому дизайну.")
},
"Edvard Munch": {
"en": ("Expressionist pioneer of The Scream", "Munch explored anxiety, love, illness, and mortality through psychologically charged imagery, most famously The Scream."),
"es": ("Pionero del expresionismo y autor de El grito", "Munch exploró la ansiedad, el amor, la enfermedad y la mortalidad mediante imágenes de gran intensidad psicológica, especialmente El grito."),
"fr": ("Pionnier de l’expressionnisme, auteur du Cri", "Munch a exploré l’angoisse, l’amour, la maladie et la mort dans des images d’une forte intensité psychologique, notamment Le Cri."),
"ru": ("Пионер экспрессионизма, автор «Крика»", "Мунк исследовал тревогу, любовь, болезнь и смертность через психологически напряжённые образы, прежде всего в картине «Крик».")
},
"Wassily Kandinsky": {
"en": ("Pioneer of abstract art", "Kandinsky helped establish abstract art by treating color, line, and form as independent elements of visual expression."),
"es": ("Pionero del arte abstracto", "Kandinsky contribuyó decisivamente al desarrollo del arte abstracto al tratar el color, la línea y la forma como elementos autónomos."),
"fr": ("Pionnier de l’art abstrait", "Kandinsky a contribué à fonder l’art abstrait en considérant la couleur, la ligne et la forme comme des éléments autonomes de l’expression."),
"ru": ("Пионер абстрактного искусства", "Кандинский сыграл ключевую роль в становлении абстракции, рассматривая цвет, линию и форму как самостоятельные средства выражения.")
},
"Henri Matisse": {
"en": ("French master of Fauvist color", "Matisse transformed twentieth-century painting through Fauvist color, simplified forms, and later cut-paper works."),
"es": ("Maestro francés del color fauvista", "Matisse transformó la pintura del siglo XX mediante el color fauvista, las formas simplificadas y sus posteriores obras con recortes de papel."),
"fr": ("Maître français de la couleur fauve", "Matisse a transformé la peinture du XXe siècle par la couleur fauve, les formes simplifiées et ses œuvres tardives en papiers découpés."),
"ru": ("Французский мастер фовистского цвета", "Матисс преобразил искусство XX века ярким фовистским цветом, упрощёнными формами и поздними композициями из вырезанной бумаги.")
},
"Kazimir Malevich": {
"en": ("Founder of Suprematism", "Malevich founded Suprematism and pushed painting toward geometric abstraction, most famously with Black Square."),
"es": ("Fundador del suprematismo", "Malevich fundó el suprematismo y llevó la pintura hacia la геометрическая abstracción, sobre todo con Cuadrado negro."),
"fr": ("Fondateur du suprématisme", "Malevitch a fondé le suprématisme et poussé la peinture vers l’abstraction géométrique, notamment avec Carré noir."),
"ru": ("Основатель супрематизма", "Малевич основал супрематизм и радикально развил геометрическую абстракцию, наиболее известную по «Чёрному квадрату».")
},
"Pablo Picasso": {
"en": ("Co-founder of Cubism", "Picasso helped revolutionize modern art through Cubism and a career spanning painting, sculpture, printmaking, and ceramics."),
"es": ("Cofundador del cubismo", "Picasso revolucionó el arte moderno, especialmente junto a Georges Braque en el cubismo, y trabajó también en escultura, grabado y cerámica."),
"fr": ("Cofondateur du cubisme", "Picasso a révolutionné l’art moderne, notamment avec Georges Braque dans le cubisme, tout en travaillant la sculpture, la gravure et la céramique."),
"ru": ("Один из основателей кубизма", "Пикассо преобразил современное искусство, особенно вместе с Жоржем Браком в кубизме, работая также в скульптуре, графике и керамике.")
},
"Amedeo Modigliani": {
"en": ("Modernist painter known for elongated portraits", "Modigliani developed a distinctive modernist style of elongated faces, necks, and simplified forms in portraits and nudes."),
"es": ("Pintor modernista de retratos alargados", "Modigliani desarrolló un estilo inconfundible de rostros y cuellos alargados y formas simplificadas en retratos y desnudos."),
"fr": ("Peintre moderniste aux portraits allongés", "Modigliani a développé un style singulier de visages et de cous allongés, avec des formes simplifiées dans ses portraits et nus."),
"ru": ("Модернист с вытянутыми портретами", "Модильяни создал узнаваемый модернистский стиль с вытянутыми лицами и шеями и упрощёнными формами в портретах и обнажённых фигурах.")
},
"Marc Chagall": {
"en": ("Painter of dreamlike Jewish and modernist imagery", "Chagall fused Jewish cultural memory, folk motifs, and modernist color into dreamlike paintings, prints, and stained glass."),
"es": ("Pintor de imágenes judías y modernistas de ensueño", "Chagall combinó memoria cultural judía, motivos folclóricos y color modernista en pinturas, grabados y vidrieras de carácter onírico."),
"fr": ("Peintre d’un imaginaire juif et moderniste", "Chagall a mêlé mémoire culturelle juive, motifs populaires et couleur moderniste dans une œuvre picturale, graphique et de vitraux très onirique."),
"ru": ("Художник еврейской и модернистской образности", "Шагал соединил еврейскую культурную память, фольклорные мотивы и модернистский цвет в живописи, графике и витражах.")
},
"Joan Miró": {
"en": ("Catalan pioneer of Surrealist abstraction", "Miró developed a highly personal visual language of signs, biomorphic forms, and vivid color associated with Surrealism and modern abstraction."),
"es": ("Pionero catalán de la abstracción surrealista", "Miró desarrolló un lenguaje visual propio de signos, formas biomórficas y colores intensos vinculado al surrealismo y la abstracción moderna."),
"fr": ("Pionnier catalan de l’abstraction surréaliste", "Miró a développé un langage visuel personnel fait de signes, de formes biomorphiques et de couleurs vives, lié au surréalisme et à l’abstraction."),
"ru": ("Каталонский пионер сюрреалистической абстракции", "Миро создал самобытный язык знаков, биоморфных форм и ярких цветов, связанный с сюрреализмом и современной абстракцией.")
},
}

def main() -> None:
    if not JSON_PATH.exists():
        raise FileNotFoundError(JSON_PATH)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_json = BACKUP_DIR / f"person_i18n_batch10_{stamp}.json"
    backup_js = BACKUP_DIR / f"person_i18n_batch10_{stamp}.js"
    shutil.copy2(JSON_PATH, backup_json)
    if JS_PATH.exists():
        shutil.copy2(JS_PATH, backup_js)

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    people = data["people"]
    changed = 0

    for person, langs in DATA.items():
        if person not in people:
            raise KeyError(f"Missing person: {person}")
        for lang, (hint, significance) in langs.items():
            entry = people[person]["languages"].get(lang)
            if entry is None:
                raise KeyError(f"Missing {lang} data for {person}")
            if entry.get("hint") != hint:
                entry["hint"] = hint
                changed += 1
            if entry.get("historical_significance") != significance:
                entry["historical_significance"] = significance
                changed += 1

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if JS_PATH.exists():
        JS_PATH.write_text(
            "const PERSON_I18N = "
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + ";\n",
            encoding="utf-8",
        )

    # Independent post-write checks.
    reloaded = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert len(reloaded["people"]) == 289
    assert reloaded["languages"] == data["languages"]
    for person, langs in DATA.items():
        for lang, (hint, significance) in langs.items():
            entry = reloaded["people"][person]["languages"][lang]
            assert entry["hint"] == hint
            assert entry["historical_significance"] == significance

    print(f"Batch 10 applied: {len(DATA)} people, {changed} field changes.")
    print(f"Backup JSON: {backup_json}")
    print(f"Backup JS:   {backup_js}")

if __name__ == "__main__":
    main()
