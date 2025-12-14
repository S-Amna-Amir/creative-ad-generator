import pandas as pd

INPUT_PATH = "data/processed/products_clean.csv"
OUTPUT_PATH = "data/processed/prompts.csv"

def build_prompt(row):
    return (
        f"Generate a short promotional ad for the following product:\n"
        f"Product: {row['product_name']}\n"
        f"Category: {row['category']}\n"
        f"Description: {row['description']}"
    )

def prepare_prompts():
    df = pd.read_csv(INPUT_PATH)
    df["prompt"] = df.apply(build_prompt, axis=1)
    df[["product_id", "prompt"]].to_csv(OUTPUT_PATH, index=False)
    print(f"Prompts saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    prepare_prompts()
