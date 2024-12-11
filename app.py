import pandas as pd
import numpy as np
import streamlit as st
import joblib

scaler = joblib.load("scaler.pkl")
model = joblib.load("best_aqi_predictor_model.pkl")
expected_features = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "SO2", "CO",
    "Ozone", "Benzene", "Toluene", "RH", "WS", "WD", "SR", "BP", "AT"
]
def calculate_aqi(pollutant, concentration):
    aqi_breakpoints = {
        "PM2.5": [(0, 30), (31, 60), (61, 90), (91, 120), (121, 250)],
        "PM10": [(0, 50), (51, 100), (101, 250), (251, 350), (351, 430)],
        "SO2": [(0, 40), (41, 80), (81, 380), (381, 800), (801, 1600)],
        "NO2": [(0, 40), (41, 80), (81, 180), (181, 280), (281, 400)],
        "CO": [(0, 1), (1.1, 2), (2.1, 10), (10.1, 17), (17.1, 34)],
        "Ozone": [(0, 50), (51, 100), (101, 168), (169, 208), (209, 748)]
    }

    aqi_ranges = [(0, 50), (51, 100), (101, 200), (201, 300), (301, 400), (401, 500)]
    breakpoints = aqi_breakpoints.get(pollutant)

    if not breakpoints:
        return None

    for (low_c, high_c), (low_aqi, high_aqi) in zip(breakpoints, aqi_ranges):
        if low_c <= concentration <= high_c:
            
            return ((high_aqi - low_aqi) / (high_c - low_c)) * (concentration - low_c) + low_aqi

    return None

st.title("AQI Prediction and Forecasting App")
st.sidebar.header("Enter Current Air Quality Parameters")
input_values = {}
for feature in expected_features:
    input_values[feature] = st.sidebar.number_input(f"{feature}", value=0.0)

input_data = pd.DataFrame([input_values])
input_data = input_data[expected_features]

try:
   
    scaled_data = scaler.transform(input_data)
    predicted_aqi = model.predict(scaled_data)
    st.write("### Predicted Current AQI (Model):", round(predicted_aqi[0], 2))
    aqi_results = {}
    for pollutant in ["PM2.5", "PM10", "SO2", "NO2", "CO", "Ozone"]:
        aqi_results[pollutant] = calculate_aqi(pollutant, input_values[pollutant])
    manual_aqi = max(aqi_results.values(), default=None)

    st.write("### Calculated AQI (Manual):", round(manual_aqi, 2) if manual_aqi else "Insufficient Data")
    st.write("#### Individual Pollutant AQI Contributions")
    st.dataframe(pd.DataFrame(aqi_results.items(), columns=["Pollutant", "AQI"]))
except ValueError as e:
    st.error(f"Error: {e}")

if st.button("Forecast AQI for Next 7 Days"):
    try:
        forecast_data = input_data.copy()
        forecast_results = []

        for day in range(1, 8):
            
            scaled_forecast_data = scaler.transform(forecast_data)
            predicted_aqi = model.predict(scaled_forecast_data)[0]
            forecast_results.append({"Day": f"Day {day}", "Predicted AQI": round(predicted_aqi, 2)})

            
            # Replace PM2.5 and PM10 with random fluctuations for demonstration
            forecast_data["PM2.5"] += np.random.uniform(-10, 10)
            forecast_data["PM10"] += np.random.uniform(-15, 15)

       
        st.write("### AQI Forecast for the Next 7 Days")
        st.dataframe(pd.DataFrame(forecast_results))
    except Exception as e:
        st.error(f"Error during forecasting: {e}")
