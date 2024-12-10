import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib


data = pd.read_csv("G:\\Projects\\aqi_forecasting\\Data\\ananadvihar(8hr).csv")


data.fillna(method='ffill', inplace=True)

features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'SO2', 'CO', 'Ozone', 'WS', 'Temp']


scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[features])


joblib.dump(scaler, 'models/scaler.pkl')


from sklearn.ensemble import RandomForestRegressor


X = data_scaled
y = data['AQI']  

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'models/aqi_forecasting_model.pkl')


from pmdarima import auto_arima
import joblib

# Specify which features to forecast (PM2.5, PM10, NO, etc.)
features = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'SO2', 'CO', 'Ozone', 'WS', 'Temp']


feature_forecasters = {}


for feature in features:
    print(f"Training model for {feature}...")
    
    
    forecaster = auto_arima(data[feature], seasonal=True, m=7)  

    
    feature_forecasters[feature] = forecaster


joblib.dump(feature_forecasters, 'models/feature_forecaster.pkl')

print("Time-series forecasting models have been trained and saved.")