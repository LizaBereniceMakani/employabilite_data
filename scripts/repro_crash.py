import pandas as pd
import os
import glob

data_dir = "data"
files = ["offres_apec_enhanced.csv", "offres_apec_raw.csv", "offres_francetravail_raw.csv", "offres_wttj_raw.csv", "offres_apec_listings.csv"]

dfs = []
for f in files:
    path = os.path.join(data_dir, f)
    if os.path.exists(path):
        print(f"Loading {f}...")
        try:
            df = pd.read_csv(path)
        except:
            df = pd.read_csv(path, encoding='cp1252')
        
        # Normalize columns
        df.columns = [c.lower().strip() for c in df.columns]
        
        # Dedup columns
        if df.columns.duplicated().any():
            print(f"  Removing duplicate cols: {df.columns[df.columns.duplicated()].tolist()}")
            df = df.loc[:, ~df.columns.duplicated()]
        
        # Check if 'lien' exists
        if 'lien' not in df.columns and 'url' in df.columns:
            df.rename(columns={'url': 'lien'}, inplace=True)
            
        dfs.append(df)

print("Concatenating...")
df_full = pd.concat(dfs, ignore_index=True)
print(f"Full shape: {df_full.shape}")

print("Dedup rows...")
if 'lien' in df_full.columns:
    df_full.drop_duplicates(subset=['lien'], keep='first', inplace=True)
print(f"After dedup: {df_full.shape}")

# Simulate skills
print("Simulating skills df...")
# Create a dummy df_skills with same length
df_skills = pd.DataFrame({'Python': [0]*len(df_full), 'SQL': [1]*len(df_full)})
# RESET INDEX matches what script does
df_full = df_full.reset_index(drop=True)
df_skills = df_skills.reset_index(drop=True)

print(f"df_full index: {df_full.index}")
print(f"df_skills index: {df_skills.index}")

print("Concat axis=1...")
print("Success without duplicates.")

# TEST DUPLICATE via RENAME
print("\n--- Testing Duplicate via Rename ---")
df_dup = pd.DataFrame({'A': [1,2], 'B': [3,4]})
print(f"Original cols: {df_dup.columns.tolist()}")
# Create duplicate col 'A' via rename
df_dup.rename(columns={'B': 'A'}, inplace=True)
print(f"After rename cols: {df_dup.columns.tolist()}")
print(f"Duplicated? {df_dup.columns.duplicated().any()}")

df_target = pd.DataFrame({'C': [5,6]})
print("Concat Success!")

# TEST APPLY ON DUPLICATE COLS
print("\n--- Testing Apply on Duplicate ---")
df_dup = pd.DataFrame({'desc': ['a', 'b'], 'other': ['c', 'd']})
# Duplicate desc
df_dup['desc_copy'] = df_dup['desc']
df_dup.rename(columns={'desc_copy': 'desc'}, inplace=True)
print(f"Cols: {df_dup.columns.tolist()}")

try:
    print("Applying on duplicate column...")
    res_apply = df_dup['desc'].apply(lambda x: len(str(x)))
    print(f"Apply Result Type: {type(res_apply)}")
    print(res_apply)
except Exception as e:
    print(f"Apply CRASHED: {e}")

# TEST CONCAT COLLISION
print("\n--- Testing Concat Collision ---")
df_left = pd.DataFrame({'A': [1], 'B': [2]})
df_right = pd.DataFrame({'A': [3]})
try:
    pd.concat([df_left, df_right], axis=1)
    print("Collision Success")
except Exception as e:
    print(f"Collision Crash: {e}")
