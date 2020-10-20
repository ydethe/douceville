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


def corr_diplome(nom, col):
    corr = defaultdict(dict)
    
    if nom == 'brevet':
        corr["nom_diplome"] = "brevet"
        corr["etabl"]["Patronyme"] = "nom", to_cap
        corr["etabl"]["Libellé académie"] = "academie", to_cap
        corr["etabl"]["Code département"] = "departement", to_int
        corr["etabl"]["Secteur d'enseignement"] = "secteur", secteur_to_bool
        corr["etabl"]["Libellé commune"] = "commune", to_cap
        corr["etabl"]["Numero d'etablissement"] = "UAI", to_maj
        corr["res"]["Presents"] = "presents", to_int
        corr["res"]["Admis"] = "admis", to_int
        corr["res"]["Admis sans mention"] = "mentions", to_int
    else:
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
            corr["res"]["Mentions_%s" % c] = "mentions", to_int

    return corr
