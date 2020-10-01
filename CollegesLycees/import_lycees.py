from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from init_db import Lycee
from init_db import corr_acces_gt, corr_reussite_gt, corr_mention_gt
from init_db import corr_acces_pro, corr_reussite_pro, corr_mention_pro


def import_sheet(session, dfs, sheet_name, corr_dict):
    print("Importation %s..." % sheet_name)
    df = dfs[sheet_name]
    n = len(df.index)
    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        dat = {}
        for xl_k in corr_dict.keys():
            db_k,fct = corr_dict[xl_k]
            try:
                val = fct(row[xl_k])
            except Exception as e:
                print(row)
                raise e
                exit(1)
            if not val is None:
                dat[db_k] = val

        istat = session.query(Lycee).\
           filter(Lycee.UAI==dat['UAI']).\
           update(dat)
        if istat == 0:
            enr = Lycee(**dat)
            session.add(enr)

    session.commit()

def import_geoloc(session, file):
    print("Importation données géoloc...")

    from collections import defaultdict

    f = open(file, 'r')
    lines = f.readlines()
    f.close()

    id_det = "<http://data.eurecom.fr/id/school/"

    geom_point = False
    info = defaultdict(dict)

    irec = 0
    for line in tqdm.tqdm(lines):
        if '/geometrie#Point' in line:
            geom_point = True
        elif '/geometry/' in line:
            geom_point = False

        if line.startswith(id_det):
            tmp = line[len(id_det):].split('>')[0]
            if '/' in tmp:
                data_id = tmp.split('/')[-1]
            else:
                data_id = tmp

        if "ecole#denominationPrincipale" in line:
            info[data_id]['denomination'] = line.split('"')[1].lower()

        if "schema#code" in line:
            info[data_id]['UAI'] = line.split('"')[1]

        if "title" in line:
            info[data_id]['nom'] = line.split('"')[1]

        if "geometrie#coordX" in line and not geom_point:
            info[data_id]['longitude'] = float(line.split('"')[1])

        if "geometrie#coordY" in line and not geom_point:
            info[data_id]['latitude'] = float(line.split('"')[1])

        if line.endswith(" .\n") and not line.startswith("@prefix"):
            if 'latitude' in info[data_id].keys() and 'longitude' in info[data_id].keys() and 'denomination' in info[data_id].keys():
                if not 'lycee' in info[data_id]['denomination']:
                    continue

                dat = info[data_id]
                istat = session.query(Lycee).\
                   filter(Lycee.UAI==dat['UAI']).\
                   update(dat)
                if istat != 0:
                    irec += 1

    print("%i enregistrements mis à jour" % irec)
    s.commit()

# https://www.data.gouv.fr/fr/datasets/liste-des-etablissements-des-premier-et-second-degres-pour-les-secteurs-publics-et-prives-en-france
# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement

if __name__ == '__main__':
    engine = create_engine('sqlite:///lycee.db')
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    df = pd.read_excel('ival-2018-donn-es--32258.xls', sheet_name=None)

    import_sheet(s, df, 'ACCES_GT', corr_acces_gt)
    import_sheet(s, df, 'ACCES_PRO', corr_acces_pro)
    import_sheet(s, df, 'REUSSITE_GT', corr_reussite_gt)
    import_sheet(s, df, 'REUSSITE_PRO', corr_reussite_pro)
    import_sheet(s, df, 'MENTIONS_GT', corr_mention_gt)
    import_sheet(s, df, 'MENTIONS_PRO', corr_mention_pro)

    import_geoloc(s, 'dataset-564055.ttl')


