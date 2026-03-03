# India Coal Consumption Forecasting System

A production-grade machine learning system for forecasting **state-wise** and **country-level** coal consumption.

This project demonstrates a complete end-to-end ML lifecycle including:

- Data aggregation
- Model training
- Model persistence
- API-based inference
- Executive dashboard (Streamlit)
- Proper separation of training and serving (MLOps pattern)
# Dataset Source

This project uses publicly available Indian coal consumption data from Kaggle:

🔗 https://www.kaggle.com/datasets/zsinghrahulk/indian-coal-consumption

Please download the dataset from the above link and place the cleaned CSV file in:

```
data/raw/coal.csv
```

# System Overview

The system provides:

-  5-Year State-Level Forecast
-  5-Year Country-Level Forecast
-  Growth Percentage
-  CAGR (Compound Annual Growth Rate)
-  State Growth Ranking
-  Production API Endpoints

Models are trained once and saved. The API loads trained models for fast inference.


# Project Structure

```
coal-prod-full-project/
│
├── data/
│   ├── raw/                  # Input dataset (coal.csv)
│   └── processed/
│
├── models/
│   ├── state_models/         # Saved Prophet models per state
│   └── country_model/        # National aggregate model
│
├── src/
│   ├── train.py              # Model training script
│   ├── predict.py            # Model inference logic
│   ├── serve.py              # FastAPI backend
│
├── ui/
│   └── streamlit_app.py      # Executive dashboard
│
└── README.md
```

# Complete Deployment & Run Guide

## Prerequisites

Ensure the following are installed:

- macOS / Windows / Linux
- Anaconda or Miniconda
- Python 3.10


## Create Conda Environment

```bash
conda create -n coal-env python=3.10 -y
conda activate coal-env
```

You should now see:

```
(coal-env)
```

## Install Dependencies

Install core ML libraries via conda:

```bash
conda install -c conda-forge prophet pandas numpy scikit-learn matplotlib -y
```

Install API & dashboard libraries via pip:

```bash
pip install fastapi uvicorn streamlit joblib requests python-multipart
```

---

## Create Required Folders (First-Time Setup)

If not already present:

```bash
mkdir -p data/raw
mkdir -p models/state_models
mkdir -p models/country_model
```

## Add Training Dataset

Place your dataset inside:

```
data/raw/coal.csv
```

### Required Columns

| Column Name     | Description |
|----------------|------------|
| srcStateName  | State name |
| srcYear       | Year (numeric) |
| Coal Consumed | Total yearly coal consumption |

Example:

| srcStateName | srcYear | Coal Consumed |
|--------------|---------|---------------|
| DELHI        | 2011    | 0.131         |
| PUNJAB       | 2011    | 12.545        |


## Train Models (One-Time Step)

```bash
python src/train.py
```

Expected output:

```
Training complete. Models saved.
```

Verify models were created:

```bash
ls models/state_models
ls models/country_model
```

You should see multiple `.pkl` files.

## Start Backend API

```bash
uvicorn src.serve:app --reload
```

Expected:

```
Uvicorn running on http://127.0.0.1:8000
```

Open API documentation in browser:

```
http://127.0.0.1:8000/docs
```

Available endpoints:

- GET `/states`
- GET `/forecast/state/{state}`
- GET `/forecast/country`

Leave this terminal running.

## Start Dashboard

Open a new terminal:

```bash
conda activate coal-env
streamlit run ui/streamlit_app.py
```

Open in browser:

```
http://localhost:8501
```

You now have a fully operational production forecasting dashboard.

# Daily Usage (After Initial Setup)

You DO NOT need to retrain models daily.

To start the system:

```bash
conda activate coal-env
uvicorn src.serve:app --reload
```

In another terminal:

```bash
conda activate coal-env
streamlit run ui/streamlit_app.py
```

# Retraining Models (When New Data Is Available)

If new yearly data is added:

1. Replace:
   ```
   data/raw/coal.csv
   ```

2. Run:
   ```bash
   python src/train.py
   ```

3. Restart backend server.


#  Stop The System

Press:

```
CTRL + C
```

If port 8000 is stuck:

```bash
kill -9 $(lsof -ti:8000)
```

# 📈 System Capabilities

✔ State-wise 5-year forecast  
✔ Country-level forecast  
✔ Growth % calculation  
✔ CAGR calculation  
✔ Ranking of fastest growing states  
✔ Saved trained models  
✔ Production-ready API  
✔ Executive-level dashboard  


# Architecture Philosophy

This system follows proper ML lifecycle separation:

| Training | Inference |
|----------|-----------|
| train.py | serve.py |
| Saves models | Loads models |
| Runs occasionally | Runs continuously |

Models are NOT retrained during dashboard interaction.


# Technology Stack

- Prophet (Time Series Forecasting)
- FastAPI (Backend API)
- Streamlit (Dashboard UI)
- Conda (Environment Management)
- Joblib (Model Persistence)


# 📄 License

For academic and demonstration purposes.
