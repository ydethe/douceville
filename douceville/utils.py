import logging
from functools import wraps


def logged(fct):
    log = logging.getLogger("douceville_logger")

    @wraps(fct)
    def wrapper(*args, **kwds):
        kwds["logger"] = log
        return fct(*args, **kwds)

    return wrapper
