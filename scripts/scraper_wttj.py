import re
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.welcometothejungle.com"
SEARCH_URL = f"{BASE_URL}/fr/jobs?query=data+scientist&aroundQuery=France"

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
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


def parse_aria_label(aria_label):
    texte = aria_label.replace("Consultez l'offre ", "")
    if " | " in texte:
        titre, contrat = texte.split(" | ", 1)
        return titre.strip(), contrat.strip()
    return texte.strip(), None


def detect_contrat(titre, contrat_aria):
    # Si on a déjà trouvé le contrat via aria-label, on le garde
    if contrat_aria:
        return contrat_aria
    # Sinon on cherche dans le titre
    titre_lower = titre.lower()
    for c in CONTRATS:
        if c in titre_lower:
            return c.capitalize()
    return "Non précisé"


def parse_entreprise(href):
    try:
        parties = href.split('/')
        idx = parties.index('companies')
        return parties[idx + 1].replace('-', ' ').title()
    except:
        return "N/A"


def parse_localisation(texte_carte):
    # Les villes françaises connues à chercher dans le texte
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


def scrape_page(driver, page):
    url = f"{SEARCH_URL}&page={page}"
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'li[data-testid="search-results-list-item-wrapper"]')
            )
        )
    except:
        print(f"page {page}: timeout")

    time.sleep(2)

    cartes = driver.find_elements(
        By.CSS_SELECTOR,
        'li[data-testid="search-results-list-item-wrapper"]'
    )
    print(f"page {page}: {len(cartes)} offres")

    offres = []
    for carte in cartes:
        try:
            lien_el = carte.find_element(By.CSS_SELECTOR, 'a[aria-label]')
            aria_label = lien_el.get_attribute('aria-label')
            href = lien_el.get_attribute('href')

            titre, contrat_aria = parse_aria_label(aria_label)
            contrat = detect_contrat(titre, contrat_aria)
            entreprise = parse_entreprise(href)
            localisation = parse_localisation(carte.text)

            offres.append({
                'titre': titre,
                'entreprise': entreprise,
                'contrat': contrat,
                'localisation': localisation,
                'lien': href or 'N/A',
                'date_scraping': datetime.now().strftime('%Y-%m-%d')
            })
        except:
            continue

    return offres


def main():
    driver = init_driver()
    resultats = []

    try:
        for page in range(1, 6):
            offres = scrape_page(driver, page)
            resultats.extend(offres)
            time.sleep(3)
    finally:
        driver.quit()

    if not resultats:
        print("aucune offre recuperee")
        return

    df = pd.DataFrame(resultats)
    df = df.drop_duplicates(subset=['lien'])
    print(f"total: {len(df)} offres uniques")

    df.to_csv('../data/offres_data_science_raw.csv', index=False, encoding='utf-8-sig')
    print("sauvegarde: ../data/offres_data_science_raw.csv")
    print(df[['titre', 'entreprise', 'contrat', 'localisation']].head(10).to_string())


if __name__ == "__main__":
    main()