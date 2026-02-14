import pandas as pd
import os

files = ["data/offres_apec_raw.csv", "data/offres_wttj_raw.csv", "data/offres_apec_listings.csv"]

for f in files:
    if os.path.exists(f):
        print(f"\n--- Checking {f} ---")
        try:
            df = pd.read_csv(f)
            print(f"Columns: {list(df.columns)}")
            
            # Check Contrat
            contrat_col = next((c for c in df.columns if 'contrat' in c.lower()), None)
            if contrat_col:
                non_null = df[contrat_col].dropna().unique()
                print(f"Contrat ({contrat_col}) - Unique values (first 5): {non_null[:5]}")
                print(f"Contrat non-null count: {df[contrat_col].notna().sum()} / {len(df)}")
            else:
                print("No 'contrat' column found.")
                
            # Check Localisation
            loc_col = next((c for c in df.columns if 'loc' in c.lower()), None)
            if loc_col:
                non_null_loc = df[loc_col].dropna().unique()
                print(f"Localisation ({loc_col}) - Unique values (first 5): {non_null_loc[:5]}")
                print(f"Localisation non-null count: {df[loc_col].notna().sum()} / {len(df)}")
            else:
                print("No 'localisation' column found.")
                
        except Exception as e:
            print(f"Error reading {f}: {e}")
