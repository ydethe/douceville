from pathlib import Path
import pickle

import pandas as pd

from douceville.scripts.conv_rdf import conv_rec


def test_conv_rec():
    with open("data/data_dict.raw", "rb") as f:
        info = pickle.load(f)

    for rec in info:
        rec = conv_rec(rec)

    for k in rec.keys():
        print(k, rec[k])


def test_adresses():
    df = pd.read_excel(
        Path("data/fr-en-adresse-court.xlsx"),
        names=[
            "UAI",
            "nom",
            "unused02",
            "unused03",
            "unused04",
            "adresse",
            "lieu_dit",
            "unused07",
            "code_postal",
            "unused09",
            "commune",
            "unused11",
            "unused12",
            "unused13",
            "unused14",
            "unused15",
            "unused16",
            "unused17",
            "unused18",
            "nature",
            "unused20",
            "etat_etablissement",
            "unused22",
            "unused23",
            "unused24",
            "unused25",
            "unused26",
            "unused27",
            "unused28",
            "position",
            "unused30",
            "secteur",
            "unused32",
            "unused33",
            "date_ouverture",
        ],
        # usecols=[0, 1, 5, 6, 8, 10, 19, 21, 29, 31, 34],
        parse_dates=[34],
    )

    df = df.iloc[:, [0, 1, 5, 6, 8, 10, 19, 21, 29, 31, 34]]
    print(df)


# test_conv_rec()
test_adresses()
