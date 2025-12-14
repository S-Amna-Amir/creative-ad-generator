import pandas as pd
import os

RAW_DATA_PATH = "/opt/project/data/raw/products.csv"
PROCESSED_DATA_PATH = "/opt/project/data/processed/products_clean.csv"

def clean_text(text: str) -> str:
    return text.lower().strip()

def preprocess():
    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv(RAW_DATA_PATH)

    df["product_name"] = df["product_name"].apply(clean_text)
    df["description"] = df["description"].apply(clean_text)
    df["category"] = df["category"].apply(clean_text)

    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess()
