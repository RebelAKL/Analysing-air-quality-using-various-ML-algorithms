from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)


aqi_model = joblib.load("models/aqi_forecasting_model.pkl")  
scaler = joblib.load("models/scaler.pkl")  

#
feature_forecasters = joblib.load("models/feature_forecaster.pkl")  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    
    today = datetime.now()
    future_dates = [today + timedelta(days=i) for i in range(1, 8)]
    future_dates_str = [date.strftime('%Y-%m-%d') for date in future_dates]

    
    forecasted_features = {}
    for feature, forecaster in feature_forecasters.items():
        forecasted_features[feature] = forecaster.predict(steps=7)  

    
    future_data = pd.DataFrame(forecasted_features)

    
    future_scaled = scaler.transform(future_data)

    
    predicted_aqi = aqi_model.predict(future_scaled)

    
    forecast_results = pd.DataFrame({
        "Date": future_dates_str,
        "Predicted AQI": predicted_aqi
    })

 
    return render_template(
        "index.html", 
        forecast_table=forecast_results.to_html(index=False)
    )

if __name__ == "__main__":
    app.run(debug=True)
