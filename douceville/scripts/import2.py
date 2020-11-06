import pickle
import argparse
import os
import logging
from collections import defaultdict

import numpy as np

from sqlalchemy import create_engine, inspect, or_
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

import douceville
from douceville.utils import logged
from douceville.models import *
from douceville.scripts.conv_utils import *
from douceville.config import Config
from douceville.scripts.read_config import loadConfig
from douceville.scripts.conv_rdf import import_geoloc_db
from douceville.blueprints.isochrone.geographique import findCoordFromAddress

# def findCoordFromAddress(*args, **kwargs):
#     return 0,0


def findEtabPosition(etab):
    lat = etab.pop('latitude', None)
    lon = etab.pop('longitude', None)

    adresse = {}
    if not etab["nom"] is None:
        adresse["nom"] = etab["nom"]
    if not lat is None:
        adresse["lat"] = lat
    if not lon is None:
        adresse["lon"] = lon
    if not etab["adresse"] is None:
        adresse["adresse"] = etab["adresse"]
    if not etab["code_postal"] is None:
        adresse["cp"] = etab["code_postal"]
    if not etab["commune"] is None:
        adresse["commune"] = etab["commune"]

    etab_maj = findCoordFromAddress(**adresse)
    if etab_maj is None:
        return None

    etab["import_status"] = ImportStatus.COORD_FROM_ADDRESS
    etab.update(etab_maj)

    return etab


@logged
def insert_or_update_resulat(session, etab_res, nature, resultat, logger=None):
    q = session.query(Etablissement).filter(
        Etablissement.UAI == resultat["etablissement_id"]
    )
    if q.count() == 0:
        etab = findEtabPosition(etab_res)
        if etab is None:
            logger.error("Impossible de geolocaliser l'etablissement '%s'" % str(etab_res))
            return

        logger.warning(
            "Pas d'etab pour le resultat : %s => Insertion de %s"
            % (str(resultat), str(etab))
        )

        session.add(Etablissement(**etab))
        insert_or_update_nature(session, nature, logger=logger)

    q = (
        session.query(Resultat)
        .filter(Resultat.etablissement_id == resultat["etablissement_id"])
        .filter(Resultat.annee == resultat["annee"])
        .filter(Resultat.diplome == resultat["diplome"])
    )
    if q.count() == 0:
        session.add(Resultat(**resultat))
    # else:
    # logger.warning("Duplicat resulat : %s" % str(resultat))


@logged
def insert_or_update_nature(session, nature, logger=None):
    q = (
        session.query(Nature)
        .filter(Nature.etablissement_id == nature["etablissement_id"])
        .filter(Nature.nature == nature["nature"])
    )
    if q.count() == 0:
        session.add(Nature(**nature))
    # else:
    # logger.warning("Duplicat nature : %s" % str(nature))


@logged
def insert_or_update_etab(session, etab, logger=None):
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
        if not k in etab.keys() or etab.keys() is None:
            if not nom_aff:
                print(etab["nom"])
                nom_aff = True
            print("   %s" % k)

    q = session.query(Etablissement).filter(Etablissement.UAI == etab["UAI"])
    if q.count() == 0:
        session.add(Etablissement(**etab))
    else:
        q.update(etab)


@logged
def import_geoloc(session, file, row_limit=None, logger=None):
    logger.info("Importation données géoloc '%s'..." % file)

    df = pd.read_pickle(file)

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

    for index, row in tqdm.tqdm(df.iterrows(), total=n):
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
                val = secteur_to_bool(etab["unused_secteur"])
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
        for n in list_natures:
            if n == "":
                logger.debug(index)
            nature = {"etablissement_id": etab["UAI"], "nature": n}
            insert_or_update_nature(session, nature)

        if not row_limit is None and index >= row_limit:
            break

    session.commit()


@logged
def import_sheet(
    session,
    xls,
    sheet_name,
    skp,
    corr_dict,
    year,
    inv_mention,
    row_limit,
    logger=None,
):
    df = pd.read_excel(xls, sheet_name, skiprows=range(skp))

    if row_limit is None:
        n = len(df.index)
    else:
        n = row_limit

    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        # ==========================
        # Analyse de l'établissement
        # ==========================
        if corr_dict["nom_diplome"] == "brevet":
            nature = {"nature": "college"}
        elif "bac" in corr_dict["nom_diplome"]:
            nature = {"nature": "lycee"}

        etab = defaultdict(lambda: None)
        etab["import_status"] = ImportStatus.OK
        for xl_k in corr_dict["etabl"].keys():
            for db_k, fct in corr_dict["etabl"][xl_k]:

                if xl_k in row.keys():
                    val = fct(row[xl_k])
                else:
                    val = None

                if not val is None:
                    etab[db_k] = val

        if not "UAI" in etab.keys():
            logger.error(
                "'UAI' attribute not found @row %i : %s, %s" % (index, row, etab)
            )

        uai = etab["UAI"]
        if uai[0] != "0":
            continue

        etab["import_status"] = ImportStatus.ETAB_FROM_RESULT

        nature["etablissement_id"] = uai

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
            "etablissement_id": uai,
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

        res.pop("taux")

        for k in ["admis", "presents", "mentions"]:
            if res[k] == []:
                res.pop(k)
            else:
                res[k] = sum(res[k])

        # =====================
        # Filtrage
        # =====================
        if not "presents" in res.keys():
            logger.warning("'presents' attribute not found : %s => rec ignored" % res)
            continue

        if inv_mention and "mentions" in res.keys() and "admis" in res.keys():
            res["mentions"] = res["admis"] - res["mentions"]

        # =====================
        # Insertion
        # =====================
        insert_or_update_resulat(session, etab, nature, res)

        if not row_limit is None and index >= row_limit:
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


@logged
def import_main(logger=None):
    logger.info("Maillage, version %s" % douceville.__version__)

    parser = argparse.ArgumentParser(description="Maillage France")
    parser.add_argument("cfg", help="fichier config", type=str)

    args = parser.parse_args()

    cfg = loadConfig(args.cfg)

    logger.info("Base de données : %s" % Config.SQLALCHEMY_DATABASE_URI)
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    if not cfg.geoloc is None:
        import_geoloc(s, cfg.geoloc, row_limit=cfg.options["row_limit"])

    for src in cfg.sources:
        corr = corr_diplome(src.diplome, src.groupes)

        for annee in src.annees:
            xls = pd.ExcelFile(src.fichier % annee)
            for ong in src.onglets:
                rt = os.path.split(src.fichier % annee)[-1]
                logger.info(
                    "Importation %s@%s, %s %i..."
                    % (ong, rt, corr["nom_diplome"], annee)
                )
                import_sheet(
                    s,
                    xls,
                    ong,
                    src.skiprows,
                    corr,
                    annee,
                    src.inv_mention,
                    row_limit=cfg.options["row_limit"],
                )


if __name__ == "__main__":
    import_main()
