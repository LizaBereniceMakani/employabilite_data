import requests
import json

SEARCH_URL = "https://www.apec.fr/cms/webservices/rechercheOffre"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/json"
}
payload = {
    "motsCles": "Data Scientist",
    "pagination": {"range": 10, "startIndex": 0},
    "activeFiltre": False
}

r = requests.post(SEARCH_URL, headers=HEADERS, json=payload)
data = r.json()

print(f"Total results: {len(data['resultats'])}")
for i, off in enumerate(data["resultats"][:10]):
    t = off.get("texteOffre") or ""
    d = off.get("descriptifPoste") or ""
    p = off.get("profilRecherche") or ""
    
    print(f"#{i} ID: {off['numeroOffre']} | T: {len(t)} | D: {len(d)} | P: {len(p)}")
    if len(d) > 0:
        print("   -> HAS DESC!")

