import pickle

from sqlalchemy import create_engine, func, or_, and_, not_
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from CollegesLycees.models import Etablissement, Resultat
from CollegesLycees.conv_utils import *
from CollegesLycees.config import Config
from CollegesLycees.conv_rdf import import_geoloc_db


def insert_or_update(session, etabl, res, no_insert=False):
    if not etabl is None:
        q = session.query(Etablissement).filter(Etablissement.UAI == etabl["UAI"])
        if q.count() != 0:
            q.update(etabl)
            enr = q.first()
        elif q.count() == 0 and not no_insert:
            enr = Etablissement(**etabl)
            session.add(enr)
        r_etabl = (
            session.query(Etablissement)
            .filter(Etablissement.UAI == etabl["UAI"])
            .first()
        )

    if not res is None and not no_insert:
        res["etablissement_id"] = enr.UAI
        r_res = Resultat(**res)
        session.add(r_res)


def import_sheet(
    session, xls, sheet_name, corr_dict, year, inv_mention=False, no_insert=False
):
    print("Importation %s, %s..." % (sheet_name, corr_dict["nom_diplome"]))

    df = pd.read_excel(xls, sheet_name)

    n = len(df.index)
    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        etab = {}
        for xl_k in corr_dict["etabl"].keys():
            db_k, fct = corr_dict["etabl"][xl_k]

            val = fct(row[xl_k])

            if not val is None:
                etab[db_k] = val

        res = {
            "diplome": corr_dict["nom_diplome"],
            "annee": year,
            "admis": 0,
            "presents": 0,
            "mentions": 0,
        }
        for xl_k in corr_dict["res"].keys():
            db_k, fct = corr_dict["res"][xl_k]

            val = fct(row[xl_k])

            if val is None:
                continue

            if db_k in ["admis", "presents", "mentions"]:
                res[db_k] += val
            else:
                res[db_k] = val

        if res["admis"] == 0 or res["presents"] == 0:
            continue

        if inv_mention and res["mentions"] != 0 and res["admis"] != 0:
            res["mentions"] = res["admis"] - res["mentions"]

        if res["mentions"] == 0:
            res.pop("mentions")

        insert_or_update(s, etab, res, no_insert=no_insert)

    if not no_insert:
        session.commit()


def import_geoloc(session, file, no_insert):
    print("Importation données géoloc...")

    irec = {}
    info = import_geoloc_db()

    result = s.query(Etablissement)
    for row in tqdm.tqdm(result.all()):
        uai = row.UAI
        if not uai in info.keys():
            continue

        dat = info[uai]
        if "denomination" in dat.keys():
            dat.pop("denomination")

        istat = insert_or_update(s, dat, None, no_insert=no_insert)
        if istat != 0:
            irec[uai] = 1

    print("%i enregistrements mis à jour" % sum(irec.values()))
    s.commit()


def cleanup(s):
    print("Cleanup...")
    result = s.query(Etablissement).filter(
        or_(
            Etablissement.nom.ilike("%clinique%"),
            Etablissement.nom.ilike("%hospital%"),
            Etablissement.nom.ilike("%hopita%"),
            Etablissement.denomination.ilike("%clinique%"),
            Etablissement.denomination.ilike("%hospital%"),
            Etablissement.denomination.ilike("%hopita%"),
        )
    )
    result.delete(synchronize_session=False)

    s.commit()

    # result = s.query(Etablissement).filter(
    #     not_(
    #         or_(
    #             Etablissement.nom.ilike("%lycee%"),
    #             Etablissement.nom.ilike("%lycée%"),
    #             Etablissement.nom.ilike("%college%"),
    #             Etablissement.nom.ilike("%collège%"),
    #             Etablissement.denomination.ilike("%lycee%"),
    #             Etablissement.denomination.ilike("%lycée%"),
    #             Etablissement.denomination.ilike("%college%"),
    #             Etablissement.denomination.ilike("%collège%"),
    #         )
    #     )
    # )
    # result.delete(synchronize_session=False)

    # s.commit()


# Autres criteres :
# - RSA
# - lieux de culte
# - meteo
# - voir concurrents : jequitteparis.fr
# - immobilier

# https://www.data.gouv.fr/fr/datasets/liste-des-etablissements-des-premier-et-second-degres-pour-les-secteurs-publics-et-prives-en-france
# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement

if __name__ == "__main__":
    print("Base de données :", Config.SQLALCHEMY_DATABASE_URI)
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    xls = pd.ExcelFile("CollegesLycees/raw/menesr-depp-dnb-session-2018.xls")
    import_sheet(s, xls, "Sheet", corr_brevet, 2018, inv_mention=True, no_insert=False)

    xls = pd.ExcelFile("CollegesLycees/raw/ival-2018-donn-es--32258.xls")
    # import_sheet(s, xls, "ACCES_GT", corr_acces_gt)
    # import_sheet(s, xls, "ACCES_PRO", corr_acces_pro)
    import_sheet(s, xls, "REUSSITE_GT", corr_reussite_bac('general', ('S','L','ES')), 2018)

    for b in liste_bac_techno:
        import_sheet(s, xls, "REUSSITE_GT", corr_reussite_bac(b), 2018)

    for b in liste_bac_pro:
        import_sheet(s, xls, "REUSSITE_PRO", corr_reussite_bac(b), 2018)

    # import_sheet(s, xls, "MENTIONS_GT", corr_mention_gt)
    # import_sheet(s, xls, "MENTIONS_PRO", corr_mention_pro)

    # cleanup(s)

    # import_geoloc(s, "CollegesLycees/raw/data_dict2.raw", no_insert=False)
