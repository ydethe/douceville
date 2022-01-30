import requests


def search_data_gouv(uai: str) -> str:
    url = (
        "https://data.education.gouv.fr/api/records/1.0/search/?dataset=fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre&q=&rows=1&facet=numero_uai&facet=appellation_officielle&facet=secteur_public_prive_libe&facet=code_postal_uai&facet=localite_acheminement_uai&facet=libelle_commune&facet=appariement&facet=localisation&facet=nature_uai&facet=nature_uai_libe&facet=etat_etablissement&facet=etat_etablissement_libe&facet=code_departement&facet=code_region&facet=code_academie&facet=code_commune&facet=libelle_departement&facet=libelle_region&facet=libelle_academie&facet=secteur_prive_code_type_contrat&facet=secteur_prive_libelle_type_contrat&facet=code_ministere&facet=libelle_ministere&refine.numero_uai=%s"
        % uai
    )

    r = requests.request(method="GET", url=url)
    dat = r.json()

    if len(dat["records"]) == 0:
        return None

    return dat["records"][0]["fields"]
