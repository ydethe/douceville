from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from init_db import Lycee, corr_acces, corr_reussite, corr_mention


# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement


engine = create_engine('sqlite:///lycee.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()

# df_c = pd.read_excel (open('menesr-depp-dnb-session-2018.xls', 'rb'), sheet_name='Sheet')
df = pd.read_excel('ival-2018-donn-es--32258.xls', sheet_name=None)

def import_sheet(name, corr_dict):
    print("Importation %s..." % name)
    n = len(df[name].index)
    for index, row in tqdm.tqdm(df[name].iterrows(), total=n):
        dat = {}
        for xl_k in corr_dict.keys():
            db_k,fct = corr_dict[xl_k]
            val = fct(row[xl_k])
            if not val is None:
                dat[db_k] = val

        istat = s.query(Lycee).\
           filter(Lycee.UAI==dat['UAI']).\
           update(dat)
        if istat == 0:
            enr = Lycee(**dat)
            s.add(enr)

    s.commit()

import_sheet('ACCES_GT', corr_acces)
import_sheet('REUSSITE_GT', corr_reussite)
import_sheet('MENTIONS_GT', corr_mention)


