import json
import pickle

from rdflib import Graph


g = Graph()
g.parse("dataset-564055.ttl",format="n3")

raw = g.serialize(format="json-ld").decode("utf-8")

dat = json.loads(raw)

pickle.dump(dat, open('data_dict.raw', 'wb'))
