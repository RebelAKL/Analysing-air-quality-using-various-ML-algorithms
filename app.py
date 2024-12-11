import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

model = joblib.load("best_aqi_predictor_model.pkl")
scaler = joblib.load("scaler.pkl")


FEATURES = [
    "PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "SO2", "CO","Ozone",
    "Benzene", "Toluene", "RH", "WS", "WD", "SR", "BP", "AT"
]


default_values = {
    "Benzene": 0.1, 
    "Toluene": 0.2,  
}


st.title("Air Quality Prediction and Analysis")


st.sidebar.title("Navigation")
options = ["Manual Input", "Predict Next Days", "Graphs & Map"]
choice = st.sidebar.selectbox("Choose an option:", options)

if choice == "Manual Input":
    st.subheader("Manual Input")
    
    
    inputs = {}
    for feature in FEATURES:
        value = st.number_input(f"Enter {feature}", value=0.0)
        inputs[feature] = value

    
    input_data = pd.DataFrame([inputs])
    input_data = input_data[FEATURES]  

    
    scaled_data = scaler.transform(input_data)

   
    prediction = model.predict(scaled_data)[0]
    st.success(f"Predicted AQI: {prediction:.2f}")

elif choice == "Predict Next Days":
    st.subheader("Predict AQI for Next Days")

    #
    num_days = st.number_input("Enter number of days to predict (1-7):", min_value=1, max_value=7, value=3)

    future_data = pd.DataFrame({
        "PM2.5": [50] * num_days,
        "PM10": [80] * num_days,
        "NO": [10] * num_days,
        "NO2": [20] * num_days,
        "NOx": [30] * num_days,
        "NH3": [5] * num_days,
        "SO2": [3] * num_days,
        "CO": [0.9] * num_days,
        "Ozone":[10]*num_days,
        "Benzene": [default_values["Benzene"]] * num_days,
        "Toluene": [default_values["Toluene"]] * num_days,
        "RH": [60] * num_days,
        "WS": [3.5] * num_days,
        "WD": [180] * num_days,
        "SR": [800] * num_days,
        "BP": [1012] * num_days,
        "AT": [25] * num_days
    })

    
    scaled_future_data = scaler.transform(future_data)

    
    future_predictions = model.predict(scaled_future_data)
    st.write("Predicted AQI values:")
    for i, pred in enumerate(future_predictions):
        st.write(f"Day {i + 1}: {pred:.2f}")

elif choice == "Graphs & Map":
    st.subheader("Graphs and Location Map")

    
    st.write("PM2.5 Levels (Example Data)")
    sample_data = pd.DataFrame({
        "Time": [f"Day {i+1}" for i in range(10)],
        "PM2.5": np.random.randint(30, 150, 10)
    })
    plt.figure(figsize=(10, 5))
    plt.plot(sample_data["Time"], sample_data["PM2.5"], marker="o", color="blue")
    plt.title("PM2.5 Levels Over Time")
    plt.xlabel("Time")
    plt.ylabel("PM2.5")
    st.pyplot(plt)

    
    st.write("Location Map")
    location_map = folium.Map(location=[28.6139, 77.2090], zoom_start=10)  # Example coordinates (Delhi, India)
    folium.Marker([28.6139, 77.2090], popup="Sample Location").add_to(location_map)
    st_folium(location_map, width=700, height=500)
