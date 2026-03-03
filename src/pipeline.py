
import pandas as pd
import os

RAW_PATH = "data/raw/coal.csv"
PROCESSED_PATH = "data/processed/coal_clean.csv"

def run_pipeline():
    df = pd.read_csv(RAW_PATH)
    df["ds"] = pd.to_datetime(df["date"])
    df["y"] = df["coal_tonnes"]
    df = df[["ds", "y"]].sort_values("ds")
    df["lag7"] = df["y"].shift(7)
    df["ma30"] = df["y"].rolling(30).mean()
    df.dropna(inplace=True)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print("Pipeline completed.")

if __name__ == "__main__":
    run_pipeline()
