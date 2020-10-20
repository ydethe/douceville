import pickle
import argparse
import os

from sqlalchemy import create_engine, inspect, or_
from sqlalchemy.orm import sessionmaker

import pandas as pd
import tqdm

import maillage
from maillage.models import Etablissement, Resultat
from maillage.conv_utils import *
from maillage.config import Config
from maillage.conv_rdf import import_geoloc_db
from maillage.read_config import loadConfig


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

session = sessionmaker()
session.configure(bind=engine)
s = session()

s.query(Resultat).delete()
s.query(Etablissement).delete()

s.commit()
