from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from init_db import Lycee
from init_db import corr_acces_gt, corr_reussite_gt, corr_mention_gt
from init_db import corr_acces_pro, corr_reussite_pro, corr_mention_pro


def import_sheet(session, file, sheet_name, corr_dict):
    df = pd.read_excel('ival-2018-donn-es--32258.xls', sheet_name=sheet_name)
    print("Importation %s..." % sheet_name)
    n = len(df.index)
    for index, row in tqdm.tqdm(df.iterrows(), total=n):
        dat = {}
        for xl_k in corr_dict.keys():
            db_k,fct = corr_dict[xl_k]
            val = fct(row[xl_k])
            if not val is None:
                dat[db_k] = val

        istat = session.query(Lycee).\
           filter(Lycee.UAI==dat['UAI']).\
           update(dat)
        if istat == 0:
            enr = Lycee(**dat)
            session.add(enr)

    session.commit()


# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement

if __name__ == '__main__':
    engine = create_engine('sqlite:///lycee.db')
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    import_sheet(s, 'ival-2018-donn-es--32258.xls', 'ACCES_GT', corr_acces_gt)
    import_sheet(s, 'ival-2018-donn-es--32258.xls', 'ACCES_PRO', corr_acces_pro)
    import_sheet(s, 'ival-2018-donn-es--32258.xls', 'REUSSITE_GT', corr_reussite_gt)
    import_sheet(s, 'ival-2018-donn-es--32258.xls', 'REUSSITE_PRO', corr_reussite_pro)
    import_sheet(s, 'ival-2018-donn-es--32258.xls', 'MENTIONS_GT', corr_mention_gt)
    import_sheet(s, 'ival-2018-donn-es--32258.xls', 'MENTIONS_PRO', corr_mention_pro)


