import joblib
import pandas as pd

MODEL_DIR = "models"

def predict_state(state):

    model = joblib.load(f"{MODEL_DIR}/state_models/{state}.pkl")

    future = model.make_future_dataframe(periods=5, freq="Y")
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(5)

def predict_country():

    model = joblib.load(f"{MODEL_DIR}/country_model/india.pkl")

    future = model.make_future_dataframe(periods=5, freq="Y")
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(5)