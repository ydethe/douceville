from pathlib import Path

from sqlalchemy import create_engine
import pandas as pd
import typer

from .. import config


app = typer.Typer()

import_app = typer.Typer()
app.add_typer(import_app, name="import", help="Manage parquet data in the app.")


@import_app.command()
def etab(path: Path):
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    df = pd.read_parquet(path)
    df.to_sql(name="etablissement", con=engine, if_exists="replace")


@import_app.command()
def resultats(path: Path):
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    df = pd.read_parquet(path)
    df.to_sql(name="resultat", con=engine, if_exists="replace")
