from math import isnan
from collections import defaultdict


def to_cap(x):
    if x is None:
        return "<inconnu>"
    elif type(x) == type(0.0):
        if isnan(x):
            return "<inconnu>"
        else:
            return str(x)
    elif type(x) == type(""):
        return x.title()


def to_maj(x):
    return str(x).upper()


def idty(x):
    return x


def to_float(x):
    try:
        val = float(x)
    except Exception as e:
        val = None
    return val


def to_int(x):
    if "2A" in str(x).upper():
        return 1021
    elif "2B" in str(x).upper():
        return 1022

    try:
        val = int(x)
    except Exception as e:
        val = None
    return val


def secteur_to_bool(x):
    if x == "PR" or x == "SECTEUR PRIVE":
        return "prive"
    else:
        return "public"


liste_bac_techno = ["STMG", "STL", "ST2S", "STI2D", "STD2A", "TMD", "STHR"]

liste_bac_pro = [
    "Production",
    "Services",
    "Spe_pluritech",
    "Transformations",
    "Genie_civil",
    "Materiaux_souples",
    "Meca_elec",
    "Spe_plurivalentes",
    "Echanges_gestion",
    "Communication_info",
    "Services_personnes",
    "Services_collectivite",
]

# REUSSITE/MENTION BREVET
corr_brevet = defaultdict(dict)
corr_brevet["nom_diplome"] = "brevet"
corr_brevet["etabl"]["Patronyme"] = "nom", to_cap
corr_brevet["etabl"]["Libellé académie"] = "academie", to_cap
corr_brevet["etabl"]["Code département"] = "departement", to_int
corr_brevet["etabl"]["Secteur d'enseignement"] = "secteur", secteur_to_bool
corr_brevet["etabl"]["Libellé commune"] = "commune", to_cap
corr_brevet["etabl"]["Numero d'etablissement"] = "UAI", to_maj
corr_brevet["res"]["Presents"] = "presents", to_int
corr_brevet["res"]["Admis"] = "admis", to_int
corr_brevet["res"]["Admis sans mention"] = "mentions", to_int


def corr_reussite_bac(nom, col=None):
    if col is None:
        col = (nom,)

    corr = defaultdict(dict)
    corr["nom_diplome"] = "bac_%s" % (nom.lower())
    corr["etabl"]["UAI"] = "UAI", to_maj
    corr["etabl"]["NOM_UAI"] = "nom", to_cap
    corr["etabl"]["ACAD"] = "academie", to_cap
    corr["etabl"]["DEP"] = "departement", to_int
    corr["etabl"]["SECTEUR"] = "secteur", secteur_to_bool
    corr["etabl"]["COMMUNE_UAI"] = "commune", to_cap

    for c in col:
        corr["res"]["Presents_%s" % c] = "presents", to_int
        corr["res"]["Admis_%s" % c] = "admis", to_int

    return corr

def corr_mention_bac(nom, col=None):
    if col is None:
        col = (nom,)

    corr = defaultdict(dict)
    corr["nom_diplome"] = "bac_%s" % (nom.lower())
    corr["etabl"]["UAI"] = "UAI", to_maj
    corr["etabl"]["NOM_UAI"] = "nom", to_cap
    corr["etabl"]["ACAD"] = "academie", to_cap
    corr["etabl"]["DEP"] = "departement", to_int
    corr["etabl"]["SECTEUR"] = "secteur", secteur_to_bool
    corr["etabl"]["COMMUNE_UAI"] = "commune", to_cap

    for c in col:
        corr["res"]["Presents_%s" % c] = "presents", to_int
        corr["res"]["Admis_%s" % c] = "admis", to_int

    return corr
