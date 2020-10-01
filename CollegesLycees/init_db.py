from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Lycee(Base):
    __tablename__ = 'lycee'
    UAI              = Column(String, primary_key=True)
    nom              = Column(String)
    academie         = Column(String)
    departement      = Column(Integer)
    secteur_prive    = Column(Boolean)
    commune          = Column(String)
    taux_2nde_bac    = Column(Integer)
    va_2nde_bac      = Column(Integer)
    taux_1ere_bac    = Column(Integer)
    va_1ere_bac      = Column(Integer)
    taux_term_bac    = Column(Integer)
    va_term_bac      = Column(Integer)
    presents_gt      = Column(Integer)
    admis_gt         = Column(Integer)
    va_admis_gt      = Column(Integer)
    presents_l       = Column(Integer)
    admis_l          = Column(Integer)
    va_admis_l       = Column(Integer)
    presents_es      = Column(Integer)
    admis_es         = Column(Integer)
    va_admis_es      = Column(Integer)
    presents_s       = Column(Integer)
    admis_s          = Column(Integer)
    va_admis_s       = Column(Integer)
    presents_stmg    = Column(Integer)
    admis_stmg       = Column(Integer)
    va_admis_stmg    = Column(Integer)
    presents_stl     = Column(Integer)
    admis_stl        = Column(Integer)
    va_admis_stl     = Column(Integer)
    presents_st2s    = Column(Integer)
    admis_st2s       = Column(Integer)
    va_admis_st2s    = Column(Integer)
    presents_sti2d   = Column(Integer)
    admis_sti2d      = Column(Integer)
    va_admis_sti2d   = Column(Integer)
    presents_std2a   = Column(Integer)
    admis_std2a      = Column(Integer)
    va_admis_std2a   = Column(Integer)
    presents_tmd     = Column(Integer)
    admis_tmd        = Column(Integer)
    va_admis_tmd     = Column(Integer)
    presents_sthr    = Column(Integer)
    admis_sthr       = Column(Integer)
    va_admis_sthr    = Column(Integer)
    mentions_gt      = Column(Integer)
    va_mention_gt    = Column(Integer)
    mentions_l       = Column(Integer)
    va_mention_l     = Column(Integer)
    mentions_es      = Column(Integer)
    va_mention_es    = Column(Integer)
    mentions_s       = Column(Integer)
    va_mention_s     = Column(Integer)
    mentions_stmg    = Column(Integer)
    va_mention_stmg  = Column(Integer)
    mentions_stl     = Column(Integer)
    va_mention_stl   = Column(Integer)
    mentions_st2s    = Column(Integer)
    va_mention_st2s  = Column(Integer)
    mentions_sti2d   = Column(Integer)
    va_mention_sti2d = Column(Integer)
    mentions_std2a   = Column(Integer)
    va_mention_std2a = Column(Integer)
    mentions_tmd     = Column(Integer)
    va_mention_tmd   = Column(Integer)
    mentions_sthr    = Column(Integer)
    va_mention_sthr  = Column(Integer)


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


if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///lycee.db')

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
