import pandas as pd
import os

# Chargement
file_path = 'data/offres_enriched.csv'
if not os.path.exists(file_path):
    print("Fichier non trouvé.")
    exit()

df = pd.read_csv(file_path)
print(f"Total lignes: {len(df)}")

# Analyse par Source
if 'source' in df.columns:
    print("\n--- Répartition par Source ---")
    print(df['source'].value_counts())

# Analyse des Descriptions
print("\n--- Analyse des Descriptions ---")
# Compter les descriptions vides ou très courtes (< 20 chars)
df['desc_len'] = df['description'].fillna("").astype(str).str.len()
print(f"Descriptions vides ou < 20 chars: {len(df[df['desc_len'] < 20])} / {len(df)}")

# Croisement Source vs Description Vide
if 'source' in df.columns:
    print("\n--- Description Vide par Source ---")
    print(df[df['desc_len'] < 20]['source'].value_counts())

# Analyse des Skills
keywords = ['Python', 'SQL', 'R', 'Power BI']
print("\n--- Compte des Skills ---")
for k in keywords:
    if k in df.columns:
        count = df[k].sum()
        print(f"{k}: {count}")

# Echantillon de problème
print("\n--- Exemple de Description (Source APEC) ---")
# Prendre une offre APEC avec description mais sans Python (si possible)
sample = df[(df['source'] == 'APEC') & (df['desc_len'] > 100)]
if not sample.empty:
    print(f"Exemple APEC (Ligne {sample.index[0]}):")
    desc = sample.iloc[0]['description']
    print(desc[:300] + "...")
else:
    print("Pas d'offre APEC avec description trouvée.")
