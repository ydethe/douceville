from ..models import ImportStatus
from ..blueprints.isochrone.geographique import findCoordFromAddress


def findEtabPosition(etab: dict) -> dict:
    lat = etab.pop("latitude", None)
    lon = etab.pop("longitude", None)

    adresse = {}
    if etab["nom"] is not None:
        adresse["nom"] = etab["nom"].title()
    if lat is not None:
        adresse["lat"] = lat
    if lon is not None:
        adresse["lon"] = lon
    if etab.get("adresse", None) is not None:
        adresse["adresse"] = etab["adresse"].title()
        while "  " in adresse["adresse"]:
            adresse["adresse"] = adresse["adresse"].replace("  ", " ")
    if etab.get("code_postal", None) is not None:
        adresse["cp"] = etab["code_postal"]
    if etab.get("departement", None) is not None:
        adresse["departement"] = etab["departement"]
    if etab.get("commune", None) is not None:
        adresse["commune"] = etab["commune"].title()

    etab_maj = findCoordFromAddress(**adresse)
    if etab_maj is None:
        return None

    etab["import_status"] = ImportStatus.COORD_FROM_ADDRESS
    etab.update(etab_maj)

    return etab


# Autres criteres :
# - RSA
# - lieux de culte
# - meteo
# - voir concurrents : jequitteparis.fr
# - immobilier
# - maternité
# - age moyen

# https://www.data.gouv.fr/fr/datasets/liste-des-etablissements-des-premier-et-second-degres-pour-les-secteurs-publics-et-prives-en-france
# https://www.education.gouv.fr/les-indicateurs-de-resultats-des-lycees-1118
# https://www.data.gouv.fr/fr/datasets/diplome-national-du-brevet-par-etablissement
# https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=DonneesLocales&version=V0.1&provider=insee
