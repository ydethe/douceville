from pathlib import Path
from douceville.retriever import build_db_records


if __name__ == "__main__":
    # liste = liste_brevet()
    # liste = liste_bac_general()
    # liste_etablissements()
    # print(len(liste))

    liste_etablissements, liste_resultats = build_db_records(
        etab_pth=Path(
            "fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.parquet"
        ),
        bacgt_pth=Path("fr-en-indicateurs-de-resultat-des-lycees-gt_v2.parquet"),
        dnb_pth=Path("fr-en-dnb-par-etablissement.parquet"),
    )
