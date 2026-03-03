from fastapi import FastAPI
from src.predict import predict_state, predict_country
import os

app = FastAPI()

@app.get("/states")
def get_states():
    states = os.listdir("models/state_models")
    states = [s.replace(".pkl","") for s in states]
    return states

@app.get("/forecast/state/{state}")
def forecast_state(state: str):
    result = predict_state(state)
    return result.to_dict(orient="records")

@app.get("/forecast/country")
def forecast_country():
    result = predict_country()
    return result.to_dict(orient="records")