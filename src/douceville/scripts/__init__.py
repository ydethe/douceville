from pathlib import Path

from sqlalchemy.dialects.postgresql import insert
import pandas as pd
import typer
import rich.progress as rp


app = typer.Typer()

import_app = typer.Typer()
app.add_typer(import_app, name="import", help="Manage parquet data in the app.")


def upsert_df(df: pd.DataFrame, primary_key: str, table, connection):
    nb_rows = len(df)
    for index, row in rp.track(df.iterrows(), total=nb_rows):
        rec = row.to_dict()
        rec.pop("latitude", None)
        rec.pop("longitude", None)
        rec.pop("import_status", None)
        insert_stmt = insert(table).values(rec)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[primary_key],
            set_={c.key: c for c in insert_stmt.excluded if c.key not in [primary_key]},
        )
        connection.execute(upsert_stmt)


@import_app.command()
def etab(path: Path):
    from ..models import Etablissement, get_engine

    engine = get_engine()
    df = pd.read_parquet(path)

    with engine.connect() as conn:
        upsert_df(df, primary_key="UAI", table=Etablissement, connection=conn)
        conn.commit()


@import_app.command()
def resultats(path: Path):
    from ..models import Resultat, get_engine

    engine = get_engine()
    df = pd.read_parquet(path)

    with engine.connect() as conn:
        upsert_df(df, primary_key="idx", table=Resultat, connection=conn)
        conn.commit()
