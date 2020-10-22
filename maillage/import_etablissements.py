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
from maillage.read_config import loadConfig
from maillage.conv_rdf import import_geoloc_db


def insert_or_update(session, etabl, res, check_nullable=True, no_insert=False):
    if check_nullable and not etabl is None:
        for c in inspect(Etablissement).mapper.column_attrs:
            if not getattr(Etablissement, c.key).nullable:
                if not c.key in etabl.keys() or etabl[c.key] is None:
                    etabl = None
                    break

    if not etabl is None and not no_insert:
        q = session.query(Etablissement).filter(Etablissement.UAI == etabl["UAI"])
        if q.count() != 0:
            old_rec = q.first().asDict()
            ok = set(old_rec.keys())
            nk = set(etabl.keys())
            ck = ok.intersection(nk)
            for k in ck:
                if not k in ['nom','latitude','longitude'] and old_rec[k] != etabl[k]:
                    # print(old_rec)
                    # print(etabl)
                    # exit(1)
                    pass

            q.update(etabl)
            enr = q.first()
        elif q.count() == 0:
            enr = Etablissement(**etabl)
            session.add(enr)

    if not res is None and not no_insert:
        q = session.query(Etablissement).filter(
            Etablissement.UAI == res["etablissement_id"]
        )
        if q.count() == 0:
            print("[WARNING]Le resultat suivant ne correspond a aucun etablissement")
            print("[WARNING]", res)
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


def import_sheet(
    session,
    xls,
    sheet_name,
    skp,
    corr_dict,
    year,
    inv_mention=False,
    no_insert=False,
    geoloc2=None,
    row_limit=None,
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
        if corr_dict["nom_diplome"] == 'brevet':
            etab = {'nature':'college'}
        elif 'bac' in corr_dict["nom_diplome"]:
            etab = {'nature':'lycee'}
        
        for xl_k in corr_dict["etabl"].keys():
            db_k, fct = corr_dict["etabl"][xl_k]

            if xl_k in row.keys():
                val = fct(row[xl_k])
            else:
                val = None

            if not val is None:
                etab[db_k] = val

        uai = etab['UAI']
        if not geoloc2 is None:
            if uai in geoloc2.keys() and 'latitude' in geoloc2[uai].keys():
                etab['latitude'] = geoloc2[uai]['latitude']
                etab['longitude'] = geoloc2[uai]['longitude']
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
            # print('skip103', res)
            continue

        if inv_mention and "mentions" in res.keys() and "admis" in res.keys():
            res["mentions"] = res["admis"] - res["mentions"]

        # =====================
        # Insertion
        # =====================
        insert_or_update(session, etab, res, check_nullable=True, no_insert=no_insert)

        if not row_limit is None and index >= row_limit:
            break

    if not no_insert:
        session.commit()


def import_geoloc(session, file, no_insert=False, row_limit=None):
    print("Importation données géoloc '%s'..." % file)

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

        insert_or_update(session, etab, None, check_nullable=True, no_insert=no_insert)

        if not row_limit is None and index >= row_limit:
            break

    if not no_insert:
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

    if not cfg.geoloc is None:
        import_geoloc(s, cfg.geoloc, row_limit=cfg.options["row_limit"])

    if not cfg.geoloc2 is None:
        gl2 = import_geoloc_db(cfg.geoloc2)

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
