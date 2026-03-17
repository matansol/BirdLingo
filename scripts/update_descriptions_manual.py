"""
Manually update descriptions for level 1 and 2 birds (80 total).
Descriptions explain the DISPLAY NAME (common name), not the specific species.
"""

from pathlib import Path
import json

BASE_DIR = Path(__file__).parent.parent
BIRDS_INFO = BASE_DIR / "../data/birds_info.json"
BIRDS_DATA = BASE_DIR / "assets" / "birds_data.json"

# Import birds data
import birds_200

# Manually written descriptions for each display name (common name)
# Format: display_name -> {en, he, es, fr}
DESCRIPTIONS = {
    "House Sparrow": {
        "en": "A small, adaptable songbird found in cities and towns worldwide. Known for their cheerful chirping and brown-grey plumage with black markings.",
        "he": "ציפור שיר קטנה ומסתגלת שנמצאת בערים ובעיירות ברחבי העולם. ידועים בציוץ העליז שלהם ובנוצות חומות-אפורות עם סימנים שחורים.",
        "es": "Un pequeño pájaro cantor adaptable que se encuentra en ciudades y pueblos de todo el mundo. Conocidos por su alegre gorjeo y plumaje marrón grisáceo con marcas negras.",
        "fr": "Un petit oiseau chanteur adaptable trouvé dans les villes du monde entier. Connus pour leur gazouillis joyeux et leur plumage brun-gris avec des marques noires."
    },
    "Rock Dove": {
        "en": "The common pigeon, ancestor of all domestic pigeons. Often seen in cities, they have plump bodies and cooing calls.",
        "he": "היונה הרגילה, אב קדמון של כל היונים הביתיות. נראים לעתים קרובות בערים, יש להם גוף שמן וקולות המהמה.",
        "es": "La paloma común, ancestro de todas las palomas domésticas. A menudo se ven en ciudades, tienen cuerpos rechonchos y llamadas arrullantes.",
        "fr": "Le pigeon commun, ancêtre de tous les pigeons domestiques. Souvent vus dans les villes, ils ont un corps dodu et des roucoulements."
    },
    "Common Blackbird": {
        "en": "A medium-sized thrush with melodious song. Males are jet black with yellow beaks, while females are brown.",
        "he": "קיכלי בינוני עם שיר מנגן. הזכרים שחורים לחלוטין עם מקור צהוב, בעוד הנקבות חומות.",
        "es": "Un zorzal de tamaño mediano con canto melodioso. Los machos son negro azabache con picos amarillos, mientras que las hembras son marrones.",
        "fr": "Une grive de taille moyenne au chant mélodieux. Les mâles sont noir de jais avec un bec jaune, tandis que les femelles sont brunes."
    },
    "Starling": {
        "en": "Gregarious birds with iridescent plumage that forms spectacular murmurations in flight. They are excellent mimics and adaptable urban dwellers.",
        "he": "ציפורים חברתיות עם נוצות מנצנצות היוצרות היבטי מורמורציה מרהיבים בטיסה. הם חקיינים מצוינים ותושבי עיר מסתגלים.",
        "es": "Aves gregarias con plumaje iridiscente que forman espectaculares murmurations en vuelo. Son excelentes imitadores y habitantes urbanos adaptables.",
        "fr": "Des oiseaux grégaires au plumage irisé formant des murmures spectaculaires en vol. Ils sont d'excellents imitateurs et des citadins adaptables."
    },
    "Mallard": {
        "en": "The most familiar wild duck species, found on lakes and ponds worldwide. Males have distinctive green heads and yellow bills.",
        "he": "מין הברווז הפראי המוכר ביותר, נמצא באגמים ובבריכות ברחבי העולם. לזכרים ראש ירוק מובהק ומקור צהוב.",
        "es": "La especie de pato salvaje más familiar, encontrada en lagos y estanques de todo el mundo. Los machos tienen cabezas verdes distintivas y picos amarillos.",
        "fr": "L'espèce de canard sauvage la plus familière, trouvée sur les lacs et étangs du monde entier. Les mâles ont une tête verte distinctive et un bec jaune."
    },
    "Canada Goose": {
        "en": "Large waterfowl with distinctive black heads and white chinstraps. Known for their V-shaped flying formations and loud honking calls.",
        "he": "עוף מים גדול עם ראש שחור מובהק ורצועת סנטר לבנה. ידועים בתצורות הטיסה בצורת V ובקריאות ההונקינג הרועשות.",
        "es": "Ave acuática grande con cabezas negras distintivas y correas blancas en la barbilla. Conocidos por sus formaciones de vuelo en forma de V y llamadas estridentes.",
        "fr": "Grande volaille aquatique avec des têtes noires distinctives et des mentonnières blanches. Connus pour leurs formations de vol en V et leurs cris klaxonnants."
    },
    "Mute Swan": {
        "en": "Elegant, all-white waterfowl with gracefully curved necks and orange bills. Despite their name, they can produce various sounds including hisses.",
        "he": "עוף מים אלגנטי, לבן לחלוטין עם צוואר מעוקל בחן ומקור כתום. למרות שמם, הם יכולים להפיק קולות שונים כולל שריקות.",
        "es": "Aves acuáticas elegantes, completamente blancas con cuellos graciosamente curvados y picos naranjas. A pesar de su nombre, pueden producir varios sonidos, incluidos silbidos.",
        "fr": "Volaille aquatique élégante, toute blanche avec un cou gracieusement courbé et un bec orange. Malgré leur nom, ils peuvent produire divers sons dont des sifflements."
    },
    "Gull": {
        "en": "Seabirds with webbed feet and strong, hooked bills. Often found near coasts and inland waters, they're opportunistic feeders known for their loud cries.",
        "he": "ציפורי ים עם רגליים קרומיות ומקור חזק ומעוקל. נמצאים לעתים קרובות ליד חופים ומים פנימיים, הם מזיני הזדמנות ידועים בזעקות הרועשות שלהם.",
        "es": "Aves marinas con patas palmeadas y picos fuertes y ganchudos. A menudo se encuentran cerca de costas y aguas interiores, son alimentadores oportunistas conocidos por sus gritos fuertes.",
        "fr": "Oiseaux marins aux pieds palmés et aux becs forts et crochus. Souvent trouvés près des côtes et des eaux intérieures, ce sont des mangeurs opportunistes connus pour leurs cris forts."
    },
    "American Robin": {
        "en": "A thrush with distinctive rusty-red breast and cheerful song. Common in gardens and lawns, they hop along searching for worms.",
        "he": "קיכלי עם חזה אדום-חלוד מובהק ושיר עליז. נפוצים בגנים ובמדשאות, הם מדלגים בחיפוש אחר תולעים.",
        "es": "Un zorzal con pecho rojo oxidado distintivo y canto alegre. Comunes en jardines y césped, saltan buscando gusanos.",
        "fr": "Une grive au poitrail roux distinctif et au chant joyeux. Communs dans les jardins et pelouses, ils sautillent à la recherche de vers."
    },
    "Northern Cardinal": {
        "en": "Vibrant red songbirds with distinctive crests and black face masks. Males are brilliant red while females are tawny with red accents.",
        "he": "ציפורי שיר אדומות תוססות עם ציצית מובהקת ומסכת פנים שחורה. הזכרים אדומים מבריקים ואילו הנקבות חומות עם הדגשים אדומים.",
        "es": "Pájaros cantores rojos vibrantes con crestas distintivas y máscaras faciales negras. Los machos son rojos brillantes mientras que las hembras son leonadas con acentos rojos.",
        "fr": "Oiseaux chanteurs rouge vif avec des crêtes distinctives et des masques noirs. Les mâles sont rouge brillant tandis que les femelles sont fauves avec des accents rouges."
    },
    "Blue Jay": {
        "en": "Intelligent, noisy birds with brilliant blue plumage and black necklaces. Known for their complex social systems and loud calls.",
        "he": "ציפורים חכמות ורועשות עם נוצות כחולות מבריקות ושרשרות שחורות. ידועים במערכות החברתיות המורכבות והקריאות הרועשות שלהם.",
        "es": "Aves inteligentes y ruidosas con plumaje azul brillante y collares negros. Conocidos por sus sistemas sociales complejos y llamadas fuertes.",
        "fr": "Oiseaux intelligents et bruyants au plumage bleu brillant et colliers noirs. Connus pour leurs systèmes sociaux complexes et leurs cris forts."
    },
    "American Crow": {
        "en": "Large, all-black birds with impressive intelligence. They use tools, recognize faces, and live in complex family groups.",
        "he": "ציפורים גדולות, שחורות לחלוטין עם אינטליגנציה מרשימה. הם משתמשים בכלים, מזהים פנים וחיים בקבוצות משפחה מורכבות.",
        "es": "Aves grandes, completamente negras con inteligencia impresionante. Usan herramientas, reconocen rostros y viven en grupos familiares complejos.",
        "fr": "Grands oiseaux entièrement noirs d'une intelligence impressionnante. Ils utilisent des outils, reconnaissent les visages et vivent en groupes familiaux complexes."
    },
    "Eurasian Magpie": {
        "en": "Black and white corvids with long, iridescent tails. Highly intelligent birds known for their boldness and curiosity.",
        "he": "עורבנים שחורים ולבנים עם זנבות ארוכים ומנצנצים. ציפורים חכמות מאוד הידועות באומץ ובסקרנות שלהן.",
        "es": "Córvidos blancos y negros con colas largas e iridiscentes. Aves altamente inteligentes conocidas por su audacia y curiosidad.",
        "fr": "Corvidés noirs et blancs aux longues queues irisées. Oiseaux très intelligents connus pour leur audace et leur curiosité."
    },
    "Great Tit": {
        "en": "Bold, colorful songbirds with black heads and distinctive yellow breasts split by a black stripe. Common visitors to bird feeders.",
        "he": "ציפורי שיר נועזות וצבעוניות עם ראש שחור וחזה צהוב מובהק מפוצל בפס שחור. מבקרים נפוצים באבוסי ציפורים.",
        "es": "Pájaros cantores audaces y coloridos con cabezas negras y pechos amarillos distintivos divididos por una franja negra. Visitantes comunes de comederos de aves.",
        "fr": "Oiseaux chanteurs audacieux et colorés avec des têtes noires et des poitrines jaunes distinctives divisées par une bande noire. Visiteurs communs des mangeoires à oiseaux."
    },
    "Tit": {
        "en": "Small, acrobatic songbirds with colorful plumage. They hang upside down while foraging and are common visitors to garden feeders.",
        "he": "ציפורי שיר קטנות ואקרובטיות עם נוצות צבעוניות. הם תלויים הפוך בזמן חיפוש מזון ומבקרים נפוצים באבוסי גן.",
        "es": "Pequeños pájaros cantores acrobáticos con plumaje colorido. Cuelgan boca abajo mientras buscan comida y son visitantes comunes de comederos de jardín.",
        "fr": "Petits oiseaux chanteurs acrobatiques au plumage coloré. Ils se suspendent à l'envers en cherchant de la nourriture et sont des visiteurs communs des mangeoires de jardin."
    },
    "Barn Swallow": {
        "en": "Graceful aerial insectivores with long, forked tails and blue backs. They build mud nests in barns and under bridges.",
        "he": "טורפי חרקים אוויריים חינניים עם זנבות ארוכים ומפוצלים וגב כחול. הם בונים קני בוץ באסמים ומתחת לגשרים.",
        "es": "Insectívoros aéreos elegantes con colas largas y bifurcadas y espaldas azules. Construyen nidos de barro en graneros y bajo puentes.",
        "fr": "Insectivores aériens gracieux aux longues queues fourchues et dos bleus. Ils construisent des nids de boue dans les granges et sous les ponts."
    },
    "Eurasian Collared Dove": {
        "en": "Pale grey-brown doves with distinctive black collar markings on their necks. Their monotonous cooing is a common sound in towns.",
        "he": "יונים אפורות-חומות בהירות עם סימני צווארון שחורים מובהקים על הצוואר. ההמהמה המונוטונית שלהם היא צליל נפוץ בעיירות.",
        "es": "Palomas grises-marrones pálidas con marcas distintivas de collar negro en el cuello. Su arrullo monótono es un sonido común en los pueblos.",
        "fr": "Tourterelles gris-brun pâle avec des marques de collier noir distinctives sur le cou. Leur roucoulement monotone est un son commun dans les villes."
    },
    "Pigeon": {
        "en": "Large, plump birds with small heads and cooing calls. They're strong fliers found in woodlands and increasingly in urban areas.",
        "he": "ציפורים גדולות ושמנות עם ראש קטן וקריאות המהמה. הם מעופפים חזקים הנמצאים ביערות ויותר ויותר באזורים עירוניים.",
        "es": "Aves grandes y rechonchas con cabezas pequeñas y llamadas arrullantes. Son voladores fuertes encontrados en bosques y cada vez más en áreas urbanas.",
        "fr": "Grands oiseaux dodus à petite tête et roucoulements. Ce sont de forts volants trouvés dans les bois et de plus en plus dans les zones urbaines."
    },
    "House Finch": {
        "en": "Small songbirds with streaked brown plumage. Males have rosy-red heads and breasts, while females are plain brown and streaky.",
        "he": "ציפורי שיר קטנות עם נוצות חומות מפוספסות. לזכרים ראש וחזה אדום-ורוד, ואילו הנקבות חומות פשוטות ומפוספסות.",
        "es": "Pequeños pájaros cantores con plumaje marrón rayado. Los machos tienen cabezas y pechos rojo rosado, mientras que las hembras son marrones lisos y rayados.",
        "fr": "Petits oiseaux chanteurs au plumage brun strié. Les mâles ont une tête et une poitrine rose-rouge, tandis que les femelles sont brun uni et striées."
    },
    "Mourning Dove": {
        "en": "Slender, graceful doves with long, pointed tails and soft cooing calls. Their wings make a distinctive whistling sound in flight.",
        "he": "יונים דקיקות וחינניות עם זנבות ארוכים ומחודדים וקריאות המהמה רכות. כנפיהם משמיעים צליל שריקה מובהק בטיסה.",
        "es": "Palomas delgadas y elegantes con colas largas y puntiagudas y llamadas arrullantes suaves. Sus alas hacen un sonido silbante distintivo en vuelo.",
        "fr": "Tourterelles minces et gracieuses aux longues queues pointues et roucoulements doux. Leurs ailes font un sifflement distinctif en vol."
    },
    "Common Myna": {
        "en": "Bold, gregarious birds with brown bodies, black heads, and yellow patches around their eyes. Known for their adaptability to urban environments.",
        "he": "ציפורים נועזות וחברתיות עם גוף חום, ראש שחור וכתמים צהובים סביב העיניים. ידועות ביכולת ההסתגלות שלהן לסביבות עירוניות.",
        "es": "Aves audaces y gregarias con cuerpos marrones, cabezas negras y manchas amarillas alrededor de los ojos. Conocidas por su adaptabilidad a entornos urbanos.",
        "fr": "Oiseaux audacieux et grégaires au corps brun, tête noire et taches jaunes autour des yeux. Connus pour leur adaptabilité aux environnements urbains."
    },
    "House Crow": {
        "en": "Medium-sized corvids with glossy black plumage and grey necks. Highly adaptable urban scavengers known for their intelligence.",
        "he": "עורבנים בינוניים עם נוצות שחורות מבריקות וצוואר אפור. זבלנים עירוניים מסתגלים מאוד הידועים באינטליגנציה שלהם.",
        "es": "Córvidos de tamaño mediano con plumaje negro brillante y cuellos grises. Carroñeros urbanos altamente adaptables conocidos por su inteligencia.",
        "fr": "Corvidés de taille moyenne au plumage noir brillant et cou gris. Charognards urbains très adaptables connus pour leur intelligence."
    },
    "Robin": {
        "en": "Charming small birds with rusty-orange breasts and faces. They're beloved garden visitors known for their melodious songs and tameness around humans.",
        "he": "ציפורים קטנות ומקסימות עם חזה ופנים כתום-חלוד. הם מבקרי גן אהובים הידועים בשירים המנגנים ובאילוף שלהם סביב בני אדם.",
        "es": "Encantadores pájaros pequeños con pechos y caras naranja oxidado. Son visitantes queridos del jardín conocidos por sus cantos melodiosos y mansedumbre cerca de los humanos.",
        "fr": "Charmants petits oiseaux au poitrail et visage orange rouillé. Ce sont des visiteurs de jardin bien-aimés connus pour leurs chants mélodieux et leur docilité près des humains."
    },
    "Goldfinch": {
        "en": "Colorful finches with red faces and bright yellow wing bars. They have a delightful tinkling song and specialize in feeding on thistle seeds.",
        "he": "חוחיות צבעוניות עם פנים אדומות ופסי כנף צהובים בהירים. יש להם שיר צילצול מענג והם מתמחים בהאכלה על זרעי גדילן.",
        "es": "Pinzones coloridos con caras rojas y barras de alas amarillas brillantes. Tienen un canto tintineante encantador y se especializan en alimentarse de semillas de cardo.",
        "fr": "Chardonnerets colorés au visage rouge et barres alaires jaunes vif. Ils ont un chant tintinnabulant délicieux et se spécialisent dans les graines de chardon."
    },
    "Great Egret": {
        "en": "Large, elegant wading birds with pure white plumage and yellow bills. They hunt fish in shallow water with patient, stealthy movements.",
        "he": "ציפורי שכשוך גדולות ואלגנטיות עם נוצות לבנות טהורות ומקור צהוב. הם צדים דגים במים רדודים עם תנועות סבלניות וחמקניות.",
        "es": "Grandes y elegantes aves zancudas con plumaje blanco puro y picos amarillos. Cazan peces en aguas poco profundas con movimientos pacientes y sigilosos.",
        "fr": "Grands oiseaux échassiers élégants au plumage blanc pur et bec jaune. Ils chassent le poisson en eau peu profonde avec des mouvements patients et furtifs."
    },
    "Greater Flamingo": {
        "en": "Iconic pink wading birds with long, curved necks and specialized bills for filter feeding. Their color comes from carotenoid pigments in their food.",
        "he": "ציפורי שכשוך ורודות איקוניות עם צוואר ארוך ומעוקל ומקור מיוחד להאכלה בסינון. הצבע שלהם מגיע מפיגמנטים קרוטנואידים במזון שלהם.",
        "es": "Icónicas aves zancudas rosadas con cuellos largos y curvados y picos especializados para alimentación por filtración. Su color proviene de pigmentos carotenoides en su comida.",
        "fr": "Oiseaux échassiers roses emblématiques aux longs cous courbés et becs spécialisés pour l'alimentation par filtrage. Leur couleur provient des pigments caroténoïdes dans leur nourriture."
    },
    "Peafowl": {
        "en": "Large, ornamental birds famous for the male's spectacular iridescent tail display. Native to South Asia, they're now found in parks worldwide.",
        "he": "ציפורים גדולות ונוי מפורסמות בתצוגת הזנב הענקית והמנצנצת של הזכר. מקור בדרום אסיה, הן נמצאות כעת בפארקים ברחבי העולם.",
        "es": "Grandes aves ornamentales famosas por la espectacular exhibición de cola iridiscente del macho. Nativas del sur de Asia, ahora se encuentran en parques de todo el mundo.",
        "fr": "Grands oiseaux ornementaux célèbres pour la spectaculaire parade de queue irisée du mâle. Originaires d'Asie du Sud, on les trouve maintenant dans les parcs du monde entier."
    },
    "Common Buzzard": {
        "en": "Medium-sized raptors with broad wings and fan-shaped tails. They soar high on thermals, hunting small mammals and watching for prey from perches.",
        "he": "טורפים בינוניים עם כנפיים רחבות וזנבות בצורת מניפה. הם מרחפים גבוה בטרמיקה, צדים יונקים קטנים ומשגיחים על טרף מענפים.",
        "es": "Aves rapaces de tamaño mediano con alas anchas y colas en forma de abanico. Se elevan alto en térmicas, cazando pequeños mamíferos y vigilando presas desde perchas.",
        "fr": "Rapaces de taille moyenne aux ailes larges et queues en éventail. Ils planent haut sur les thermiques, chassant les petits mammifères et surveillant les proies depuis les perchoirs."
    },
    "Kestrel": {
        "en": "Small falcons that hover in one spot while hunting for prey below. They have distinctive pointed wings and can spot prey from great heights.",
        "he": "בזים קטנים המרחפים במקום אחד בזמן ציד טרף מתחת. יש להם כנפיים מחודדות מובהקות ויכולים לזהות טרף מגבהים רבים.",
        "es": "Pequeños halcones que se ciernen en un lugar mientras cazan presas debajo. Tienen alas puntiagudas distintivas y pueden detectar presas desde grandes alturas.",
        "fr": "Petits faucons qui planent sur place en chassant les proies en dessous. Ils ont des ailes pointues distinctives et peuvent repérer les proies depuis de grandes hauteurs."
    },
    "Barn Owl": {
        "en": "Pale, heart-faced owls that hunt at night using exceptional hearing. They swallow prey whole and regurgitate pellets of indigestible material.",
        "he": "ינשופים חיוורים עם פנים בצורת לב שצדים בלילה באמצעות שמיעה יוצאת דופן. הם בולעים טרף שלם ומחזירים גלולות של חומר בלתי מתעכל.",
        "es": "Lechuzas pálidas con cara en forma de corazón que cazan de noche usando audición excepcional. Tragan presas enteras y regurgitan pellets de material indigerible.",
        "fr": "Chouettes pâles au visage en forme de cœur qui chassent la nuit avec une audition exceptionnelle. Ils avalent les proies entières et régurgitent des boulettes de matière indigeste."
    },
    "Common Swift": {
        "en": "Highly aerial birds that eat, drink, and even mate while flying. They have scythe-like wings and spend most of their lives airborne.",
        "he": "ציפורים אוויריות מאוד שאוכלות, שותות ואפילו מזדווגות בזמן טיסה. יש להם כנפיים דמויות חרמש ומבלות את רוב חייהם באוויר.",
        "es": "Aves altamente aéreas que comen, beben e incluso se aparean mientras vuelan. Tienen alas como guadañas y pasan la mayor parte de sus vidas en el aire.",
        "fr": "Oiseaux très aériens qui mangent, boivent et même s'accouplent en vol. Ils ont des ailes en forme de faux et passent la majeure partie de leur vie en vol."
    },
    "Song Thrush": {
        "en": "Spotted brown birds known for their loud, musical songs with repeated phrases. They famously smash snails on stones to eat them.",
        "he": "ציפורים חומות מנומרות הידועות בשירים הרמים והמוזיקליים שלהן עם ביטויים חוזרים. הם מפורסמים בריסוק חלזונות על אבנים כדי לאכול אותם.",
        "es": "Pájaros marrones moteados conocidos por sus cantos fuertes y musicales con frases repetidas. Son famosos por romper caracoles en piedras para comerlos.",
        "fr": "Oiseaux bruns tachetés connus pour leurs chants forts et musicaux avec des phrases répétées. Ils sont célèbres pour écraser les escargots sur les pierres pour les manger."
    },
    "Pelican": {
        "en": "Large water birds with enormous throat pouches for catching fish. They're social birds that often fish cooperatively in groups.",
        "he": "ציפורי מים גדולות עם כיסי גרון ענקיים לתפיסת דגים. הם ציפורים חברתיות שלעתים קרובות דגות בשיתוף פעולה בקבוצות.",
        "es": "Grandes aves acuáticas con enormes bolsas en la garganta para atrapar peces. Son aves sociales que a menudo pescan cooperativamente en grupos.",
        "fr": "Grands oiseaux aquatiques aux énormes poches gulaires pour attraper les poissons. Ce sont des oiseaux sociaux qui pêchent souvent en coopération en groupes."
    },
    "White Stork": {
        "en": "Large wading birds with white bodies, black wing feathers, and long red legs. They're famous for building large nests on rooftops and bringing good luck in folklore.",
        "he": "ציפורי שכשוך גדולות עם גוף לבן, נוצות כנף שחורות ורגליים אדומות ארוכות. הן מפורסמות בבניית קנים גדולים על גגות ובהבאת מזל טוב בפולקלור.",
        "es": "Grandes aves zancudas con cuerpos blancos, plumas de alas negras y patas rojas largas. Son famosas por construir nidos grandes en los tejados y traer buena suerte en el folclore.",
        "fr": "Grands échassiers au corps blanc, plumes d'ailes noires et longues pattes rouges. Ils sont célèbres pour construire de grands nids sur les toits et porter chance dans le folklore."
    },
    "Common Crane": {
        "en": "Tall, elegant birds with long necks and legs. They perform spectacular dancing displays and migrate in distinctive V-formations with loud, trumpeting calls.",
        "he": "ציפורים גבוהות ואלגנטיות עם צוואר ורגליים ארוכות. הן מבצעות תצוגות ריקוד מרהיבות ומהגרות בתצורות V מובהקות עם קריאות חצוצרה רועשות.",
        "es": "Aves altas y elegantes con cuellos y patas largas. Realizan espectaculares exhibiciones de danza y migran en formaciones V distintivas con llamadas de trompeta fuertes.",
        "fr": "Grands oiseaux élégants aux longs cous et pattes. Ils effectuent des parades dansantes spectaculaires et migrent en formations V distinctives avec des cris de trompette."
    },
    "Grey Heron": {
        "en": "Large, long-legged wading birds that stand motionless in water waiting to spear fish. They have snake-like necks that strike with lightning speed.",
        "he": "ציפורי שכשוך גדולות עם רגליים ארוכות העומדות ללא תנועה במים בהמתנה לדקור דגים. יש להן צוואר דמוי נחש שתוקף במהירות הבזק.",
        "es": "Grandes aves zancudas de patas largas que permanecen inmóviles en el agua esperando ensartar peces. Tienen cuellos como serpientes que atacan con velocidad del rayo.",
        "fr": "Grands échassiers aux longues pattes qui se tiennent immobiles dans l'eau en attendant de harponner les poissons. Ils ont des cous serpentins qui frappent avec une rapidité éclair."
    },
    "Egret": {
        "en": "Graceful white herons with slender bodies and elegant plumes. They wade through shallow water hunting fish, frogs, and insects.",
        "he": "אנפות לבנות חינניות עם גוף דק ונוצות אלגנטיות. הן משכשכות במים רדודים וצדות דגים, צפרדעים וחרקים.",
        "es": "Garcetas blancas elegantes con cuerpos delgados y plumas elegantes. Vadean por aguas poco profundas cazando peces, ranas e insectos.",
        "fr": "Aigrettes blanches gracieuses au corps élancé et plumes élégantes. Elles pataugent dans l'eau peu profonde en chassant poissons, grenouilles et insectes."
    },
    "Cormorant": {
        "en": "Dark water birds with hooked bills that dive deep to catch fish. After swimming, they dry their wings by standing with them spread wide.",
        "he": "ציפורי מים כהות עם מקור מעוקל שצוללות עמוק כדי לתפוס דגים. לאחר שחייה, הן מייבשות את כנפיהן בעמידה עם הכנפיים פרושות לרווחה.",
        "es": "Aves acuáticas oscuras con picos ganchudos que se sumergen profundamente para atrapar peces. Después de nadar, secan sus alas parándose con ellas extendidas ampliamente.",
        "fr": "Oiseaux aquatiques sombres aux becs crochus qui plongent profondément pour attraper les poissons. Après la nage, ils sèchent leurs ailes en se tenant debout avec elles largement déployées."
    },
    "Hoopoe": {
        "en": "Exotic-looking birds with fan-like crests, zebra-striped wings, and long curved bills. They probe the ground for insects with their distinctive 'hoop-hoop' call.",
        "he": "ציפורים בעלות מראה אקזוטי עם ציצית דמוית מניפה, כנפיים מפוספסות זברה ומקור ארוך ומעוקל. הן חוקרות את הקרקע לחרקים עם הקריאה המובהקת 'הופ-הופ'.",
        "es": "Aves de aspecto exótico con crestas como abanicos, alas rayadas de cebra y picos largos y curvados. Sondean el suelo en busca de insectos con su distintiva llamada 'hup-hup'.",
        "fr": "Oiseaux d'aspect exotique avec des crêtes en éventail, des ailes rayées zèbre et de longs becs courbés. Ils sondent le sol pour les insectes avec leur cri distinctif 'hup-hup'."
    },
    "Sparrowhawk": {
        "en": "Small, agile raptors that hunt other birds in woodland and gardens. They have short, rounded wings perfect for maneuvering through trees at high speed.",
        "he": "טורפים קטנים וזריזים הצדים ציפורים אחרות ביערות ובגנים. יש להם כנפיים קצרות ועגולות מושלמות לתמרון בין עצים במהירות גבוהה.",
        "es": "Pequeñas aves rapaces ágiles que cazan otras aves en bosques y jardines. Tienen alas cortas y redondeadas perfectas para maniobrar entre árboles a alta velocidad.",
        "fr": "Petits rapaces agiles qui chassent d'autres oiseaux dans les bois et jardins. Ils ont des ailes courtes et arrondies parfaites pour manœuvrer entre les arbres à grande vitesse."
    },
    "Kingfisher": {
        "en": "Jewel-like birds with brilliant blue and orange plumage. They dive from perches to catch fish with remarkable precision and speed.",
        "he": "ציפורים דמויות תכשיט עם נוצות כחולות וכתומות מבריקות. הן צוללות מענפים כדי לתפוס דגים בדיוק ומהירות יוצאי דופן.",
        "es": "Aves como joyas con plumaje azul y naranja brillante. Se sumergen desde perchas para atrapar peces con notable precisión y velocidad.",
        "fr": "Oiseaux bijoux au plumage bleu et orange éclatant. Ils plongent depuis les perchoirs pour attraper les poissons avec une précision et une vitesse remarquables."
    },
    "Nightingale": {
        "en": "Small, brown birds famous for their extraordinarily beautiful and complex songs. Males sing day and night, especially during breeding season.",
        "he": "ציפורים קטנות וחומות מפורסמות בשירים היפים והמורכבים יוצאי הדופן שלהן. זכרים שרים יום ולילה, במיוחד במהלך עונת הרבייה.",
        "es": "Pequeños pájaros marrones famosos por sus cantos extraordinariamente hermosos y complejos. Los machos cantan día y noche, especialmente durante la temporada de reproducción.",
        "fr": "Petits oiseaux bruns célèbres pour leurs chants extraordinairement beaux et complexes. Les mâles chantent jour et nuit, surtout pendant la saison de reproduction."
    },
    "Skylark": {
        "en": "Ground-nesting songbirds that perform spectacular song flights, rising high while singing continuously. They're symbols of open countryside.",
        "he": "ציפורי שיר קוננות קרקע המבצעות טיסות שיר מרהיבות, עולות גבוה תוך שירה מתמשכת. הן סמלים של כפר פתוח.",
        "es": "Pájaros cantores que anidan en el suelo que realizan vuelos de canto espectaculares, elevándose alto mientras cantan continuamente. Son símbolos de campo abierto.",
        "fr": "Oiseaux chanteurs nichant au sol qui effectuent des vols de chant spectaculaires, montant haut tout en chantant continuellement. Ils sont des symboles de campagne ouverte."
    },
    "Chaffinch": {
        "en": "Colorful finches with distinctive white wing bars. Males have pinkish breasts and blue-grey caps, while their cheerful song accelerates to a flourish.",
        "he": "חוחיות צבעוניות עם פסי כנף לבנים מובהקים. לזכרים חזה ורדרד וכיפות כחולות-אפורות, ואילו שירתם העליזה מאיצה לפריחה.",
        "es": "Pinzones coloridos con barras de alas blancas distintivas. Los machos tienen pechos rosados ​​y gorras gris-azules, mientras que su canto alegre se acelera hasta un florecimiento.",
        "fr": "Pinsons colorés aux barres alaires blanches distinctives. Les mâles ont des poitrines rosées et des calottes gris-bleu, tandis que leur chant joyeux s'accélère jusqu'à une fioriture."
    },
    "Greenfinch": {
        "en": "Stocky finches with yellow-green plumage and bright yellow wing flashes. They have powerful bills for cracking seeds and nuts.",
        "he": "חוחיות חסונות עם נוצות צהובות-ירוקות והבהובי כנף צהובים בהירים. יש להן מקור חזק לפיצוח זרעים ואגוזים.",
        "es": "Pinzones robustos con plumaje amarillo-verde y destellos de alas amarillos brillantes. Tienen picos poderosos para romper semillas y nueces.",
        "fr": "Verdiers trapus au plumage jaune-vert et éclairs d'ailes jaunes vifs. Ils ont des becs puissants pour casser les graines et les noix."
    },
    "Hawk": {
        "en": "Broad-winged raptors that soar on thermals while scanning for prey. They hunt rodents, rabbits, and other small animals with sharp talons.",
        "he": "טורפים עם כנפיים רחבות שמרחפים בטרמיקה בזמן סריקה לטרף. הם צדים מכרסמים, ארנבות ובעלי חיים קטנים אחרים עם טפרים חדים.",
        "es": "Aves rapaces de alas anchas que se elevan en térmicas mientras buscan presas. Cazan roedores, conejos y otros animales pequeños con garras afiladas.",
        "fr": "Rapaces aux ailes larges qui planent sur les thermiques en scrutant les proies. Ils chassent les rongeurs, lapins et autres petits animaux avec des serres acérées."
    },
    "Bald Eagle": {
        "en": "Majestic raptors with distinctive white heads and tails. They're powerful fishers with 7-foot wingspans and symbols of strength and freedom.",
        "he": "טורפים מלכותיים עם ראש וזנב לבנים מובהקים. הם דייגים חזקים עם מוטת כנפיים בן 7 רגל וסמלים של כוח וחירות.",
        "es": "Majestuosas aves rapaces con cabezas y colas blancas distintivas. Son poderosos pescadores con envergaduras de 7 pies y símbolos de fuerza y libertad.",
        "fr": "Rapaces majestueux aux têtes et queues blanches distinctives. Ce sont de puissants pêcheurs avec des envergures de 7 pieds et des symboles de force et de liberté."
    },
    "Osprey": {
        "en": "Fish-eating raptors with reversible outer toes for gripping slippery prey. They plunge feet-first into water to catch fish near the surface.",
        "he": "טורפים אוכלי דגים עם אצבעות חיצוניות הפיכות לאחיזת טרף חלקלק. הם צוללים רגליים קדימה למים כדי לתפוס דגים ליד פני השטח.",
        "es": "Aves rapaces que comen pescado con dedos exteriores reversibles para agarrar presas resbaladizas. Se zambullen con los pies primero en el agua para atrapar peces cerca de la superficie.",
        "fr": "Rapaces piscivores aux doigts extérieurs réversibles pour saisir les proies glissantes. Ils plongent pieds en avant dans l'eau pour attraper les poissons près de la surface."
    },
    "Peregrine Falcon": {
        "en": "The fastest animals on Earth, diving at speeds over 200 mph to strike prey in mid-air. They hunt other birds with incredible precision.",
        "he": "בעלי החיים המהירים ביותר על פני כדור הארץ, צוללים במהירויות מעל 200 mph כדי לתקוף טרף באוויר. הם צדים ציפורים אחרות בדיוק מדהים.",
        "es": "Los animales más rápidos de la Tierra, sumergiéndose a velocidades superiores a 200 mph para atacar presas en el aire. Cazan otras aves con increíble precisión.",
        "fr": "Les animaux les plus rapides de la Terre, plongeant à des vitesses de plus de 200 mph pour frapper les proies en plein vol. Ils chassent d'autres oiseaux avec une précision incroyable."
    },
    "Great Horned Owl": {
        "en": "Powerful nocturnal hunters with distinctive ear tufts and deep hooting calls. They're apex predators that can take prey as large as skunks and rabbits.",
        "he": "צוידי לילה חזקים עם ציציות אוזן מובהקות וקריאות הו-הוט עמוקות. הם טורפי פסגה שיכולים לקחת טרף גדול כמו בואשנים וארנבות.",
        "es": "Poderosos cazadores nocturnos con mechones de orejas distintivos y llamadas de ulular profundas. Son depredadores principales que pueden tomar presas tan grandes como zorrillos y conejos.",
        "fr": "Puissants chasseurs nocturnes aux aigrettes auriculaires distinctives et hululements profonds. Ce sont des prédateurs apex qui peuvent prendre des proies aussi grandes que des mouffettes et des lapins."
    },
    "Snowy Owl": {
        "en": "Arctic owls with striking white plumage and yellow eyes. Unlike most owls, they hunt during the day in their treeless tundra habitat.",
        "he": "ינשופי ארקטי עם נוצות לבנות מרשימות ועיניים צהובות. בניגוד לרוב הינשופים, הם צדים במהלך היום בבית הגידול הטונדרה חסר העצים שלהם.",
        "es": "Búhos árticos con plumaje blanco llamativo y ojos amarillos. A diferencia de la mayoría de los búhos, cazan durante el día en su hábitat de tundra sin árboles.",
        "fr": "Hiboux arctiques au plumage blanc frappant et yeux jaunes. Contrairement à la plupart des hiboux, ils chassent pendant la journée dans leur habitat de toundra sans arbres."
    },
    "Golden Eagle": {
        "en": "Large, powerful raptors with golden-brown plumage. They soar on 7-foot wingspans and hunt mammals and birds in mountainous terrain.",
        "he": "טורפים גדולים וחזקים עם נוצות חומות-זהובות. הם מרחפים על מוטות כנפיים בני 7 רגל וצדים יונקים וציפורים בשטח הררי.",
        "es": "Grandes y poderosas aves rapaces con plumaje marrón dorado. Se elevan con envergaduras de 7 pies y cazan mamíferos y aves en terreno montañoso.",
        "fr": "Grands rapaces puissants au plumage brun doré. Ils planent sur des envergures de 7 pieds et chassent mammifères et oiseaux en terrain montagneux."
    },
    "Kite": {
        "en": "Graceful raptors with long, forked tails and buoyant flight. They're masterful flyers that soar effortlessly while scanning for food, often scavenging as well as hunting.",
        "he": "טורפים חינניים עם זנבות ארוכים ומפוצלים וטיסה צפה. הם מעופפים מומחים שמרחפים ללא מאמץ תוך סריקת מזון, לעתים קרובות מזבלים וגם צדים.",
        "es": "Aves rapaces elegantes con colas largas y bifurcadas y vuelo flotante. Son voladores magistrales que se elevan sin esfuerzo mientras buscan comida, a menudo carroñando además de cazar.",
        "fr": "Rapaces gracieux aux longues queues fourchues et vol flottant. Ce sont des volants magistraux qui planent sans effort en cherchant de la nourriture, souvent charognards en plus de chasser."
    },
    "Red Kite": {
        "en": "Graceful raptors with rusty-red plumage and distinctive forked tails. They're opportunistic feeders that soar on thermals with effortless elegance.",
        "he": "טורפים חינניים עם נוצות אדומות-חלודות וזנבות מפוצלים מובהקים. הם מזיני הזדמנות המרחפים בטרמיקה באלגנטיות ללא מאמץ.",
        "es": "Aves rapaces elegantes con plumaje rojo oxidado y colas bifurcadas distintivas. Son alimentadores oportunistas que se elevan en térmicas con elegancia sin esfuerzo.",
        "fr": "Rapaces gracieux au plumage rouge rouille et queues fourchues distinctives. Ce sont des mangeurs opportunistes qui planent sur les thermiques avec une élégance sans effort."
    },
    "Downy Woodpecker": {
        "en": "Small woodpeckers with black and white markings that drum on tree trunks. They excavate nest holes and search bark crevices for insects.",
        "he": "נקרים קטנים עם סימנים שחורים ולבנים התופחים על גזעי עצים. הם חופרים חורי קן ומחפשים בסדקי קליפה אחר חרקים.",
        "es": "Pequeños pájaros carpinteros con marcas blancas y negras que tamborilear en troncos de árboles. Excavan agujeros de nidos y buscan grietas de corteza en busca de insectos.",
        "fr": "Petits pics aux marques noires et blanches qui tambourinent sur les troncs d'arbres. Ils creusent des trous de nids et fouillent les crevasses d'écorce pour les insectes."
    },
    "Great Spotted Woodpecker": {
        "en": "Bold black and white woodpeckers with distinctive drumming sounds. Males have red patches on their heads, and they excavate holes in trees for nesting.",
        "he": "נקרים שחורים ולבנים נועזים עם צלילי תיפוף מובהקים. לזכרים יש כתמים אדומים על הראש, והם חופרים חורים בעצים לקינון.",
        "es": "Audaces pájaros carpinteros blancos y negros con sonidos de tamborileo distintivos. Los machos tienen manchas rojas en la cabeza, y excavan agujeros en árboles para anidar.",
        "fr": "Pics audacieux noirs et blancs aux sons de tambourinage distinctifs. Les mâles ont des taches rouges sur la tête, et ils creusent des trous dans les arbres pour nicher."
    },
    "Woodpecker": {
        "en": "Tree-climbing birds that drum on wood with their strong bills. They have stiff tail feathers for support and sticky tongues for extracting insects from bark.",
        "he": "ציפורים מטפסות עצים התופחות על עץ עם המקור החזק שלהן. יש להן נוצות זנב נוקשות לתמיכה ולשונות דביקות להוצאת חרקים מהקליפה.",
        "es": "Aves trepadoras de árboles que tamborilear en madera con sus fuertes picos. Tienen plumas de cola rígidas para apoyo y lenguas pegajosas para extraer insectos de la corteza.",
        "fr": "Oiseaux grimpeurs d'arbres qui tambourinent sur le bois avec leurs becs forts. Ils ont des plumes de queue rigides pour le soutien et des langues collantes pour extraire les insectes de l'écorce."
    },
    "Northern Mockingbird": {
        "en": "Gray songbirds famous for mimicking dozens of other bird species. They sing day and night, especially during breeding season, repeating each phrase several times.",
        "he": "ציפורי שיר אפורות מפורסמות בחיקוי עשרות מיני ציפורים אחרים. הם שרים יום ולילה, במיוחד במהלך עונת הרבייה, חוזרים על כל ביטוי מספר פעמים.",
        "es": "Pájaros cantores grises famosos por imitar docenas de otras especies de aves. Cantan día y noche, especialmente durante la temporada de reproducción, repitiendo cada frase varias veces.",
        "fr": "Oiseaux chanteurs gris célèbres pour imiter des dizaines d'autres espèces d'oiseaux. Ils chantent jour et nuit, surtout pendant la saison de reproduction, répétant chaque phrase plusieurs fois."
    },
    "American Goldfinch": {
        "en": "Small finches that molt twice a year, with males turning brilliant yellow in summer. They specialize in eating seeds and perform acrobatic feeding flights.",
        "he": "חוחיות קטנות שמשיל פעמיים בשנה, עם זכרים הופכים לצהוב מבריק בקיץ. הן מתמחות באכילת זרעים ומבצעות טיסות האכלה אקרובטיות.",
        "es": "Pequeños pinzones que mudan dos veces al año, con machos que se vuelven amarillo brillante en verano. Se especializan en comer semillas y realizan vuelos de alimentación acrobáticos.",
        "fr": "Petits chardonnerets qui muent deux fois par an, les mâles devenant jaune vif en été. Ils se spécialisent dans la consommation de graines et effectuent des vols d'alimentation acrobatiques."
    },
    "Chickadee": {
        "en": "Small, friendly birds with black caps and bibs. Named for their distinctive 'chick-a-dee-dee-dee' call, they're acrobatic feeders that cache food for winter.",
        "he": "ציפורים קטנות וידידותיות עם כיפות וחיבות שחורות. נקראות על שם הקריאה המובהקת 'צ'יק-א-די-די-די', הן מזיני אקרובטיקה המאחסנות מזון לחורף.",
        "es": "Pequeños pájaros amigables con gorras y baberos negros. Nombrados por su llamada distintiva 'chick-a-dee-dee-dee', son alimentadores acrobáticos que almacenan comida para el invierno.",
        "fr": "Petits oiseaux amicaux avec des calottes et bavettes noires. Nommés pour leur cri distinctif 'chick-a-dee-dee-dee', ce sont des mangeurs acrobatiques qui cachent de la nourriture pour l'hiver."
    },
    "Titmouse": {
        "en": "Active, crested songbirds related to chickadees. They're curious, social birds that visit feeders and cache seeds in bark crevices for later.",
        "he": "ציפורי שיר פעילות עם ציצית הקשורות לירגזים. הן ציפורים סקרניות וחברתיות המבקרות באבוסים ומאחסנות זרעים בסדקי קליפה למאוחר יותר.",
        "es": "Pájaros cantores activos con crestas relacionados con carboneros. Son aves curiosas y sociales que visitan comederos y almacenan semillas en grietas de corteza para más tarde.",
        "fr": "Oiseaux chanteurs actifs à crête apparentés aux mésanges. Ce sont des oiseaux curieux et sociaux qui visitent les mangeoires et cachent des graines dans les crevasses d'écorce pour plus tard."
    },
    "Cedar Waxwing": {
        "en": "Sleek, crested birds with yellow-tipped tails and red waxy wing tips. They travel in flocks, feeding on berries and catching insects in aerial swoops.",
        "he": "ציפורים חלקות עם ציצית וזנבות בעלי קצה צהוב וקצות כנף שעווה אדומות. הן נוסעות בלהקות, ניזונות מפירות יער ותופסות חרקים בטיסות אוויריות.",
        "es": "Pájaros elegantes con crestas con colas de punta amarilla y puntas de alas cerosas rojas. Viajan en bandadas, alimentándose de bayas y atrapando insectos en picadas aéreas.",
        "fr": "Oiseaux élégants à crête avec des queues à bout jaune et des extrémités d'ailes cireuses rouges. Ils voyagent en groupes, se nourrissant de baies et attrapant des insectes en piqués aériens."
    },
    "Baltimore Oriole": {
        "en": "Brilliant orange and black songbirds that weave hanging basket nests. Males are vibrant orange while females are yellowish, both with melodious songs.",
        "he": "ציפורי שיר כתומות ושחורות מבריקות שאורגות קני סל תלויים. הזכרים כתומים תוססים ואילו הנקבות צהבהבות, שתיהן עם שירים מנגנים.",
        "es": "Pájaros cantores naranja y negro brillantes que tejen nidos de cestas colgantes. Los machos son de color naranja vibrante mientras que las hembras son amarillentas, ambas con cantos melodiosos.",
        "fr": "Oiseaux chanteurs orange et noir brillants qui tissent des nids de panier suspendus. Les mâles sont orange vif tandis que les femelles sont jaunâtres, tous deux avec des chants mélodieux."
    },
    "Scarlet Tanager": {
        "en": "Stunning red birds with jet-black wings (males in breeding plumage). They forage high in forest canopies, eating insects and fruits with their thick bills.",
        "he": "ציפורים אדומות מהממות עם כנפיים שחורות כפחם (זכרים בנוצות רבייה). הן מחפשות מזון גבוה בחופות יער, אוכלות חרקים ופירות עם המקור העבה שלהן.",
        "es": "Impresionantes pájaros rojos con alas negras como carbón (machos en plumaje de reproducción). Forrajean alto en doseles de bosque, comiendo insectos y frutas con sus picos gruesos.",
        "fr": "Oiseaux rouges magnifiques aux ailes noir de jais (mâles en plumage nuptial). Ils se nourrissent haut dans les canopées forestières, mangeant des insectes et des fruits avec leurs becs épais."
    },
    "Eastern Bluebird": {
        "en": "Vibrant blue birds with rusty-orange breasts. They nest in cavities and hunt insects from perches, bringing flashes of color to open woodlands.",
        "he": "ציפורים כחולות תוססות עם חזה כתום-חלוד. הן מקננות בחללים וצדות חרקים מענפים, מביאות הבהובי צבע ליערות פתוחים.",
        "es": "Pájaros azules vibrantes con pechos naranja oxidado. Anidan en cavidades y cazan insectos desde perchas, trayendo destellos de color a bosques abiertos.",
        "fr": "Oiseaux bleus vibrants aux poitrines orange rouillé. Ils nichent dans des cavités et chassent les insectes depuis des perchoirs, apportant des éclairs de couleur aux bois ouverts."
    },
    "Hummingbird": {
        "en": "Tiny, iridescent birds that can hover in place by beating their wings up to 80 times per second. They feed on flower nectar with their long, specialized bills.",
        "he": "ציפורים זעירות ומנצנצות שיכולות לרחף במקום על ידי הנפת כנפיים עד 80 פעמים בשנייה. הן ניזונות מצוף פרחים עם המקור הארוך והמיוחד שלהן.",
        "es": "Diminutas aves iridiscentes que pueden flotar en el lugar batiendo sus alas hasta 80 veces por segundo. Se alimentan del néctar de flores con sus largos picos especializados.",
        "fr": "Minuscules oiseaux irisés qui peuvent planer sur place en battant leurs ailes jusqu'à 80 fois par seconde. Ils se nourrissent du nectar des fleurs avec leurs longs becs spécialisés."
    },
    "Wood Duck": {
        "en": "Spectacularly colorful ducks with iridescent plumage. Males have distinctive patterns and colors, while they nest in tree cavities near water.",
        "he": "ברוזים צבעוניים בצורה מרהיבה עם נוצות מנצנצות. לזכרים יש דפוסים וצבעים מובהקים, בעוד הם מקננים בחללי עצים ליד מים.",
        "es": "Patos espectacularmente coloridos con plumaje iridiscente. Los machos tienen patrones y colores distintivos, mientras que anidan en cavidades de árboles cerca del agua.",
        "fr": "Canards spectaculairement colorés au plumage irisé. Les mâles ont des motifs et couleurs distinctifs, tandis qu'ils nichent dans des cavités d'arbres près de l'eau."
    },
    "Great Blue Heron": {
        "en": "Tall, stately wading birds with blue-grey plumage. They stand motionless in shallow water, then strike with lightning speed to catch fish.",
        "he": "ציפורי שכשוך גבוהות ומלכותיות עם נוצות כחולות-אפורות. הן עומדות ללא תנועה במים רדודים, ואז תוקפות במהירות הבזק כדי לתפוס דגים.",
        "es": "Altas y majestuosas aves zancudas con plumaje gris azulado. Permanecen inmóviles en aguas poco profundas, luego atacan con velocidad del rayo para atrapar peces.",
        "fr": "Grands échassiers majestueux au plumage gris-bleu. Ils se tiennent immobiles dans l'eau peu profonde, puis frappent avec une rapidité éclair pour attraper les poissons."
    },
    "Canada Jay": {
        "en": "Fluffy grey birds with white foreheads, also called Gray Jays. They're bold forest dwellers that cache food and have remarkable memories for finding it.",
        "he": "ציפורים אפורות ופלומתיות עם מצח לבן, נקראות גם עורבני אפור. הם תושבי יער נועזים המאחסנים מזון ויש להם זיכרונות יוצאי דופן למצוא אותו.",
        "es": "Pájaros grises esponjosos con frentes blancas, también llamados arrendajos grises. Son habitantes audaces del bosque que almacenan comida y tienen recuerdos notables para encontrarla.",
        "fr": "Oiseaux gris duveteux au front blanc, aussi appelés geais gris. Ce sont des habitants audacieux de la forêt qui cachent de la nourriture et ont des mémoires remarquables pour la retrouver."
    },
    "Jay": {
        "en": "Colorful, intelligent corvids with loud, harsh calls. They collect and bury acorns for winter, playing an important role in forest regeneration.",
        "he": "עורבנים צבעוניים וחכמים עם קריאות רועשות וקשות. הם אוספים וקוברים בלוטים לחורף, ממלאים תפקיד חשוב בהתחדשות היער.",
        "es": "Córvidos coloridos e inteligentes con llamadas fuertes y ásperas. Recolectan y entierran bellotas para el invierno, desempeñando un papel importante en la regeneración forestal.",
        "fr": "Corvidés colorés et intelligents aux cris forts et rauques. Ils collectent et enterrent des glands pour l'hiver, jouant un rôle important dans la régénération forestière."
    },
    "Sandpiper": {
        "en": "Small wading birds that run along shorelines probing for food. They bob their tails constantly and often gather in flocks on mudflats.",
        "he": "ציפורי שכשוך קטנות הרצות לאורך קווי חוף ומחפשות מזון. הן מכשכשות בזנבות כל הזמן ולעתים קרובות מתאספות בלהקות על שטחי בוץ.",
        "es": "Pequeñas aves zancudas que corren por las costas sondeando en busca de comida. Menean sus colas constantemente y a menudo se reúnen en bandadas en marismas.",
        "fr": "Petits échassiers qui courent le long des rivages en cherchant de la nourriture. Ils remuent constamment leur queue et se rassemblent souvent en groupes sur les vasières."
    },
    "Lapwing": {
        "en": "Distinctive waders with crests and broad, rounded wings. Known for their tumbling display flights and loud 'peewit' calls that give them their name.",
        "he": "ציפורי שכשוך מובהקות עם ציציות וכנפיים רחבות ועגולות. ידועות בטיסות התצוגה המתהפכות שלהן ובקריאות 'פיויט' הרועשות שנותנות להן את שמן.",
        "es": "Aves zancudas distintivas con crestas y alas anchas y redondeadas. Conocidas por sus vuelos de exhibición volteadores y llamadas fuertes 'peewit' que les dan su nombre.",
        "fr": "Échassiers distinctifs avec des crêtes et des ailes larges et arrondies. Connus pour leurs vols d'affichage culbutants et cris forts 'peewit' qui leur donnent leur nom."
    },
    "Little Owl": {
        "en": "Small, chunky owls active both day and night. They have fierce yellow eyes and often bob their heads when curious or alarmed.",
        "he": "ינשופים קטנים וחסונים פעילים ביום ובלילה. יש להם עיניים צהובות עזות ולעתים קרובות מנענעים את הראש כשהם סקרנים או מודאגים.",
        "es": "Búhos pequeños y rechonchos activos tanto de día como de noche. Tienen feroces ojos amarillos y a menudo mueven la cabeza cuando están curiosos o alarmados.",
        "fr": "Petits hiboux trapus actifs jour et nuit. Ils ont de féroces yeux jaunes et hochent souvent la tête lorsqu'ils sont curieux ou alarmés."
    },
    "Tawny Owl": {
        "en": "Nocturnal woodland owls with distinctive hooting calls. They hunt rodents and small birds at night, locating prey with excellent hearing.",
        "he": "ינשופי יער ליליים עם קריאות הו-הוט מובהקות. הם צדים מכרסמים וציפורים קטנות בלילה, מאתרים טרף עם שמיעה מצוינת.",
        "es": "Búhos de bosque nocturnos con llamadas de ulular distintivas. Cazan roedores y pequeñas aves por la noche, localizando presas con excelente audición.",
        "fr": "Hiboux forestiers nocturnes aux hululements distinctifs. Ils chassent les rongeurs et petits oiseaux la nuit, localisant les proies avec une excellente audition."
    },
    "Long-eared Owl": {
        "en": "Slender owls with long ear tufts and orange eyes. They're nocturnal hunters of open country that roost in dense cover during the day.",
        "he": "ינשופים דקיקים עם ציציות אוזן ארוכות ועיניים כתומות. הם צוידי לילה של שטח פתוח שמתגודדים בכיסוי צפוף במהלך היום.",
        "es": "Búhos delgados con mechones de orejas largos y ojos naranjas. Son cazadores nocturnos de campo abierto que se posan en cobertura densa durante el día.",
        "fr": "Hiboux minces aux longues aigrettes auriculaires et yeux orange. Ce sont des chasseurs nocturnes de terrain ouvert qui se perchent dans une couverture dense pendant la journée."
    },
    "Black Redstart": {
        "en": "Small songbirds with distinctive rusty-red tails that quiver constantly. Males are dark grey-black, while they're often found around rocky habitats and buildings.",
        "he": "ציפורי שיר קטנות עם זנבות אדומים-חלודים מובהקים שרועדים כל הזמן. הזכרים אפורים-שחורים כהים, ולעתים קרובות נמצאים סביב בתי גידול סלעיים ובניינים.",
        "es": "Pequeños pájaros cantores con colas rojas oxidadas distintivas que tiemblan constantemente. Los machos son gris-negro oscuro, mientras que a menudo se encuentran alrededor de hábitats rocosos y edificios.",
        "fr": "Petits oiseaux chanteurs aux queues rouge rouille distinctives qui tremblent constamment. Les mâles sont gris-noir foncé, tandis qu'on les trouve souvent autour d'habitats rocheux et de bâtiments."
    },
    "Wheatear": {
        "en": "Ground-dwelling birds with white rumps and distinctive black 'T' patterns on their tails. They perch on rocks and fence posts in open habitats.",
        "he": "ציפורים קרקעיות עם עכוז לבן ודפוסי 'T' שחורים מובהקים על זנבותיהן. הן יושבות על סלעים ועמודי גדר בבתי גידול פתוחים.",
        "es": "Aves que viven en el suelo con rabadillas blancas y patrones distintivos de 'T' negra en sus colas. Se posan en rocas y postes de cerca en hábitats abiertos.",
        "fr": "Oiseaux vivant au sol avec des croupions blancs et des motifs distinctifs de 'T' noir sur leurs queues. Ils se perchent sur des rochers et des poteaux de clôture dans des habitats ouverts."
    },
    "Stonechat": {
        "en": "Compact songbirds that perch prominently on bushes and wires. Named for their call that sounds like two stones being knocked together.",
        "he": "ציפורי שיר קומפקטיות היושבות בולטות על שיחים וחוטים. נקראות על שם הקריאה שנשמעת כמו שתי אבנים שמוקשות יחד.",
        "es": "Pájaros cantores compactos que se posan prominentemente en arbustos y alambres. Nombrados por su llamada que suena como dos piedras golpeadas juntas.",
        "fr": "Oiseaux chanteurs compacts qui se perchent bien en vue sur les buissons et fils. Nommés pour leur cri qui ressemble à deux pierres frappées ensemble."
    },
    "Waxwing": {
        "en": "Crested songbirds with silky plumage and red waxy wing tips. They travel in nomadic flocks, feasting on berries during winter irruptions.",
        "he": "ציפורי שיר עם ציצית ונוצות משיי וקצות כנף שעווה אדומות. הן נוסעות בלהקות נוודיות, נהנות מפירות יער במהלך פרצי חורף.",
        "es": "Pájaros cantores con crestas con plumaje sedoso y puntas de alas cerosas rojas. Viajan en bandadas nómadas, festejando con bayas durante irrupciones de invierno.",
        "fr": "Oiseaux chanteurs à crête au plumage soyeux et extrémités d'ailes cireuses rouges. Ils voyagent en groupes nomades, se régalant de baies pendant les irruptions hivernales."
    }
}

def update_birds_info_json(filepath, birds_dict):
    """Update birds_info.json with new descriptions"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updates_made = 0
    # data is a dict with bird names as keys
    for name, bird in data.items():
        # Find this bird in our master list
        bird_data = birds_dict.get(name)
        if bird_data and bird_data.get('difficulty') in [1, 2]:
            # Get the display name (en field)
            display_name = bird_data['en']
            if display_name in DESCRIPTIONS:
                # Update descriptions
                desc = DESCRIPTIONS[display_name]
                if 'description' not in bird:
                    bird['description'] = {}
                bird['description']['en'] = desc['en']
                bird['description']['he'] = desc['he']
                bird['description']['es'] = desc['es']
                bird['description']['fr'] = desc['fr']
                updates_made += 1
                print(f"✓ Updated {name} (display: {display_name})")
    
    # Save updated data
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updates_made

def update_birds_data_json(filepath, birds_dict):
    """Update assets/birds_data.json with new descriptions"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    updates_made = 0
    # data is a list of bird objects
    for bird in data:
        # Extract bird name from the image field (which is the slug)
        image_name = bird.get('image', '')
        if not image_name:
            continue
        
        # Find this bird in our master list
        bird_data = birds_dict.get(image_name)
        if bird_data and bird_data.get('difficulty') in [1, 2]:
            # Get the display name (en field)
            display_name = bird_data['en']
            if display_name in DESCRIPTIONS:
                # Update descriptions
                desc = DESCRIPTIONS[display_name]
                if 'description' not in bird:
                    bird['description'] = {}
                bird['description']['en'] = desc['en']
                bird['description']['he'] = desc['he']
                bird['description']['es'] = desc['es']
                bird['description']['fr'] = desc['fr']
                updates_made += 1
                print(f"✓ Updated {image_name} (display: {display_name})")
    
    # Save updated data
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return updates_made

def main():
    # Create birds dictionary for lookup
    all_birds = birds_200._D1 + birds_200._D2 + birds_200._D3 + birds_200._D4 + birds_200._D5
    birds_dict = {b['name']: b for b in all_birds}
    
    print("Updating descriptions for level 1 and 2 birds...\n")
    
    # Update birds_info.json
    if BIRDS_INFO.exists():
        count1 = update_birds_info_json(BIRDS_INFO, birds_dict)
        print(f"\n✓ Updated {count1} birds in birds_info.json")
    else:
        print(f"✗ {BIRDS_INFO} not found")
    
    # Update assets/birds_data.json
    if BIRDS_DATA.exists():
        count2 = update_birds_data_json(BIRDS_DATA, birds_dict)
        print(f"✓ Updated {count2} birds in assets/birds_data.json")
    else:
        print(f"✗ {BIRDS_DATA} not found")
    
    print("\n✓ All descriptions updated successfully!")

if __name__ == "__main__":
    main()
