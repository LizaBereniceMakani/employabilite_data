import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print(f"CLIENT_ID loaded: {bool(CLIENT_ID)} (Length: {len(str(CLIENT_ID))})")
print(f"CLIENT_SECRET loaded: {bool(CLIENT_SECRET)} (Length: {len(str(CLIENT_SECRET))})")

TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"

data = {
    "grant_type": "client_credentials",
    "scope": "api_offresdemploiv2 o2dsoffre",
}

print(f"Testing Auth URL: {TOKEN_URL}")
try:
    r = requests.post(
        TOKEN_URL,
        data=data,
        auth=(CLIENT_ID, CLIENT_SECRET),
        timeout=10,
    )
    print(f"Status Code: {r.status_code}")
    token = r.json()["access_token"]
    
    # Test Search
    SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"motsCles": "Data Scientist", "range": "0-0"} # Juste 1 résultat
    
    print(f"Testing Search URL: {SEARCH_URL}")
    r2 = requests.get(SEARCH_URL, headers=headers, params=params)
    print(f"Search Status: {r2.status_code}")
    if r2.status_code == 206 or r2.status_code == 200:
        data = r2.json()
        if "resultats" in data and len(data["resultats"]) > 0:
            off = data["resultats"][0]
            print("KEYS:", off.keys())
            print(f"Description len: {len(off.get('description', ''))}")
            print("SAMPLE DESC:", off.get('description', '')[:100])
        else:
            print("No results found.")
    else:
        print(r2.text)
except Exception as e:
    print(f"Exception: {e}")
