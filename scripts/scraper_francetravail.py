import os
import time
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Configuration OAuth
TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
API_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
SCOPE = "api_offresdemploiv2 o2dsoffre"

# Configuration Scraping
KEYWORDS = [
    "Data Scientist", "Data Analyst", "Data Engineer", 
    "Machine Learning", "Business Intelligence", "Big Data",
    "Intelligence Artificielle"
]
PAGE_SIZE = 100 # Max range is often 150
MAX_OFFERS_PER_KEYWORD = 300 # On vise ~2000 total

TIMEOUT = 15

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError("CLIENT_ID ou CLIENT_SECRET manquant dans le fichier .env")


def get_token():
    print("Authentification France Travail...")
    data = {"grant_type": "client_credentials", "scope": SCOPE}
    try:
        r = requests.post(
            TOKEN_URL,
            data=data,
            auth=(CLIENT_ID, CLIENT_SECRET),
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()["access_token"]
    except requests.exceptions.HTTPError as e:
        print(f"Erreur Auth: {e}")
        print(r.text)
        raise

def get_offres(token, keyword, start, end):
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "motsCles": keyword,
        "range": f"{start}-{end}",
    }
    try:
        r = requests.get(API_URL, headers=headers, params=params, timeout=TIMEOUT)
        if r.status_code == 200 or r.status_code == 206:
            return r.json().get("resultats", [])
        elif r.status_code == 204:
            return []
        else:
            print(f"  Erreur API {r.status_code}: {r.text[:200]}")
            return []
    except Exception as e:
        print(f"  Exception req: {e}")
        return []

def parse_offre(o):
    return {
        "titre": o.get("intitule"),
        "entreprise": o.get("entreprise", {}).get("nom"),
        "contrat": o.get("typeContrat"),
        "localisation": o.get("lieuTravail", {}).get("libelle"),
        "salaire": o.get("salaire", {}).get("libelle"),
        "description": o.get("description"), # Le champ clé !
        "lien": o.get("origineOffre", {}).get("urlOrigine"),
        "date_publication": o.get("dateCreation", "")[:10],
        "date_scraping": datetime.now().strftime("%Y-%m-%d"),
        "source": "France Travail",
    }

def main():
    try:
        token = get_token()
    except:
        return

    all_offers = []
    seen_ids = set()

    for kw in KEYWORDS:
        print(f"--- Recherche: {kw} ---")
        current_count = 0
        
        # Pagination
        for start in range(0, MAX_OFFERS_PER_KEYWORD, PAGE_SIZE):
            end = start + PAGE_SIZE - 1
            print(f"  Page {start}-{end}...")
            
            results = get_offres(token, kw, start, end)
            
            if not results:
                print("  Fin des résultats.")
                break
                
            new_in_page = 0
            for off in results:
                off_id = off.get("id")
                if off_id and off_id not in seen_ids:
                    seen_ids.add(off_id)
                    all_offers.append(parse_offre(off))
                    new_in_page += 1
            
            print(f"  + {new_in_page} nouvelles offres.")
            current_count += len(results)
            
            if len(results) < PAGE_SIZE:
                break
                
            time.sleep(1) # Poil de politesse

    print(f"Total offres récupérées : {len(all_offers)}")

    if all_offers:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        
        output = os.path.join(data_dir, "offres_francetravail_raw.csv")
        
        df = pd.DataFrame(all_offers)
        # Si fichier existe, on peut merger ou écraser. Ici on écrase pour repartir propre
        df.to_csv(output, index=False, encoding="utf-8-sig")
        print(f"Sauvegarde dans {output}")
    else:
        print("Aucune offre trouvée.")

if __name__ == "__main__":
    main()