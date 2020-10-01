from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

from CollegesLycees.init_db import Lycee


# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement

def idty(x):
    return x

def to_float(x):
    try:
        val = float(x)
    except Exception as e:
        val = None
    return val

def to_int(x):
    try:
        val = int(x)
    except Exception as e:
        val = None
    return val

def secteur_to_bool(x):
    return x == 'PR'

corr_acces = {}
corr_acces['UAI']             = 'UAI', idty
corr_acces['NOM_UAI']         = 'nom', idty
corr_acces['ACAD']            = 'academie', idty
corr_acces['DEP']             = 'departement', to_int
corr_acces['SECTEUR']         = 'secteur_prive', secteur_to_bool
corr_acces['COMMUNE_UAI']     = 'commune', idty
corr_acces['TAUX_2NDE_BAC']   = 'taux_2nde_bac', to_int
corr_acces['VA_2NDE_BAC']     = 'va_2nde_bac', to_int
corr_acces['TAUX_1ERE_BAC']   = 'taux_1ere_bac', to_int
corr_acces['VA_1ERE_BAC']     = 'va_1ere_bac', to_int
corr_acces['TAUX_TERM_BAC']   = 'taux_term_bac', to_int
corr_acces['VA_TERM_BAC']     = 'va_term_bac', to_int

corr_reussite = {}
corr_reussite['UAI']            = 'UAI', idty
corr_reussite['NOM_UAI']        = 'nom', idty
corr_reussite['ACAD']           = 'academie', idty
corr_reussite['DEP']            = 'departement', to_int
corr_reussite['SECTEUR']        = 'secteur_prive', secteur_to_bool
corr_reussite['COMMUNE_UAI']    = 'commune', idty
corr_reussite['Presents_GT']    = 'presents_gt'   , to_int
corr_reussite['Admis_GT']       = 'admis_gt'      , to_int
corr_reussite['VA_GT']          = 'va_admis_gt'   , to_int
corr_reussite['Presents_L']     = 'presents_l'    , to_int
corr_reussite['Admis_L']        = 'admis_l'       , to_int
corr_reussite['VA_L']           = 'va_admis_l'    , to_int
corr_reussite['Presents_ES']    = 'presents_es'   , to_int
corr_reussite['Admis_ES']       = 'admis_es'      , to_int
corr_reussite['VA_ES']          = 'va_admis_es'   , to_int
corr_reussite['Presents_S']     = 'presents_s'    , to_int
corr_reussite['Admis_S']        = 'admis_s'       , to_int
corr_reussite['VA_S']           = 'va_admis_s'    , to_int
corr_reussite['Presents_STMG']  = 'presents_stmg' , to_int
corr_reussite['Admis_STMG']     = 'admis_stmg'    , to_int
corr_reussite['VA_STMG']        = 'va_admis_stmg' , to_int
corr_reussite['Presents_STL']   = 'presents_stl'  , to_int
corr_reussite['Admis_STL']      = 'admis_stl'     , to_int
corr_reussite['VA_STL']         = 'va_admis_stl'  , to_int
corr_reussite['Presents_ST2S']  = 'presents_st2s' , to_int
corr_reussite['Admis_ST2S']     = 'admis_st2s'    , to_int
corr_reussite['VA_ST2S']        = 'va_admis_st2s' , to_int
corr_reussite['Presents_STI2D'] = 'presents_sti2d', to_int
corr_reussite['Admis_STI2D']    = 'admis_sti2d'   , to_int
corr_reussite['VA_STI2D']       = 'va_admis_sti2d', to_int
corr_reussite['Presents_STD2A'] = 'presents_std2a', to_int
corr_reussite['Admis_STD2A']    = 'admis_std2a'   , to_int
corr_reussite['VA_STD2A']       = 'va_admis_std2a', to_int
corr_reussite['Presents_TMD']   = 'presents_tmd'  , to_int
corr_reussite['Admis_TMD']      = 'admis_tmd'     , to_int
corr_reussite['VA_TMD']         = 'va_admis_tmd'  , to_int
corr_reussite['Presents_STHR']  = 'presents_sthr' , to_int
corr_reussite['Admis_STHR']     = 'admis_sthr'    , to_int
corr_reussite['VA_STHR']        = 'va_admis_sthr' , to_int

corr_mention = {}
corr_mention['UAI']            = 'UAI', idty
corr_mention['NOM_UAI']        = 'nom', idty
corr_mention['ACAD']           = 'academie', idty
corr_mention['DEP']            = 'departement', to_int
corr_mention['SECTEUR']        = 'secteur_prive', secteur_to_bool
corr_mention['COMMUNE_UAI']    = 'commune', idty
corr_mention['Mentions_GT'] = 'mentions_gt', to_int
corr_mention['VA_GT'] = 'va_mention_gt', to_int
corr_mention['Mentions_L'] = 'mentions_l', to_int
corr_mention['VA_L'] = 'va_mention_l', to_int
corr_mention['Mentions_ES'] = 'mentions_es', to_int
corr_mention['VA_ES'] = 'va_mention_es', to_int
corr_mention['Mentions_S'] = 'mentions_s', to_int
corr_mention['VA_S'] = 'va_mention_s', to_int
corr_mention['Mentions_STMG'] = 'mentions_stmg', to_int
corr_mention['VA_STMG'] = 'va_mention_stmg', to_int
corr_mention['Mentions_STL'] = 'mentions_stl', to_int
corr_mention['VA_STL'] = 'va_mention_stl', to_int
corr_mention['Mentions_ST2S'] = 'mentions_st2s', to_int
corr_mention['VA_ST2S'] = 'va_mention_st2s', to_int
corr_mention['Mentions_STI2D'] = 'mentions_sti2d', to_int
corr_mention['VA_STI2D'] = 'va_mention_sti2d', to_int
corr_mention['Mentions_STD2A'] = 'mentions_std2a', to_int
corr_mention['VA_STD2A'] = 'va_mention_std2a', to_int
corr_mention['Mentions_TMD'] = 'mentions_tmd', to_int
corr_mention['VA_TMD'] = 'va_mention_tmd', to_int
corr_mention['Mentions_STHR'] = 'mentions_sthr', to_int
corr_mention['VA_STHR'] = 'va_mention_sthr', to_int

engine = create_engine('sqlite:///lycee.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()

# df_c = pd.read_excel (open('menesr-depp-dnb-session-2018.xls', 'rb'), sheet_name='Sheet')
df = pd.read_excel('ival-2018-donn-es--32258.xls', sheet_name=None)

n = len(df['ACCES_GT'].index)
for index, row in tqdm.tqdm(df['ACCES_GT'].iterrows(), total=n):
    dat = {}
    for xl_k in corr_acces.keys():
        db_k,fct = corr_acces[xl_k]
        val = fct(row[xl_k])
        if not val is None:
            dat[db_k] = val

    enr = Lycee(**dat)
    s.add(enr)

s.commit()

n = len(df['REUSSITE_GT'].index)
for index, row in tqdm.tqdm(df['REUSSITE_GT'].iterrows(), total=n):
    dat = {}
    for xl_k in corr_reussite.keys():
        db_k,fct = corr_reussite[xl_k]
        val = fct(row[xl_k])
        if not val is None:
            dat[db_k] = val

    stmt = update(Lycee).where(Lycee.UAI==dat['UAI']).values(**dat)

s.commit()

n = len(df['MENTIONS_GT'].index)
for index, row in tqdm.tqdm(df['MENTIONS_GT'].iterrows(), total=n):
    dat = {}
    for xl_k in corr_mention.keys():
        db_k,fct = corr_mention[xl_k]
        val = fct(row[xl_k])
        if not val is None:
            dat[db_k] = val

    stmt = update(Lycee).where(Lycee.UAI==dat['UAI']).values(**dat)

s.commit()

