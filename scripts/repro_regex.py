import pandas as pd
import re

# Simulation du reading
csv_content = """titre,entreprise,contrat,localisation,salaire,description,lien,date_scraping,source,mot_cle_recherche
Data Scientist,iPepper,CDI,Paris,50k,"Rechercher une offre
Data Scientist
Descriptif du poste
Contexte
Nous recherchons un Data Scientist...
Compétences techniques
.Langages et bibliothèques
.Python (obligatoire)
.Pandas, NumPy, Scikit-learn
.TensorFlow",http://lien,2026-02-10,APEC,Data
"""

from io import StringIO
df = pd.read_csv(StringIO(csv_content))
desc = df.iloc[0]['description']
print(f"Description loaded: {len(desc)} chars")
print(f"Content snippet: {desc[30:100]}")

keywords = {
    "Python": [r"python"],
    "SQL": [r"sql"]
}

print("\n--- Testing Regex ---")
text_lower = desc.lower()
for k, patterns in keywords.items():
    found = False
    for pat in patterns:
        if re.search(pat, text_lower):
            found = True
            print(f"MATCH: {k} found with pattern '{pat}'")
            break
    if not found:
        print(f"FAIL: {k} NOT found")
