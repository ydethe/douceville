import pickle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from init_db import Etablissement
from init_db import corr_brevet
from init_db import corr_acces_gt, corr_reussite_gt, corr_mention_gt
from init_db import corr_acces_pro, corr_reussite_pro, corr_mention_pro

def insert_or_update(session, dat, no_insert=False):
    q = session.query(Etablissement).filter(Etablissement.UAI==dat['UAI'])
    if len(q.all()) != 0:
        istat = q.update(dat)
        return 1
    elif len(q.all()) == 0 and not no_insert:
        enr = Etablissement(**dat)                                          
        session.add(enr)
        return 0

def import_sheet(session, dfs, sheet_name, corr_dict, inv_mention=False):
    print("Importation %s..." % sheet_name)

    df = dfs[sheet_name]
    n = len(df.index)
    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        dat = {}
        for xl_k in corr_dict.keys():
            db_k,fct = corr_dict[xl_k]

            if 'admis_' in db_k:
                k_admis = db_k
            if 'mentions_' in db_k:
                k_mentions = db_k

            val = fct(row[xl_k])
            if not val is None:
                dat[db_k] = val

        if inv_mention and k_mentions in dat.keys() and k_admis in dat.keys():
            dat[k_mentions] = dat[k_admis] - dat[k_mentions]

        insert_or_update(s, dat)

    session.commit()

def import_geoloc(session, file):
    print("Importation données géoloc...")

    irec = 0
    info = pickle.loads(open('data_dict.raw','rb').read())
    for rec in tqdm.tqdm(info):
        if not '@id' in rec.keys():
            continue

        uai = rec['@id'].split('/')[-1].upper()
        dat = None
        if '/geometry/' in rec['@id']:
            lon = rec['http://data.ign.fr/ontologies/geometrie#coordX'][0]['@value']
            lat = rec['http://data.ign.fr/ontologies/geometrie#coordY'][0]['@value']

            dat = {}
            dat['UAI'] = uai
            dat['latitude'] = lat
            dat['longitude'] = lon

        elif 'http://purl.org/dc/terms/title' in rec.keys():
            nom = rec['http://purl.org/dc/terms/title'][0]['@value']
            dat = {}
            dat['UAI'] = uai
            dat['nom'] = nom
        
        if dat is None:
            continue

        istat = insert_or_update(s, dat, no_insert=True)
        if istat != 0:
            irec += 1

    print("%i enregistrements mis à jour" % irec)
    s.commit()

# https://www.data.gouv.fr/fr/datasets/liste-des-etablissements-des-premier-et-second-degres-pour-les-secteurs-publics-et-prives-en-france
# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement

if __name__ == '__main__':
    engine = create_engine('sqlite:///etablissements.db')
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    df = pd.read_excel('menesr-depp-dnb-session-2018.xls', sheet_name=None)
    import_sheet(s, df, 'Sheet', corr_brevet, inv_mention=True)

    df = pd.read_excel('ival-2018-donn-es--32258.xls', sheet_name=None)
    import_sheet(s, df, 'ACCES_GT', corr_acces_gt)
    import_sheet(s, df, 'ACCES_PRO', corr_acces_pro)
    import_sheet(s, df, 'REUSSITE_GT', corr_reussite_gt)
    import_sheet(s, df, 'REUSSITE_PRO', corr_reussite_pro)
    import_sheet(s, df, 'MENTIONS_GT', corr_mention_gt)
    import_sheet(s, df, 'MENTIONS_PRO', corr_mention_pro)

    import_geoloc(s, 'dataset-564055.ttl')


