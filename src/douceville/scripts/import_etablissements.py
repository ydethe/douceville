from pathlib import Path
import pickle
import os
import logging
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import numpy as np
import typer
import pandas as pd
import rich.progress as rp

from ..models import Resultat, Etablissement, ImportStatus
from .conv_utils import (
    to_maj,
    to_cap,
    to_lieu_dit,
    to_float,
    to_nature,
    cp_to_dep,
    secteur_to_bool,
    idty,
    corr_diplome,
)
from ..config import config
from .read_config import loadConfig
from .crawler import search_data_gouv
from ..blueprints.isochrone.geographique import findCoordFromAddress


def findEtabPosition(etab: dict) -> dict:
    lat = etab.pop("latitude", None)
    lon = etab.pop("longitude", None)

    adresse = {}
    if etab["nom"] is not None:
        adresse["nom"] = etab["nom"].title()
    if lat is not None:
        adresse["lat"] = lat
    if lon is not None:
        adresse["lon"] = lon
    if etab.get("adresse", None) is not None:
        adresse["adresse"] = etab["adresse"].title()
        while "  " in adresse["adresse"]:
            adresse["adresse"] = adresse["adresse"].replace("  ", " ")
    if etab.get("code_postal", None) is not None:
        adresse["cp"] = etab["code_postal"]
    if etab.get("departement", None) is not None:
        adresse["departement"] = etab["departement"]
    if etab.get("commune", None) is not None:
        adresse["commune"] = etab["commune"].title()

    etab_maj = findCoordFromAddress(**adresse)
    if etab_maj is None:
        return None

    etab["import_status"] = ImportStatus.COORD_FROM_ADDRESS
    etab.update(etab_maj)

    return etab


def insert_or_update_resulat(session, etab_res, resultat):
    logger = logging.getLogger("douceville_logger")

    q = session.query(Etablissement).filter(Etablissement.UAI == resultat["etablissement_uai"])
    if q.count() == 0:
        etab = findEtabPosition(etab_res)
        if etab is None:
            logger.error("Impossible de geolocaliser l'etablissement '%s'" % str(etab_res))
            return

        logger.warning(
            "Pas d'etab pour le resultat : %s => Insertion de %s" % (str(resultat), str(etab))
        )

        session.add(Etablissement(**etab))

    q = (
        session.query(Resultat)
        .filter(Resultat.etablissement_uai == resultat["etablissement_uai"])
        .filter(Resultat.annee == resultat["annee"])
        .filter(Resultat.diplome == resultat["diplome"])
    )
    if q.count() == 0:
        session.add(Resultat(**resultat))
    # else:
    # logger.warning("Duplicat resulat : %s" % str(resultat))


def insert_or_update_etab(session, etab):
    l_keys = [
        "UAI",
        "nom",
        "adresse",
        "lieu_dit",
        "code_postal",
        "commune",
        "position",
        "departement",
        "academie",
        "secteur",
        "ouverture",
    ]

    nom_aff = False
    for k in l_keys:
        if k not in etab.keys() or etab.keys() is None:
            if not nom_aff:
                print(etab["nom"])
                nom_aff = True
            print("   %s" % k)

    q = session.query(Etablissement).filter(Etablissement.UAI == etab["UAI"])
    if q.count() == 0:
        session.add(Etablissement(**etab))
    else:
        q.update(etab)


def import_geoloc(session, file, row_limit=None):
    logger = logging.getLogger("douceville_logger")

    logger.info("Importation données géoloc '%s'..." % file)

    df = pd.read_excel(file)

    names = [
        ("UAI", to_maj),
        ("nom", to_cap),
        ("unused1", None),
        ("unused2", None),
        ("unused_secteur", None),
        ("adresse", to_cap),
        ("lieu_dit", to_lieu_dit),
        ("unused6", None),
        ("code_postal", to_maj),
        ("unused8", None),
        ("commune", to_cap),
        ("unused10", None),
        ("unused11", None),
        ("unused12", None),
        ("latitude", to_float),
        ("longitude", to_float),
        ("unused15", None),
        ("unused16", None),
        ("unused17", None),
        ("nature", to_nature),
        ("unused19", None),
        ("unused", None),
        ("departement", cp_to_dep),
        ("unused22", None),
        ("unused23", None),
        ("unused24", None),
        ("unused25", None),
        ("unused26", None),
        ("academie", to_cap),
        ("unused28", None),
        ("unused29", None),
        ("secteur", secteur_to_bool),
        ("unused31", None),
        ("unused32", None),
        ("ouverture", idty),
    ]

    if row_limit is None:
        n = len(df.index)
    else:
        n = row_limit

    for index, row in rp.track(df.iterrows(), total=n):
        etab = defaultdict(lambda: None)
        etab["import_status"] = ImportStatus.OK

        if row["Etat établissement"] != "OUVERT":
            continue

        for i, (k, fct) in enumerate(names):
            if "unused" in k:
                continue

            val = fct(row.values[i])
            if k == "nature" and val is None:
                val = to_nature(etab["nom"])
            if k == "secteur" and val is None:
                raw_val = etab.pop("unused_secteur", "sans objet")
                val = secteur_to_bool(raw_val)
            etab[k] = val

        if etab["UAI"][0] != "0":
            continue

        etab = findEtabPosition(etab)
        if etab is None:
            continue

        list_natures = etab.pop("nature", None)

        if list_natures is None:
            continue

        insert_or_update_etab(session, etab)

        if row_limit is not None and index >= row_limit:
            break

    session.commit()


def import_geoloc2(session, df, file):
    info = pickle.loads(open(file, "rb").read())

    db = {}
    for krec, rec in rp.track(enumerate(info)):
        if "@id" not in rec.keys():
            continue

        uai = rec["@id"].split("/")[-1].upper()

        if uai in db.keys():
            dat = db[uai]
        else:
            dat = {"UAI": uai}

        if "/geometry/" in rec["@id"]:
            lon = rec["http://data.ign.fr/ontologies/geometrie#coordX"][0]["@value"]
            lat = rec["http://data.ign.fr/ontologies/geometrie#coordY"][0]["@value"]

            dat["latitude"] = lat
            dat["longitude"] = lon

        if "http://purl.org/dc/terms/title" in rec.keys():
            nom = rec["http://purl.org/dc/terms/title"][0]["@value"]
            dat["nom"] = nom

        if "http://data.eurecom.fr/ontologies/ecole#denominationPrincipale" in rec.keys():
            denom = rec["http://data.eurecom.fr/ontologies/ecole#denominationPrincipale"][0][
                "@value"
            ]
            dat["secteur"] = secteur_to_bool(denom)
            if dat["secteur"] not in ["public", "prive"]:
                gouv_dat = search_data_gouv(uai)
                if gouv_dat is None:
                    dat = None
                else:
                    secteur = gouv_dat["secteur_public_prive_libe"].lower()
                    secteur = secteur.replace("é", "e")
                    dat["secteur"] = secteur
                    assert dat["secteur"] in ["public", "prive"]
            else:
                assert dat["secteur"] in ["public", "prive"]

        if dat is not None:
            db[uai] = dat

    db["0312843X"] = {"UAI": "0312843X", "longitude": 1.398089, "latitude": 43.464582}
    db["0312868Z"] = {"UAI": "0312868Z", "longitude": 1.249387, "latitude": 43.348657}
    db["0312842W"] = {"UAI": "0312842W", "longitude": 1.373549, "latitude": 43.750734}
    db["0311842J"] = {"UAI": "0311842J", "longitude": 1.579625, "latitude": 43.728851}
    db["0312354R"] = {"UAI": "0312354R", "longitude": 1.320462, "latitude": 43.780609}
    db["0311270M"] = {"UAI": "0311270M", "longitude": 1.522781, "latitude": 43.537348}
    db["0311843K"] = {"UAI": "0311843K", "longitude": 1.120444, "latitude": 43.413620}
    db["0311268K"] = {"UAI": "0311268K", "longitude": 0.730726, "latitude": 43.117691}
    db["0312058U"] = {"UAI": "0312058U", "longitude": 0.952023, "latitude": 43.081886}
    db["0310087B"] = {"UAI": "0310087B", "longitude": 1.474957, "latitude": 43.549452}
    db["0311879Z"] = {"UAI": "0311879Z", "longitude": 1.551114, "latitude": 43.473410}

    for etab in rp.track(db.values()):
        etab = findEtabPosition(etab)
        if etab is None:
            continue

        insert_or_update_etab(session, etab)


def import_sheet(
    session,
    xls,
    sheet_name,
    skp,
    corr_dict,
    backup_group,
    year,
    inv_mention,
    row_limit,
):
    logger = logging.getLogger("douceville_logger")

    df = pd.read_excel(xls, sheet_name, skiprows=range(skp))

    if row_limit is None:
        n = len(df.index)
    else:
        n = row_limit

    for index, row in rp.track(df.iterrows(), total=n):
        # ==========================
        # Analyse de l'établissement
        # ==========================
        etab = defaultdict(lambda: None)
        etab["import_status"] = ImportStatus.OK
        for xl_k in corr_dict["etabl"].keys():
            for db_k, fct in corr_dict["etabl"][xl_k]:

                if xl_k in row.keys():
                    val = fct(row[xl_k])
                else:
                    val = None

                if val is not None:
                    etab[db_k] = val

        if "UAI" not in etab.keys():
            logger.error("'UAI' attribute not found @row %i : %s, %s" % (index, row, etab))

        uai = etab["UAI"]
        if uai[0] != "0":
            continue

        etab["import_status"] = ImportStatus.ETAB_FROM_RESULT

        # =====================
        # Analyse des résultats
        # =====================
        res = {
            "diplome": corr_dict["nom_diplome"],
            "annee": year,
            "admis": [],
            "presents": [],
            "mentions": [],
            "taux": [],
            "etablissement_uai": uai,
        }
        for xl_k in corr_dict["res"].keys():
            db_k, fct = corr_dict["res"][xl_k]

            if xl_k in row.keys():
                val = fct(row[xl_k])
            else:
                val = None

            if val is None:
                continue

            if db_k in ["admis", "presents", "mentions", "taux"]:
                res[db_k].append(val)
            else:
                res[db_k] = val

        if res["admis"] == [] and res["mentions"] == [] and res["taux"] != []:
            adm = 0
            for p, t in zip(res["presents"], res["taux"]):
                adm += p * t
            res["admis"] = [int(np.round(adm / 100, 0))]

        for k in ["admis", "presents", "mentions"]:
            k_bck = k + "_bck"
            if res[k] == []:
                if k_bck in res.keys():
                    res[k] = res[k_bck]
                else:
                    res.pop(k)
            else:
                res[k] = sum(res[k])

            res.pop(k_bck, None)

        res.pop("taux")
        res.pop("taux_bck", None)

        # =====================
        # Filtrage
        # =====================
        if "presents" not in res.keys():
            logger.warning("'presents' attribute not found : %s => rec ignored" % res)
            continue

        if inv_mention and "mentions" in res.keys() and "admis" in res.keys():
            res["mentions"] = res["admis"] - res["mentions"]

        # =====================
        # Insertion
        # =====================
        insert_or_update_resulat(session, etab, res)

        if row_limit is not None and index >= row_limit:
            break

    session.commit()


# Autres criteres :
# - RSA
# - lieux de culte
# - meteo
# - voir concurrents : jequitteparis.fr
# - immobilier
# - maternité
# - age moyen

# https://www.data.gouv.fr/fr/datasets/liste-des-etablissements-des-premier-et-second-degres-pour-les-secteurs-publics-et-prives-en-france
# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement
# https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee

tapp = typer.Typer()


@tapp.command()
def import_etablissements(cfg: Path = typer.Argument(..., help="Fichier de config (.yml)")):
    """Maillage France"""
    logger = logging.getLogger("douceville_logger")

    cfg = loadConfig(cfg)

    logger.info("Base de données : %s" % config.SQLALCHEMY_DATABASE_URI)
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    if cfg.geoloc is not None:
        import_geoloc(s, cfg.geoloc, row_limit=cfg.options["row_limit"])

    if cfg.geoloc2 is not None:
        import_geoloc2(s, cfg.geoloc2)

    for src in cfg.sources:
        corr = corr_diplome(src)

        for annee in src.annees:
            xls = src.fichier % annee
            for ong in src.onglets:
                rt = os.path.split(src.fichier % annee)[-1]
                logger.info("Importation %s@%s, %s %i..." % (ong, rt, corr["nom_diplome"], annee))
                import_sheet(
                    s,
                    xls,
                    ong,
                    src.skiprows,
                    corr,
                    src.backup_group,
                    annee,
                    src.inv_mention,
                    row_limit=cfg.options["row_limit"],
                )


def import_main():
    tapp()