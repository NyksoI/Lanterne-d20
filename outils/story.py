"""Données du jeu : règles (races, classes, compétences), PNJ et aventure.
Construit app/src/main/assets/game.json.
Placeholders dans les textes : {nom}, {race}, {classe}.
"""
import json, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from portraits import build as build_portraits
from font import FONT, lantern

ABILITIES = [
    {"id": "FOR", "name": "Force"}, {"id": "DEX", "name": "Dextérité"}, {"id": "CON", "name": "Constitution"},
    {"id": "INT", "name": "Intelligence"}, {"id": "SAG", "name": "Sagesse"}, {"id": "CHA", "name": "Charisme"},
]

SKILLS = {
    "persuasion": ["Persuasion", "CHA"], "tromperie": ["Tromperie", "CHA"],
    "intimidation": ["Intimidation", "CHA"], "representation": ["Représentation", "CHA"],
    "perspicacite": ["Perspicacité", "SAG"], "perception": ["Perception", "SAG"],
    "medecine": ["Médecine", "SAG"], "investigation": ["Investigation", "INT"],
    "arcanes": ["Arcanes", "INT"], "histoire": ["Histoire", "INT"], "religion": ["Religion", "INT"],
    "athletisme": ["Athlétisme", "FOR"], "discretion": ["Discrétion", "DEX"],
    "escamotage": ["Escamotage", "DEX"], "acrobaties": ["Acrobaties", "DEX"],
}

# bonus : caractéristiques ; skills : maîtrises raciales
RACES = [
    ("humain", "Humain", "Polyvalent et ambitieux.", {"FOR": 1, "DEX": 1, "CON": 1, "INT": 1, "SAG": 1, "CHA": 1}, []),
    ("elfe", "Elfe", "Gracieux, l'oreille fine, mémoire de plusieurs siècles.", {"DEX": 2, "INT": 1}, ["perception"]),
    ("demi_elfe", "Demi-Elfe", "Entre deux mondes, à l'aise partout.", {"CHA": 2, "DEX": 1}, ["persuasion"]),
    ("nain", "Nain", "Robuste comme la pierre, rancunier comme elle.", {"CON": 2, "SAG": 1}, ["histoire"]),
    ("halfelin", "Halfelin", "Petit, chanceux et bien plus malin qu'on ne croit.", {"DEX": 2, "CHA": 1}, ["discretion"]),
    ("gnome", "Gnome", "Curieux, inventif, intarissable.", {"INT": 2, "DEX": 1}, ["arcanes"]),
    ("tieffelin", "Tieffelin", "Sang infernal, cornes et regard de braise.", {"CHA": 2, "INT": 1}, ["tromperie"]),
    ("drakeide", "Drakéide", "Descendant des dragons, fier et imposant.", {"FOR": 2, "CHA": 1}, ["intimidation"]),
    ("demi_orc", "Demi-Orc", "Force brute et volonté de fer.", {"FOR": 2, "CON": 1}, ["intimidation"]),
    ("githyanki", "Githyanki", "Guerrier astral au code d'honneur implacable.", {"FOR": 2, "INT": 1}, ["athletisme"]),
    ("aasimar", "Aasimar", "Touché par le divin, une lueur dans le regard.", {"CHA": 2, "SAG": 1}, ["religion"]),
    ("tabaxi", "Tabaxi", "Félin agile, curieux de tout ce qui brille.", {"DEX": 2, "CHA": 1}, ["perception"]),
    ("goliath", "Goliath", "Géant des montagnes, compétitif jusqu'à l'os.", {"FOR": 2, "CON": 1}, ["athletisme"]),
    ("firbolg", "Firbolg", "Gardien des forêts, doux et discret.", {"SAG": 2, "FOR": 1}, ["medecine"]),
]

# scores de base FOR DEX CON INT SAG CHA
CLASSES = [
    ("barde", "Barde", "Charme, musique et mensonges élégants.", [8, 14, 12, 13, 10, 15],
     ["persuasion", "tromperie", "representation", "perspicacite"]),
    ("roublard", "Roublard", "Ombres, serrures et poches des autres.", [10, 15, 13, 12, 14, 8],
     ["discretion", "escamotage", "tromperie", "perception"]),
    ("guerrier", "Guerrier", "Acier, muscles et regard qui glace.", [15, 13, 14, 8, 12, 10],
     ["athletisme", "intimidation", "perception"]),
    ("magicien", "Magicien", "Savoir arcanique et esprit affûté.", [8, 14, 13, 15, 12, 10],
     ["arcanes", "histoire", "investigation", "perspicacite"]),
    ("clerc", "Clerc", "La foi comme bouclier, la parole comme remède.", [13, 10, 14, 8, 15, 12],
     ["religion", "medecine", "perspicacite", "persuasion"]),
    ("paladin", "Paladin", "Un serment sacré et une volonté inébranlable.", [15, 8, 13, 10, 12, 14],
     ["athletisme", "intimidation", "persuasion", "religion"]),
    ("occultiste", "Occultiste", "Un pacte avec une entité. Des secrets à la pelle.", [8, 14, 13, 12, 10, 15],
     ["arcanes", "tromperie", "intimidation", "investigation"]),
    ("rodeur", "Rôdeur", "Pisteur infatigable, l'œil partout.", [12, 15, 13, 10, 14, 8],
     ["perception", "discretion", "athletisme", "perspicacite"]),
]

NPCS = {
    "ondine": {"name": "Mère Ondine", "race": "Aasimar", "title": "Prêtresse de l'Aube", "portrait": "npc_ondine"},
    "grommash": {"name": "Grommash", "race": "Demi-Orc", "title": "Videur du Chaudron", "portrait": "npc_grommash"},
    "brunhilde": {"name": "Brunhilde Martelfer", "race": "Naine", "title": "Tavernière", "portrait": "npc_brunhilde"},
    "zephyr": {"name": "Zéphyr", "race": "Tieffelin", "title": "Marchand de secrets", "portrait": "npc_zephyr"},
    "pipo": {"name": "Pipo Pieddoux", "race": "Halfelin", "title": "Pickpocket", "portrait": "npc_pipo"},
    "voss": {"name": "Capitaine Voss", "race": "Drakéide", "title": "Garde des docks", "portrait": "npc_voss"},
    "kezra": {"name": "Kezra", "race": "Githyanki", "title": "Mercenaire", "portrait": "npc_kezra"},
    "ithil": {"name": "Lady Ithil Sylvenar", "race": "Elfe", "title": "Noble de Port-Brume", "portrait": "npc_ithil"},
}


def say(text, nxt="Continuer"):
    return {"text": nxt, "next": text}


def c(text, next=None, **kw):
    d = {"text": text}
    if next:
        d["next"] = next
    m = {"races": "races", "classes": "classes", "requires": "requires", "hide": "hideIf", "set": "set"}
    for k, v in kw.items():
        if k == "check":
            skill, dc, ok, ko = v[:4]
            d["check"] = {"skill": skill, "dc": dc}
            if len(v) > 4:
                d["check"]["advantage"] = v[4]
            d["success"] = ok
            d["failure"] = ko
        else:
            d[m[k]] = v
    return d


N = {}


def node(id, npc, text, choices=None, **kw):
    n = {"npc": npc, "text": text, "choices": choices or []}
    n.update(kw)
    N[id] = n


# ─────────────────────────── ACTE I : LE TEMPLE ───────────────────────────
node("intro", None,
     "Port-Brume, à la tombée de la nuit. La pluie fouette les pavés et, au large, la Brume grignote déjà la mer. "
     "Une cloche sonne sans fin au Temple de l'Aube. On t'a fait venir en urgence, {nom}.",
     [c("Entrer dans le temple", "ondine_1")])

node("ondine_1", "ondine",
     "Merci d'être venu si vite. Cette nuit, on a volé la Lanterne d'Aube. C'est sa lumière qui tient la Brume loin du port. "
     "Si elle n'est pas rallumée ici avant l'aube… les créatures de la Brume entreront dans la ville.",
     [c("« Je vous la ramènerai. »", "ondine_go"),
      c("« Vous me cachez quelque chose. »", check=["perspicacite", 10, "ondine_secret", "ondine_sincere"]),
      c("« Que fait vraiment cette lanterne ? »", check=["religion", 12, "ondine_lore", "ondine_go"]),
      c("« Je sens la lumière qui vous habite… la même que la mienne. »", "ondine_aasimar", races=["aasimar"]),
      c("« Votre serment est le mien. L'Aube ne tombera pas. »", "ondine_aasimar", classes=["clerc", "paladin"]),
      c("« Et qu'est-ce que j'y gagne ? »", "ondine_prix")])

node("ondine_secret", "ondine",
     "Elle détourne le regard. « Une noble, Lady Ithil Sylvenar, voulait acheter la Lanterne la semaine dernière. J'ai refusé. "
     "Je ne veux accuser personne sans preuve… mais elle n'a pas l'habitude qu'on lui dise non. »",
     [c("« C'est noté. »", "ondine_go")], set=["soupcon_ithil"])

node("ondine_sincere", "ondine",
     "Elle soutient ton regard, fatiguée. Si elle cache quelque chose, tu ne sais pas le lire. « Je n'ai que l'urgence à t'offrir. »",
     [c("Hocher la tête", "ondine_go")])

node("ondine_lore", "ondine",
     "« Ce n'est pas qu'une lampe. Sa flamme est liée à l'autel : loin du temple, elle faiblit, pâlit, puis s'éteint. "
     "Celui qui l'a volée croit avoir un trésor. Il n'aura bientôt qu'un bout de verre froid. »",
     [c("« Voilà un argument qui pourrait servir. »", "ondine_go")], set=["lore_lanterne"])

node("ondine_aasimar", "ondine",
     "Ses yeux s'illuminent. Elle pose deux doigts sur ton front et une chaleur douce t'envahit. "
     "« Que l'Aube guide ta langue et ta lame. » Tu gagnes 1 point d'inspiration.",
     [c("« Merci, Mère. »", "ondine_go")], set=["benediction"], inspiration=1)

node("ondine_prix", "ondine",
     "« Cent pièces d'or et la gratitude du temple. Et accessoirement, une ville qui ne sera pas dévorée. »",
     [c("« Marché conclu. »", "ondine_go")])

node("ondine_go", "ondine",
     "« Commence par le Chaudron Fêlé, la taverne du port. Tout ce qui se murmure à Port-Brume finit par s'y dire à voix haute. »",
     [c("Prendre la route de la taverne", "porte_1")])

# ─────────────────────────── ACTE II : LA TAVERNE ───────────────────────────
node("porte_1", "grommash",
     "Un demi-orc large comme la porte te barre le passage. « Pas d'armes dans le Chaudron. Tu les poses, ou tu repars. »",
     [c("Poser ses armes sans discuter", "porte_ok"),
      c("« Pousse-toi. »", check=["intimidation", 12, "porte_respect", "porte_boue"]),
      c("« Je viens pour une affaire du temple, tu peux me faire confiance. »", check=["persuasion", 10, "porte_ok", "porte_ok_grogne"]),
      c("« Grommash, c'est ça ? Ma mère connaissait ton clan. »", "porte_clan", races=["demi_orc", "goliath"])])

node("porte_ok", "grommash", "Il grogne, satisfait, et s'écarte. « Pas de bagarre. »", [c("Entrer", "taverne")])
node("porte_ok_grogne", "grommash", "« Le temple, hein… » Il te fouille quand même de la tête aux pieds avant de te laisser passer.",
     [c("Entrer", "taverne")])
node("porte_respect", "grommash", "Il te jauge longuement… puis éclate de rire. « Toi, t'as du cran. Garde ton arme, mais tiens-toi bien. »",
     [c("Entrer", "taverne")], set=["armes"])
node("porte_boue", "grommash",
     "Il t'attrape par le col et te dépose délicatement… dans la flaque de boue. « Réessaie, sans armes. » "
     "Toute la terrasse a vu ça.",
     [c("Se relever, poser ses armes et entrer", "taverne")], set=["boue"])
node("porte_clan", "grommash", "Son visage se fend d'un sourire plein de défenses. « Entre, frère. Garde ta hache. Et dis à Brunhilde que tu viens de ma part. »",
     [c("Entrer", "taverne")], set=["armes", "ami_grommash"])

node("taverne", None,
     "Le Chaudron Fêlé sent la bière tiède et le bois mouillé. Brunhilde essuie des chopes derrière le comptoir. "
     "Une silhouette encapuchonnée attend dans le coin le plus sombre. Un halfelin se faufile entre les tables, l'air beaucoup trop innocent.",
     [c("Parler à la tavernière", "brunhilde_1", hide=["vu_brunhilde"]),
      c("Approcher la silhouette encapuchonnée", "zephyr_1", hide=["vu_zephyr"]),
      c("Rendre la bague à Zéphyr", "zephyr_bague", requires=["bague", "vu_zephyr"], hide=["bague_rendue", "piste_docks"]),
      c("Interpeller le halfelin", "pipo_1", hide=["vu_pipo"]),
      c("Partir vers l'entrepôt 7, sur les docks", "docks", requires=["piste_docks"]),
      c("Partir vers les docks, à la recherche de l'entrepôt gardé", "docks", requires=["info_entrepot"], hide=["piste_docks"]),
      c("Partir vers les docks au hasard", "docks_hasard", hide=["piste_docks", "info_entrepot"])])

# Brunhilde
node("brunhilde_1", "brunhilde",
     "« Qu'est-ce que je te sers ? Et si c'est des ennuis, la porte est derrière toi. »",
     [c("« Une bière. Et des nouvelles. »", "brunhilde_biere"),
      c("« Grommash m'envoie. »", "brunhilde_grommash", requires=["ami_grommash"]),
      c("« Par la barbe de Moradin ! Une fille de la forge ! »", "brunhilde_nain", races=["nain"]),
      c("Frapper le comptoir : « Je veux savoir qui a volé la Lanterne. »", check=["intimidation", 15, "brunhilde_respect", "brunhilde_colere"]),
      c("« Je chante pour payer ma tournée ! »", check=["representation", 11, "brunhilde_chant", "brunhilde_hue"])],
     set=["vu_brunhilde"])

node("brunhilde_biere", "brunhilde",
     "Elle fait glisser une chope. « Des nouvelles ? Il y a des gardes devant un entrepôt des docks depuis hier. Personne ne garde des harengs comme ça. "
     "Et si tu veux des noms, le cornu dans le coin vend des secrets. Cher. »",
     [c("Remercier et revenir à la salle", "taverne")], set=["info_entrepot"])

node("brunhilde_grommash", "brunhilde",
     "« Ce gros nounours t'aime bien ? Alors moi aussi. » Elle se penche. « L'entrepôt gardé, sur les docks. Le mot de passe des gardes, c'est Fer-de-Lune. "
     "Je l'ai entendu à la troisième tournée. »",
     [c("« Je te dois une bière. »", "taverne")], set=["info_entrepot", "mot_de_passe"])

node("brunhilde_nain", "brunhilde",
     "Son visage s'éclaire. « Enfin quelqu'un de bonne pierre dans ce trou ! » Elle baisse la voix. "
     "« Entrepôt gardé sur les docks. Les gardes disent Fer-de-Lune pour passer. Cette chope est pour moi. »",
     [c("Trinquer avec elle", "taverne")], set=["info_entrepot", "mot_de_passe"])

node("brunhilde_respect", "brunhilde",
     "Elle te fixe sans ciller… puis sourit. « J'aime les gens directs. Entrepôt des docks, gardé jour et nuit depuis hier. Et le cornu dans le coin en sait plus. »",
     [c("« Merci. »", "taverne")], set=["info_entrepot"])

node("brunhilde_colere", "brunhilde",
     "Une chope te frôle l'oreille et éclate contre le mur. « On ne frappe pas MON comptoir. Bois ou dégage. » Elle te tourne le dos.",
     [c("Battre en retraite", "taverne")], set=["brunhilde_fachee"])

node("brunhilde_chant", "brunhilde",
     "La salle reprend le refrain en tapant sur les tables. Brunhilde, hilare, te glisse à l'oreille : "
     "« Entrepôt gardé sur les docks. Mot de passe : Fer-de-Lune. Tu l'as pas eu de moi. »",
     [c("Saluer la foule", "taverne")], set=["info_entrepot", "mot_de_passe"])

node("brunhilde_hue", "brunhilde",
     "Les huées couvrent ta voix. Brunhilde a pitié : « Arrête, par pitié. Va voir l'entrepôt gardé sur les docks, et laisse mes clients tranquilles. »",
     [c("Se faire tout petit", "taverne")], set=["info_entrepot"])

# Zéphyr
node("zephyr_1", "zephyr",
     "Deux yeux rouges luisent sous la capuche. « Les secrets ont un prix, étranger. Qu'est-ce que tu offres ? »",
     [c("« La ville entière brûlera dans la Brume. Toi aussi. Aide-moi. »", check=["persuasion", 13, "zephyr_info", "zephyr_faveur"]),
      c("« Je travaille pour la Garde. Parle, ou tu finis au cachot. »", check=["tromperie", 14, "zephyr_peur", "zephyr_menteur"]),
      c("« Tu as peur de quelqu'un, ça se voit. »", check=["perspicacite", 12, "zephyr_aveu", "zephyr_faveur"]),
      c("« Entre cornus, on se comprend, non ? »", "zephyr_frere", races=["tieffelin"]),
      c("Lire ses pensées superficielles (pacte occulte)", classes=["occultiste"], check=["arcanes", 12, "zephyr_aveu", "zephyr_menteur"])],
     set=["vu_zephyr"])

node("zephyr_info", "zephyr",
     "Il soupire. « Bien. Des hommes de Lady Ithil ont déposé une caisse à l'entrepôt 7. Une githyanki la garde. "
     "Et le capitaine des docks regarde ailleurs, contre de l'or. »",
     [c("« Merci, Zéphyr. »", "taverne")], set=["piste_docks", "nom_ithil"])

node("zephyr_peur", "zephyr",
     "Il pâlit. « Pas le cachot… Entrepôt 7. Les hommes de Lady Ithil. Une githyanki garde la caisse. Je n'ai rien dit ! »",
     [c("Le laisser trembler", "taverne")], set=["piste_docks", "nom_ithil"])

node("zephyr_aveu", "zephyr",
     "Ses épaules s'affaissent. « Lady Ithil. Elle a menacé de me livrer à la Garde si je parlais. La Lanterne est à l'entrepôt 7. "
     "La mercenaire qui la garde, Kezra, n'est pas mauvaise. Elle a de l'honneur. Ithil lui a menti sur ce qu'elle protège. »",
     [c("« Tu as bien fait de parler. »", "taverne")], set=["piste_docks", "nom_ithil", "kezra_honneur"])

node("zephyr_frere", "zephyr",
     "Il rabat sa capuche et sourit, crocs compris. « Un frère de sang infernal… Écoute bien. Lady Ithil. Entrepôt 7. "
     "Garde githyanki, Kezra, une femme d'honneur à qui on a menti. Et le capitaine Voss se laisse acheter. »",
     [c("« Je te revaudrai ça. »", "taverne")], set=["piste_docks", "nom_ithil", "kezra_honneur"])

node("zephyr_faveur", "zephyr",
     "« Joli discours. Mais rien n'est gratuit. Le petit halfelin là-bas m'a volé une bague. Rapporte-la-moi, et je te dirai tout. »",
     [c("« Marché conclu. »", "taverne")], set=["quete_bague"])

node("zephyr_menteur", "zephyr",
     "Il ricane. « Je vends des mensonges depuis vingt ans, je les reconnais. » Il glisse une pièce vers toi. "
     "« Prouve ta valeur : le halfelin m'a volé une bague. Rapporte-la. »",
     [c("« Très bien. »", "taverne")], set=["quete_bague"])


node("zephyr_bague", "zephyr",
     "Il fait tourner la bague entre ses doigts, ému. « Elle était à ma mère. » Puis, à voix basse : "
     "« Lady Ithil. Entrepôt 7. La garde s'appelle Kezra : une githyanki d'honneur, à qui on a menti. Dis-lui la vérité. »",
     [c("« Prends-en soin. »", "taverne")], set=["piste_docks", "nom_ithil", "kezra_honneur", "bague_rendue"])

# Pipo
node("pipo_1", "pipo",
     "Le halfelin te percute « par accident ». « Oh ! Mille pardons, je ne vous avais pas vu ! » Sa main traîne un peu trop près de ta bourse.",
     [c("« Ta main est dans ma bourse. »", check=["perception", 12, "pipo_pris", "pipo_vole"]),
      c("Lui faire les poches pendant qu'il fait les tiennes", check=["escamotage", 14, "pipo_bague", "pipo_file"]),
      c("« Cousin ! Toujours les doigts agiles ? »", "pipo_cousin", races=["halfelin", "gnome"]),
      c("« Pas de mal. Tu connais bien le port ? »", "pipo_bavard")],
     set=["vu_pipo"])

node("pipo_pris", "pipo",
     "Pris la main dans le sac, il lève les bras. « D'accord, d'accord ! Tiens, prends ça pour te faire pardonner. » "
     "Il te tend une bague gravée. « Et un tuyau gratuit : sous l'entrepôt 7, il y a une vieille bouche d'égout. Personne ne la surveille. »",
     [c("« Disparais. »", "taverne")], set=["bague", "egouts"])

node("pipo_vole", "pipo",
     "Il s'éloigne en sifflotant. Quelques minutes plus tard, tu réalises que ta bourse est plus légère. Bien joué, petit.",
     [c("Soupirer", "taverne")], set=["vole"])

node("pipo_bague", "pipo",
     "Pendant qu'il fouille ta poche, tu vides la sienne. Tu repars avec une bague gravée d'une flamme infernale. Il n'a rien senti.",
     [c("Sourire innocemment", "taverne")], set=["bague"])

node("pipo_file", "pipo",
     "Il attrape ton poignet, éclate de rire. « Pas mal ! Mais pas assez ! » Et il file par la fenêtre avant que tu puisses réagir.",
     [c("Le regarder disparaître", "taverne")])

node("pipo_cousin", "pipo",
     "Il rougit jusqu'aux oreilles. « Bon, bon… Entre cousins. » Il te rend une bague qu'il a « trouvée » sur le cornu, "
     "et te glisse : « Sous l'entrepôt 7, il y a une bouche d'égout. Personne ne la surveille. »",
     [c("« Merci, cousin. »", "taverne")], set=["bague", "egouts"])

node("pipo_bavard", "pipo",
     "« Le port ? Comme ma poche ! Enfin, comme la tienne. » Il rit. « Si tu dois entrer quelque part sur les docks, "
     "passe par les égouts. Les gardes ne descendent jamais. »",
     [c("« Bon à savoir. »", "taverne")], set=["egouts"])

# ─────────────────────────── ACTE III : LES DOCKS ───────────────────────────
node("docks_hasard", None,
     "Sous la pluie, des dizaines d'entrepôts se ressemblent tous. La Brume monte. Il faut trouver le bon, vite.",
     [c("Chercher des traces de passage récent", check=["investigation", 12, "docks", "docks_perdu"]),
      c("Tendre l'oreille", check=["perception", 13, "docks", "docks_perdu"]),
      c("Retourner à la taverne chercher des infos", "taverne")])

node("docks_perdu", None,
     "Tu tournes en rond une bonne heure avant de remarquer des torches devant l'entrepôt 7. Tu as perdu du temps : l'horizon pâlit déjà.",
     [c("Approcher", "docks")], set=["retard"])

node("docks", None,
     "L'entrepôt 7. Deux torches, une porte bardée de fer, et un drakéide en armure qui fait les cent pas, la pluie grésillant sur ses écailles.",
     [c("Parler au garde", "voss_1", hide=["voss_hostile"]),
      c("Descendre par la bouche d'égout", "egouts", requires=["egouts"]),
      c("Se glisser le long du mur jusqu'à une fenêtre", check=["discretion", 15, "entrepot_discret", "voss_alerte"])])

node("voss_1", "voss",
     "« Halte. Zone fermée sur ordre du conseil. Fais demi-tour, citoyen. »",
     [c("« Fer-de-Lune. »", "voss_passe", requires=["mot_de_passe"]),
      c("« Lady Ithil vous a payé. Si la Lanterne ne revient pas, le port meurt à l'aube. Vous aussi. »",
        requires=["nom_ithil"], check=["persuasion", 14, "voss_allie", "voss_refus", ["soupcon_ithil"]]),
      c("« Écarte-toi, lézard. »", check=["intimidation", 14, "voss_recule", "voss_refus", ["armes"]]),
      c("« Par le souffle de nos ancêtres, frère d'écailles… regarde-moi dans les yeux. »", "voss_drake", races=["drakeide"]),
      c("« Au nom de mon serment, je vous ordonne de vous écarter. »", "voss_serment", classes=["paladin"]),
      c("Reculer dans l'ombre", "docks")])

node("voss_passe", "voss",
     "Il se raidit, puis s'écarte. « Vous êtes en avance. Lady Ithil arrive à l'aube. » Il te croit de son camp.",
     [c("Entrer d'un pas assuré", "entrepot")])

node("voss_recule", "voss",
     "Il recule d'un pas, la main tremblante sur son épée. « Je… je n'ai rien vu. » Il s'éloigne dans la pluie.",
     [c("Entrer", "entrepot")])

node("voss_allie", "voss",
     "Le capitaine baisse la tête. « Je pensais garder des bijoux, pas condamner ma ville. » Il dégaine. « Je viens avec toi. »",
     [c("« Bienvenue dans l'équipe. »", "entrepot")], set=["voss_allie"])

node("voss_drake", "voss",
     "Il te fixe, puis pose un poing sur son cœur. « Ancêtre de flamme… tu as raison. J'ai pris de l'or sale. Laisse-moi réparer ça. »",
     [c("« Suis-moi. »", "entrepot")], set=["voss_allie"])

node("voss_serment", "voss",
     "Ta voix résonne comme une cloche de temple. Le drakéide recule d'un pas, honteux. « Pardonnez-moi. Je vous suis. »",
     [c("Entrer", "entrepot")], set=["voss_allie"])

node("voss_refus", "voss",
     "« Assez ! Dégage, ou je t'embroche. » Il pointe sa lance vers toi. Inutile d'insister par ici.",
     [c("Reculer", "docks")], set=["voss_hostile"])

node("voss_alerte", "voss",
     "Une latte de bois craque sous ton pied. « QUI VA LÀ ? » Le drakéide te repère et donne l'alarme : à l'intérieur, une lame sort de son fourreau.",
     [c("Foncer à l'intérieur avant qu'il ne te rattrape", "entrepot")], set=["alerte"])

node("egouts", None,
     "L'eau noire t'arrive à la taille. L'odeur est indescriptible. Une grille rouillée te sépare de l'entrepôt.",
     [c("Forcer la grille", check=["athletisme", 13, "entrepot_discret", "egouts_bruit"]),
      c("Crocheter le cadenas", check=["escamotage", 12, "entrepot_discret", "egouts_bruit"]),
      c("Trouver un autre passage dans le noir", check=["perception", 14, "entrepot_discret", "egouts_bruit"])])

node("egouts_bruit", None,
     "La grille cède dans un fracas métallique qui résonne dans tout le bâtiment. Tant pis pour la discrétion.",
     [c("Monter", "entrepot")], set=["alerte"])

node("entrepot_discret", None,
     "Tu te glisses à l'intérieur sans un bruit. Au centre, sur une caisse, la Lanterne d'Aube palpite faiblement. "
     "Une githyanki est assise juste à côté, dos à toi, aiguisant une épée d'argent.",
     [c("Prendre la Lanterne sans un bruit", check=["escamotage", 15, "fin_furtive", "kezra_1", ["benediction"]]),
      c("Se montrer et lui parler", "kezra_1")], set=["discret"])

node("entrepot", None,
     "À l'intérieur, la Lanterne d'Aube palpite faiblement sur une caisse. Devant elle, une githyanki se lève, épée d'argent en main.",
     [c("Lui faire face", "kezra_1")])

# ─────────────────────────── ACTE IV : KEZRA & ITHIL ───────────────────────────
node("kezra_1", "kezra",
     "« Un pas de plus et ma lame chante. On m'a payée pour garder cette caisse jusqu'à l'aube. Je tiens toujours parole. »",
     [c("« On t'a menti. Cette lanterne protège la ville, et Ithil va la laisser mourir. »",
        check=["persuasion", 15, "kezra_doute", "kezra_combat", ["kezra_honneur", "voss_allie"]]),
      c("« Regarde sa flamme : elle faiblit loin du temple. Ce n'est pas un trésor. »",
        check=["arcanes", 13, "kezra_doute", "kezra_combat", ["lore_lanterne"]]),
      c("« Ta parole, tu l'as donnée à une menteuse. Où est ton honneur ? »", requires=["kezra_honneur"],
        check=["perspicacite", 11, "kezra_doute", "kezra_combat"]),
      c("« Pose cette épée avant que je te la fasse avaler. »", check=["intimidation", 17, "kezra_respect", "kezra_combat"]),
      c("« Tchk'va. Une fille de Vlaakith ne sert pas une elfe. »", "kezra_gith", races=["githyanki"]),
      c("Dégainer", "kezra_combat")])

node("kezra_doute", "kezra",
     "Elle regarde la flamme vaciller. Longtemps. Puis elle abaisse son épée. « Si tu dis vrai, l'elfe m'a déshonorée. "
     "Prends-la. Et si Ithil vient la réclamer… je serai à tes côtés. »",
     [c("Prendre la Lanterne", "ithil_1")], set=["kezra_allie", "lanterne"])

node("kezra_respect", "kezra",
     "Un sourire carnassier. « Enfin quelqu'un qui ne tremble pas. » Elle te lance la Lanterne. « Je n'ai pas été payée assez pour mourir. »",
     [c("Attraper la Lanterne", "ithil_1")], set=["lanterne"])

node("kezra_gith", "kezra",
     "Elle se fige en entendant ta langue natale. « Tchk'va… » Elle s'agenouille brièvement. « Pardonne-moi. Je me bats avec toi. »",
     [c("« Relève-toi, sœur. »", "ithil_1")], set=["kezra_allie", "lanterne"])

node("kezra_combat", "kezra",
     "« Alors dansons. » Son épée d'argent fend l'air. Elle est rapide, terriblement rapide.",
     [c("Encaisser et contre-attaquer", check=["athletisme", 15, "kezra_vaincue", "fin_kezra", ["voss_allie", "armes"]]),
      c("Esquiver et la désarmer", check=["acrobaties", 15, "kezra_vaincue", "fin_kezra", ["voss_allie"]])])

node("kezra_vaincue", "kezra",
     "Son épée glisse sur le sol. Elle lève les mains, essoufflée. « Bien combattu. Prends-la. » C'est à ce moment que la porte s'ouvre.",
     [c("Se retourner", "ithil_1")], set=["lanterne"])

node("ithil_1", "ithil",
     "Lady Ithil entre, deux gardes derrière elle, son manteau à peine mouillé. « Quelle touchante scène. "
     "Rendez-moi cette lanterne, {nom}, et je vous rendrai très riche. Refusez, et vous ne verrez pas l'aube. »",
     [c("« La Brume va avaler cette ville. Vous y compris. Renoncez. »", check=["persuasion", 16, "fin_redemption", "ithil_combat", ["lore_lanterne"]]),
      c("« Trop tard. La vraie Lanterne est déjà au temple. Celle-ci n'est qu'un leurre. »", check=["tromperie", 15, "fin_ruse", "ithil_combat"]),
      c("« Vos gardes sont deux. Nous sommes plus. Partez. »", requires=["kezra_allie"],
        check=["intimidation", 13, "fin_fuite", "ithil_combat", ["voss_allie"]]),
      c("« Sylvenar… Votre lignée gardait autrefois cette ville. Qu'en penserait votre mère ? »", races=["elfe", "demi_elfe"],
        check=["histoire", 10, "fin_redemption", "ithil_combat"]),
      c("Charger", "ithil_combat")])

node("ithil_combat", "ithil",
     "« Tuez-les. » Ses gardes s'avancent et Ithil lève une main crépitante de magie.",
     [c("Foncer sur Ithil avant qu'elle ne lance son sort", check=["athletisme", 14, "fin_combat", "fin_defaite", ["kezra_allie", "voss_allie"]]),
      c("Lancer la Lanterne vers la porte et courir", check=["acrobaties", 14, "fin_combat", "fin_defaite", ["kezra_allie"]])])

# ─────────────────────────── FINS ───────────────────────────
END = lambda kind, title: {"kind": kind, "title": title}

node("fin_furtive", None,
     "Tu repars par où tu es venu, la Lanterne sous ta cape. Personne ne t'a vu. À l'aube, sa flamme se rallume sur l'autel, "
     "et la Brume recule en sifflant. Quelque part, une githyanki se demande comment elle va expliquer ça.",
     end=END("victoire", "L'ombre et la lumière"))

node("fin_redemption", "ithil",
     "Ithil regarde la flamme mourante. Ses épaules tombent. « Je voulais la vendre pour sauver ma maison… pas tuer ma ville. » "
     "Elle t'accompagne au temple et, à l'aube, la Brume recule. Port-Brume parlera longtemps de toi, {nom}.",
     end=END("victoire", "La parole plus forte que l'acier"))

node("fin_ruse", "ithil",
     "Le doute traverse son visage. « Un leurre ? » Elle siffle ses gardes et part en courant vers le temple. "
     "Le temps qu'elle comprenne, tu as déjà rallumé la Lanterne sur l'autel. La Brume recule. Le Chaudron te paie à boire pendant un mois.",
     end=END("victoire", "Le plus beau des mensonges"))

node("fin_fuite", "ithil",
     "Ithil compte vos lames, blêmit, et recule. « Ce n'est pas fini. » Elle disparaît dans la pluie. "
     "À l'aube, la Lanterne brille à nouveau sur l'autel. Mais quelque part, une noble humiliée prépare sa revanche…",
     end=END("victoire", "Une victoire… pour l'instant"))

node("fin_combat", None,
     "Le combat est bref et brutal. Ithil s'effondre, sonnée, et ses gardes s'enfuient. Tu cours jusqu'au temple, "
     "la Lanterne serrée contre toi, et la poses sur l'autel aux premières lueurs. La Brume hurle, puis recule.",
     end=END("victoire", "Par la force des armes"))

node("fin_defaite", None,
     "Une lumière violette, puis le noir. Tu te réveilles sur les pavés mouillés. L'aube est passée, et la Brume a envahi le port. "
     "Au loin, des cloches sonnent l'alarme. L'histoire de Port-Brume vient de prendre un tournant très sombre.",
     end=END("defaite", "La Brume l'emporte"))

node("fin_kezra", "kezra",
     "La lame d'argent s'arrête à un cheveu de ta gorge. « Tu t'es bien battu. Pas assez. » Elle t'assomme d'un coup de pommeau. "
     "À ton réveil, l'entrepôt est vide, et la Brume roule dans les rues.",
     end=END("defaite", "Battu par l'acier githyanki"))


def check_story():
    """Vérifie que tous les liens pointent vers des nœuds existants et que tout est atteignable."""
    errs = []
    for nid, n in N.items():
        if n.get("npc") and n["npc"] not in NPCS:
            errs.append(f"{nid}: npc inconnu {n['npc']}")
        if not n["choices"] and not n.get("end"):
            errs.append(f"{nid}: impasse")
        for ch in n["choices"]:
            for k in ("next", "success", "failure"):
                if k in ch and ch[k] not in N:
                    errs.append(f"{nid}: lien cassé {ch[k]}")
            if "check" in ch and ch["check"]["skill"] not in SKILLS:
                errs.append(f"{nid}: compétence inconnue {ch['check']['skill']}")
            if "check" not in ch and "next" not in ch:
                errs.append(f"{nid}: choix sans destination")
            for r in ch.get("races", []):
                if r not in [x[0] for x in RACES]:
                    errs.append(f"{nid}: race inconnue {r}")
            for r in ch.get("classes", []):
                if r not in [x[0] for x in CLASSES]:
                    errs.append(f"{nid}: classe inconnue {r}")
    # atteignabilité
    seen, todo = set(), ["intro"]
    while todo:
        x = todo.pop()
        if x in seen:
            continue
        seen.add(x)
        for ch in N[x]["choices"]:
            for k in ("next", "success", "failure"):
                if k in ch:
                    todo.append(ch[k])
    unreachable = set(N) - seen
    if unreachable:
        errs.append(f"inatteignables : {unreachable}")
    return errs


if __name__ == "__main__":
    errs = check_story()
    if errs:
        print("\n".join(errs)); sys.exit(1)
    game = {
        "title": "La Lanterne d'Aube",
        "start": "intro",
        "abilities": ABILITIES,
        "skills": [{"id": k, "name": v[0], "ability": v[1]} for k, v in SKILLS.items()],
        "races": [{"id": i, "name": n, "desc": d, "bonus": b, "skills": s, "portrait": i} for i, n, d, b, s in RACES],
        "classes": [{"id": i, "name": n, "desc": d, "scores": sc, "skills": s} for i, n, d, sc, s in CLASSES],
        "npcs": NPCS,
        "portraits": {**build_portraits(), "scene_lanterne": lantern()},
        "font": FONT,
        "nodes": N,
    }
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "app", "src", "main", "assets", "game.json")
    json.dump(game, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
    ends = [k for k, v in N.items() if v.get("end")]
    print(f"OK : {len(N)} scènes, {len(ends)} fins, {len(RACES)} races, {len(CLASSES)} classes -> {out}")
