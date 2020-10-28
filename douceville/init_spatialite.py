from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.sql import select, func

from douceville.config import DevConfig


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension(DevConfig.SQLITE_SPATIALITE_PATH)


engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI, echo=True)
listen(engine, "connect", load_spatialite)

conn = engine.connect()
conn.execute(select([func.InitSpatialMetaData()]))
conn.close()
