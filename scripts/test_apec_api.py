import requests
import json

SEARCH_URL = "https://www.apec.fr/cms/webservices/rechercheOffre"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/json"
}

payload = {
    "motsCles": "Data Scientist",
    "pagination": {"range": 1, "startIndex": 0},
    "activeFiltre": False
}

try:
    print("Envoi requête API APEC...")
    r = requests.post(SEARCH_URL, headers=HEADERS, json=payload, timeout=10)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        if "resultats" in data and len(data["resultats"]) > 0:
            offre = data["resultats"][0]
            print("\n--- CLES DISPONIBLES ET LONGEURS ---")
            for k in offre.keys():
                val = str(offre[k])
                print(f"{k}: {len(val)}")
                
            print("\n--- CONTENU TEST ---")
            print(f"Propriété 'texteOffre': {len(str(offre.get('texteOffre')))}")
            print(f"Propriété 'descriptifPoste': {len(str(offre.get('descriptifPoste')))}")
            print(f"Propriété 'profilRecherche': {len(str(offre.get('profilRecherche')))}")
        else:
            print("Pas de résultats.")
    else:
        print(r.text)

except Exception as e:
    print(e)
