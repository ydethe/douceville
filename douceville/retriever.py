import typing as T

import requests
from pydantic import BaseModel
import rich.progress as rp


class ResultatBrevet(BaseModel):
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


class ResultatLyceeGeneral(BaseModel):
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


def liste_brevet() -> T.List[ResultatBrevet]:
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
        records.extend([ResultatBrevet.model_validate(res) for res in data["results"]])

    last_offset = number_of_batch * limit
    response = requests.get(url.format(offset=last_offset, limit=limit))
    data = response.json()
    if "results" in data.keys():
        records.extend([ResultatBrevet.model_validate(res) for res in data["results"]])

    return records


def liste_bac_general() -> T.List[ResultatLyceeGeneral]:
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
        records.extend([ResultatLyceeGeneral.model_validate(res) for res in data["results"]])

    last_offset = number_of_batch * limit
    response = requests.get(url.format(offset=last_offset, limit=limit))
    data = response.json()
    if "results" in data.keys():
        records.extend([ResultatLyceeGeneral.model_validate(res) for res in data["results"]])

    return records


if __name__ == "__main__":
    # liste = liste_brevet()
    liste = liste_bac_general()
    # print(len(liste))
