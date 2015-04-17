#!/usr/bin/env python
# table_test.py
"""
Make a random table
"""

import argparse
import sys
import re
import json
import random


### WebAPI ###
import webapi
class WebAPI(webapi.WebAPI):
    submit_button = webapi.submit_button('Tabulate!')

    def run(self, form_input):
        headers = [random.choice(words) for x in xrange(5)]
        output = [{headers[x]:random.randint(0,100) for x in range(5)} for x in xrange(10)]

        return {'output_type' : 'table',
                'output' : output,
                'headers' : output[0].keys()}

words = ["precant", "gun", "parallelinervate", "Mider", "boun", "apograph", "apostle", "esca", "description", "superindividual", "rumfustian", "sanjakbeg", "niggling", "subbrachyskelic", "orthoaxis", "aerosteam", "shaftlike", "ullaged", "planable", "galvanocontractility", "nonrectangular", "narsinga", "upmast", "zarnich", "niggerdom", "twaddlemonger", "Jeannie", "bonetail", "tersulphate", "coinstantaneity", "ennomic", "diiamb", "niello", "vulgarian", "counterenamel", "sleepwalker", "prytany", "hatcher", "calvous", "potamophilous", "Eirene", "keratectasia", "unpossibility", "suspensation", "telephonographic", "fluvioterrestrial", "sinaite", "bravehearted", "nucleation", "tabaniform", "glycerose", "lilied", "undrilled", "trophodynamics", "Dike", "legal", "octopartite", "unsympathizability", "Sui", "decence", "unsepulchre", "Bluenoser", "echoless", "Linum", "wiskinky", "monophony", "lingula", "tecuma", "pinnae", "unsublimable", "octadic", "orthobenzoquinone", "subpolar", "telangiosis", "baud", "nymphaline", "Evadne", "cuckooflower", "morphologist", "thither", "fabulously", "demibeast", "allthing", "cowquake", "unmackly", "pustulatous", "japery", "wander", "toxin", "dihalo", "anchor", "submerse", "planity", "watertight", "Ephydra", "Hortensia", "unsavory", "whomble", "Akka", "Turklike", "thwartover", "probationership", "canopic", "unpersonal", "scelerat", "boundingly", "dismalness", "sulphbismuthite", "pinkroot", "vellinch", "immigration", "annet", "strawwalker", "bedlamite", "bullit", "heterolobous", "ungual", "overtimbered", "metadromous", "Olivier", "Cinemascope", "scrapped", "photophonic", "incestuous", "crystallochemistry", "pudicity", "Wachaga", "bacteric", "microzoal", "tawer", "concubitancy", "saccharification", "earthpea", "underdrawn", "frounce", "autobiographical", "definably", "fourstrand", "slart", "Diopsis", "falcer", "morphosis", "penstick", "eustachium", "antirevolutionist", "intersterile", "horner", "osteophlebitis", "tracheoscopy", "emmarble", "unfloatable", "rerental", "reapposition", "pewless", "Sanskrit", "derivation", "unenriching", "ligament", "tetragonidium", "buffy", "Merino", "prodivorce", "subcommit", "sapwood", "heliotropical", "bullnose", "controllership", "embracery", "micrologic", "ngapi", "nonactionable", "Bee", "caption", "pedatisected", "unclerklike", "lesiy", "discrested", "copygraph", "asystolic", "aerarium", "orthodoxist", "triconodontid", "oscillometer", "nonintersector", "Laodicean", "tubulibranchian", "premorally", "delightfully", "retrieveless", "laudatory", "microcytosis", "niterbush", "defensively", "bindwood", "polynomialism", "chined", "sestuor", "surrebuttal", "reunite", "aphorist", "unwalking", "tomfoolery", "indesirable", "humbugger", "aerostatics", "philosophism", "violence", "gondolier", "hysterics", "amarelle", "brusquely", "supercontrol", "thixle", "highboy", "androdioecism", "boroughmonger", "pollucite", "pathognomic", "torulous", "Chamaecistus", "counterindication", "woven", "orphanship", "rheumatismal", "vulgarize", "apozemical", "unconfected", "perten", "millionaire", "Lushei", "skelter", "Anodon", "philatelical", "maleficent", "chromocollography", "antibibliolatry", "undrubbed", "underlanguaged", "forbearantly", "cladoselachian", "insense", "wavewise", "manistic", "untranquil", "rectangle", "unweariness", "planiform", "wailsome", "geet", "bishopric", "autolyze", "triploidite", "bisti", "cerebric", "cystoflagellate", "misalignment", "pedicellus", "Feringi", "hemitropic", "palace", "hazardless", "obesely", "interzonal", "rootery", "cist", "undercitizen", "whirlwindish", "soundly", "dacryosyrinx", "luteal", "smeltery", "unsaddled", "Assiniboin", "Japanology", "deuteroproteose", "palaeolithoid", "goup", "ettle", "adventurish", "lardizabalaceous", "bacterioscopical", "complainant", "bywoner", "misatone", "adjunctive", "philonatural", "octodactylous", "granophyric", "whata", "echopractic", "subarcuation", "Hippuritidae", "sectiuncle", "apperceptionism", "zoophily", "tolite", "Whitsuntide", "basketmaking", "malicho", "strephonade", "nonviscid", "paralogical", "drumwood", "overwander", "persuasibly", "malmignatte", "Ardisia", "ternately", "wiz", "plinthlike", "xanthoma", "coeliomyalgia", "ureterolithotomy", "vaccicide", "camata", "cacophony", "lapidicolous", "folklorism", "machicoulis", "unisonous", "muscicole", "unshaven", "synergistically", "firedog", "gutte", "militaristic", "contradictiousness", "Baluchi", "amacrinal", "protyl", "pantamorphia", "treater", "rusky", "rhizocorm", "unpartitioned", "irritating", "unreigning", "basification", "muddiness", "obispo", "schoolward", "commendable", "pronged", "enlacement", "bulbocavernous", "eumitotic", "schloop", "misservice", "outhector", "hoodwink", "leafy", "axillar", "fairyism", "experientialist", "crowshay", "labialism", "yis", "ethologic", "pictured", "engagedly", "epicardia", "significavit", "Begoniales", "ungreased", "seducer", "helices", "roomful", "exchangeable", "stereofluoroscopic", "about", "phyla", "weigher", "iyo", "hydrastine", "printable", "topped", "repile", "bisexuous", "Quitu", "enemy", "malformation", "radicalism", "chawan", "hirudine", "innutrition", "underspore", "vaporary", "Stuartia", "underadjustment", "nonsentence", "perfectionation", "oversententious", "metempsychosical", "gametoid", "refractometry", "uncomparably", "fetometry", "bodyhood", "rabbitberry", "vomeropalatine", "Gadslid", "singled", "lapidific", "scoreless", "jungleside", "indemnity", "Exobasidium", "generalissima", "alangine", "nonproducing", "prolegomenary", "vacuous", "cervicodynia", "macromethod", "wastefully", "unscoffing", "urde", "murmurous", "osphyarthritis", "disarmingly", "unethical", "spawning", "campfight", "resorption", "semiperoid", "unlovelily", "preimprove", "anthochlorine", "stack", "kinsmanly", "deceive", "grassflat", "undercitizen", "cyclization", "witchlike", "ugsome", "hypereutectoid", "daverdy", "testamentum", "preimprove", "herniate", "Clothilda", "rotograph", "insertional", "impotency", "osteology", "uterine", "vernacularness", "inbread", "Thuringian", "Bacchical", "Varsovian", "ultraexclusive", "ferruginean", "tawdrily", "celiopyosis", "wheeple", "luculently", "stoof", "hydrodromican", "hollyhock", "coenobioid", "unadaptive", "warple", "aggregate", "psychophysiology", "neurotendinous", "horse", "disconcertedly", "mutic", "antitonic", "sigmaspire", "frumentarious", "licensed", "gaunty", "unsqueezed", "countertechnicality", "sphalerite", "tombolo", "emerge", "roriferous", "untrumping", "oriflamb", "pedograph", "tarlike", "Ditremidae", "earn", "phenomenality", "seamanlike", "paraboloidal", "ventrotomy", "hominivorous", "frequency", "unraveled", "intrachordal", "prunetol", "undeliberatingly", "Nomarthra", "cass", "chelicer", "thyroidectomy", "protopectin", "canalize", "celiomyomotomy", "vivisector", "subpubic", "martyress", "caswellite", "petiolus", "forebridge", "hydrophthalmus", "Arcifera", "epichile", "prefactory", "uninterpreted", "Medizer", "antiarthritic", "rattletrap", "locality", "filmslide", "esophagomalacia", "aglimmer", "noctograph", "spinnable", "splendaciously", "plasmodesmic", "decker", "microcolon", "puddlelike", "stigmeology", "Froebelist", "megasporic", "audibleness", "cream", "goodwillit", "Furcellaria", "stoat", "Schwalbea", "unmulcted", "jocundly", "bounce", "lipper", "unbenumb", "circumventer", "parakeratosis", "beshrivel", "andrenid", "stomacher", "parenticide", "khoja", "ungroundably", "tartratoferric", "parisonic", "restively", "daytale", "congealable", "apprehender", "nomothetes", "president", "scatophagy", "pilgrimage", "orrhoid", "gingersnap", "teneral", "Brahma", "littoral", "Krama", "Antikamnia", "superreform", "toral", "unblade", "blackhead", "horrorsome", "arundinaceous", "baidarka", "monocondylian", "antecornu", "allothigenetic", "sulphophosphorous", "veniplex", "Susquehanna", "hydroscopist", "operabily", "madrier", "mucosogranular", "metropolitical", "aminoacetone", "disherit", "scarflike", "trug", "palaeotypographical", "Rhabdophora", "iliahi", "osseous", "altrices", "remnantal", "Deiphobus", "begrudgingly", "Cristatella", "Platonicism", "end", "cest", "nonfanatical", "semicretin", "hornplant", "disruptionist", "Belleek", "primrosetide", "counterdoctrine", "restorativeness", "uppoint", "cestode", "irremissibly", "xanthochroia", "mollifyingness", "sulfoamide", "praiseworthy", "minimistic", "exomphalos", "symphyseal", "myoendocarditis", "disseize", "Kjeldahl", "overboil", "elongated", "physostomous", "Antilocapridae", "emblaze", "biomechanical", "unsentimentality", "vitrifaction", "where", "vitamin", "postdoctorate", "subgenus", "quillaic", "bristlecone", "resun", "varve", "aiguillette", "degu", "Israelitic", "bouser", "itcze", "ventilatory", "farrierlike", "phosgenic", "anthocyanidin", "liberator", "Lepidodendraceae", "dynamogenous", "undonkey", "homoeoteleuton", "Polly", "bebilya", "cellulosity", "recadency", "hedonistically", "autopathic", "overrigged", "uninthroned", "stropper", "sportswomanly", "pumple", "gymnospermal", "circumscissile", "nonsubstitution", "unmold", "tumulary", "listwork", "hyothyroid", "nonsurvival", "cartmaker", "discontinuable", "khu", "ricine", "magnum", "megafog", "nonalienation", "alcoholization", "birchman", "proadmission", "impunctual", "coredeemer", "airdrome", "Trey", "attachedly", "herschelite", "circumaviate", "lyery", "androgone", "overpole", "khalifa", "pseudalveolar", "ripsnorter", "disparager", "Dermestidae", "choanoid", "Epilachnides", "prefortunately", "litterer", "nursery", "unsolidly", "Carlo", "causticize", "Carmel", "oxblood", "Parisianization", "yappy", "pantelephonic", "postcordial", "souther", "habitable", "Polyandria", "gab", "misgraft", "saltativeness", "dispetal", "undespotic", "anopluriform", "bonaventure", "annet", "nonpredictable", "kingfish", "malpighiaceous", "Slavonize", "clonicity", "probability", "carnauba", "torrefication", "phytosaurian", "noneducation", "refutable", "subinvolution", "cathography", "clave", "constitutiveness", "rummage", "polypharmacist", "clinodiagonal", "sauropod", "trapfall", "monomastigate", "femorococcygeal", "ukiyoye", "Karaism", "catwalk", "colocentesis", "overcourtesy", "restratification", "corrigible", "pleasingness", "Derrick", "cheirognomy", "sanguineousness", "mesatipellic", "fallaciously", "hypertropical", "Gosplan", "planetal", "sensitive", "excursively", "costoxiphoid", "Hormogoneae", "transcondylar", "interdiffuse", "slather", "encyclopedia", "ungilded", "areality", "epihydric", "verticillate", "frabjous", "exomphalous", "blepharoblennorrhea", "petrifaction", "transplantar", "Natchezan", "prefortunate", "cotemporanean", "furnishing", "redback", "Mckay", "unawful", "boxbush", "myelin", "virginlike", "montmorilonite", "natimortality", "kindheartedly", "geldant", "pepperily", "watcher", "shwanpan", "bukh", "unpiety", "financier", "grudgefully", "encinillo", "endamoebiasis", "impardonably", "warmish", "flummydiddle", "churchful", "nonionized", "playfolk", "gentlemanhood", "reshape", "superinstitution", "quisquilious", "prolixly", "unassaulted", "campanular", "dobrao", "peck", "alligatored", "hyperaminoacidemia", "orchiepididymitis", "poof", "macrosporangium", "unrealize", "lithoclast", "Tubulifera", "athrob", "Hylocereus", "suckless", "trippingly", "glycogenolysis", "laterocervical", "amiced", "asterophyllite", "bisdiapason", "lifelet", "Protoceratidae", "unacademical", "extracellular", "ceryl", "vociferance", "adenomyofibroma", "forbidder", "Yankeeness", "rowdyish", "orseller", "saccharilla", "ramental", "marbler", "hypohyal", "redoublement", "retransmission", "offended", "cerithioid", "prevaccination", "oyster", "basidiolichen", "Yakan", "chalazoidite", "aphyric", "hernant", "milvine", "forty", "intersole", "arthroderm", "unmicaceous", "respiration", "graperoot", "foremade", "pterotheca", "tentation", "sciarid", "elvish", "Corybantic", "semibody", "ichneumonoid", "billow", "penetrativeness", "Phoeniculus", "encephalomere", "storekeeper", "sillyhow", "grousewards", "horsemanship", "referent", "scoptophilic", "elevation", "panpsychistic", "sceneshifter", "precandidacy", "restorable", "serpenticidal", "bozo", "whew", "Gasteropoda", "gracer", "athecate", "upland", "sleeplike", "spinales", "democrat", "sabulite", "siderographic", "relationless", "architectural", "provoking", "sadr", "ferryman", "arachnid", "cauliflower", "gimmer", "tenuiflorous", "algometry", "repatent", "heathless", "prolabor", "aerogeologist", "rehear", "rectangularly", "orthopedically", "slodder", "cathedratic", "uncustomed", "starshake", "olfactor", "evenmete", "hemorrhodin", "masoned", "finitely", "curr", "prayingly", "unethical", "confirmative", "Phaca", "orthoaxis", "odoom", "bielectrolysis", "ultrafantastic", "tunelessly", "oppositionary", "presanguine", "amphictyonic", "rutinose", "jovial", "betuckered", "astronomer", "berryless", "bashaw", "recoinage", "lucific", "predefinition", "barbellate", "unassociativeness", "Trevor", "Irene", "granitelike", "preprimitive", "boobyism", "interwrought", "Koreishite", "superoutput", "monasterial", "vertigines", "Myrsinaceae", "ovariotomist", "coloproctitis", "handrailing", "exteriorization", "Joachimite", "microchiropteran", "agglutinationist", "unbatted", "Pacinian", "undouble", "ditrigonally", "unjuvenile", "psiloceratan", "Manganja", "solitudinarian", "neuritis", "dinornithoid", "nonirreparable", "Micawberish", "unfiend", "diminutival", "floretum", "overstudious", "rainspout", "microlite", "prehorizon", "lowermost", "signal", "troctolite", "salesclerk", "ectoenzyme", "alimentariness", "catabolic", "Eleutherozoa", "piepoudre", "lisper", "stoothing", "postmastership", "indefluent"]
