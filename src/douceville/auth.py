from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAsync
from fief_client.integrations.fastapi import FiefAuth

from .config import config


fief = FiefAsync(
    "https://fief.johncloud.fr",
    config.FIEF_CLIENT_ID,
    config.FIEF_CLIENT_SECRET,
)

scheme = OAuth2AuthorizationCodeBearer(
    "https://fief.johncloud.fr/authorize",
    "https://fief.johncloud.fr/api/token",
    scopes={"openid": "openid", "offline_access": "offline_access"},
    auto_error=False,
)

# https://docs.fief.dev/integrate/python/fastapi/#checking-for-permissions
auth = FiefAuth(fief, scheme)
