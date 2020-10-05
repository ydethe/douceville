import sqlite3

import pandas as pd


conn = sqlite3.connect('etablissements.db', isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT * FROM etablissement", conn)
db_df.to_csv('database.csv', index=False)

