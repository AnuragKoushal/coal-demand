# 🇮🇳 India Coal Consumption Forecasting System

A production-grade machine learning system for forecasting **state-wise** and **country-level** coal consumption using Facebook Prophet.

This project demonstrates a complete MLOps-style workflow including:

- Data aggregation
- Model training
- Model persistence
- API-based inference
- Executive dashboard (Streamlit)
- Clean separation of training and serving

---

# 📊 System Overview

This system forecasts:

- 🔹 5-Year State-Level Coal Demand
- 🔹 5-Year National Coal Demand
- 🔹 Growth Percentage
- 🔹 CAGR
- 🔹 State Growth Ranking

Models are trained once and saved. The API loads trained models for fast inference.

---

# 🏗 Project Structure


coal-prod-full-project/
│
├── data/
│ ├── raw/ # Input dataset (coal.csv)
│ └── processed/
│
├── models/
│ ├── state_models/ # Saved Prophet models per state
│ └── country_model/ # National aggregate model
│
├── src/
│ ├── train.py # Model training script
│ ├── predict.py # Model inference logic
│ ├── serve.py # FastAPI backend
│
├── ui/
│ └── streamlit_app.py # Executive dashboard
│
└── README.md


---

# 🚀 Full Deployment & Run Guide

## 1️⃣ Prerequisites

- macOS / Windows / Linux
- Anaconda or Miniconda installed
- Python 3.10

---

## 2️⃣ Create Conda Environment

```bash
conda create -n coal-env python=3.10 -y
conda activate coal-env

You should now see:

(coal-env)
3️⃣ Install Dependencies

Install forecasting & scientific libraries:

conda install -c conda-forge prophet pandas numpy scikit-learn matplotlib -y

Install backend & UI dependencies:

pip install fastapi uvicorn streamlit joblib requests python-multipart
4️⃣ Create Required Folders (First-Time Setup)
mkdir -p data/raw
mkdir -p models/state_models
mkdir -p models/country_model
5️⃣ Add Training Dataset

Place your dataset inside:

data/raw/coal.csv
Required Columns
Column Name	Description
srcStateName	State name
srcYear	Year (numeric)
Coal Consumed	Total coal consumption value

Example:

srcStateName	srcYear	Coal Consumed
DELHI	2011	0.131
PUNJAB	2011	12.545
6️⃣ Train Models (One-Time Step)
python src/train.py

Expected Output:

Training complete. Models saved.

Verify model creation:

ls models/state_models
ls models/country_model

You should see multiple .pkl model files.

7️⃣ Start Backend API
uvicorn src.serve:app --reload

Expected:

Uvicorn running on http://127.0.0.1:8000

Open API documentation:

http://127.0.0.1:8000/docs

Available endpoints:

GET /states

GET /forecast/state/{state}

GET /forecast/country

Leave this terminal running.

8️⃣ Start Dashboard

Open a new terminal:

conda activate coal-env
streamlit run ui/streamlit_app.py

Open in browser:

http://localhost:8501

You now have a live production forecasting dashboard.

🔄 Normal Daily Usage

After initial setup and training:

You DO NOT need to retrain models every time.

Simply:

conda activate coal-env
uvicorn src.serve:app --reload

Then in another terminal:

streamlit run ui/streamlit_app.py
🔁 Retraining Models

Retrain only when new yearly data is available.

Steps:

Replace dataset:

data/raw/coal.csv

Run:

python src/train.py

Restart backend server.

🛑 Stopping the System

Press:

CTRL + C

If port 8000 is stuck:

kill -9 $(lsof -ti:8000)