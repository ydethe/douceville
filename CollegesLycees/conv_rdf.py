import json
import pickle
from collections import defaultdict

import tqdm
from rdflib import Graph


def create_cache():
    g = Graph()
    g.parse("dataset-564055.ttl",format="n3")

    raw = g.serialize(format="json-ld").decode("utf-8")

    info = json.loads(raw)
        
    pickle.dump(info, open('data_dict.raw', 'wb'))
    
def import_geoloc_db():
    info = pickle.loads(open('data_dict.raw','rb').read())
        
    db = {}
    for rec in tqdm.tqdm(info):
        if not '@id' in rec.keys():
            continue

        uai = rec['@id'].split('/')[-1].upper()
        dat = {}
        if '/geometry/' in rec['@id']:
            lon = rec['http://data.ign.fr/ontologies/geometrie#coordX'][0]['@value']
            lat = rec['http://data.ign.fr/ontologies/geometrie#coordY'][0]['@value']
            
            dat['latitude'] = lat
            dat['longitude'] = lon

        elif 'http://purl.org/dc/terms/title' in rec.keys():
            nom = rec['http://purl.org/dc/terms/title'][0]['@value']
            dat['nom'] = nom
        
        elif "http://data.eurecom.fr/ontologies/ecole#denominationPrincipale" in rec.keys():
            denom = rec["http://data.eurecom.fr/ontologies/ecole#denominationPrincipale"][0]['@value']
            dat['denomination'] = denom
        
        if dat != {}:
            dat['UAI'] = uai
            db[uai] = dat
            
    db['0312843X'] = {'UAI':'0312843X', 'longitude':1.398089, 'latitude':43.464582}
    db['0312868Z'] = {'UAI':'0312868Z', 'longitude':1.249387, 'latitude':43.348657}
    db['0312842W'] = {'UAI':'0312842W', 'longitude':1.373549, 'latitude':43.750734}
    db['0311842J'] = {'UAI':'0311842J', 'longitude':1.579625, 'latitude':43.728851}
    db['0312354R'] = {'UAI':'0312354R', 'longitude':1.320462, 'latitude':43.780609}
    db['0311270M'] = {'UAI':'0311270M', 'longitude':1.522781, 'latitude':43.537348}
    db['0311843K'] = {'UAI':'0311843K', 'longitude':1.120444, 'latitude':43.413620}
    db['0311268K'] = {'UAI':'0311268K', 'longitude':0.730726, 'latitude':43.117691}
        
    return db
    
if __name__ == '__main__':
    create_cache()


