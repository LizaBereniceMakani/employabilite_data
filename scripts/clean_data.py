import pandas as pd
import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, "data", "offres_raw_merged.csv")
output_path = os.path.join(base_dir, "data", "offres_clean.csv")

df = pd.read_csv(input_path)
print(f"avant nettoyage: {len(df)} lignes")


# 1. Supprimer les vrais doublons
df = df.drop_duplicates(subset=['titre', 'entreprise'])
print(f"apres deduplication: {len(df)} lignes")


# 2. Nettoyer les valeurs manquantes
df['entreprise'] = df['entreprise'].fillna('Confidentiel')
df['localisation'] = df['localisation'].fillna('France')
df['contrat'] = df['contrat'].fillna('Non précisé')
df['titre'] = df['titre'].fillna('N/A')


# 3. Standardiser les types de contrat
def standardise_contrat(c):
    if pd.isna(c):
        return 'Non précisé'
    c = str(c).lower().strip()
    
    # Mapping APEC codes
    if '101888' in c: return 'CDI'
    if '101887' in c: return 'CDD'
    if '597137' in c: return 'Intérim/Mission'
    if '597141' in c: return 'Alternance' # Possible code
    
    if 'alternance' in c or 'alternant' in c or 'alter' in c or 'appr' in c:
        return 'Alternance'
    if 'stage' in c or 'intern' in c:
        return 'Stage'
    if 'cdi' in c or 'durée indéterminée' in c:
        return 'CDI'
    if 'cdd' in c or 'durée déterminée' in c:
        return 'CDD'
    if 'freelance' in c or 'indep' in c:
        return 'Freelance'
    if 'vie' in c:
        return 'VIE'
    return 'Non précisé'

df['contrat'] = df['contrat'].apply(standardise_contrat)


# 4 & 5. Region avec Départements
def get_region(loc):
    if pd.isna(loc):
        return 'Autre'
    loc = str(loc).lower()
    
    # 1. Ile-de-France (Nettoyage plus large)
    idf_keys = [
        'paris', 'boulogne', 'levallois', 'puteaux', 'massy', 'vélizy', 'saclay', 
        'versailles', 'saint-cloud', 'neuilly', 'issy', 'montrouge', 'courbevoie', 
        'nanterre', 'défense', 'suresnes', 'rueil', 'clichy', 'ivry', 'pantin',
        'saint-denis', 'bagneux', 'fontenay', 'vincennes', 'creteil', 'cergy'
    ]
    if any(k in loc for k in idf_keys): return 'Île-de-France'
    if re.search(r'\b(75|92|93|94|91|95|77|78)\d{0,3}\b', loc): return 'Île-de-France'

    # 2. Grandes métropoles
    if 'lyon' in loc or 'villeurbanne' in loc or '69' in loc: return 'Auvergne-Rhône-Alpes'
    if 'marseille' in loc or 'aix' in loc or 'sophia' in loc or 'nice' in loc or '06' in loc or '13' in loc: return 'PACA'
    if 'bordeaux' in loc or 'merignac' in loc or 'pessac' in loc or '33' in loc: return 'Nouvelle-Aquitaine'
    if 'toulouse' in loc or 'blagnac' in loc or '31' in loc: return 'Occitanie'
    if 'nantes' in loc or '44' in loc: return 'Pays de la Loire'
    if 'rennes' in loc or '35' in loc: return 'Bretagne'
    if 'lille' in loc or 'villeneuve' in loc or '59' in loc: return 'Hauts-de-France'
    if 'strasbourg' in loc or '67' in loc: return 'Grand Est'
    if 'montpellier' in loc or '34' in loc: return 'Occitanie'
    if 'grenoble' in loc or '38' in loc: return 'Auvergne-Rhône-Alpes'
    
    # 3. Cas APEC "France"
    if loc.strip() == 'france':
        return 'France Entière (Non précisé)'
        
    if 'télétravail' in loc or 'remote' in loc:
        return 'Télétravail'
        
    return 'Autre'

df['region'] = df['localisation'].apply(get_region)

# Clean localisation name for display
def nettoie_ville_display(loc):
    if pd.isna(loc): return 'France'
    loc = str(loc)
    # Remove dept number prefix if present (e.g. "75 - Paris")
    loc = re.sub(r'^\d{2,3}\s*-\s*', '', loc)
    return loc.strip().title()

df['localisation'] = df['localisation'].apply(nettoie_ville_display)


# 6. Ajouter une colonne séniorité
def get_seniorite(titre):
    if pd.isna(titre):
        return 'Non précisé'
    titre = str(titre).lower()
    if 'senior' in titre or 'lead' in titre or 'principal' in titre:
        return 'Senior'
    if 'junior' in titre or 'débutant' in titre:
        return 'Junior'
    if 'manager' in titre or 'head' in titre or 'directeur' in titre:
        return 'Manager'
    if 'alternance' in titre or 'alternant' in titre or 'stage' in titre:
        return 'Junior'
    return 'Confirmé'

df['seniorite'] = df['titre'].apply(get_seniorite)


# 7. Nettoyer les titres (supprimer balises HTML résiduelles)
df['titre'] = df['titre'].str.replace(r'<.*?>', '', regex=True).str.strip()


# Résumé final
print(f"\naprès nettoyage: {len(df)} lignes")
print(f"\ndistribution contrats:\n{df['contrat'].value_counts()}")
print(f"\ndistribution régions:\n{df['region'].value_counts()}")
print(f"\ndistribution séniorité:\n{df['seniorite'].value_counts()}")

df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\nsauvegarde: {output_path}")