import sys
import json
import joblib
import numpy as np


model = joblib.load("best_aqi_predictor_model.pkl")
scaler = joblib.load("scaler.pkl")  

def predict(features):
    
    features_array = np.array([features]).reshape(1, -1)
    
    scaled_features = scaler.transform(features_array)
    
    aqi = model.predict(scaled_features)
    return aqi[0]

if __name__ == "__main__":
   
    input_features = json.loads(sys.argv[1])
    
    features = [
        input_features['PM2.5'],
        input_features['PM10'],
        input_features['NO'],
        input_features['NO2'],
        input_features['NOx'],
        input_features['NH3'],
        input_features['SO2'],
        input_features['CO'],
        input_features['Ozone'],
        input_features['RH'],
        input_features['WS'],
        input_features['WD'],
        input_features['SR'],
        input_features['BP'],
        input_features['AT']
    ]
    
    predicted_aqi = predict(features)
    print(json.dumps({'AQI': predicted_aqi}))
