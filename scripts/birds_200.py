"""
200 Birds master list — difficulty 1 (very common) to 5 (very rare/endangered).
Each entry: (slug, en, he, es, fr, scientific, category, difficulty, locations)
Locations: EU=Europe, US=United States, IL=Israel, AF=Africa, AS=Asia
"""

_EU = ["Europe"]
_US = ["US"]
_IL = ["Israel"]
_W  = ["Europe", "US", "Israel", "Africa", "Asia"]
_EA = ["Europe", "Israel", "Asia"]
_EI = ["Europe", "Israel"]
_UE = ["US", "Europe"]
_UA = ["US", "Africa"]
_IA = ["Israel", "Africa", "Asia"]
_AF = ["Africa"]
_AS = ["Asia"]

def _b(slug, en, he, es, fr, sci, cat, diff, locs):
    return {"name": slug, "en": en, "he": he, "es": es, "fr": fr,
            "scientific": sci, "category": cat, "difficulty": diff, "locations": locs}

# ── DIFFICULTY 1 — Very Common (40 birds) ───────────────────────────────────
_D1 = [
_b("house_sparrow","House Sparrow","דרור הבית","Gorrión común","Moineau domestique","Passer domesticus","Songbird",1,_W),
_b("rock_pigeon","Rock Dove","יונת הסלע","Paloma bravía, paloma asiática","Pigeon biset","Columba livia","Urban Bird",1,_W),
_b("common_blackbird","Common Blackbird","שחרור","Mirlo común o, más comúnmente, mirlo","Merle noir","Turdus merula","Songbird",1,_EA),
_b("european_starling","Starling","זרזיר מצוי","Estornino pinto","Étourneau sansonnet","Sturnus vulgaris","Songbird",1,_W),
_b("mallard","Mallard","ברכייה","Ánade real, ánade azulón","Canard colvert","Anas platyrhynchos","Water Bird",1,_W),
_b("canada_goose","Canada Goose","ברנטה קנדית","Barnacla canadiense","Bernache du Canada","Branta canadensis","Water Bird",1,_US),
_b("mute_swan","Mute Swan","ברבור מצוי","Cisne vulgar","Cygne tuberculé","Cygnus olor","Water Bird",1,_EI),
_b("herring_gull","Gull","שחף צפוני","Gaviota plateada","Goéland argenté","Larus argentatus","Water Bird",1,_EI),
_b("american_robin","American Robin","קיכלי אדום-חזה","Zorzal robín","Merle d'Amérique","Turdus migratorius","Songbird",1,_US),
_b("northern_cardinal","Northern Cardinal","קרדינל צפוני","Cardenal norteño","Cardinal rouge","Cardinalis cardinalis","Songbird",1,_US),
_b("blue_jay","Blue Jay","עורבני כחול","Arrendajo azul","Geai bleu","Cyanocitta cristata","Songbird",1,_US),
_b("american_crow","American Crow","עורב אמריקאי","Cuervo americano","Corneille d'Amérique","Corvus brachyrhynchos","Songbird",1,_US),
_b("eurasian_magpie","Eurasian Magpie","עקעק זנבתן","Urraca común","Pie bavarde","Pica pica","Songbird",1,_EA),
_b("great_tit","Great Tit","ירגזי מצוי","Carbonero común","Mésange charbonnière","Parus major","Songbird",1,_EA),
_b("blue_tit","Tit","ירגזי כחול","Herrerillo común","Mésange bleue","Cyanistes caeruleus","Songbird",1,_EU),
_b("barn_swallow","Barn Swallow","סנונית הרפתות","Golondrina común","Hirondelle rustique","Hirundo rustica","Songbird",1,_W),
_b("eurasian_collared_dove","Eurasian Collared Dove","תור צווארון","Tórtola turca","Tourterelle turque","Streptopelia decaocto","Urban Bird",1,_EA),
_b("common_wood_pigeon","Pigeon","יונת ענק","Paloma torcaz","Pigeon ramier","Columba palumbus","Urban Bird",1,_EI),
_b("house_finch","House Finch","פרוש הבית","Pinzón mexicano, camachuelo mexicano","Roselin familier","Haemorhous mexicanus","Songbird",1,_US),
_b("mourning_dove","Mourning Dove","יונת אבל","Tórtola llorona","Tourterelle triste","Zenaida macroura","Urban Bird",1,_US),
_b("common_myna","Common Myna","מיינה מצויה","Miná común","Martin triste","Acridotheres tristis","Songbird",1,_IA),
_b("house_crow","House Crow","עורב הודי","Cuervo indio","Corbeau familier","Corvus splendens","Urban Bird",1,_IA),
_b("european_robin","Robin","אדום-החזה","Petirrojo europeo","Rouge-gorge familier","Erithacus rubecula","Songbird",1,_EI),
_b("goldfinch","Goldfinch","חוחית","Jilguero europeo","Chardonneret élégant","Carduelis carduelis","Songbird",1,_EA),
_b("great_egret","Great Egret","לבנית גדולה","Garceta grande","Grande Aigrette","Ardea alba","Water Bird",1,_W),
_b("flamingo","Greater Flamingo","פלמינגו מצוי","Flamenco común","Flamant rose","Phoenicopterus roseus","Water Bird",1,["Israel","Africa"]),
_b("peacock","Peafowl","טווס מצוי","Pavo real común","Paon bleu","Pavo cristatus","Game Bird",1,[]),
_b("common_buzzard","Common Buzzard","עקב חורף","Busardo ratonero","Buse variable","Buteo buteo","Raptor",1,_EU),
_b("kestrel","Kestrel","בז מצוי","Cernícalo vulgar","Faucon crécerelle","Falco tinnunculus","Raptor",1,_EI),
_b("barn_owl","Barn Owl","תנשמת לבנה","Lechuza común","L'Effraie des clochers","Tyto alba","Raptor",1,["Europe","Israel","Africa"]),
_b("common_swift","Common Swift","סיס חומות","Vencejo común","Martinet noir","Apus apus","Songbird",1,_W),
_b("song_thrush","Song Thrush","קיכלי רונן","Zorzal común","Grive musicienne","Turdus philomelos","Songbird",1,_EI),
_b("pelican","Pelican","שקנאי","Pelícano dálmata","Pélican frisé","Pelecanus crispus","Water Bird",1,["Israel","Africa","Asia"]),
_b("white_stork","White Stork","חסידה לבנה","Cigüeña blanca","Cigogne blanche","Ciconia ciconia","Water Bird",1,["Europe","Israel","Africa","Asia"]),
_b("common_crane","Common Crane","עגור","Grulla común","Grue cendrée","Grus grus","Water Bird",1,_EI),
_b("grey_heron","Grey Heron","אנפה אפורה","Garza real","Héron cendré","Ardea cinerea","Water Bird",1,_EA),
_b("little_egret","Egret","לבנית קטנה","Garceta común","Aigrette garzette","Egretta garzetta","Water Bird",1,_EI),
_b("cormorant","Cormorant","קורמורן גדול","Cormorán grande","Grand Cormoran","Phalacrocorax carbo","Water Bird",1,_EI),
_b("hoopoe","Hoopoe","דוכיפת מצויה","Abubilla","Huppe fasciée","Upupa epops","Exotic Bird",1,["Europe","Israel","Africa","Asia"]),
_b("sparrowhawk","Sparrowhawk","נץ מצוי","Gavilán común","Épervier d'Europe","Accipiter nisus","Raptor",1,_EI),
]

# ── DIFFICULTY 2 — Common (40 birds) ────────────────────────────────────────
_D2 = [
_b("black_headed_gull","Gull","שחף אגמים","Gaviota reidora","Mouette rieuse","Chroicocephalus ridibundus","Water Bird",2,_EI),
_b("common_kingfisher","Kingfisher","שלדג גמדי","Martín pescador","Martin-pêcheur d'Europe","Alcedo atthis","Songbird",2,_EA),
_b("nightingale","Nightingale","זמיר הירדן","Ruiseñor común","Rossignol philomèle","Luscinia megarhynchos","Songbird",2,_EI),
_b("skylark","Skylark","זרעית השדה","Alondra común","Alouette des champs","Alauda arvensis","Songbird",2,_EU),
_b("chaffinch","Chaffinch","פרוש מצוי","Pinzón vulgar","Pinson des arbres","Fringilla coelebs","Songbird",2,_EU),
_b("greenfinch","Greenfinch","ירקון (עוף)","Verderón europeo","Verdier d'Europe","Chloris chloris","Songbird",2,_EU),
_b("red_tailed_hawk","Hawk","עקב אדום-זנב","Halcón de cola roja","Buse à queue rousse","Buteo jamaicensis","Raptor",2,_US),
_b("bald_eagle","Bald Eagle","עיטם לבן-ראש","Águila cabeza blanca","Pygargue à tête blanche","Haliaeetus leucocephalus","Raptor",2,_US),
_b("osprey","Osprey","שלך","Águila pescadora","Balbuzard pêcheur","Pandion haliaetus","Raptor",2,["Europe","Israel","US","Africa","Asia"]),
_b("peregrine_falcon","Peregrine Falcon","בז נודד","Halcón peregrino","Faucon pèlerin","Falco peregrinus","Raptor",2,_W),
_b("great_horned_owl","Great Horned Owl","אוח וירג'יניה","Búho real americano","Grand-duc d'Amérique","Bubo virginianus","Raptor",2,_US),
_b("snowy_owl","Snowy Owl","אוח השלג","Búho nival","Harfang des neiges","Bubo scandiacus","Raptor",2,["Europe","Asia"]),
_b("golden_eagle","Golden Eagle","עיט זהוב","Águila real","Aigle royal","Aquila chrysaetos","Raptor",2,_EA),
_b("black_kite","Kite","דיה שחורה","Milano negro","Milan noir","Milvus migrans","Raptor",2,["Europe","Israel","Africa","Asia"]),
_b("red_kite","Red Kite","דיה אדומה","Milano real","Milan royal","Milvus milvus","Raptor",2,_EU),
_b("downy_woodpecker","Downy Woodpecker","נקר עדין","Carpintero velloso","Pic mineur","Dryobates pubescens","Songbird",2,_US),
_b("great_spotted_woodpecker","Great Spotted Woodpecker","נקר עקוד","Pico picapinos","Pic épeiche","Dendrocopos major","Songbird",2,_EU),
_b("green_woodpecker","Woodpecker","נקר ירוק","Pito real","Pic vert","Picus viridis","Songbird",2,_EU),
_b("northern_mockingbird","Northern Mockingbird","לצן צפוני","Sinsonte norteño","Moqueur polyglotte","Mimus polyglottos","Songbird",2,_US),
_b("american_goldfinch","American Goldfinch","קנרית אמריקאית","Jilguero yanqui","Chardonneret jaune","Spinus tristis","Songbird",2,_US),
_b("black_capped_chickadee","Chickadee","ירגזי שחור-כיפה","Carbonero cabecinegro","Mésange à tête noire","Poecile atricapillus","Songbird",2,_US),
_b("tufted_titmouse","Titmouse","ירגזי דו-גוני","Carbonero copetón","Mésange bicolore","Baeolophus bicolor","Songbird",2,_US),
_b("cedar_waxwing","Cedar Waxwing","אמבלרון","Ampelis americano","Jaseur d'Amérique","Bombycilla cedrorum","Songbird",2,_US),
_b("baltimore_oriole","Baltimore Oriole","פזאי בולטימור","Turpial de Baltimore","Oriole de Baltimore","Icterus galbula","Songbird",2,_US),
_b("scarlet_tanager","Scarlet Tanager","טנאגר ארגמן","Tángara escarlata","Tangara écarlate","Piranga olivacea","Songbird",2,_US),
_b("eastern_bluebird","Eastern Bluebird","כחלי מזרחי","Azulejo oriental","Merlebleu de l'Est","Sialia sialis","Songbird",2,_US),
_b("ruby_throated_hummingbird","Hummingbird","יונק דבש גרון ארגמן","Colibrí vientre rufo","Colibri à gorge rubis","Archilochus colubris","Songbird",2,_US),
_b("wood_duck","Wood Duck","ברווז עצים","Pato joyuyo","Canard branchu","Aix sponsa","Water Bird",2,_US),
_b("great_blue_heron","Great Blue Heron","אנפה כחולה גדולה","Garza azulada","Grand Héron","Ardea herodias","Water Bird",2,_US),
_b("canada_jay","Canada Jay","עורבני קנדה","Arrendajo canadiense","Mésangeai du Canada","Perisoreus canadensis","Songbird",2,_US),
_b("eurasian_jay","Jay","עורבני שחור-כיפה","Arrendajo euroasiático","Geai des chênes","Garrulus glandarius","Songbird",2,_EU),
_b("common_sandpiper","Sandpiper","חופמי מצוי","Andarríos chico","Chevalier guignette","Actitis hypoleucos","Water Bird",2,_EI),
_b("lapwing","Lapwing","קיווית מצוייצת","Avefría europea","Vanneau huppé","Vanellus vanellus","Water Bird",2,_EU),
_b("little_owl","Little Owl","כוס החורבות","Mochuelo europeo","Chevêche d'Athéna","Athene noctua","Raptor",2,_EI),
_b("tawny_owl","Tawny Owl","לילית מצויה","Cárabo común","Chouette hulotte","Strix aluco","Raptor",2,_EU),
_b("long_eared_owl","Long-eared Owl","ינשוף עצים","Búho chico","Hibou moyen-duc","Asio otus","Raptor",2,_EI),
_b("black_redstart","Black Redstart","חכלילית סלעים","Colirrojo tizón","Rougequeue noir","Phoenicurus ochruros","Songbird",2,_EU),
_b("wheatear","Wheatear","סלעית אירופית","Collalba gris","Traquet motteux","Oenanthe oenanthe","Songbird",2,_EI),
_b("stonechat","Stonechat","דוחל שחור-גרון","Tarabilla común","Tarier pâtre","Saxicola rubicola","Songbird",2,_EI),
_b("waxwing","Waxwing","אמבלרון בוהמי","Ampelis europeo","Jaseur de Bohême","Bombycilla garrulus","Songbird",2,_EU),
]

# ── DIFFICULTY 3 — Moderately Rare (50 birds) ───────────────────────────────
_D3 = [
_b("puffin","Puffin","תוכי ים אטלנטי","Frailecillo atlántico","Macareux moine","Fratercula arctica","Water Bird",3,_EU),
_b("gannet","Gannet","סולה צפונית","Alcatraz común","Fou de Bassan","Morus bassanus","Water Bird",3,_EU),
_b("avocet","Avocet","סייפן","Avoceta común","Avocette élégante","Recurvirostra avosetta","Water Bird",3,_EI),
_b("curlew","Curlew","כרון","Zarapito real","Courlis cendré","Numenius arquata","Water Bird",3,_EU),
_b("oystercatcher","Oystercatcher","שלצדף החוף","Ostrero euroasiático","Huîtrier pie","Haematopus ostralegus","Water Bird",3,_EU),
_b("snipe","Snipe","חרטום","Agachadiza común","Bécassine des marais","Gallinago gallinago","Water Bird",3,_EU),
_b("common_tern","Common Tern","שחפית ים","Charrán común","Sterne pierregarin","Sterna hirundo","Water Bird",3,_EI),
_b("common_coot","Coot","מרית מצויה","Focha común","Foulque macroule","Fulica atra","Water Bird",3,_EI),
_b("moorhen","Moorhen","סופית מצויה","Gallineta común","Gallinule poule-d'eau","Gallinula chloropus","Water Bird",3,_EA),
_b("bittern","Bittern","כוס הסוף","Avetoro común","Butor étoilé","Botaurus stellaris","Water Bird",3,_EU),
_b("grebe","Grebe","טבלן מצויץ","Somormujo lavanco","Grèbe huppé","Podiceps cristatus","Water Bird",3,_EI),
_b("shearwater","Shearwater","יסעור אטלנטי","Pardela pichoneta","Puffin des Anglais","Puffinus puffinus","Water Bird",3,_EU),
_b("common_swift_apus","Common Swift","סיס חומות","Vencejo común","Martinet noir","Apus apus","Songbird",3,_EI),
_b("house_martin","Delichon","סנונית בתים","Avión común","Hirondelle de fenêtre","Delichon urbicum","Songbird",3,_EU),
_b("sand_martin","Swallow","כוכית גדות","Avión zapador","Hirondelle de rivage","Riparia riparia","Songbird",3,_EU),
_b("wryneck","Wryneck","סבראש","Torcecuello europeo","Torcol fourmilier","Jynx torquilla","Songbird",3,_EI),
_b("nuthatch","Nuthatch","פשוש","Trepador azul","Sittelle torchepot","Sitta europaea","Songbird",3,_EU),
_b("treecreeper","Treecreeper","זחלן","Agateador europeo","Grimpereau des jardins","Certhia familiaris","Songbird",3,_EU),
_b("wren","Wren","גדרון מצוי","Chochín común","Troglodyte mignon","Troglodytes troglodytes","Songbird",3,_EU),
_b("dunnock","Dunnock","סתרי מצוי","Acentor común","Accenteur mouchet","Prunella modularis","Songbird",3,_EU),
_b("blackcap","Blackcap","סבכי שחור-כיפה","Curruca capirotada","Fauvette à tête noire","Sylvia atricapilla","Songbird",3,_EI),
_b("garden_warbler","Garden Warbler","סבכי אפור","Curruca mosquitera","Fauvette des jardins","Sylvia borin","Songbird",3,_EU),
_b("chiffchaff","Chiffchaff","עלווית חורף","Mosquitero común","Pouillot véloce","Phylloscopus collybita","Songbird",3,_EI),
_b("willow_warbler","Willow Warbler","עלווית אפורה","Mosquitero musical","Pouillot fitis","Phylloscopus trochilus","Songbird",3,_EU),
_b("reed_warbler","Reed Warbler","קנית קטנה","Carricero común","Rousserolle effarvatte","Acrocephalus scirpaceus","Songbird",3,_EI),
_b("sedge_warbler","Sedge Warbler","קנית פסים","Carricerín común","Phragmite des joncs","Acrocephalus schoenobaenus","Songbird",3,_EU),
_b("long_tailed_tit","Tit","גנובתן אירופי","Mito común","Mésange à longue queue","Aegithalos caudatus","Songbird",3,_EU),
_b("coal_tit","Tit","ירגזי שחור","Carbonero garrapinos","Mésange noire","Periparus ater","Songbird",3,_EU),
_b("marsh_tit","Tit","ירגזי ביצות","Carbonero palustre","Mésange nonnette","Poecile palustris","Songbird",3,_EU),
_b("bullfinch","Bullfinch","אדמונית אירופית","Camachuelo común","Bouvreuil pivoine","Pyrrhula pyrrhula","Songbird",3,_EU),
_b("siskin","Siskin","חורפי","Lúgano, lugano","Tarin des aulnes","Spinus spinus","Songbird",3,_EU),
_b("linnet","Linnet","תפוחית מצויה","Pardillo común","Linotte mélodieuse","Linaria cannabina","Songbird",3,_EU),
_b("yellowhammer","Yellowhammer","גיבתון צהוב","Escribano cerillo","Bruant jaune","Emberiza citrinella","Songbird",3,_EU),
_b("corn_bunting","Corn Bunting","גיבתון עפרוני","Triguero","Bruant proyer","Emberiza calandra","Songbird",3,_EI),
_b("booted_eagle","Booted Eagle","עיט גמדי","Águila","Aigle botté","Hieraaetus pennatus","Raptor",3,_EI),
_b("short_toed_eagle","Eagle","חיוויאי הנחשים","Culebrera europea","Circaète Jean-le-Blanc","Circaetus gallicus","Raptor",3,_EI),
_b("levant_sparrowhawk","Sparrowhawk","נץ קצר-אצבעות","Gavilán griego","L'Épervier à pieds courts","Accipiter brevipes","Raptor",3,_EI),
_b("white_tailed_eagle","Eagle","עיטם לבן-זנב","Pigargo europeo","Pygargue à queue blanche","Haliaeetus albicilla","Raptor",3,_EU),
_b("marsh_harrier","Harrier","זרון סוף","Aguilucho lagunero occidental","Busard des roseaux","Circus aeruginosus","Raptor",3,_EI),
_b("montagu_harrier","Harrier","זרון פס","Aguilucho cenizo","Busard cendré","Circus pygargus","Raptor",3,_EI),
_b("hobby","Hobby","בז עצים","Alcotán europeo","Faucon hobereau","Falco subbuteo","Raptor",3,_EI),
_b("merlin","Merlin","בז גמדי","Esmerejón","Faucon émerillon","Falco columbarius","Raptor",3,_EU),
_b("lanner_falcon","Lanner Falcon","בז צוקים","Halcón borní,  barní","Faucon lanier","Falco biarmicus","Raptor",3,_IL),
_b("scops_owl","Owl","שעיר מצוי","Autillo, autillo común","Petit-duc scops","Otus scops","Raptor",3,_EI),
_b("bee_eater","Bee-eater","שרקרק מצוי","Abejaruco europeo","Guêpier d'Europe","Merops apiaster","Exotic Bird",3,_EI),
_b("roller","Roller","כחל מצוי","Carraca europea","Rollier d'Europe","Coracias garrulus","Exotic Bird",3,_EI),
_b("little_bustard","Bustard","חובה קטנה","Sisón común","Outarde canepetière","Tetrax tetrax","Game Bird",3,_EU),
_b("common_quail","Quail","שליו נודד","Codorniz común","Caille des blés","Coturnix coturnix","Game Bird",3,_EI),
_b("pheasant","Pheasant","פסיון מצוי","Faisán común","Faisan de Colchide","Phasianus colchicus","Game Bird",3,_EU),
_b("red_legged_partridge","Partridge","חוגלה אדמונית","Perdiz roja","Perdrix rouge","Alectoris rufa","Game Bird",3,_EU),
_b("kinglet","Kinglet","מלכילון אורנים","Reyezuelo sencillo","Roitelet huppé","Regulus regulus","Songbird",3,_EU),
]

# ── DIFFICULTY 4 — Rare (40 birds) ──────────────────────────────────────────
_D4 = [
_b("great_bustard","Bustard","חובה גדולה","Avutarda común","Grande Outarde","Otis tarda","Game Bird",4,_EU),
_b("black_grouse","Grouse","שכווי שחור","Gallo lira común","Tétras lyre","Lyrurus tetrix","Game Bird",4,_EU),
_b("capercaillie","Capercaillie","שכווי ענק","Urogallo común","Grand Tétras","Tetrao urogallus","Game Bird",4,_EU),
_b("grey_partridge","Partridge","חוגלית אפורה","Perdiz pardilla","Perdrix grise","Perdix perdix","Game Bird",4,_EU),
_b("water_rail","Water Rail","רלית המים","Rascón europeo","Râle d'eau","Rallus aquaticus","Water Bird",4,_EI),
_b("purple_heron","Heron","אנפה ארגמנית","Garza imperial","Héron pourpré","Ardea purpurea","Water Bird",4,_EI),
_b("night_heron","Heron","אנפת לילה מצויה","Martinete común, huaco⁸","Bihoreau gris","Nycticorax nycticorax","Water Bird",4,_EI),
_b("squacco_heron","Heron","אנפית סוף","Garcilla cangrejera","Crabier chevelu","Ardeola ralloides","Water Bird",4,_IL),
_b("glossy_ibis","Ibis","מגלן חום","Morito común","Ibis falcinelle","Plegadis falcinellus","Water Bird",4,_EI),
_b("spoonbill","Spoonbill","כפן מצוי","Espátula común","Spatule blanche","Platalea leucorodia","Water Bird",4,_EI),
_b("ferruginous_duck","Duck","צולל ביצות","Porrón pardo","Fuligule nyroca","Aythya nyroca","Water Bird",4,["Israel","Europe"]),
_b("garganey","Garganey","קרקיר","Cerceta carretona","Sarcelle d'été","Spatula querquedula","Water Bird",4,_EI),
_b("black_stork","Stork","חסידה שחורה","Cigüeña negra","Cigogne noire","Ciconia nigra","Water Bird",4,["Europe","Israel","Asia"]),
_b("saker_falcon","Saker Falcon","בז ציידים","Halcón sacre","Faucon sacre","Falco cherrug","Raptor",4,_EI),
_b("bonelli_eagle","Eagle","עיט ניצי","Águila azor perdicera","Aigle de Bonelli","Aquila fasciata","Raptor",4,_EI),
_b("imperial_eagle","Eagle","עיט שמש","Águila imperial oriental","Aigle impérial","Aquila heliaca","Raptor",4,_EI),
_b("steppe_eagle","Eagle","עיט ערבות","Águila esteparia","Aigle des steppes","Aquila nipalensis","Raptor",4,_IL),
_b("griffon_vulture","Vulture","נשר מקראי","Buitre leonado","Vautour fauve","Gyps fulvus","Raptor",4,_EI),
_b("egyptian_vulture","Vulture","רחם (עוף)","Alimoche común, abanto, guirre","Vautour percnoptère","Neophron percnopterus","Raptor",4,_EI),
_b("black_vulture","Vulture","עוזנייה שחורה","Buitre negro","Vautour moine","Aegypius monachus","Raptor",4,_EU),
_b("eagle_owl","Owl","אוח מצוי","Búho real","Hibou grand-duc","Bubo bubo","Raptor",4,_EU),
_b("ural_owl","Owl","לילית אורל","Cárabo uralense","Chouette de l'Oural","Strix uralensis","Raptor",4,_EU),
_b("pygmy_owl","Owl","ינשוף גמד","Mochuelo alpino","Chevêchette d'Europe","Glaucidium passerinum","Raptor",4,_EU),
_b("tengmalm_owl","Owl","כוס חום","Mochuelo boreal","Nyctale de Tengmalm","Aegolius funereus","Raptor",4,_EU),
_b("ortolan_bunting","Bunting","גיבתון גנים","Escribano hortelano","Bruant ortolan","Emberiza hortulana","Songbird",4,_EI),
_b("hawfinch","Hawfinch","פצחן מצוי","Picogordo común","Gros-bec casse-noyaux","Coccothraustes coccothraustes","Songbird",4,_EU),
_b("crossbill","Crossbill","צלוב-מקור מצוי","Piquituerto común","Bec-croisé des sapins","Loxia curvirostra","Songbird",4,_EU),
_b("redpoll","Redpoll","חוחית אדומת מצח","Pardillo sizerín","Sizerin flammé","Acanthis flammea","Songbird",4,_EU),
_b("twite","Twite","חוחית הרים","Pardillo piquigualdo","Linotte à bec jaune","Linaria flavirostris","Songbird",4,_EU),
_b("snow_bunting","Bunting","גיבתון השלג","Escribano nival","Bruant des neiges","Plectrophenax nivalis","Songbird",4,_EU),
_b("lapland_bunting","Bunting","גיבתון לפלנד","Escribano lapón","Bruant lapon","Calcarius lapponicus","Songbird",4,_EU),
_b("brambling","Brambling","פרוש הרים","Pinzón real","Pinson du Nord","Fringilla montifringilla","Songbird",4,_EU),
_b("firecrest","Firecrest","מלכילון לבן-גבות","Reyezuelo listado","Roitelet à triple bandeau","Regulus ignicapilla","Songbird",4,_EU),
_b("bearded_tit","Tit","שפמתן","Bigotudo","Panure à moustaches","Panurus biarmicus","Songbird",4,_EU),
_b("penduline_tit","Tit","רמית (עוף)","Pájaro moscón europeo","Rémiz penduline","Remiz pendulinus","Songbird",4,_EI),
_b("wallcreeper","Wallcreeper","כותלי","Treparriscos, arañero","Tichodrome échelette","Tichodroma muraria","Songbird",4,_EU),
_b("dipper","Dipper","אמודאי אירופי","Mirlo acuático europeo","Cincle plongeur","Cinclus cinclus","Songbird",4,_EU),
_b("ring_ouzel","Ouzel","קיכלי סהרון","Mirlo capiblanco","Merle à plastron","Turdus torquatus","Songbird",4,_EU),
_b("bluethroat","Bluethroat","כחול-החזה","Pechiazul","Gorgebleue à miroir","Luscinia svecica","Songbird",4,_EI),
_b("wryneck_eur","Wryneck","סבראש","Torcecuello euroasiático","Torcol fourmilier","Jynx torquilla","Songbird",4,_EI),
]

# ── DIFFICULTY 5 — Very Rare / Endangered (30 birds) ────────────────────────
_D5 = [
_b("kakapo","Kakapo","קאקאפו","Kakapo","Kakapo","Strigops habroptilus","Exotic Bird",5,[]),
_b("california_condor","Condor","קונדור קליפורני","Cóndor de California","Condor de Californie","Gymnogyps californianus","Raptor",5,_US),
_b("philippine_eagle","Eagle","עיט פיליפיני","Águila monera","Pithécophage des Philippines","Pithecophaga jefferyi","Raptor",5,["Asia"]),
_b("whooping_crane","Crane","עגור אמריקאי","Grulla trompetera","Grue blanche","Grus americana","Water Bird",5,_US),
_b("california_clapper_rail","Rail","רעמית קליפורניה","Rascón de Ridgway","Râle de Californie","Rallus obsoletus","Water Bird",5,_US),
_b("spixs_macaw","Macaw","מקאו ספיקס","Guacamayo de Spix","Ara de Spix","Cyanopsitta spixii","Exotic Bird",5,[]),
_b("blue_throated_macaw","Parrot","ארה כחולת-גרון","Guacamayo barba azul","L'Ara canindé","Ara glaucogularis","Exotic Bird",5,[]),
_b("regent_honeyeater","Honeyeater","ינשוף הדבש","Mielero regente","Méliphage régent","Anthochaera phrygia","Exotic Bird",5,[]),
_b("forest_owlet","Owlet","כוס יער","Mochuelo forestal","Chevêche forestière","Heteroglaux blewitti","Raptor",5,["Asia"]),
_b("stellers_sea_eagle","Eagle","עיטם שטלר","Pigargo de Steller","Pygargue empereur","Haliaeetus pelagicus","Raptor",5,["Asia"]),
_b("harpy_eagle","Eagle","הרפיה (עוף)","Águila harpía","Harpie féroce","Harpia harpyja","Raptor",5,[]),
_b("martial_eagle","Eagle","עיט לוחם","Águila marcial","Aigle martial","Polemaetus bellicosus","Raptor",5,_AF),
_b("secretary_bird","Secretarybird","לבלר (עוף)","Secretario","Messager sagittaire","Sagittarius serpentarius","Raptor",5,_AF),
_b("shoebill","Shoebill","מנעלן","Picozapato","Bec-en-sabot du Nil","Balaeniceps rex","Water Bird",5,_AF),
_b("african_spoonbill","Spoonbill","כפן אפריקאי","Espátula africana","Spatule d'Afrique","Platalea alba","Water Bird",5,_AF),
_b("javan_rhino_hornbill","Hornbill","קלאו קרנפי","Cálao rinoceronte","Calao rhinocéros","Buceros rhinoceros","Exotic Bird",5,["Asia"]),
_b("resplendent_quetzal","Quetzal","קורוקו הדור","Quetzal resplandeciente","Quetzal resplendissant","Pharomachrus mocinno","Exotic Bird",5,[]),
_b("superb_lyrebird","Lyrebird","נבלי הדור","Ave lira soberbia","Ménure superbe","Menura novaehollandiae","Exotic Bird",5,[]),
_b("bird_of_paradise","Bird-of-paradise","בת עדן ראגי","Raggi","Paradisier de Raggi","Paradisaea raggiana","Exotic Bird",5,[]),
_b("kiwi","Kiwi","קיווי חום דרומי","Kiwi común","Kiwi austral","Apteryx australis","Flightless Bird",5,[]),
_b("bali_myna","Myna","מיינה באלי","Estornino de Bali","L'Étourneau de Rothschild","Leucopsar rothschildi","Exotic Bird",5,["Asia"]),
_b("palawan_peacock_pheasant","Pheasant","טווסון פלאוואן","Espejuelo de Palawán","L'Éperonnier napoléon","Polyplectron napoleonis","Game Bird",5,["Asia"]),
_b("blue_crowned_laughingthrush","Laughingthrush","פשפשון כתר כחול","Charlatán coroniazul","Garrulaxe de Courtois","Pterorhinus courtoisi","Songbird",5,["Asia"]),
_b("amsterdam_albatross","Albatross","אלבטרוס אמסטרדם","Albatros de Ámsterdam","Albatros d'Amsterdam","Diomedea amsterdamensis","Water Bird",5,[]),
_b("cahow","Petrel","יסעור ברמודה","Petrel cahow","Pétrel des Bermudes","Pterodroma cahow","Water Bird",5,_US),
_b("ivory_billed_woodpecker","Woodpecker","נקר שנהבי","Carpintero pico de marfil","Pic à bec ivoire","Campephilus principalis","Songbird",5,_US),
_b("po_ouli","Po'ouli","פואולי","Po-o-uli masqué","Poʻouli","Melamprosops phaeosoma","Songbird",5,_US),
_b("giant_ibis","Ibis","מגלן ענק","Ibis gigante","Ibis géant","Thaumatibis gigantea","Water Bird",5,["Asia"]),
_b("new_caledonian_lorikeet","Lorikeet","לוריקיט קלדוני","Lori diadema","Lori à diadème","Charmosyna diadema","Exotic Bird",5,[]),
_b("swift_parrot","Parrot","תוכי מהיר","Periquito migrador","Perruche de Latham","Lathamus discolor","Exotic Bird",5,[]),
]

# ── Combined list ────────────────────────────────────────────────────────────
BIRDS_200 = _D1 + _D2 + _D3 + _D4 + _D5

if __name__ == "__main__":
    from collections import Counter
    diff = Counter(b["difficulty"] for b in BIRDS_200)
    print(f"Total: {len(BIRDS_200)} birds")
    for d in sorted(diff):
        print(f"  Level {d}: {diff[d]} birds")
