import pickle
import argparse
import os
import logging

import numpy as np

from sqlalchemy import create_engine, inspect, or_
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

import douceville
from douceville.utils import logged
from douceville.models import Etablissement, Resultat, Nature
from douceville.scripts.conv_utils import *
from douceville.config import Config
from douceville.scripts.read_config import loadConfig
from douceville.scripts.conv_rdf import import_geoloc_db


@logged
def insert_or_update(session, etabl, res, check_nullable=True, logger=None):
    etabl_valid = not etabl is None
    log_valid = ""
    if check_nullable and not etabl is None:
        for c in inspect(Etablissement).mapper.column_attrs:
            if not getattr(Etablissement, c.key).nullable:
                log_valid += "* %s" % c.key
                if c.key in etabl.keys():
                    log_valid += " -> %s\n" % etabl[c.key]
                else:
                    log_valid += "\n"
                if not c.key in etabl.keys() or etabl[c.key] is None:
                    etabl_valid = False
            else:
                log_valid += "  %s" % c.key
                if c.key in etabl.keys():
                    log_valid += " -> %s\n" % etabl[c.key]
                else:
                    log_valid += "\n"

    if not etabl_valid:
        logger.error("etabl invalide")
        logger.error("%s" % str(etabl))
        logger.error(log_valid)
        # exit(0)
    else:
        if (
            "latitude" in etabl.keys()
            and "longitude" in etabl.keys()
            and not etabl["latitude"] is None
            and not etabl["longitude"] is None
        ):
            lat = etabl.pop("latitude")
            lon = etabl.pop("longitude")
            etabl["position"] = "POINT(%f %f)" % (lon, lat)
        etabl.pop("latitude", None)
        etabl.pop("longitude", None)

        nature = etabl.pop("nature", None)
        
        q = (
            session.query(Nature)
            .filter(Nature.etablissement_id == etabl["UAI"])
        )
        found_natures = [r.nature for r in q.all() if not r.nature is None] + [nature]
        q.delete()
        session.commit()

        q = session.query(Etablissement).filter(Etablissement.UAI == etabl["UAI"])
        if q.count() != 0:
            old_rec = q.first().asDict()
            ok = set(old_rec.keys())
            nk = set(etabl.keys())
            ck = ok.intersection(nk)
            for k in ck:
                if not k in ["nom", "latitude", "longitude"] and old_rec[k] != etabl[k]:
                    # print(old_rec)
                    # print(etabl)
                    # exit(1)
                    pass

            q.update(etabl)
            enr = q.first()
        elif q.count() == 0:
            enr = Etablissement(**etabl)
            session.add(enr)

        session.commit()

        for rn in found_natures:
            for n in coor_nature[rn]:
                if rn != n:
                    rec = Nature(nature=n, etablissement_id=etabl["UAI"])
                    session.add(rec)
        
    if not res is None:
        q = session.query(Etablissement).filter(
            Etablissement.UAI == res["etablissement_id"]
        )
        if q.count() == 0:
            logger.warning("Le resultat suivant ne correspond a aucun etablissement")
            logger.warning("%s" % res)
            return

        q = (
            session.query(Resultat)
            .filter(Resultat.annee == res["annee"])
            .filter(Resultat.diplome == res["diplome"])
            .filter(Resultat.etablissement_id == res["etablissement_id"])
        )
        if q.count() != 0:
            q.update(res)
        elif q.count() == 0:
            r_res = Resultat(**res)
            session.add(r_res)

        session.commit()


def import_sheet(
    session,
    xls,
    sheet_name,
    skp,
    corr_dict,
    year,
    inv_mention=False,
    geoloc2=None,
    row_limit=None,
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
            etab = {"nature": "college"}
        elif "bac" in corr_dict["nom_diplome"]:
            etab = {"nature": "lycee"}

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
        if uai[:2] == "97":
            continue

        if not geoloc2 is None:
            if uai in geoloc2.keys() and "latitude" in geoloc2[uai].keys():
                etab["latitude"] = geoloc2[uai]["latitude"]
                etab["longitude"] = geoloc2[uai]["longitude"]
            else:
                etab = None

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
            logger.warning("'present' attribute not found : %s" % res)
            continue

        if inv_mention and "mentions" in res.keys() and "admis" in res.keys():
            res["mentions"] = res["admis"] - res["mentions"]

        # =====================
        # Insertion
        # =====================
        insert_or_update(session, etab, res, check_nullable=True)

        if not row_limit is None and index >= row_limit:
            break

    session.commit()


@logged
def import_geoloc(session, file, row_limit=None, logger=None):
    logger.info("Importation données géoloc '%s'..." % file)

    df = pd.read_pickle(file)

    names = [
        ("UAI", to_maj),
        ("nom", to_cap),
        ("unused1", None),
        ("unused2", None),
        ("unused3", None),
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
        ("unused_etat", to_min),
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
        etab = {}

        if row["Etat établissement"] != "OUVERT":
            continue

        for i, (k, fct) in enumerate(names):
            if "unused" in k:
                continue

            val = fct(row.values[i])
            etab[k] = val

        if etab["UAI"][:2] == "97" or etab["UAI"][:2] == "98":
            continue

        insert_or_update(session, etab, None, check_nullable=True)

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

    if not cfg.geoloc2 is None:
        gl2 = import_geoloc_db(cfg.geoloc2)
    else:
        gl2 = None

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
                    geoloc2=gl2,
                    row_limit=cfg.options["row_limit"],
                )


if __name__ == "__main__":
    import_main()