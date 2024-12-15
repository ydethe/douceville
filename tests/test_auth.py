import requests


payload = "grant_type=client_credentials&client_id=bf773c0884b346f4be45aa191253c8f2&client_secret=WDXeDWlD74cz6Nf2MWdAucdpOi6cDQNEUz4VMKgyoW0iI9MZSxRS&audience=https%3A%2F%2Fjohncloud.kinde.com%2Fapi"
headers = {"content-type": "application/x-www-form-urlencoded"}

res = requests.post("https://johncloud.kinde.com/oauth2/token", data=payload, headers=headers)
token = res.json()

# ---------------------------------
headers = {"content-type": "application/json", "authorization": f"Bearer {token['access_token']}"}

res = requests.get("https://johncloud.kinde.com/api/v1/users", headers=headers)
print(res.text)
