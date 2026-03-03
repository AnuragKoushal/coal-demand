import pandas as pd
import os
import joblib
from prophet import Prophet
from sklearn.metrics import mean_absolute_percentage_error

DATA_PATH = "data/raw/coal.csv"
MODEL_DIR = "models"

def train_models():

    df = pd.read_csv(DATA_PATH)

    df_state = (
        df.groupby(["srcStateName", "srcYear"])["Coal Consumed"]
        .sum()
        .reset_index()
    )

    df_state["ds"] = pd.to_datetime(df_state["srcYear"], format="%Y")
    df_state["y"] = df_state["Coal Consumed"]

    os.makedirs(f"{MODEL_DIR}/state_models", exist_ok=True)

    # Train per state
    for state in df_state["srcStateName"].unique():

        state_df = df_state[df_state["srcStateName"] == state][["ds", "y"]]

        if len(state_df) < 5:
            continue

        model = Prophet(yearly_seasonality=False)
        model.fit(state_df)

        joblib.dump(model, f"{MODEL_DIR}/state_models/{state}.pkl")

    # Train country model
    country_df = df_state.groupby("ds")["y"].sum().reset_index()

    country_model = Prophet(yearly_seasonality=False)
    country_model.fit(country_df)

    os.makedirs(f"{MODEL_DIR}/country_model", exist_ok=True)
    joblib.dump(country_model, f"{MODEL_DIR}/country_model/india.pkl")

    print("Training complete. Models saved.")

if __name__ == "__main__":
    train_models()