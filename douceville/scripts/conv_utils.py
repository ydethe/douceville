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
    """

    Examples:
    >>> f = open('douceville/scripts/liste_nature.txt', 'r')
    >>> natures = f.readlines()
    >>> f.close()
    >>> for n in natures:
    ...    if to_nature(n) is None:
    ...       print(n.strip(), slugify(n.strip()), to_nature(n))

    """
    s = slugify(x.strip())
    if "elementaire" in s:
        nature = ["elementaire"]
    elif "elemenetaire" in s:
        nature = ["elementaire"]
    elif "elem-" in s:
        nature = ["elementaire"]
    elif "ele-" in s:
        nature = ["elementaire"]
    elif "elemenaire" in s:
        nature = ["elementaire"]
    elif "college" in s:
        nature = ["college"]
    elif "lycee" in s:
        nature = ["lycee"]
    elif "general-et-technologique" in s:
        nature = ["lycee"]
    elif "lp-" in s:
        nature = ["lycee"]
    elif "lyc-" in s:
        nature = ["lycee"]
    elif "etablissement-regional-denseignt-adapte" in s:
        nature = ["college EREA"]
    elif "maison-familiale-rurale" in s:
        nature = ["maison familiale rurale"]
    elif "prof" in s:
        nature = ["lycee"]
    elif "maternelle" in s:
        nature = ["maternelle"]
    elif "maternellle" in s:
        nature = ["maternelle"]
    elif "primaire" in s:
        nature = ["maternelle", "elementaire"]
    elif "pimaire" in s:
        nature = ["maternelle", "elementaire"]
    elif "priimaire" in s:
        nature = ["maternelle", "elementaire"]
    elif "premier-degre" in s:
        nature = ["maternelle", "elementaire"]
    elif "prmaire" in s:
        nature = ["maternelle", "elementaire"]
    elif "plein-air" in s:
        nature = ["maternelle", "elementaire"]
    elif "second-" in s:
        nature = ["college", "lycee"]
    elif "secondaire" in s:
        nature = ["college", "lycee"]
    elif "2nd-degr" in s:
        nature = ["college", "lycee"]
    elif "2d-degr" in s:
        nature = ["college", "lycee"]
    elif "2-degr" in s:
        nature = ["college", "lycee"]
    elif "segpa" in s:
        nature = ["college SEGPA"]
    elif "etablissement-de-reinsertion-scolaire" in s:
        nature = ["college ERS"]
    elif "ecole-sans-effectifs-permanents" in s:
        nature = None
    else:
        nature = None

    return nature


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


def corr_diplome(src):
    corr = defaultdict(dict)
    # nature
    if src.diplome == "brevet":
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
        corr["nom_diplome"] = "bac_%s" % (src.diplome.lower())
        corr["etabl"]["UAI"] = (("UAI", to_maj),)
        corr["etabl"]["NOM_UAI"] = (("nom", to_cap),)
        corr["etabl"]["ACAD"] = (("academie", to_cap),)
        corr["etabl"]["DEP"] = (("departement", to_int),)
        corr["etabl"]["SECTEUR"] = (("secteur", secteur_to_bool),)
        corr["etabl"]["COMMUNE_UAI"] = (("commune", to_cap),)

        if not src.backup_group is None:
            corr["res"]["Presents_%s" % src.backup_group] = "presents_bck", to_int
            corr["res"]["Admis_%s" % src.backup_group] = "admis_bck", to_int
            corr["res"]["Mentions_%s" % src.backup_group] = "mentions_bck", to_int
            corr["res"]["Taux_%s" % src.backup_group] = "taux_bck", to_int

        for c in src.groupes:
            corr["res"]["Presents_%s" % c] = "presents", to_int
            corr["res"]["Admis_%s" % c] = "admis", to_int
            corr["res"]["Mentions_%s" % c] = "mentions", to_int
            corr["res"]["Taux_%s" % c] = "taux", to_int

    return corr


if __name__ == "__main__":
    import doctest

    doctest.testmod()
