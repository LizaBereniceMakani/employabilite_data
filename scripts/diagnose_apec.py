import pandas as pd
import os

file_path = 'data/offres_apec_raw.csv'
print(f"Reading {file_path}...")

# Try reading raw with default engine
try:
    df = pd.read_csv(file_path, on_bad_lines='skip')
    print(f"Loaded {len(df)} lines.")
    
    if 'description' in df.columns:
        df['desc_len'] = df['description'].fillna("").astype(str).str.len()
        print(f"Mean Length: {df['desc_len'].mean()}")
        print(f"Median Length: {df['desc_len'].median()}")
        print(f"Min Length: {df['desc_len'].min()}")
        print(f"Max Length: {df['desc_len'].max()}")
        
        print("\n--- Distribution ---")
        print(df['desc_len'].describe())

        print("\n--- Sample Short Description (< 100 chars) ---")
        short = df[df['desc_len'] < 100]
        if not short.empty:
            print(short.iloc[0]['description'])
            
        print("\n--- Sample Long Description (> 1000 chars) ---")
        long = df[df['desc_len'] > 1000]
        if not long.empty:
            print(long.iloc[0]['description'][:200] + "...")
            
    else:
        print("Column 'description' not found in raw headers.")
        print(df.columns)

except Exception as e:
    print(f"Error reading CSV: {e}")
