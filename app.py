from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  

model = joblib.load("best_aqi_predictor_model.pkl")

scaler = joblib.load("scaler.pkl") 

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  
        features = np.array(data['features']).reshape(1, -1)  
        scaled_features = scaler.transform(features)  
        prediction = model.predict(scaled_features)
        return jsonify({'AQI': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
