from datetime import datetime
import typing as T

import requests
from pydantic import BaseModel
import rich.progress as rp
import pandas as pd

from .models import Etablissement
from .scripts.import_etablissements import findEtabPosition


class ResultatBrevetAPI(BaseModel):
    session: str
    numero_d_etablissement: str
    type_d_etablissement: str
    patronyme: str | None
    secteur_d_enseignement: str
    commune: str
    libelle_commune: str
    code_departement: str
    libelle_departement: str
    code_academie: str
    libelle_academie: str
    code_region: str
    libelle_region: str
    inscrits: int
    presents: int
    admis: int
    admis_sans_mention: int
    nombre_d_admis_mention_ab: int
    admis_mention_bien: int
    admis_mention_tres_bien: int
    taux_de_reussite: str


class ResultatLyceeGeneralAPI(BaseModel):
    etablissement: str | int | None
    annee: str | int | None
    ville: str | int | None
    code_etablissement: str | int | None
    commune: str | int | None
    academie: str | int | None
    departement: str | int | None
    secteur_public_pu_prive_pr: str | int | None
    effectif_presents_serie_l: str | int | None
    effectif_presents_serie_es: str | int | None
    effectif_presents_serie_s: str | int | None
    effectif_presents_serie_stg: str | int | None
    effectif_presents_serie_sti2d: str | int | None
    effectif_presents_serie_std2a: str | int | None
    effectif_presents_serie_stmg: str | int | None
    effectif_presents_serie_sti: str | int | None
    effectif_presents_serie_stl: str | int | None
    effectif_presents_serie_st2s: str | int | None
    effectif_presents_serie_musiq_danse: str | int | None
    effectif_presents_serie_hotellerie: str | int | None
    effectif_presents_total_series: str | int | None
    taux_brut_de_reussite_serie_l: str | float | None
    taux_brut_de_reussite_serie_es: str | float | None
    taux_brut_de_reussite_serie_s: str | float | None
    taux_brut_de_reussite_serie_stg: str | float | None
    taux_brut_de_reussite_serie_sti2d: str | float | None
    taux_brut_de_reussite_serie_std2a: str | float | None
    taux_brut_de_reussite_serie_stmg: str | int | None
    taux_brut_de_reussite_serie_sti: str | float | None
    taux_brut_de_reussite_serie_stl: str | float | None
    taux_brut_de_reussite_serie_st2s: str | int | None
    taux_brut_de_reussite_serie_musiq_danse: str | float | None
    taux_brut_de_reussite_serie_hotellerie: str | float | None
    taux_brut_de_reussite_total_series: str | float | None
    taux_reussite_attendu_acad_serie_l: str | float | None
    taux_reussite_attendu_acad_serie_es: str | float | None
    taux_reussite_attendu_acad_serie_s: str | float | None
    taux_reussite_attendu_acad_serie_stg: str | float | None
    taux_reussite_attendu_acad_serie_sti2d: str | float | None
    taux_reussite_attendu_acad_serie_std2a: str | float | None
    taux_reussite_attendu_acad_serie_stmg: str | float | None
    taux_reussite_attendu_acad_serie_sti: str | float | None
    taux_reussite_attendu_acad_serie_stl: str | float | None
    taux_reussite_attendu_acad_serie_st2s: str | float | None
    taux_reussite_attendu_acad_serie_musiq_danse: str | float | None
    taux_reussite_attendu_acad_serie_hotellerie: str | float | None
    taux_reussite_attendu_acad_total_series: str | float | None
    taux_reussite_attendu_france_serie_l: str | int | None
    taux_reussite_attendu_france_serie_es: str | int | None
    taux_reussite_attendu_france_serie_s: str | int | None
    taux_reussite_attendu_france_serie_stg: str | float | None
    taux_reussite_attendu_france_serie_sti2d: str | float | None
    taux_reussite_attendu_france_serie_std2a: str | float | None
    taux_reussite_attendu_france_serie_stmg: str | float | None
    taux_reussite_attendu_france_serie_sti: str | float | None
    taux_reussite_attendu_france_serie_stl: str | float | None
    taux_reussite_attendu_france_serie_st2s: str | float | None
    taux_reussite_attendu_france_serie_musiq_danse: str | float | None
    taux_reussite_attendu_france_serie_hotellerie: str | float | None
    taux_reussite_attendu_france_total_series: str | float | None
    taux_mention_brut_serie_l: str | float | None
    taux_mention_brut_serie_es: str | float | None
    taux_mention_brut_serie_s: str | float | None
    taux_mention_brut_serie_sti2d: str | float | None
    taux_mention_brut_serie_std2a: str | float | None
    taux_mention_brut_serie_stmg: str | int | None
    taux_mention_brut_serie_stl: str | float | None
    taux_mention_brut_serie_st2s: str | int | None
    taux_mention_brut_serie_musiq_danse: str | float | None
    taux_mention_brut_serie_hotellerie: str | float | None
    taux_mention_brut_toutes_series: str | float | None
    taux_mention_attendu_serie_l: str | float | None
    taux_mention_attendu_serie_es: str | float | None
    taux_mention_attendu_serie_s: str | float | None
    taux_mention_attendu_serie_sti2d: str | float | None
    taux_mention_attendu_serie_std2a: str | float | None
    taux_mention_attendu_serie_stmg: str | float | None
    taux_mention_attendu_serie_stl: str | float | None
    taux_mention_attendu_serie_st2s: str | float | None
    taux_mention_attendu_serie_musiq_danse: str | float | None
    taux_mention_attendu_serie_hotellerie: str | float | None
    taux_mention_attendu_toutes_series: str | float | None
    sructure_pedagogique_en_5_groupes: str | int | None
    sructure_pedagogique_en_7_groupes: str | int | None
    effectif_de_seconde: int | None
    effectif_de_premiere: int | None
    effectif_de_terminale: int | None
    taux_acces_brut_seconde_bac: int | None
    taux_acces_attendu_acad_seconde_bac: str | None
    taux_acces_attendu_france_seconde_bac: str | None
    taux_acces_brut_premiere_bac: str | int | None
    taux_acces_attendu_acad_premiere_bac: str | None
    taux_acces_attendu_france_premiere_bac: str | None
    taux_acces_brut_terminale_bac: str | int | None
    taux_acces_attendu_france_terminale_bac: str | None
    libelle_region_2016: str | int | None
    code_region_2016: str | int | None
    code_departement: str | int | None
    libelle_departement: str | int | None
    va_reu_total: str | int | None
    va_acc_seconde: str | int | None
    va_men_total: str | int | None
    va_reu_l: str | int | None
    va_reu_es: str | int | None
    va_reu_s: str | int | None
    va_reu_stg: str | int | None
    va_reu_sti2d: str | int | None
    va_reu_std2a: str | int | None
    va_reu_stmg: str | int | None
    va_reu_sti: str | int | None
    va_reu_stl: str | int | None
    va_reu_st2s: str | int | None
    va_reu_musiq_danse: str | int | None
    va_reu_hotellerie: str | int | None
    va_acc_premiere: str | int | None
    va_acc_terminale: str | int | None
    va_men_l: str | int | None
    va_men_es: str | int | None
    va_men_s: str | int | None
    va_men_sti2d: str | int | None
    va_men_std2a: str | int | None
    va_men_stmg: str | int | None
    va_men_stl: str | int | None
    va_men_st2s: str | int | None
    va_men_musiq_danse: str | int | None
    va_men_hotellerie: str | int | None
    presents_gnle: int | None
    taux_reu_brut_gnle: str | int | None
    va_reu_gnle: str | int | None
    taux_men_brut_gnle: str | int | None
    va_men_gnle: str | int | None
    nombre_de_mentions_tb_avec_felicitations_g: int | None
    nombre_de_mentions_tb_sans_felicitations_g: int | None
    nombre_de_mentions_b_g: int | None
    nombre_de_mentions_ab_g: int | None
    nombre_de_mentions_tb_avec_felicitations_t: int | None
    nombre_de_mentions_tb_sans_felicitations_t: int | None
    nombre_de_mentions_b_t: int | None
    nombre_de_mentions_ab_t: int | None


class EtablissementAPI(BaseModel):
    numero_uai: str
    appellation_officielle: str | None
    denomination_principale: str | None
    patronyme_uai: str | None
    secteur_public_prive_libe: str | int | None
    adresse_uai: str | int | None
    lieu_dit_uai: str | int | None
    boite_postale_uai: str | int | None
    code_postal_uai: str | int | None
    localite_acheminement_uai: str | int | None
    libelle_commune: str | int | None
    coordonnee_x: str | float | None
    coordonnee_y: str | float | None
    epsg: str | int | None
    latitude: str | float | None
    longitude: str | float | None
    appariement: str | int | None
    localisation: str | int | None
    nature_uai: str | int | None
    nature_uai_libe: str | int | None
    etat_etablissement: str | int | None
    etat_etablissement_libe: str | int | None
    code_departement: str | int | None
    code_region: str | int | None
    code_academie: str | int | None
    code_commune: str | int | None
    libelle_departement: str | int | None
    libelle_region: str | int | None
    libelle_academie: str | int | None
    secteur_prive_code_type_contrat: str | int | None
    secteur_prive_libelle_type_contrat: str | int | None
    code_ministere: str | int | None
    libelle_ministere: str | int | None
    date_ouverture: datetime | None

    @property
    def nom(self) -> str:
        if self.appellation_officielle is None:
            nom = self.nature_uai_libe.title()
        else:
            nom = self.appellation_officielle.title()
        return nom

    def build_db_record(self) -> Etablissement:
        etab_dict = {}
        etab_dict["nom"] = self.nom
        etab_dict["adresse"] = self.adresse_uai
        etab_dict["code_postal"] = self.code_postal_uai
        etab_dict["commune"] = self.libelle_commune
        etab_dict["nature"] = self.nature_uai_libe.title()
        etab_dict = findEtabPosition(etab_dict.copy())

        etab_dict["UAI"] = self.numero_uai
        etab_dict["lieu_dit"] = self.lieu_dit_uai
        etab_dict["academie"] = self.libelle_academie
        etab_dict["secteur"] = self.secteur_public_prive_libe.lower().replace("é", "e")
        etab_dict["ouverture"] = self.date_ouverture

        db_etab = Etablissement(**etab_dict)

        return db_etab

    @classmethod
    def fromPandasRow(cls, row) -> "EtablissementAPI":
        dat = dict(**row)
        ts = dat.pop("date_ouverture", None)
        dt = ts.to_pydatetime()
        row["date_ouverture"] = dt
        res = cls(**row)
        return res


def liste_brevet() -> T.List[ResultatBrevetAPI]:
    url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-dnb-par-etablissement/records?limit={limit}&offset={offset}"
    response = requests.get(url.format(offset=1, limit=1))
    data = response.json()
    total_count = data["total_count"]

    limit = 100
    records = []
    number_of_batch = total_count // limit
    for batch_num in rp.track(range(number_of_batch)):
        response = requests.get(url.format(offset=batch_num * limit, limit=limit))
        data = response.json()
        if "results" not in data.keys():
            continue
        records.extend([ResultatBrevetAPI.model_validate(res) for res in data["results"]])

    last_offset = number_of_batch * limit
    response = requests.get(url.format(offset=last_offset, limit=limit))
    data = response.json()
    if "results" in data.keys():
        records.extend([ResultatBrevetAPI.model_validate(res) for res in data["results"]])

    return records


def liste_bac_general() -> T.List[ResultatLyceeGeneralAPI]:
    url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indicateurs-de-resultat-des-lycees-denseignement-general-et-technologique/records?limit={limit}&offset={offset}"
    response = requests.get(url.format(offset=1, limit=1))
    data = response.json()
    total_count = data["total_count"]

    limit = 100
    records = []
    number_of_batch = total_count // limit
    for batch_num in rp.track(range(number_of_batch)):
        response = requests.get(url.format(offset=batch_num * limit, limit=limit))
        data = response.json()
        if "results" not in data.keys():
            continue
        records.extend([ResultatLyceeGeneralAPI.model_validate(res) for res in data["results"]])

    last_offset = number_of_batch * limit
    response = requests.get(url.format(offset=last_offset, limit=limit))
    data = response.json()
    if "results" in data.keys():
        records.extend([ResultatLyceeGeneralAPI.model_validate(res) for res in data["results"]])

    return records


def liste_etablissements() -> T.List[EtablissementAPI]:
    from . import logger

    limit = 20

    # url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/records?where=code_departement%3D%2202A%22&limit=20"
    url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/records?where=code_departement%3D%22{code_departement}%22&limit={limit}&offset={offset}"

    list_dpts = [f"{c:03d}" for c in range(1, 96)]
    list_dpts.remove("020")
    list_dpts.extend(["02A", "02B"])

    records = []
    for code in list_dpts:
        response = requests.get(url.format(code_departement=code, limit=1, offset=1))
        data = response.json()
        total_count = data["total_count"]

        logger.info(f"Téléchargement du département {code} - {total_count} établissements")

        number_of_batch = total_count // limit
        for batch_num in rp.track(range(number_of_batch)):
            response = requests.get(
                url.format(code_departement=code, offset=batch_num * limit, limit=limit)
            )
            data = response.json()
            if "results" not in data.keys():
                logger.warning(f"Error '{data['message']}'")
                continue
            new_recs = [EtablissementAPI.model_validate(res) for res in data["results"]]
            records.extend(new_recs)
            for r in new_recs:
                if "carnot" in r.nom.lower() and "dijon" in r.libelle_commune.lower():
                    print(r)

        last_offset = number_of_batch * limit
        response = requests.get(url.format(code_departement=code, offset=last_offset, limit=limit))
        data = response.json()
        if "results" not in data.keys():
            logger.warning(f"Error '{data['message']}'")
            continue
        new_recs = [EtablissementAPI.model_validate(res) for res in data["results"]]
        records.extend(new_recs)
        for r in new_recs:
            if "carnot" in r.nom.lower() and "dijon" in r.libelle_commune.lower():
                print(r)

    return records


def build_db_records():
    df = pd.read_parquet(
        "fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.parquet"
    )

    records = []
    for index, row in df.iterrows():
        etab = EtablissementAPI.fromPandasRow(row)
        db_etab = etab.build_db_record()
        if db_etab.commune.lower() == "dijon" and "carnot" in db_etab.nom:
            print(db_etab)
        records.append(db_etab)
