﻿from CollegesLycees import db


class Etablissement(db.Model):
    __tablename__ = 'etablissement'

    # Identification
    UAI              = db.Column(db.String, primary_key=True)
    nom              = db.Column(db.String)
    academie         = db.Column(db.String)
    departement      = db.Column(db.Integer)
    secteur_prive    = db.Column(Boolean)
    commune          = db.Column(db.String)
    latitude         = db.Column(db.Float)
    longitude        = db.Column(db.Float)
    denomination     = db.Column(db.String)

    # Brevet
    presents_brevet  = db.Column(db.Integer)
    admis_brevet     = db.Column(db.Integer)
    mentions_brevet  = db.Column(db.Integer)

    # Filiere generale et techno
    taux_2nde_gt_bac    = db.Column(db.Integer)
    va_2nde_gt_bac      = db.Column(db.Integer)
    taux_1ere_gt_bac    = db.Column(db.Integer)
    va_1ere_gt_bac      = db.Column(db.Integer)
    taux_term_gt_bac    = db.Column(db.Integer)
    va_term_gt_bac      = db.Column(db.Integer)

    presents_gt       = db.Column(db.Integer)
    admis_gt          = db.Column(db.Integer)
    va_admis_gt       = db.Column(db.Integer)
    presents_l        = db.Column(db.Integer)
    admis_l           = db.Column(db.Integer)
    va_admis_l        = db.Column(db.Integer)
    presents_es       = db.Column(db.Integer)
    admis_es          = db.Column(db.Integer)
    va_admis_es       = db.Column(db.Integer)
    presents_s        = db.Column(db.Integer)
    admis_s           = db.Column(db.Integer)
    va_admis_s        = db.Column(db.Integer)
    presents_stmg     = db.Column(db.Integer)
    admis_stmg        = db.Column(db.Integer)
    va_admis_stmg     = db.Column(db.Integer)
    presents_stl      = db.Column(db.Integer)
    admis_stl         = db.Column(db.Integer)
    va_admis_stl      = db.Column(db.Integer)
    presents_st2s     = db.Column(db.Integer)
    admis_st2s        = db.Column(db.Integer)
    va_admis_st2s     = db.Column(db.Integer)
    presents_sti2d    = db.Column(db.Integer)
    admis_sti2d       = db.Column(db.Integer)
    va_admis_sti2d    = db.Column(db.Integer)
    presents_std2a    = db.Column(db.Integer)
    admis_std2a       = db.Column(db.Integer)
    va_admis_std2a    = db.Column(db.Integer)
    presents_tmd      = db.Column(db.Integer)
    admis_tmd         = db.Column(db.Integer)
    va_admis_tmd      = db.Column(db.Integer)
    presents_sthr     = db.Column(db.Integer)
    admis_sthr        = db.Column(db.Integer)
    va_admis_sthr     = db.Column(db.Integer)

    mentions_gt       = db.Column(db.Integer)
    va_mention_gt     = db.Column(db.Integer)
    mentions_l        = db.Column(db.Integer)
    va_mention_l      = db.Column(db.Integer)
    mentions_es       = db.Column(db.Integer)
    va_mention_es     = db.Column(db.Integer)
    mentions_s        = db.Column(db.Integer)
    va_mention_s      = db.Column(db.Integer)
    mentions_stmg     = db.Column(db.Integer)
    va_mention_stmg   = db.Column(db.Integer)
    mentions_stl      = db.Column(db.Integer)
    va_mention_stl    = db.Column(db.Integer)
    mentions_st2s     = db.Column(db.Integer)
    va_mention_st2s   = db.Column(db.Integer)
    mentions_sti2d    = db.Column(db.Integer)
    va_mention_sti2d  = db.Column(db.Integer)
    mentions_std2a    = db.Column(db.Integer)
    va_mention_std2a  = db.Column(db.Integer)
    mentions_tmd      = db.Column(db.Integer)
    va_mention_tmd    = db.Column(db.Integer)
    mentions_sthr     = db.Column(db.Integer)
    va_mention_sthr   = db.Column(db.Integer)

    # Filiere pro
    taux_2nde_pro_bac = db.Column(db.Integer)
    va_2nde_pro_bac   = db.Column(db.Integer)
    taux_1ere_pro_bac = db.Column(db.Integer)
    va_1ere_pro_bac   = db.Column(db.Integer)
    taux_term_pro_bac = db.Column(db.Integer)
    va_term_pro_bac   = db.Column(db.Integer)

    presents_pro = db.Column(db.Integer)
    admis_pro = db.Column(db.Integer)
    va_admis_pro = db.Column(db.Integer)
    presents_production = db.Column(db.Integer)
    admis_production = db.Column(db.Integer)
    va_admis_production = db.Column(db.Integer)
    presents_services = db.Column(db.Integer)
    admis_services = db.Column(db.Integer)
    va_admis_services = db.Column(db.Integer)
    presents_spe_pluritech = db.Column(db.Integer)
    admis_spe_pluritech = db.Column(db.Integer)
    va_admis_spe_pluritech = db.Column(db.Integer)
    presents_transformations = db.Column(db.Integer)
    admis_transformations = db.Column(db.Integer)
    va_admis_transformations = db.Column(db.Integer)
    presents_genie_civil = db.Column(db.Integer)
    admis_genie_civil = db.Column(db.Integer)
    va_admis_genie_civil = db.Column(db.Integer)
    presents_materiaux_souples = db.Column(db.Integer)
    admis_materiaux_souples = db.Column(db.Integer)
    va_admis_materiaux_souples = db.Column(db.Integer)
    presents_meca_elec = db.Column(db.Integer)
    admis_meca_elec = db.Column(db.Integer)
    va_admis_meca_elec = db.Column(db.Integer)
    presents_spe_plurivalentes = db.Column(db.Integer)
    admis_spe_plurivalentes = db.Column(db.Integer)
    va_admis_spe_plurivalentes = db.Column(db.Integer)
    presents_echanges_gestion = db.Column(db.Integer)
    admis_echanges_gestion = db.Column(db.Integer)
    va_admis_echanges_gestion = db.Column(db.Integer)
    presents_communication_info = db.Column(db.Integer)
    admis_communication_info = db.Column(db.Integer)
    va_admis_communication_info = db.Column(db.Integer)
    presents_services_personnes = db.Column(db.Integer)
    admis_services_personnes = db.Column(db.Integer)
    va_admis_services_personnes = db.Column(db.Integer)
    presents_services_collectivite = db.Column(db.Integer)
    admis_services_collectivite = db.Column(db.Integer)
    va_admis_services_collectivite = db.Column(db.Integer)

    mentions_pro = db.Column(db.Integer)
    va_mention_pro = db.Column(db.Integer)
    mentions_production = db.Column(db.Integer)
    va_mention_production = db.Column(db.Integer)
    mentions_services = db.Column(db.Integer)
    va_mention_services = db.Column(db.Integer)
    mentions_spe_pluritech = db.Column(db.Integer)
    va_mention_spe_pluritech = db.Column(db.Integer)
    mentions_transformations = db.Column(db.Integer)
    va_mention_transformations = db.Column(db.Integer)
    mentions_genie_civil = db.Column(db.Integer)
    va_mention_genie_civil = db.Column(db.Integer)
    mentions_materiaux_souples = db.Column(db.Integer)
    va_mention_materiaux_souples = db.Column(db.Integer)
    mentions_meca_elec = db.Column(db.Integer)
    va_mention_meca_elec = db.Column(db.Integer)
    mentions_spe_plurivalentes = db.Column(db.Integer)
    va_mention_spe_plurivalentes = db.Column(db.Integer)
    mentions_echanges_gestion = db.Column(db.Integer)
    va_mention_echanges_gestion = db.Column(db.Integer)
    mentions_communication_info = db.Column(db.Integer)
    va_mention_communication_info = db.Column(db.Integer)
    mentions_services_personnes = db.Column(db.Integer)
    va_mention_services_personnes = db.Column(db.Integer)
    mentions_services_collectivite = db.Column(db.Integer)
    va_mention_services_collectivite = db.Column(db.Integer)

    def __repr__(self):
        return '<Etablissement {}>'.format(self.nom)
        
        