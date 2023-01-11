import logging
from functools import wraps
from cryptography.fernet import Fernet
import json

from douceville.config import Config


class Serializer(object):
    """

    Examples:
    >>> s = Serializer()
    >>> d = {'a':0, 'b':3}
    >>> token = s.serialize(d)
    >>> token
    >>> d2 = s.deserialize(token)
    >>> d2

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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
