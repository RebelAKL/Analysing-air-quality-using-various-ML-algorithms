from flask import Flask, render_template
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the saved models
aqi_model = joblib.load("models/aqi_forecasting_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_forecasters = joblib.load("models/feature_forecaster.pkl")  # Loaded forecasters for each feature

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    # Generate future dates for prediction
    today = datetime.now()
    future_dates = [today + timedelta(days=i) for i in range(1, 8)]
    future_dates_str = [date.strftime('%Y-%m-%d') for date in future_dates]

    # Forecast features (PM2.5, PM10, etc.) for the next 7 days
    forecasted_features = {}
    for feature, forecaster in feature_forecasters.items():
        forecasted_features[feature] = forecaster.predict(steps=7)

    # Create DataFrame for forecasted features
    forecast_df = pd.DataFrame(forecasted_features)
    
    # Scale the forecasted features
    forecast_scaled = scaler.transform(forecast_df)

    # Predict AQI for the next 7 days
    predicted_aqi = aqi_model.predict(forecast_scaled)

    # Prepare the results in a table
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
