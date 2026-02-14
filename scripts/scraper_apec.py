
import requests
import pandas as pd
from datetime import datetime
import time
import random
import os
import re

# Configuration
KEYWORDS = [
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "Intelligence Artificielle",
    "Business Intelligence",
    "Data Steward"
]
NUM_PAGES_PER_KEYWORD = 40  # 40 * 20 = 800 offres potentielles par mot clé
SEARCH_URL = "https://www.apec.fr/cms/webservices/rechercheOffre"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.apec.fr"
}

def clean_html(raw_html):
    if not isinstance(raw_html, str):
        return ""
    # Enlever balises HTML
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    # Nettoyer espaces
    cleantext = re.sub(r'\s+', ' ', cleantext).strip()
    return cleantext

def get_apec_offers():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    output_final = os.path.join(data_dir, "offres_apec_raw.csv")

    all_offers = []
    seen_ids = set()
    
    print(f"--- Démarrage du Scraping API APEC (Cible: {len(KEYWORDS)*NUM_PAGES_PER_KEYWORD*20} offres max) ---")
    
    for kw in KEYWORDS:
        print(f"\nRecherche: {kw}")
        empty_pages_consecutive = 0
        
        for page in range(NUM_PAGES_PER_KEYWORD):
            if empty_pages_consecutive > 2:
                print("  -> Fin des résultats pour ce mot clé.")
                break
                
            try:
                payload = {
                    "motsCles": kw,
                    "pagination": {"range": 20, "startIndex": page * 20},
                    "activeFiltre": False
                }
                
                # Délai aléatoire pour être gentil (même si c'est une API publique)
                time.sleep(random.uniform(0.5, 1.5))
                
                r = requests.post(SEARCH_URL, headers=HEADERS, json=payload, timeout=15)
                
                if r.status_code == 200:
                    data = r.json()
                    if "resultats" in data and len(data["resultats"]) > 0:
                        empty_pages_consecutive = 0
                        new_count = 0
                        
                        for off in data["resultats"]:
                            if off['numeroOffre'] not in seen_ids:
                                seen_ids.add(off['numeroOffre'])
                                new_count += 1
                                
                                # Extraction Description (Concatenation pour max d'infos)
                                part1 = off.get("texteOffre") or ""
                                part2 = off.get("descriptifPoste") or ""
                                part3 = off.get("profilRecherche") or ""
                                # On assemble tout pour être sûr de ne rien rater
                                desc_html = f"{part1} {part2} {part3}"
                                
                                description_clean = clean_html(desc_html)
                                
                                # Formatage
                                mapped = {
                                    "titre": off.get("intituleSurbrillance") or off.get("intitule"),
                                    "entreprise": off.get("nomCommercial"),
                                    "contrat": off.get("typeContratLibelle"),
                                    "localisation": off.get("lieuTravailLibelle"),
                                    "salaire": off.get("salaireTexte"),
                                    "description": description_clean,
                                    "lien": f"https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/{off['numeroOffre']}",
                                    "date_scraping": datetime.now().strftime("%Y-%m-%d"),
                                    "source": "APEC",
                                    "mot_cle_recherche": kw,
                                    "id_apec": off['numeroOffre']
                                }
                                all_offers.append(mapped)
                        
                        print(f"  Page {page+1}: +{new_count} nouvelles offres (Total unique: {len(all_offers)})")
                    else:
                        empty_pages_consecutive += 1
                else:
                    print(f"  Erreur API Page {page+1}: {r.status_code}")
                    break
                    
            except Exception as e:
                print(f"  Exception Page {page+1}: {e}")
                time.sleep(2)
                
    # Sauvegarde finale
    print(f"\n--- Sauvegarde de {len(all_offers)} offres dans {output_final} ---")
    df = pd.DataFrame(all_offers)
    
    # Colonnes finales
    cols = ["titre", "entreprise", "contrat", "localisation", "salaire", "description", "lien", "date_scraping", "source", "mot_cle_recherche"]
    # Garanti que toutes les cols existent
    for c in cols:
        if c not in df.columns:
            df[c] = ""
            
    df = df[cols]
    df.to_csv(output_final, index=False, encoding="utf-8-sig")
    print("Terminé.")

if __name__ == "__main__":
    get_apec_offers()
