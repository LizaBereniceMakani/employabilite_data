
import pandas as pd
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    wttj_path = os.path.join(data_dir, "offres_data_science_raw.csv")
    apec_path = os.path.join(data_dir, "offres_apec_raw.csv")
    output_path = os.path.join(data_dir, "offres_raw_merged.csv")

    df_wttj = pd.read_csv(wttj_path)
    df_apec = pd.read_csv(apec_path)
    
    # Add source column to WTTJ if missing
    if "source" not in df_wttj.columns:
        df_wttj["source"] = "WTTJ"
        
    # Ensure source column exists in APEC (it should)
    if "source" not in df_apec.columns:
        df_apec["source"] = "APEC"

    # Concatenate
    df_merged = pd.concat([df_wttj, df_apec], ignore_index=True)
    
    # Save
    df_merged.to_csv(output_path, index=False, encoding="utf-8-sig")
    
    print(f"Fusion terminée : {len(df_merged)} offres au total.")
    print(f" - WTTJ : {len(df_wttj)}")
    print(f" - APEC : {len(df_apec)}")
    print(f"Sauvegardé dans : {output_path}")

if __name__ == "__main__":
    main()
