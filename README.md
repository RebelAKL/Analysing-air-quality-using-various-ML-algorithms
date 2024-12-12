**Air Quality Index (AQI) Forecasting and Prediction Project Documentation**

---

### **Project Overview**
The AQI Forecasting and Prediction project is designed to analyze air quality parameters and predict the AQI using machine learning models. This application also allows users to input air quality data manually and provides a calculated AQI based on standard pollutant-specific formulas. The platform forecasts AQI for up to seven days and presents results through an interactive and user-friendly interface.

---

### **Key Features**
1. **Manual Input of Air Quality Parameters:**
   - Users can manually input values for pollutants like PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO, Benzene, Toluene, and meteorological parameters.
   - Provides both model-predicted AQI and manually calculated AQI using pollutant-specific breakpoints.

2. **Forecasting AQI for the Next 7 Days:**
   - Uses trained machine learning models to predict AQI for future days.
   - Generates realistic forecasts based on current and historical air quality data.

3. **Visualization:**
   - Displays individual pollutant AQI contributions.
   - Presents forecasted AQI trends in tabular and graphical formats for better analysis.

4. **Interactive Streamlit Application:**
   - A web-based interface to facilitate easy interaction and data visualization.

---

### **Technologies Used**
1. **Programming Language:**
   - Python

2. **Libraries and Frameworks:**
   - **Streamlit:** For building an interactive web application.
   - **Pandas:** For data manipulation and analysis.
   - **Numpy:** For numerical computations.
   - **Scikit-learn:** For data preprocessing and machine learning model implementation.
   - **XGBoost:** For gradient boosting modeling.
   - **Joblib:** For saving and loading machine learning models and scalers.

3. **Machine Learning Models:**
   - **XGBoost:**
     - Pros: Handles missing data well, highly accurate, and efficient.
     - Cons: Computationally intensive and requires parameter tuning.
   - **Random Forest (RF):**
     - Pros: Robust to overfitting and interpretable with feature importance.
     - Cons: Slower with large datasets and less effective for continuous data.
   - **Linear Regression (LR):**
     - Pros: Simple, fast, and interpretable.
     - Cons: Limited by its assumption of linearity and sensitivity to outliers.
   - After comparison, XGBoost was selected as the best model for its high accuracy and robustness.

4. **Deployment Environment:**
   - Streamlit app run locally or on a cloud platform for web-based interaction.

---

### **Working of the Application**
#### **Data Input**
- Users provide air quality parameter data either manually or through an automated dataset.
- Parameters include pollutants (PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO, Benzene, Toluene) and meteorological factors (RH, WS, WD, SR, BP, AT).

#### **Processing**
- Input data is scaled using a pre-trained `StandardScaler` from Scikit-learn.
- Features are ordered as per the model’s training schema to ensure consistency.

#### **AQI Calculation**
1. **Manual AQI Calculation:**
   - Breakpoints for pollutants are used to calculate individual AQI values.
   - The overall AQI is determined as the maximum value among the pollutant-specific AQI values.
2. **Model Prediction:**
   - Scaled input data is fed into the pre-trained regression model to predict the AQI.

#### **Forecasting**
- The trained model predicts AQI for the next 7 days based on simulated fluctuations in pollutant levels.

#### **Output**
- Displays the predicted AQI (model) and calculated AQI (manual).
- Provides a forecast for AQI trends in the next 7 days.
- Outputs individual pollutant AQI contributions for better understanding.

---

### **Dataset**
- **Source:** CCR providied 24hr step data of Ananad Vihar station Delhi from 1/01/2024 tp 10/12/2024
- **Features:**
  - Pollutants: PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO, Benzene, Toluene, Ozone.
  - Meteorological parameters: RH (Relative Humidity), WS (Wind Speed), WD (Wind Direction), SR (Solar Radiation), BP (Barometric Pressure), AT (Ambient Temperature).
- **Size:** Over 1000 entries recorded every 8 hours for one year.

---

### **Challenges and Solutions**
1. **Mismatch in Feature Order:**
   - Resolved by explicitly reordering features in input data to match the training schema.
2. **Handling Missing Pollutants:**
   - Manual AQI calculation accommodates missing values by considering only available pollutants.
3. **Prediction Consistency:**
   - Ensured correct scaling and feature alignment for reliable predictions.

---

### **Future Enhancements**
1. **Dynamic Data Integration:**
   - Incorporate real-time air quality data APIs for live predictions.
2. **Advanced Visualization:**
   - Add interactive graphs for better insights into AQI trends.
3. **Mobile Compatibility:**
   - Optimize the app interface for mobile devices.
4. **Extended Forecasting:**
   - Improve model capability to forecast AQI for 14 or 30 days.

---

### **Conclusion**
The AQI Forecasting and Prediction project provides an accessible and practical solution for analyzing and forecasting air quality. It leverages advanced machine learning techniques and pollutant-specific calculations to offer accurate predictions and insights into air quality trends, aiding users in making informed decisions about environmental conditions.

