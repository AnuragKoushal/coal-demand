import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")
st.title("🇮🇳 India Coal Consumption Forecast Dashboard")
st.markdown("Indraneel Chakravorty")

# -------------------------------------------------
# Utility Functions (SAFE CALCULATIONS)
# -------------------------------------------------
def safe_growth(start, end):
    if start > 0:
        return ((end - start) / start) * 100
    return 0

def safe_cagr(start, end, years=5):
    if start > 0 and end > 0:
        return ((end / start) ** (1/years) - 1) * 100
    return 0

# -------------------------------------------------
# Check API Connection
# -------------------------------------------------
try:
    states_response = requests.get(f"{API_BASE}/states")
    states_response.raise_for_status()
    states = states_response.json()
except Exception:
    st.error("⚠ Backend not running. Start FastAPI server first.")
    st.stop()

# =================================================
# COUNTRY SECTION
# =================================================
st.header("🇮🇳 Country-Level Forecast")

try:
    country_response = requests.get(f"{API_BASE}/forecast/country")
    country_response.raise_for_status()

    country_df = pd.DataFrame(country_response.json())

    # Safety: clip negative predictions
    country_df["yhat"] = country_df["yhat"].clip(lower=0)
    country_df["Year"] = pd.to_datetime(country_df["ds"]).dt.year

    latest_value = country_df["yhat"].iloc[0]
    final_value = country_df["yhat"].iloc[-1]

    growth_pct = safe_growth(latest_value, final_value)
    cagr = safe_cagr(latest_value, final_value)

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Forecast", f"{latest_value:,.2f}")
    col2.metric("5-Year Growth %", f"{growth_pct:.2f}%")
    col3.metric("CAGR", f"{cagr:.2f}%")

    fig = plt.figure()
    plt.plot(country_df["Year"], country_df["yhat"], marker="o")
    plt.title("India Coal Consumption Forecast (Next 5 Years)")
    plt.xlabel("Year")
    plt.ylabel("Coal Consumption")
    plt.grid(True)
    st.pyplot(fig)

    if growth_pct > 0:
        st.success("📈 National coal demand projected to grow steadily.")
    elif growth_pct < 0:
        st.warning("📉 National coal demand projected to decline.")
    else:
        st.info("➡ Stable coal demand projected.")

except Exception as e:
    st.error("Error loading country forecast.")

# =================================================
# STATE SECTION
# =================================================
st.header("State-Level Forecast")

selected_state = st.selectbox("Select State", states)

if selected_state:

    try:
        state_response = requests.get(
            f"{API_BASE}/forecast/state/{selected_state}"
        )
        state_response.raise_for_status()

        state_df = pd.DataFrame(state_response.json())

        # Safety: clip negative values
        state_df["yhat"] = state_df["yhat"].clip(lower=0)
        state_df["Year"] = pd.to_datetime(state_df["ds"]).dt.year

        state_latest = state_df["yhat"].iloc[0]
        state_final = state_df["yhat"].iloc[-1]

        state_growth = safe_growth(state_latest, state_final)
        state_cagr = safe_cagr(state_latest, state_final)

        col4, col5, col6 = st.columns(3)
        col4.metric("Latest Forecast", f"{state_latest:,.2f}")
        col5.metric("5-Year Growth %", f"{state_growth:.2f}%")
        col6.metric("CAGR", f"{state_cagr:.2f}%")

        fig2 = plt.figure()
        plt.plot(state_df["Year"], state_df["yhat"], marker="o")
        plt.title(f"{selected_state} Coal Forecast (Next 5 Years)")
        plt.xlabel("Year")
        plt.ylabel("Coal Consumption")
        plt.grid(True)
        st.pyplot(fig2)

        if state_growth > 0:
            st.success(f"{selected_state} shows projected growth.")
        elif state_growth < 0:
            st.warning(f"{selected_state} shows projected decline.")
        else:
            st.info(f"{selected_state} demand remains stable.")

    except Exception:
        st.error("Error loading state forecast.")

# =================================================
# GROWTH RANKING
# =================================================
st.header("State Growth Ranking (Next 5 Years)")

growth_summary = []

for state in states:
    try:
        res = requests.get(f"{API_BASE}/forecast/state/{state}")
        df_temp = pd.DataFrame(res.json())
        df_temp["yhat"] = df_temp["yhat"].clip(lower=0)

        start = df_temp["yhat"].iloc[0]
        end = df_temp["yhat"].iloc[-1]

        growth = safe_growth(start, end)
        growth_summary.append((state, growth))

    except:
        continue

if growth_summary:
    growth_df = pd.DataFrame(growth_summary, columns=["State", "Growth %"])
    growth_df = growth_df.sort_values("Growth %", ascending=False)
    st.dataframe(growth_df, use_container_width=True)
else:
    st.info("Not enough data for ranking.")