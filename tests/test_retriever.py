from pathlib import Path
from douceville.retriever import build_dataframes


if __name__ == "__main__":
    # liste_etablissements, liste_resultats = build_db_records(
    #     etab_pth=Path(
    #         "data/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.parquet"
    #     ),
    #     bacgt_pth=Path("data/fr-en-indicateurs-de-resultat-des-lycees-gt_v2.parquet"),
    #     dnb_pth=Path("data/fr-en-dnb-par-etablissement.parquet"),
    # )

    df_etab, df_res = build_dataframes(
        etab_pth=Path(
            "data/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.parquet"
        ),
        bacgt_pth=Path("data/fr-en-indicateurs-de-resultat-des-lycees-gt_v2.parquet"),
        dnb_pth=Path("data/fr-en-dnb-par-etablissement.parquet"),
        destination_folder=Path("data"),
    )
