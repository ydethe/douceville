from datetime import datetime
import typing as T
from dataclasses import dataclass

import rich.progress as rp
import pandas as pd
import numpy as np

from .models import Etablissement, Resultat
from .scripts.import_etablissements import findEtabPosition


@dataclass
class ResultatBrevetAPI:
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

    def build_db_record(self) -> T.List[Resultat]:
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

            res = Resultat(
                diplome=f"Baccalauréat {d.upper()}",
                annee=int(self.annee.year),
                presents=effectif,
                admis=taux_reu,
                mentions=taux_men,
                etablissement_uai=self.uai,
            )
            records.append(res)
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
        return nom

    def build_db_record(self) -> Etablissement:

        etab_dict = {}
        etab_dict["nom"] = self.nom
        etab_dict["adresse"] = self.adresse_uai
        etab_dict["code_postal"] = self.code_postal_uai
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

        etab_dict = findEtabPosition(etab_dict.copy())

        etab_dict["UAI"] = self.numero_uai
        etab_dict["lieu_dit"] = self.lieu_dit_uai.title()
        etab_dict["academie"] = self.libelle_academie.title()
        etab_dict["secteur"] = self.secteur_public_prive_libe.lower().replace("e", "é")
        etab_dict["ouverture"] = self.date_ouverture

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


def build_db_records():
    from . import logger

    # ========================================
    # Traitement des établissement
    # ========================================
    # df = pd.read_parquet(
    #     "fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre.parquet"
    # )

    # records = []
    # for index, row in rp.track(df.iterrows(),total=len(df)):
    #     etab = EtablissementAPI.fromPandasRow(row)
    #     db_etab = etab.build_db_record()
    #     if db_etab is None:
    #         continue
    #     records.append(db_etab)

    # logger.info(f"{len(records)} établissements chargés")

    # ========================================
    # Traitement des résultats du BAC
    # ========================================
    df = pd.read_parquet("fr-en-indicateurs-de-resultat-des-lycees-gt_v2.parquet")
    print(df["presents_s"])
    records = []
    for index, row in rp.track(df.iterrows(), total=len(df)):
        etab = ResultatLyceeGeneralAPI.fromPandasRow(row)
        db_etab = etab.build_db_record()
        if db_etab is None or len(db_etab) == 0:
            continue
        records.extend(db_etab)

    logger.info(f"{len(records)} résultats pour le BAC chargés")
