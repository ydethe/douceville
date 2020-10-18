from math import isnan
from collections import defaultdict


def to_cap(x):
    if x is None:
        return '<inconnu>'
    elif type(x) == type(0.0):
        if isnan(x):
            return '<inconnu>'
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
    if '2A' in x.upper():
        return 1021
    elif '2B' in x.upper():
        return 1022

    try:
        val = int(x)
    except Exception as e:
        val = None
    return val


def secteur_to_bool(x):
    if x == "PR" or x == "SECTEUR PRIVE":
        return 'prive'
    else:
        return 'public'


# BREVET
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
