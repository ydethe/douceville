from collections import defaultdict

import yaml


class Config:
    """Class whose attributes are the entries of the configuration file,
    with automatic conversion of arrays and matrix to np.array instances

    """

    def __init__(self, d: dict = {}):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(
                    self,
                    a,
                    [Config(x) if isinstance(x, dict) else x for x in b],
                )
            elif isinstance(b, dict):
                setattr(self, a, Config(b))
            else:
                setattr(self, a, b)

    def __repr__(self):
        return str(self.__dict__)


def loadConfigV1(info):
    if not hasattr(info, "sources"):
        info.sources = []

    n = len(info.sources)

    if not hasattr(info, "geoloc"):
        info.geoloc = None

    if not hasattr(info, "geoloc2"):
        info.geoloc2 = None

    for i in range(n):
        src = info.sources[i]
        if not hasattr(src, "groupes"):
            info.sources[i].groupes = [src.diplome]

        if not hasattr(src, "inv_mention"):
            info.sources[i].inv_mention = False

        if not hasattr(src, "skiprows"):
            info.sources[i].skiprows = 0

    return info


def loadConfigV2(info):
    info = loadConfigV1(info)

    opts = defaultdict(lambda: None)
    if not info.options is None:
        for opt in info.options:
            opts.update(opt.__dict__)

    info.options = opts

    return info


def loadConfig(fic):
    f = open(fic, "r")
    info = Config(yaml.load(f, Loader=yaml.FullLoader))
    f.close()

    info.cfgfile = fic

    if info.ident.ver == 1:
        return loadConfigV1(info)
    elif info.ident.ver == 2:
        return loadConfigV2(info)
