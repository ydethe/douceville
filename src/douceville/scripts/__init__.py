from pathlib import Path

import sqlalchemy.engine
from sqlalchemy import create_engine
import pandas as pd
import typer

from .. import config


app = typer.Typer()

import_app = typer.Typer()
app.add_typer(import_app, name="import", help="Manage parquet data in the app.")


def upsert_df(df: pd.DataFrame, table_name: str, engine: sqlalchemy.engine.Engine):
    """Implements the equivalent of pd.DataFrame.to_sql(..., if_exists='update')
    (which does not exist). Creates or updates the db records based on the
    dataframe records.
    Conflicts to determine update are based on the dataframes index.
    This will set primary keys on the table equal to the index names
    1. Create a temp table from the dataframe
    2. Insert/update from temp table into table_name
    Returns: True if successful
    """

    temp_table_name = "temp_table"
    df.to_sql(temp_table_name, engine, index=True, if_exists="replace")

    index = list(df.index.names)
    index_sql_txt = ", ".join([f'"{i}"' for i in index])
    columns = list(df.columns)
    headers = index + columns
    headers_sql_txt = ", ".join(
        [f'"{i}"' for i in headers]
    )  # index1, index2, ..., column 1, col2, ...

    # col1 = exluded.col1, col2=excluded.col2
    update_column_stmt = ", ".join([f'"{col}" = EXCLUDED."{col}"' for col in columns])

    # Compose and execute upsert query
    query_upsert = f"""
    INSERT INTO "{table_name}" ({headers_sql_txt})
    SELECT {headers_sql_txt} FROM "{temp_table_name}"
    ON CONFLICT ({index_sql_txt}) DO UPDATE
    SET {update_column_stmt};
    """
    with engine.connect() as conn:
        conn.execute(query_upsert)
        conn.execute(f'DROP TABLE "{temp_table_name}"')


@import_app.command()
def etab(path: Path):
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    df = pd.read_parquet(path)

    upsert_df(df, table_name="etablissement", engine=engine)


@import_app.command()
def resultats(path: Path):
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    df = pd.read_parquet(path)
    df.to_sql(name="resultat", con=engine, if_exists="replace")
