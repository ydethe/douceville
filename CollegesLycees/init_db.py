from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Lycee(Base):
    __tablename__ = 'lycee'

    # Identification
    UAI              = Column(String, primary_key=True)
    nom              = Column(String)
    academie         = Column(String)
    departement      = Column(Integer)
    secteur_prive    = Column(Boolean)
    commune          = Column(String)

    # Filiere generale et techno
    taux_2nde_gt_bac    = Column(Integer)
    va_2nde_gt_bac      = Column(Integer)
    taux_1ere_gt_bac    = Column(Integer)
    va_1ere_gt_bac      = Column(Integer)
    taux_term_gt_bac    = Column(Integer)
    va_term_gt_bac      = Column(Integer)

    presents_gt       = Column(Integer)
    admis_gt          = Column(Integer)
    va_admis_gt       = Column(Integer)
    presents_l        = Column(Integer)
    admis_l           = Column(Integer)
    va_admis_l        = Column(Integer)
    presents_es       = Column(Integer)
    admis_es          = Column(Integer)
    va_admis_es       = Column(Integer)
    presents_s        = Column(Integer)
    admis_s           = Column(Integer)
    va_admis_s        = Column(Integer)
    presents_stmg     = Column(Integer)
    admis_stmg        = Column(Integer)
    va_admis_stmg     = Column(Integer)
    presents_stl      = Column(Integer)
    admis_stl         = Column(Integer)
    va_admis_stl      = Column(Integer)
    presents_st2s     = Column(Integer)
    admis_st2s        = Column(Integer)
    va_admis_st2s     = Column(Integer)
    presents_sti2d    = Column(Integer)
    admis_sti2d       = Column(Integer)
    va_admis_sti2d    = Column(Integer)
    presents_std2a    = Column(Integer)
    admis_std2a       = Column(Integer)
    va_admis_std2a    = Column(Integer)
    presents_tmd      = Column(Integer)
    admis_tmd         = Column(Integer)
    va_admis_tmd      = Column(Integer)
    presents_sthr     = Column(Integer)
    admis_sthr        = Column(Integer)
    va_admis_sthr     = Column(Integer)

    mentions_gt       = Column(Integer)
    va_mention_gt     = Column(Integer)
    mentions_l        = Column(Integer)
    va_mention_l      = Column(Integer)
    mentions_es       = Column(Integer)
    va_mention_es     = Column(Integer)
    mentions_s        = Column(Integer)
    va_mention_s      = Column(Integer)
    mentions_stmg     = Column(Integer)
    va_mention_stmg   = Column(Integer)
    mentions_stl      = Column(Integer)
    va_mention_stl    = Column(Integer)
    mentions_st2s     = Column(Integer)
    va_mention_st2s   = Column(Integer)
    mentions_sti2d    = Column(Integer)
    va_mention_sti2d  = Column(Integer)
    mentions_std2a    = Column(Integer)
    va_mention_std2a  = Column(Integer)
    mentions_tmd      = Column(Integer)
    va_mention_tmd    = Column(Integer)
    mentions_sthr     = Column(Integer)
    va_mention_sthr   = Column(Integer)

    # Filiere pro
    taux_2nde_pro_bac = Column(Integer)
    va_2nde_pro_bac   = Column(Integer)
    taux_1ere_pro_bac = Column(Integer)
    va_1ere_pro_bac   = Column(Integer)
    taux_term_pro_bac = Column(Integer)
    va_term_pro_bac   = Column(Integer)

    presents_pro = Column(Integer)
    admis_pro = Column(Integer)
    va_admis_pro = Column(Integer)
    presents_production = Column(Integer)
    admis_production = Column(Integer)
    va_admis_production = Column(Integer)
    presents_services = Column(Integer)
    admis_services = Column(Integer)
    va_admis_services = Column(Integer)
    presents_spe_pluritech = Column(Integer)
    admis_spe_pluritech = Column(Integer)
    va_admis_spe_pluritech = Column(Integer)
    presents_transformations = Column(Integer)
    admis_transformations = Column(Integer)
    va_admis_transformations = Column(Integer)
    presents_genie_civil = Column(Integer)
    admis_genie_civil = Column(Integer)
    va_admis_genie_civil = Column(Integer)
    presents_materiaux_souples = Column(Integer)
    admis_materiaux_souples = Column(Integer)
    va_admis_materiaux_souples = Column(Integer)
    presents_meca_elec = Column(Integer)
    admis_meca_elec = Column(Integer)
    va_admis_meca_elec = Column(Integer)
    presents_spe_plurivalentes = Column(Integer)
    admis_spe_plurivalentes = Column(Integer)
    va_admis_spe_plurivalentes = Column(Integer)
    presents_echanges_gestion = Column(Integer)
    admis_echanges_gestion = Column(Integer)
    va_admis_echanges_gestion = Column(Integer)
    presents_communication_info = Column(Integer)
    admis_communication_info = Column(Integer)
    va_admis_communication_info = Column(Integer)
    presents_services_personnes = Column(Integer)
    admis_services_personnes = Column(Integer)
    va_admis_services_personnes = Column(Integer)
    presents_services_collectivite = Column(Integer)
    admis_services_collectivite = Column(Integer)
    va_admis_services_collectivite = Column(Integer)

    mentions_pro = Column(Integer)
    va_mention_pro = Column(Integer)
    mentions_production = Column(Integer)
    va_mention_production = Column(Integer)
    mentions_services = Column(Integer)
    va_mention_services = Column(Integer)
    mentions_spe_pluritech = Column(Integer)
    va_mention_spe_pluritech = Column(Integer)
    mentions_transformations = Column(Integer)
    va_mention_transformations = Column(Integer)
    mentions_genie_civil = Column(Integer)
    va_mention_genie_civil = Column(Integer)
    mentions_materiaux_souples = Column(Integer)
    va_mention_materiaux_souples = Column(Integer)
    mentions_meca_elec = Column(Integer)
    va_mention_meca_elec = Column(Integer)
    mentions_spe_plurivalentes = Column(Integer)
    va_mention_spe_plurivalentes = Column(Integer)
    mentions_echanges_gestion = Column(Integer)
    va_mention_echanges_gestion = Column(Integer)
    mentions_communication_info = Column(Integer)
    va_mention_communication_info = Column(Integer)
    mentions_services_personnes = Column(Integer)
    va_mention_services_personnes = Column(Integer)
    mentions_services_collectivite = Column(Integer)
    va_mention_services_collectivite = Column(Integer)


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


# ACCES_GT
corr_acces_gt = {}
corr_acces_gt['UAI']             = 'UAI', idty
corr_acces_gt['NOM_UAI']         = 'nom', idty
corr_acces_gt['ACAD']            = 'academie', idty
corr_acces_gt['DEP']             = 'departement', to_int
corr_acces_gt['SECTEUR']         = 'secteur_prive', secteur_to_bool
corr_acces_gt['COMMUNE_UAI']     = 'commune', idty
corr_acces_gt['TAUX_2NDE_BAC']   = 'taux_2nde_gt_bac'  , to_int
corr_acces_gt['VA_2NDE_BAC']     = 'va_2nde_gt_bac'    , to_int
corr_acces_gt['TAUX_1ERE_BAC']   = 'taux_1ere_gt_bac'  , to_int
corr_acces_gt['VA_1ERE_BAC']     = 'va_1ere_gt_bac'    , to_int
corr_acces_gt['TAUX_TERM_BAC']   = 'taux_term_gt_bac'  , to_int
corr_acces_gt['VA_TERM_BAC']     = 'va_term_gt_bac'    , to_int

# REUSSITE_GT
corr_reussite_gt = {}
corr_reussite_gt['UAI']            = 'UAI', idty
corr_reussite_gt['NOM_UAI']        = 'nom', idty
corr_reussite_gt['ACAD']           = 'academie', idty
corr_reussite_gt['DEP']            = 'departement', to_int
corr_reussite_gt['SECTEUR']        = 'secteur_prive', secteur_to_bool
corr_reussite_gt['COMMUNE_UAI']    = 'commune', idty
corr_reussite_gt['Presents_GT']    = 'presents_gt'   , to_int
corr_reussite_gt['Admis_GT']       = 'admis_gt'      , to_int
corr_reussite_gt['VA_GT']          = 'va_admis_gt'   , to_int
corr_reussite_gt['Presents_L']     = 'presents_l'    , to_int
corr_reussite_gt['Admis_L']        = 'admis_l'       , to_int
corr_reussite_gt['VA_L']           = 'va_admis_l'    , to_int
corr_reussite_gt['Presents_ES']    = 'presents_es'   , to_int
corr_reussite_gt['Admis_ES']       = 'admis_es'      , to_int
corr_reussite_gt['VA_ES']          = 'va_admis_es'   , to_int
corr_reussite_gt['Presents_S']     = 'presents_s'    , to_int
corr_reussite_gt['Admis_S']        = 'admis_s'       , to_int
corr_reussite_gt['VA_S']           = 'va_admis_s'    , to_int
corr_reussite_gt['Presents_STMG']  = 'presents_stmg' , to_int
corr_reussite_gt['Admis_STMG']     = 'admis_stmg'    , to_int
corr_reussite_gt['VA_STMG']        = 'va_admis_stmg' , to_int
corr_reussite_gt['Presents_STL']   = 'presents_stl'  , to_int
corr_reussite_gt['Admis_STL']      = 'admis_stl'     , to_int
corr_reussite_gt['VA_STL']         = 'va_admis_stl'  , to_int
corr_reussite_gt['Presents_ST2S']  = 'presents_st2s' , to_int
corr_reussite_gt['Admis_ST2S']     = 'admis_st2s'    , to_int
corr_reussite_gt['VA_ST2S']        = 'va_admis_st2s' , to_int
corr_reussite_gt['Presents_STI2D'] = 'presents_sti2d', to_int
corr_reussite_gt['Admis_STI2D']    = 'admis_sti2d'   , to_int
corr_reussite_gt['VA_STI2D']       = 'va_admis_sti2d', to_int
corr_reussite_gt['Presents_STD2A'] = 'presents_std2a', to_int
corr_reussite_gt['Admis_STD2A']    = 'admis_std2a'   , to_int
corr_reussite_gt['VA_STD2A']       = 'va_admis_std2a', to_int
corr_reussite_gt['Presents_TMD']   = 'presents_tmd'  , to_int
corr_reussite_gt['Admis_TMD']      = 'admis_tmd'     , to_int
corr_reussite_gt['VA_TMD']         = 'va_admis_tmd'  , to_int
corr_reussite_gt['Presents_STHR']  = 'presents_sthr' , to_int
corr_reussite_gt['Admis_STHR']     = 'admis_sthr'    , to_int
corr_reussite_gt['VA_STHR']        = 'va_admis_sthr' , to_int

# MENTION_GT
corr_mention_gt = {}
corr_mention_gt['UAI']            = 'UAI', idty
corr_mention_gt['NOM_UAI']        = 'nom', idty
corr_mention_gt['ACAD']           = 'academie', idty
corr_mention_gt['DEP']            = 'departement', to_int
corr_mention_gt['SECTEUR']        = 'secteur_prive', secteur_to_bool
corr_mention_gt['COMMUNE_UAI']    = 'commune', idty
corr_mention_gt['Mentions_GT'] = 'mentions_gt', to_int
corr_mention_gt['VA_GT'] = 'va_mention_gt', to_int
corr_mention_gt['Mentions_L'] = 'mentions_l', to_int
corr_mention_gt['VA_L'] = 'va_mention_l', to_int
corr_mention_gt['Mentions_ES'] = 'mentions_es', to_int
corr_mention_gt['VA_ES'] = 'va_mention_es', to_int
corr_mention_gt['Mentions_S'] = 'mentions_s', to_int
corr_mention_gt['VA_S'] = 'va_mention_s', to_int
corr_mention_gt['Mentions_STMG'] = 'mentions_stmg', to_int
corr_mention_gt['VA_STMG'] = 'va_mention_stmg', to_int
corr_mention_gt['Mentions_STL'] = 'mentions_stl', to_int
corr_mention_gt['VA_STL'] = 'va_mention_stl', to_int
corr_mention_gt['Mentions_ST2S'] = 'mentions_st2s', to_int
corr_mention_gt['VA_ST2S'] = 'va_mention_st2s', to_int
corr_mention_gt['Mentions_STI2D'] = 'mentions_sti2d', to_int
corr_mention_gt['VA_STI2D'] = 'va_mention_sti2d', to_int
corr_mention_gt['Mentions_STD2A'] = 'mentions_std2a', to_int
corr_mention_gt['VA_STD2A'] = 'va_mention_std2a', to_int
corr_mention_gt['Mentions_TMD'] = 'mentions_tmd', to_int
corr_mention_gt['VA_TMD'] = 'va_mention_tmd', to_int
corr_mention_gt['Mentions_STHR'] = 'mentions_sthr', to_int
corr_mention_gt['VA_STHR'] = 'va_mention_sthr', to_int

# ACCES_PRO
corr_acces_pro = {}
corr_acces_pro['UAI']           = 'UAI', idty
corr_acces_pro['NOM_UAI']       = 'nom', idty
corr_acces_pro['ACAD']          = 'academie', idty
corr_acces_pro['DEP']           = 'departement', to_int
corr_acces_pro['SECTEUR']       = 'secteur_prive', secteur_to_bool
corr_acces_pro['COMMUNE_UAI']   = 'commune', idty
corr_acces_pro['TAUX_2NDE_BAC'] = 'taux_2nde_pro_bac', to_int
corr_acces_pro['VA_2NDE_BAC']   = 'va_2nde_pro_bac', to_int
corr_acces_pro['TAUX_1ERE_BAC'] = 'taux_1ere_pro_bac', to_int
corr_acces_pro['VA_1ERE_BAC']   = 'va_1ere_pro_bac', to_int
corr_acces_pro['TAUX_TERM_BAC'] = 'taux_term_pro_bac', to_int
corr_acces_pro['VA_TERM_BAC']   = 'va_term_pro_bac', to_int

# REUSSITE_PRO
corr_reussite_pro = {}
corr_reussite_pro['UAI']           = 'UAI', idty
corr_reussite_pro['NOM_UAI']       = 'nom', idty
corr_reussite_pro['ACAD']          = 'academie', idty
corr_reussite_pro['DEP']           = 'departement', to_int
corr_reussite_pro['SECTEUR']       = 'secteur_prive', secteur_to_bool
corr_reussite_pro['COMMUNE_UAI']   = 'commune', idty
corr_reussite_pro['Presents_PRO'] =                   'presents_pro', to_int
corr_reussite_pro['Admis_PRO'] =                      'admis_pro', to_int
corr_reussite_pro['VA_PRO'] =                         'va_admis_pro', to_int
corr_reussite_pro['Presents_Production'] =            'presents_production', to_int
corr_reussite_pro['Admis_Production'] =               'admis_production', to_int
corr_reussite_pro['VA_Production'] =                  'va_admis_production', to_int
corr_reussite_pro['Presents_Services'] =              'presents_services', to_int
corr_reussite_pro['Admis_Services'] =                 'admis_services', to_int
corr_reussite_pro['VA_Services'] =                    'va_admis_services', to_int
corr_reussite_pro['Presents_Spe_pluritech'] =         'presents_spe_pluritech', to_int
corr_reussite_pro['Admis_Spe_pluritech'] =            'admis_spe_pluritech', to_int
corr_reussite_pro['VA_Spe_pluritech'] =               'va_admis_spe_pluritech', to_int
corr_reussite_pro['Presents_Transformations'] =       'presents_transformations', to_int
corr_reussite_pro['Admis_Transformations'] =          'admis_transformations', to_int
corr_reussite_pro['VA_Transformations'] =             'va_admis_transformations', to_int
corr_reussite_pro['Presents_Genie_civil'] =           'presents_genie_civil', to_int
corr_reussite_pro['Admis_Genie_civil'] =              'admis_genie_civil', to_int
corr_reussite_pro['VA_Genie_civil'] =                 'va_admis_genie_civil', to_int
corr_reussite_pro['Presents_Materiaux_souples'] =     'presents_materiaux_souples', to_int
corr_reussite_pro['Admis_Materiaux_souples'] =        'admis_materiaux_souples', to_int
corr_reussite_pro['VA_Materiaux_souples'] =           'va_admis_materiaux_souples', to_int
corr_reussite_pro['Presents_Meca_elec'] =             'presents_meca_elec', to_int
corr_reussite_pro['Admis_Meca_elec'] =                'admis_meca_elec', to_int
corr_reussite_pro['VA_Meca_elec'] =                   'va_admis_meca_elec', to_int
corr_reussite_pro['Presents_Spe_plurivalentes'] =     'presents_spe_plurivalentes', to_int
corr_reussite_pro['Admis_Spe_plurivalentes'] =        'admis_spe_plurivalentes', to_int
corr_reussite_pro['VA_Spe_plurivalentes'] =           'va_admis_spe_plurivalentes', to_int
corr_reussite_pro['Presents_Echanges_gestion'] =      'presents_echanges_gestion', to_int
corr_reussite_pro['Admis_Echanges_gestion'] =         'admis_echanges_gestion', to_int
corr_reussite_pro['VA_Echanges_gestion'] =            'va_admis_echanges_gestion', to_int
corr_reussite_pro['Presents_Communication_info'] =    'presents_communication_info', to_int
corr_reussite_pro['Admis_Communication_info'] =       'admis_communication_info', to_int
corr_reussite_pro['VA_Communication_info'] =          'va_admis_communication_info', to_int
corr_reussite_pro['Presents_Services_personnes'] =    'presents_services_personnes', to_int
corr_reussite_pro['Admis_Services_personnes'] =       'admis_services_personnes', to_int
corr_reussite_pro['VA_Services_personnes'] =          'va_admis_services_personnes', to_int
corr_reussite_pro['Presents_Services_collectivite'] = 'presents_services_collectivite', to_int
corr_reussite_pro['Admis_Services_collectivite'] =    'admis_services_collectivite', to_int
corr_reussite_pro['VA_Services_collectivite'] =       'va_admis_services_collectivite', to_int

# MENTION_GT
corr_mention_pro = {}
corr_mention_pro['UAI']           = 'UAI', idty
corr_mention_pro['NOM_UAI']       = 'nom', idty
corr_mention_pro['ACAD']          = 'academie', idty
corr_mention_pro['DEP']           = 'departement', to_int
corr_mention_pro['SECTEUR']       = 'secteur_prive', secteur_to_bool
corr_mention_pro['COMMUNE_UAI']   = 'commune', idty
corr_mention_pro['Mentions_PRO']                   = 'mentions_pro', to_int
corr_mention_pro['VA_PRO']                         = 'va_mention_pro', to_int
corr_mention_pro['Mentions_Production']            = 'mentions_production', to_int
corr_mention_pro['VA_Production']                  = 'va_mention_production', to_int
corr_mention_pro['Mentions_Services']              = 'mentions_services', to_int
corr_mention_pro['VA_Services']                    = 'va_mention_services', to_int
corr_mention_pro['Mentions_Spe_pluritech']         = 'mentions_spe_pluritech', to_int
corr_mention_pro['VA_Spe_pluritech']               = 'va_mention_spe_pluritech', to_int
corr_mention_pro['Mentions_Transformations']       = 'mentions_transformations', to_int
corr_mention_pro['VA_Transformations']             = 'va_mention_transformations', to_int
corr_mention_pro['Mentions_Genie_civil']           = 'mentions_genie_civil', to_int
corr_mention_pro['VA_Genie_civil']                 = 'va_mention_genie_civil', to_int
corr_mention_pro['Mentions_Materiaux_souples']     = 'mentions_materiaux_souples', to_int
corr_mention_pro['VA_Materiaux_souples']           = 'va_mention_materiaux_souples', to_int
corr_mention_pro['Mentions_Meca_elec']             = 'mentions_meca_elec', to_int
corr_mention_pro['VA_Meca_elec']                   = 'va_mention_meca_elec', to_int
corr_mention_pro['Mentions_Spe_plurivalentes']     = 'mentions_spe_plurivalentes', to_int
corr_mention_pro['VA_Spe_plurivalentes']           = 'va_mention_spe_plurivalentes', to_int
corr_mention_pro['Mentions_Echanges_gestion']      = 'mentions_echanges_gestion', to_int
corr_mention_pro['VA_Echanges_gestion']            = 'va_mention_echanges_gestion', to_int
corr_mention_pro['Mentions_Communication_info']    = 'mentions_communication_info', to_int
corr_mention_pro['VA_Communication_info']          = 'va_mention_communication_info', to_int
corr_mention_pro['Mentions_Services_personnes']    = 'mentions_services_personnes', to_int
corr_mention_pro['VA_Services_personnes']          = 'va_mention_services_personnes', to_int
corr_mention_pro['Mentions_Services_collectivite'] = 'mentions_services_collectivite', to_int
corr_mention_pro['VA_Services_collectivite']       = 'va_mention_services_collectivite', to_int


if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///lycee.db')

    from sqlalchemy.orm import sessionmaker
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
