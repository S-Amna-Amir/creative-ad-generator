import pandas as pd
from ad_generator import AdGenerator
from quality_check import validity_score

INPUT_PATH = "data/processed/prompts.csv"
OUTPUT_PATH = "data/processed/generated_ads.csv"

def main():
    df = pd.read_csv(INPUT_PATH)
    generator = AdGenerator()

    ads = []
    scores = []
    for _, row in df.iterrows():
        ad_text = generator.generate_ad(row["prompt"])
        ads.append(ad_text)
        scores.append(validity_score(ad_text))

    df["generated_ad"] = ads
    df["quality_score"] = scores
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated ads saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
