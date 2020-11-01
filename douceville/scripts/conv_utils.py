from math import isnan
from collections import defaultdict

from slugify import slugify


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


def to_nature(x):
    s = slugify(x)
    if "elementaire" in s:
        return "elementaire"
    elif "college" in s:
        return "college"
    elif "lycee" in s:
        return "lycee"
    elif "prof" in s:
        return "lycee"
    elif "maternelle" in s:
        return "maternelle"
    else:
        return s


def to_maj(x):
    return str(x).upper()


def to_min(x):
    return str(x).lower()


def idty(x):
    return x


def to_float(x):
    try:
        val = float(x)
        if isnan(val):
            val = None
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
    if type(x) != type(""):
        return None
    elif x == "SANS OBJET":
        return "public"
    elif x == "PR" or x == "SECTEUR PRIVE":
        return "prive"
    elif x == "PU" or x == "SECTEUR PUBLIC":
        return "public"
    else:
        return x.lower()


def cp_to_dep(x):
    x = str(x)
    if x == "-":
        return None
    if len(x) >= 4:
        return to_int(x[:-3])
    elif len(x) == 2:
        return to_int(x)
    else:
        return None


def to_lieu_dit(x):
    ld = x
    if type(ld) == type(""):
        res = to_min(x)
    else:
        res = None
    return res


def corr_diplome(nom, groupe):
    corr = defaultdict(dict)

    if nom == "brevet":
        corr["nom_diplome"] = "brevet"
        corr["etabl"]["Patronyme"] = (("nom", to_cap),)
        corr["etabl"]["Libellé académie"] = (("academie", to_cap),)
        corr["etabl"]["Commune"] = (("code_postal", to_maj),)
        corr["etabl"]["Commune_et_arrondissement"] = (
            ("code_postal", to_maj),
            ("departement", cp_to_dep),
        )
        corr["etabl"]["Commune et arrondissement"] = (
            ("code_postal", to_maj),
            ("departement", cp_to_dep),
        )
        corr["etabl"]["Code département"] = (("departement", to_int),)
        corr["etabl"]["Secteur d'enseignement"] = (("secteur", secteur_to_bool),)
        corr["etabl"]["Secteur_d_enseignement"] = (("secteur", secteur_to_bool),)
        corr["etabl"]["Libellé commune"] = (("commune", to_cap),)
        corr["etabl"]["Commune et arrondissement Lib L"] = (("commune", to_cap),)
        corr["etabl"]["Commune_et_arrondissement_Lib_L"] = (("commune", to_cap),)
        corr["etabl"]["Numéro d'établissement"] = (("UAI", to_maj),)
        corr["etabl"]["Numero d'etablissement"] = (("UAI", to_maj),)
        corr["etabl"]["Numero_d_etablissement"] = (("UAI", to_maj),)
        corr["res"]["Presents"] = "presents", to_int
        corr["res"]["Nombre_de_presents"] = "presents", to_int
        corr["res"]["Nombre de présents"] = "presents", to_int
        corr["res"]["Admis"] = "admis", to_int
        corr["res"]["Nombre_total_d_admis"] = "admis", to_int
        corr["res"]["Nombre total d'admis"] = "admis", to_int
        corr["res"]["Admis sans mention"] = "mentions", to_int
        corr["res"]["Nombre_d_admis_sans_Mention"] = "mentions", to_int
        corr["res"]["Nombre d'admis sans Mention"] = "mentions", to_int
    else:
        corr["nom_diplome"] = "bac_%s" % (nom.lower())
        corr["etabl"]["UAI"] = (("UAI", to_maj),)
        corr["etabl"]["NOM_UAI"] = (("nom", to_cap),)
        corr["etabl"]["ACAD"] = (("academie", to_cap),)
        corr["etabl"]["DEP"] = (("departement", to_int),)
        corr["etabl"]["SECTEUR"] = (("secteur", secteur_to_bool),)
        corr["etabl"]["COMMUNE_UAI"] = (("commune", to_cap),)

        for c in groupe:
            corr["res"]["Presents_%s" % c] = "presents", to_int
            corr["res"]["Admis_%s" % c] = "admis", to_int
            corr["res"]["Mentions_%s" % c] = "mentions", to_int
            corr["res"]["Taux_%s" % c] = "taux", to_int

    return corr


coor_nature = {}
coor_nature["maternelle"] = ["maternelle"]
coor_nature["elementaire"] = ["elementaire"]
coor_nature["college"] = ["college"]
coor_nature["lycee"] = ["lycee"]
coor_nature["ecole-de-plein-air"] = []
coor_nature["ecole-sans-effectifs-permanents"] = []
coor_nature["ecole-regionale-du-premier-degre"] = ("maternelle", "elementaire")
coor_nature["ecole-secondaire-specialisee-2-d-cycle"] = ("college", "lycee")
coor_nature["etablissement-de-reinsertion-scolaire"] = []
coor_nature["etablissement-experimental"] = []
coor_nature["etablissement-regional-d-enseignt-adapte"] = []
coor_nature["maison-familiale-rurale-education-orient"] = []
coor_nature["section-enseigt-general-et-technologique"] = []
