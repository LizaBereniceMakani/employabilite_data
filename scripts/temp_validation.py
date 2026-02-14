import pandas as pd

try:
    df = pd.read_csv('data/offres_enriched.csv')
    print(f"Total Offers: {len(df)}")
    
    # Check length
    df['desc_len'] = df['description'].fillna("").astype(str).str.len()
    print("\n--- Description Length per Source ---")
    print(df.groupby('source')['desc_len'].mean())
    
    # Check empty
    empty_desc = len(df[df['desc_len'] < 50])
    print(f"\nOffers with empty/short description (<50 chars): {empty_desc} ({empty_desc/len(df):.1%})")
    
    # Check key skills
    print("\n--- Key Skills Frequency ---")
    skills = ['Python', 'SQL', 'Power BI', 'Excel']
    for s in skills:
        if s in df.columns:
            count = df[s].sum()
            print(f"{s}: {count} ({count/len(df):.1%})")
            
    # Check columns fill rate
    print("\n--- Columns Fill Rate ---")
    cols = ['contrat', 'localisation', 'entreprise', 'titre']
    for c in cols:
        fill = df[c].notna().sum()
        print(f"{c}: {fill} ({fill/len(df):.1%})")
        
except Exception as e:
    print(e)
