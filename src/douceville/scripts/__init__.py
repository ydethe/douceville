from pathlib import Path
import asyncio

from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert
import pandas as pd
import numpy as np
import typer
import rich.progress as rp
from asgiref.wsgi import WsgiToAsgi
from hypercorn.middleware import ProxyFixMiddleware
from hypercorn.asyncio import serve
from hypercorn.config import Config


app = typer.Typer()

import_app = typer.Typer()
app.add_typer(import_app, name="import", help="Manage parquet data in the app.")


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


@app.command()
def run():
    from .. import logger
    from ..app import app as flask_app

    asgi_app = WsgiToAsgi(flask_app)
    fixed_app = ProxyFixMiddleware(asgi_app, mode="legacy", trusted_hops=1)

    cfg = Config()
    cfg.bind = ["0.0.0.0:3566"]
    cfg.accesslog = logger
    cfg.errorlog = logger
    asyncio.run(serve(app=fixed_app, config=cfg, mode="asgi"))
    # 3566
