import logging
from functools import wraps
from cryptography.fernet import Fernet
import json
import requests

from flask import url_for

from douceville.config import Config


class Serializer(object):
    """

    Examples:
    >>> s = Serializer()
    >>> d = {'a':0, 'b':3}
    >>> token = s.serialize(d)
    >>> d2 = s.deserialize(token)
    >>> str(d2)
    "{'a': 0, 'b': 3}"

    """

    def __init__(self):
        self.fernet = Fernet(Config.SECRET_KEY)

    def serialize(self, d):
        j = json.dumps(d).encode()
        token = self.fernet.encrypt(j)
        return token.decode()

    def deserialize(self, s, ttl=30):
        j = self.fernet.decrypt(s.encode(), ttl=ttl)
        d = json.loads(j)
        return d


def logged(fct):
    log = logging.getLogger("douceville_logger")

    @wraps(fct)
    def wrapper(*args, **kwds):
        kwds["logger"] = log
        return fct(*args, **kwds)

    return wrapper

def api_call(fct, key, **kwargs):
    '''

    Examples:
    ---------
    >>> res = api_call('query', "gAAAAABfuV6-MIILJzGxg0NhBulhyxDGUjZ_L_hW-3Gg5ME_NZkYxaPpCVj6cK3gBGUwVWR5rH-tfpz5Bzh1fRP97NVtn8UJ5O3q73glQ6FiPDd8ZPQzOGkvud5RU10hFbmpTdstJswE", nature='college',adresse='toulouse',distance=600)
    >>> res.keys()
    dict_keys(['etablissements', 'isochrone'])
    
    '''
    url = "%s/%s" % (Config.DOUCEVILLE_API_URL, fct)
    
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer %s" % key,
    }
    r = requests.get(url, params=kwargs, headers=headers)
    return r.json()

if __name__ == "__main__":
    import doctest

    doctest.testmod()
