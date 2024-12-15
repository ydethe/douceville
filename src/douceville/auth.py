from fastapi import HTTPException, status, Request
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType
from kinde_sdk import Configuration

from .config import config


# https://pypi.org/project/auth0_fastapi/
# https://stytch.com/dashboard/user-management?env=test

# Initialize Kinde client with configuration
configuration = Configuration(host=config.KINDE_ISSUER_URL)
kinde_api_client_params = {
    "configuration": configuration,
    "domain": config.KINDE_ISSUER_URL,
    "client_id": config.CLIENT_ID,
    "client_secret": config.CLIENT_SECRET,
    "grant_type": config.GRANT_TYPE,
    "callback_url": config.KINDE_CALLBACK_URL,
}
if config.GRANT_TYPE == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = config.CODE_VERIFIER


# User clients dictionary to store Kinde clients for each user
user_clients = {}

# Dependency to get the current user's KindeApiClient instance
def get_kinde_client(request: Request) -> KindeApiClient:
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    if user_id not in user_clients:
        # If the client does not exist, create a new instance
        user_clients[user_id] = KindeApiClient()

    kinde_client = user_clients[user_id]
    # Ensure the client is authenticated
    if not kinde_client.is_authenticated():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    return kinde_client
