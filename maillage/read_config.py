import yaml


class Config:
    """Class whose attributes are the entries of the configuration file,
    with automatic conversion of arrays and matrix to np.array instances

    """

    def __init__(self, d: dict = {}, _default=True):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(
                    self,
                    a,
                    [
                        Config(x, _default=False) if isinstance(x, dict) else x
                        for x in b
                    ],
                )
            elif isinstance(b, dict):
                setattr(self, a, Config(b, _default=False))
            else:
                setattr(self, a, b)

        if _default:
            self.__default_sources()

    def __default_sources(self):
        if not hasattr(self, "sources"):
            self.sources = []

        n = len(self.sources)

        if not hasattr(self, "geoloc"):
            self.geoloc = None

        for i in range(n):
            if self.sources[i].diplome == "geoloc":
                continue

            src = self.sources[i]
            if not hasattr(src, "groupes"):
                self.sources[i].groupes = [src.diplome]

            if not hasattr(src, "inv_mention"):
                self.sources[i].inv_mention = False

            if not hasattr(src, "skiprows"):
                self.sources[i].skiprows = 0

    def __repr__(self):
        return str(self.__dict__)


def loadConfigV1(info):
    return info


def loadConfig(fic):
    f = open(fic, "r")
    info = Config(yaml.load(f, Loader=yaml.FullLoader))
    f.close()

    info.cfgfile = fic

    if info.ident.ver == 1:
        return loadConfigV1(info)
