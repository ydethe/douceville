from pathlib import Path
from typing_extensions import Annotated

from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
import pandas as pd
import numpy as np
import typer
import rich.progress as rp

from ..auth import create_access_token, check_token as auth_check_token
from .. import logger
from ..config import config


app = typer.Typer()

import_app = typer.Typer()
app.add_typer(import_app, name="import", help="Manage parquet data in the app.")

token_app = typer.Typer()
app.add_typer(token_app, name="token", help="Manage tokens.")


def upsert_df(df: pd.DataFrame, primary_key: str, table, connection: Connection):
    nb_rows = len(df)
    for index, row in rp.track(df.iterrows(), total=nb_rows):
        rec = row.to_dict()
        rec.pop("latitude", None)
        rec.pop("longitude", None)
        rec.pop("import_status", None)
        lk = list(rec.keys())
        for k in lk:
            if isinstance(rec[k], float) and np.isnan(rec[k]):
                rec[k] = -1
        insert_stmt = insert(table).values(rec)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[primary_key],
            set_={c.key: c for c in insert_stmt.excluded if c.key not in [primary_key]},
        )
        connection.execute(upsert_stmt)


@import_app.command()
def etab(path: Path):
    from ..schemas import Etablissement, get_engine

    engine = get_engine()
    df = pd.read_parquet(path)

    with engine.connect() as conn:
        upsert_df(df, primary_key="UAI", table=Etablissement, connection=conn)
        conn.commit()


@import_app.command()
def resultats(path: Path):
    from ..schemas import Resultat, get_engine

    engine = get_engine()
    df = pd.read_parquet(path)

    with engine.connect() as conn:
        upsert_df(df, primary_key="idx", table=Resultat, connection=conn)
        conn.commit()


@token_app.command(name="create")
def create_token(
    email: Annotated[str, typer.Argument(help="Email of a user")] = None,
    password: Annotated[str, typer.Argument(help="Password of a user")] = None,
):
    if email is None or password is None:
        email = config.SUPABASE_TEST_USER
        password = config.SUPABASE_TEST_PASSWORD

    token = create_access_token(config.SUPABASE_URL, config.SUPABASE_KEY, email, password)

    logger.info(f"Created token for user '{email}'")
    print(token)


@token_app.command(name="check")
def check_token(token: Annotated[str, typer.Argument(help="Token to check")]):
    user = auth_check_token(
        token, config.SUPABASE_JWT_SECRET, config.SUPABASE_URL, config.SUPABASE_ADMIN_KEY
    )

    logger.info(f"Checked token for user : '{user}'")
