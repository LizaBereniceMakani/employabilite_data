
import re
import time
import pandas as pd
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

BASE_URL = "https://www.welcometothejungle.com"
KEYWORDS = [
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "Intelligence Artificielle"
]
PAGES_PER_KEYWORD = 5  # 5 pages * 30 offres = 150 par mot clé -> Total ~750

# Mots-clés pour détecter le type de contrat dans le titre
CONTRATS = ['alternance', 'stage', 'cdi', 'cdd', 'freelance', 'alternant']

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

def parse_aria_label(aria_label):
    texte = aria_label.replace("Consultez l'offre ", "")
    if " | " in texte:
        parts = texte.split(" | ", 1)
        return parts[0].strip(), parts[1].strip()
    return texte.strip(), None

def detect_contrat(titre, contrat_aria):
    if contrat_aria:
        return contrat_aria
    titre_lower = titre.lower()
    for c in CONTRATS:
        if c in titre_lower:
            return c.capitalize()
    return "Non précisé"

def parse_entreprise(href):
    try:
        parties = href.split('/')
        if 'companies' in parties:
            idx = parties.index('companies')
            return parties[idx + 1].replace('-', ' ').title()
        return "N/A"
    except:
        return "N/A"

def parse_localisation(texte_carte):
    villes = [
        'Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Nantes',
        'Lille', 'Strasbourg', 'Rennes', 'Grenoble', 'Montpellier',
        'Nice', 'Sophia', 'Saclay', 'Puteaux', 'Boulogne', 'Levallois',
        'La Défense', 'Massy', 'Vélizy', 'Remote', 'Télétravail', 'France'
    ]
    for ville in villes:
        if ville.lower() in texte_carte.lower():
            return ville
    return "France"

def scrape_listing_page(driver, page, keyword):
    """Récupère les infos de base + liens d'une page de recherche."""
    # Encodage manuel simple pour l'URL
    kw_url = keyword.replace(" ", "+")
    url = f"{BASE_URL}/fr/jobs?query={kw_url}&aroundQuery=France&page={page}"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'li[data-testid="search-results-list-item-wrapper"]')
            )
        )
    except:
        print(f"    Page {page}: timeout ou vide")
        return []

    time.sleep(2) # Chargement JS

    cartes = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="search-results-list-item-wrapper"]')
    print(f"    Page {page}: {len(cartes)} offres trouvées")

    offres_page = []
    for carte in cartes:
        try:
            lien_el = carte.find_element(By.CSS_SELECTOR, 'a[aria-label]')
            aria_label = lien_el.get_attribute('aria-label')
            href = lien_el.get_attribute('href')

            titre, contrat_aria = parse_aria_label(aria_label)
            contrat = detect_contrat(titre, contrat_aria)
            entreprise = parse_entreprise(href)
            localisation = parse_localisation(carte.text)

            offres_page.append({
                'titre': titre,
                'entreprise': entreprise,
                'contrat': contrat,
                'localisation': localisation,
                'lien': href,
                'date_scraping': datetime.now().strftime('%Y-%m-%d'),
                'mot_cle_recherche': keyword,
                'source': 'WTTJ'
            })
        except:
            continue
    return offres_page

def scrape_job_details(driver, url):
    """Visite une page d'offre pour récupérer la description."""
    try:
        driver.get(url)
        # Attente d'un élément de contenu (le main ou une section de description)
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )
        time.sleep(1) # Rendu final

        # Essayer de récupérer le texte principal
        # WTTJ change souvent ses classes, le tag main est le plus sûr pour le contenu global
        main_content = driver.find_element(By.TAG_NAME, "main")
        text = main_content.text
        return text
    except Exception as e:
        # print(f"Erreur description: {e}") 
        return ""

def main():
    driver = init_driver()
    all_results = []
    seen_links = set()

    print("Démarrage du scraping WTTJ complet...")

    try:
        # 1. Récupération de tous les liens (Phase Listing)
        for kw in KEYWORDS:
            print(f"\n--- Recherche: {kw} ---")
            for page in range(1, PAGES_PER_KEYWORD + 1):
                offres = scrape_listing_page(driver, page, kw)
                if not offres:
                    break
                
                # Ajout seulement si pas déjà vu (dédoublonnage immédiat)
                for off in offres:
                    if off['lien'] not in seen_links:
                        seen_links.add(off['lien'])
                        all_results.append(off)
                
                time.sleep(random.uniform(2, 4))
        
        print(f"\nPhase 1 terminée: {len(all_results)} offres uniques trouvées.")
        
        # Sauvegarde intermédiaire des listings (au cas où)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        pd.DataFrame(all_results).to_csv(os.path.join(data_dir, "offres_wttj_listings_only.csv"), index=False, encoding='utf-8-sig')
        print("Sauvegarde intermédiaire: offres_wttj_listings_only.csv")

        print("Démarrage de la Phase 2: Récupération des descriptions...")
        
        output_path = os.path.join(data_dir, "offres_wttj_raw.csv")
        # Initialiser le fichier final avec headers
        if not os.path.exists(output_path):
            pd.DataFrame(columns=[
                "titre", "entreprise", "contrat", "localisation", "lien", 
                "date_scraping", "source", "mot_cle_recherche", "description"
            ]).to_csv(output_path, index=False, encoding="utf-8-sig")

        # 2. Récupération des détails (Phase Détail)
        for i, offre in enumerate(all_results):
            if i % 5 == 0:
                print(f"  Traitement offre {i}/{len(all_results)}...")
            
            desc = scrape_job_details(driver, offre['lien'])
            offre['description'] = desc
            
            # Sauvegarde incrémentale
            df_one = pd.DataFrame([offre])
            df_one.to_csv(output_path, mode='a', header=False, index=False, encoding='utf-8-sig')

            # Délai respectueux (augmenté pour éviter blocage)
            time.sleep(random.uniform(2.0, 5.0))

    finally:
        driver.quit()

    print(f"Scraping terminé. Données sauvegardées dans {output_path}")

if __name__ == "__main__":
    main()
