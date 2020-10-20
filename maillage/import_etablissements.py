import pickle
import argparse
import os

import numpy as np

from sqlalchemy import create_engine, inspect, or_
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

import maillage
from maillage.models import Etablissement, Resultat
from maillage.conv_utils import *
from maillage.config import Config
from maillage.conv_rdf import import_geoloc_db
from maillage.read_config import loadConfig


def insert_or_update(session, etabl, res, no_insert=False):
    for c in inspect(Etablissement).mapper.column_attrs:
        if not getattr(Etablissement, c.key).nullable and not c.key in etabl.keys():
            # print('skip22', etabl)
            etabl = None
            return

    if not etabl is None and not no_insert:
        q = session.query(Etablissement).filter(Etablissement.UAI == etabl["UAI"])
        if q.count() != 0:
            q.update(etabl)
            enr = q.first()
        elif q.count() == 0:
            enr = Etablissement(**etabl)
            session.add(enr)

    if not res is None and not no_insert:
        res["etablissement_id"] = enr.UAI
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


def import_sheet(
    session, xls, sheet_name, skp, corr_dict, year, inv_mention=False, no_insert=False
):
    df = pd.read_excel(xls, sheet_name, skiprows=range(skp))

    n = len(df.index)
    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        # ==========================
        # Analyse de l'établissement
        # ==========================
        etab = {}
        for xl_k in corr_dict["etabl"].keys():
            db_k, fct = corr_dict["etabl"][xl_k]

            if xl_k in row.keys():
                val = fct(row[xl_k])
            else:
                val = None

            if not val is None:
                etab[db_k] = val

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
            # print('skip103', res)
            continue

        if inv_mention and "mentions" in res.keys() and "admis" in res.keys():
            res["mentions"] = res["admis"] - res["mentions"]

        # =====================
        # Insertion
        # =====================
        insert_or_update(session, etab, res, no_insert=no_insert)

    if not no_insert:
        session.commit()


def import_geoloc(session, file, no_insert=False):
    print("Importation données géoloc '%s'..." % file)

    irec = {}
    info = import_geoloc_db(file)

    result = session.query(Etablissement)
    for row in tqdm.tqdm(result.all()):
        uai = row.UAI
        if not uai in info.keys():
            continue

        dat = info[uai]
        if "denomination" in dat.keys():
            dat.pop("denomination")

        istat = insert_or_update(session, dat, None, no_insert=no_insert)
        if istat != 0:
            irec[uai] = 1

    print("%i enregistrements mis à jour" % sum(irec.values()))
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


def import_main():
    print("Maillage, version", maillage.__version__)

    parser = argparse.ArgumentParser(description="Maillage France")
    parser.add_argument("cfg", help="fichier config", type=str)

    args = parser.parse_args()

    cfg = loadConfig(args.cfg)

    print("Base de données :", Config.SQLALCHEMY_DATABASE_URI)
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    src_geoloc = None
    for src in cfg.sources:
        corr = corr_diplome(src.diplome, src.groupes)

        for annee in src.annees:
            xls = pd.ExcelFile(src.fichier % annee)
            for ong in src.onglets:
                rt = os.path.split(src.fichier % annee)[-1]
                print(
                    "Importation %s@%s, %s %i..."
                    % (ong, rt, corr["nom_diplome"], annee)
                )
                import_sheet(s, xls, ong, src.skiprows, corr, annee, src.inv_mention)

    if not cfg.geoloc is None:
        import_geoloc(s, cfg.geoloc)


if __name__ == "__main__":
    import_main()
