import pickle

from sqlalchemy import create_engine, func, or_, and_, not_
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from CollegesLycees.models import Etablissement
from CollegesLycees.conv_utils import corr_brevet
from CollegesLycees.conv_utils import corr_acces_gt, corr_reussite_gt, corr_mention_gt
from CollegesLycees.conv_utils import (
    corr_acces_pro,
    corr_reussite_pro,
    corr_mention_pro,
)
from CollegesLycees.conv_rdf import import_geoloc_db


def insert_or_update(session, dat, no_insert=False):
    if dat is None:
        return 0

    q = session.query(Etablissement).filter(Etablissement.UAI == dat["UAI"])
    if len(q.all()) != 0:
        q.update(dat)
        return 1
    elif len(q.all()) == 0 and not no_insert:
        enr = Etablissement(**dat)
        session.add(enr)
        return 0
    else:
        return 0


def import_sheet(
    session, xls, sheet_name, corr_dict, inv_mention=False, no_insert=False
):
    print("Importation %s..." % sheet_name)

    df = pd.read_excel(xls, sheet_name)

    n = len(df.index)
    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        dat = {}
        for xl_k in corr_dict.keys():
            db_k, fct = corr_dict[xl_k]

            if "admis_" in db_k:
                k_admis = db_k
            if "mentions_" in db_k:
                k_mentions = db_k

            val = fct(row[xl_k])

            # try:
            # val = fct(row[xl_k])
            # except Exception as e:
            # print(row)
            # print(row[xl_k])
            # raise e
            if not val is None:
                dat[db_k] = val

        if inv_mention and k_mentions in dat.keys() and k_admis in dat.keys():
            dat[k_mentions] = dat[k_admis] - dat[k_mentions]

        insert_or_update(s, dat, no_insert=no_insert)

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

        istat = insert_or_update(s, dat, no_insert=no_insert)
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

    result = s.query(Etablissement).filter(
        not_(
            or_(
                Etablissement.nom.ilike("%lycee%"),
                Etablissement.nom.ilike("%lycée%"),
                Etablissement.nom.ilike("%college%"),
                Etablissement.nom.ilike("%collège%"),
                Etablissement.denomination.ilike("%lycee%"),
                Etablissement.denomination.ilike("%lycée%"),
                Etablissement.denomination.ilike("%college%"),
                Etablissement.denomination.ilike("%collège%"),
            )
        )
    )
    result.delete(synchronize_session=False)

    s.commit()


# https://www.data.gouv.fr/fr/datasets/liste-des-etablissements-des-premier-et-second-degres-pour-les-secteurs-publics-et-prives-en-france
# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement

if __name__ == "__main__":
    # engine = create_engine('sqlite:///etablissements.db')
    engine = create_engine("postgresql+psycopg2://cl_user@localhost/etablissements")

    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    if True:
        xls = pd.ExcelFile("menesr-depp-dnb-session-2018.xls")
        import_sheet(s, xls, "Sheet", corr_brevet, inv_mention=True)

        xls = pd.ExcelFile("ival-2018-donn-es--32258.xls")
        import_sheet(s, xls, "ACCES_GT", corr_acces_gt)
        import_sheet(s, xls, "ACCES_PRO", corr_acces_pro)
        import_sheet(s, xls, "REUSSITE_GT", corr_reussite_gt)
        import_sheet(s, xls, "REUSSITE_PRO", corr_reussite_pro)
        import_sheet(s, xls, "MENTIONS_GT", corr_mention_gt)
        import_sheet(s, xls, "MENTIONS_PRO", corr_mention_pro)

        cleanup(s)

    import_geoloc(s, "data_dict2.raw", no_insert=True)
