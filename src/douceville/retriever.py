from datetime import datetime
from pathlib import Path
import typing as T
from dataclasses import dataclass

import rich.progress as rp
import pandas as pd
import numpy as np

from .models import Etablissement, Resultat
from .scripts.import_etablissements import findEtabPosition
from . import logger


@dataclass
class ResultatBrevetAPI:
    annee: int
    uai: str
    presents: int
    admis: int
    admis_sans_mention: int

    @classmethod
    def fromPandasRow(cls, row) -> "ResultatBrevetAPI":
        res = cls(
            annee=int(row["session"]),
            uai=row["numero_d_etablissement"],
            presents=int(row["presents"]),
            admis=int(row["admis"]),
            admis_sans_mention=int(row["admis_sans_mention"]),
        )
        return res

    def build_dataframe_record(self) -> dict:
        mentions = self.presents - self.admis_sans_mention
        res = dict(
            diplome="Brevet",
            annee=self.annee,
            presents=self.presents,
            admis=self.admis,
            mentions=mentions,
            etablissement_uai=self.uai,
        )
        return res

    def build_db_record(self) -> Resultat:
        res_dict = self.build_dataframe_record()

        db_res = Resultat(**res_dict)

        return db_res


@dataclass
class ResultatLyceeGeneralAPI:
    annee: datetime
    uai: str

    presents_l: int
    presents_es: int
    presents_s: int
    presents_sti2d: int
    presents_std2a: int
    presents_stmg: int
    presents_stl: int
    presents_st2s: int
    presents_s2tmd: int
    presents_sthr: int

    taux_reu_l: str
    taux_reu_es: str
    taux_reu_s: str
    taux_reu_sti2d: str
    taux_reu_std2a: str
    taux_reu_stmg: str
    taux_reu_stl: str
    taux_reu_st2s: str
    taux_reu_s2tmd: str
    taux_reu_sthr: str

    taux_men_l: str
    taux_men_es: str
    taux_men_s: str
    taux_men_sti2d: str
    taux_men_std2a: str
    taux_men_stmg: str
    taux_men_stl: str
    taux_men_st2s: str
    taux_men_s2tmd: str
    taux_men_sthr: str

    def build_dataframe_record(self, liste_uai: T.List[str]) -> T.List[dict]:
        if self.uai not in liste_uai:
            return []

        diplomes = [
            "l",
            "es",
            "s",
            "sti2d",
            "std2a",
            "stmg",
            "stl",
            "st2s",
            "s2tmd",
            "sthr",
        ]

        records = []
        for d in diplomes:
            effectif_brut = getattr(self, f"presents_{d}")
            if effectif_brut is None or np.isnan(effectif_brut):
                continue
            effectif = int(effectif_brut)

            taux_reu_brut = getattr(self, f"taux_reu_{d}")
            if taux_reu_brut == "" or taux_reu_brut is None:
                taux_reu = None
            else:
                taux_reu = int(effectif / 100 * float(taux_reu_brut))

            taux_men_brut = getattr(self, f"taux_men_{d}")
            if taux_men_brut == "" or taux_men_brut is None:
                taux_men = None
            else:
                taux_men = int(effectif / 100 * float(taux_men_brut))

            res = dict(
                diplome=f"Baccalauréat {d.upper()}",
                annee=int(self.annee.year),
                presents=effectif,
                admis=taux_reu,
                mentions=taux_men,
                etablissement_uai=self.uai,
            )
            records.append(res)

        return records

    def build_db_record(self, liste_uai: T.List[str]) -> T.List[Resultat]:
        df_rec = self.build_dataframe_record(liste_uai)
        records = [Resultat(**param) for param in df_rec]
        return records

    @classmethod
    def fromPandasRow(cls, row) -> "ResultatLyceeGeneralAPI":
        res = cls(
            annee=row["annee"],
            uai=row["uai"],
            presents_l=row["presents_l"],
            presents_es=row["presents_es"],
            presents_s=row["presents_s"],
            presents_sti2d=row["presents_sti2d"],
            presents_std2a=row["presents_std2a"],
            presents_stmg=row["presents_stmg"],
            presents_stl=row["presents_stl"],
            presents_st2s=row["presents_st2s"],
            presents_s2tmd=row["presents_s2tmd"],
            presents_sthr=row["presents_sthr"],
            taux_reu_l=row["taux_reu_l"],
            taux_reu_es=row["taux_reu_es"],
            taux_reu_s=row["taux_reu_s"],
            taux_reu_sti2d=row["taux_reu_sti2d"],
            taux_reu_std2a=row["taux_reu_std2a"],
            taux_reu_stmg=row["taux_reu_stmg"],
            taux_reu_stl=row["taux_reu_stl"],
            taux_reu_st2s=row["taux_reu_st2s"],
            taux_reu_s2tmd=row["taux_reu_s2tmd"],
            taux_reu_sthr=row["taux_reu_sthr"],
            taux_men_l=row["taux_men_l"],
            taux_men_es=row["taux_men_es"],
            taux_men_s=row["taux_men_s"],
            taux_men_sti2d=row["taux_men_sti2d"],
            taux_men_std2a=row["taux_men_std2a"],
            taux_men_stmg=row["taux_men_stmg"],
            taux_men_stl=row["taux_men_stl"],
            taux_men_st2s=row["taux_men_st2s"],
            taux_men_s2tmd=row["taux_men_s2tmd"],
            taux_men_sthr=row["taux_men_sthr"],
        )
        return res


@dataclass
class EtablissementAPI:
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
        while "  " in nom:
            nom = nom.replace("  ", " ")
        return nom

    def build_dataframe_record(self) -> dict:
        if self.numero_uai in ["0313198H"]:
            return None

        etab_dict = {}
        etab_dict["position"] = None
        etab_dict["nom"] = self.nom
        etab_dict["adresse"] = self.adresse_uai
        etab_dict["code_postal"] = self.code_postal_uai
        etab_dict["departement"] = self.libelle_departement
        etab_dict["commune"] = self.libelle_commune
        if "lyc" in self.nature_uai_libe.lower():
            etab_dict["nature"] = "Lycée"
        elif "coll" in self.nature_uai_libe.lower():
            etab_dict["nature"] = "Collège"
        elif "element" in self.nature_uai_libe.lower():
            etab_dict["nature"] = "Elementaire"
        elif "matern" in self.nature_uai_libe.lower():
            etab_dict["nature"] = "Maternelle"
        else:
            # logger.warning(f"Unable to determine nature '{self}'")
            return None

        if isinstance(self.latitude, float) and isinstance(self.longitude, float):
            if not np.isnan(self.latitude) and not np.isnan(self.longitude):
                etab_dict["position"] = f"POINT({self.longitude} {self.latitude})"
                etab_dict["latitude"] = self.latitude
                etab_dict["longitude"] = self.longitude
            else:
                etab_dict = findEtabPosition(etab_dict.copy())
        else:
            etab_dict = findEtabPosition(etab_dict.copy())

        if (
            etab_dict["latitude"] is None
            or self.code_departement.startswith("98")
            and etab_dict["latitude"] > 0
        ):
            etab_dict["position"] = None
            etab_dict["latitude"] = None
            etab_dict["longitude"] = None

        etab_dict["UAI"] = self.numero_uai
        if self.lieu_dit_uai is not None:
            etab_dict["lieu_dit"] = self.lieu_dit_uai.title()
        etab_dict["academie"] = self.libelle_academie.title()
        etab_dict["secteur"] = self.secteur_public_prive_libe.lower().replace("e", "é")
        etab_dict["ouverture"] = self.date_ouverture

        return etab_dict

    def build_db_record(self) -> Etablissement:
        etab_dict = self.build_dataframe_record()

        if etab_dict is None:
            return None

        db_etab = Etablissement(**etab_dict)

        return db_etab

    @classmethod
    def fromPandasRow(cls, row) -> "EtablissementAPI":
        dat = dict(**row)
        ts = dat.pop("date_ouverture", None)
        dt = ts.to_pydatetime()
        row["date_ouverture"] = dt
        row.pop("position")
        res = cls(**row)
        return res


def build_db_records(
    etab_pth: Path, bacgt_pth: Path, dnb_pth: Path
) -> T.Tuple[T.List[Etablissement], T.List[Resultat]]:
    # ========================================
    # Traitement des établissement
    # ========================================
    df = pd.read_parquet(etab_pth)

    liste_etablissements: T.List[Etablissement] = []
    for index, row in rp.track(df.iterrows(), total=len(df), description="Annuaire"):
        etab = EtablissementAPI.fromPandasRow(row)
        db_etab = etab.build_db_record()
        if db_etab is None:
            continue
        liste_etablissements.append(db_etab)

    logger.info(f"{len(liste_etablissements)} établissements chargés")
    liste_uai = [x.UAI for x in liste_etablissements]

    liste_resultats: T.List[Resultat] = []
    # ========================================
    # Traitement des résultats du BAC GT
    # ========================================
    df = pd.read_parquet(bacgt_pth)

    for index, row in rp.track(df.iterrows(), total=len(df), description="Bac GT"):
        resultats = ResultatLyceeGeneralAPI.fromPandasRow(row)
        db_resultats = resultats.build_db_record(liste_uai)
        if db_resultats is None or len(db_resultats) == 0:
            continue
        liste_resultats.extend(db_resultats)

    # ========================================
    # Traitement des résultats du DNB
    # ========================================
    df = pd.read_parquet(dnb_pth)

    for index, row in rp.track(df.iterrows(), total=len(df), description="DNB"):
        resultat = ResultatBrevetAPI.fromPandasRow(row)
        db_resultat = resultat.build_db_record()
        if db_resultat is None or db_resultat.etablissement_uai not in liste_uai:
            continue
        liste_resultats.append(db_resultat)

    logger.info(f"{len(liste_resultats)} résultats chargés")

    return liste_etablissements, liste_resultats


def build_dataframes(
    etab_pth: Path, bacgt_pth: Path, dnb_pth: Path, destination_folder: Path
) -> T.Tuple[pd.DataFrame, pd.DataFrame]:
    # ========================================
    # Traitement des établissement
    # ========================================
    df = pd.read_parquet(etab_pth)

    liste_etablissements = []
    for index, row in rp.track(df.iterrows(), total=len(df), description="Annuaire"):
        etab = EtablissementAPI.fromPandasRow(row)
        db_etab = etab.build_dataframe_record()
        if db_etab is None:
            continue
        if db_etab["position"] is None:
            logger.warning(f"Unable to find position of {db_etab}")
            continue
        liste_etablissements.append(db_etab)

    df_etab = pd.DataFrame.from_records(liste_etablissements)
    df_etab.to_parquet(destination_folder / f"etablissements_{datetime.now():%Y-%m_%d}.parquet")

    logger.info(f"{len(liste_etablissements)} établissements chargés")
    liste_uai = [x["UAI"] for x in liste_etablissements]

    liste_resultats = []
    # ========================================
    # Traitement des résultats du BAC GT
    # ========================================
    df = pd.read_parquet(bacgt_pth)

    for index, row in rp.track(df.iterrows(), total=len(df), description="Bac GT"):
        resultats = ResultatLyceeGeneralAPI.fromPandasRow(row)
        db_resultats = resultats.build_dataframe_record(liste_uai)
        if db_resultats is None or len(db_resultats) == 0:
            continue
        liste_resultats.extend(db_resultats)

    # ========================================
    # Traitement des résultats du DNB
    # ========================================
    df = pd.read_parquet(dnb_pth)

    for index, row in rp.track(df.iterrows(), total=len(df), description="DNB"):
        resultat = ResultatBrevetAPI.fromPandasRow(row)
        db_resultat = resultat.build_dataframe_record()
        if db_resultat is None or db_resultat["etablissement_uai"] not in liste_uai:
            continue
        liste_resultats.append(db_resultat)

    df_res = pd.DataFrame.from_records(liste_resultats)
    df_res.to_parquet("data/resultats.parquet")

    logger.info(f"{len(liste_resultats)} résultats chargés")

    return df_etab, df_res
