# 🔥 ClimateGuard AI

## AI-Based Wildfire Risk Analysis and Prediction System

ClimateGuard AI is a machine-learning-based wildfire risk analysis prototype that combines satellite fire observations with meteorological data to estimate fire-detection probability across India.

The project integrates **NASA VIIRS active-fire observations**, **ERA5-Land weather data**, machine learning, geospatial visualization, and an interactive Streamlit dashboard.

---

## 🎯 Project Objective

The main objectives of ClimateGuard AI are to:

- Analyze historical wildfire/hotspot observations.
- Integrate fire observations with weather conditions.
- Identify environmental patterns associated with fire detections.
- Train a machine-learning model for fire-risk estimation.
- Generate geographic fire-risk visualizations.
- Provide an interactive dashboard for exploring model predictions.

---

## 🛰️ Data Sources

### VIIRS Active Fire Data

VIIRS satellite fire observations are used to identify historical fire/hotspot detections.

### ERA5-Land Weather Data

ERA5-Land data provides meteorological variables used by the model.

The project currently uses:

- Temperature
- Relative humidity
- Precipitation
- Wind speed
- Latitude
- Longitude
- Month
- Day of year

The current experimental dataset covers **India during 2024**.

---

## 🧠 Machine Learning

ClimateGuard AI currently uses a:

**Random Forest Classifier**

Input features:

```text
Temperature
Relative Humidity
Precipitation
Wind Speed
Latitude
Longitude
Month
Day of Year
        ↓
Random Forest
        ↓
Estimated Fire-Detection Probability
```

The probability is converted into four project visualization categories:

| Probability | Risk Level |
|---|---|
| 0–25% | LOW |
| 25–50% | MODERATE |
| 50–75% | HIGH |
| 75–100% | EXTREME |

These categories are experimental project thresholds and are **not official wildfire warning levels**.

---

## 📊 Baseline Model Results

The initial random train/test split produced:

| Metric | Result |
|---|---:|
| Accuracy | 90.13% |
| Precision | 89.52% |
| Recall | 94.88% |
| F1 Score | 92.12% |

These results represent the current experimental baseline.

Because geographically and temporally related observations may occur in both the training and test sets, these metrics should **not** be interpreted as validated real-world wildfire forecasting performance.

Future versions should use stronger spatial and temporal holdout validation.

---

## 🔥 ClimateGuard Pipeline

```text
VIIRS Fire Observations
          +
ERA5-Land Weather Data
          ↓
Data Cleaning & Preprocessing
          ↓
Spatial/Temporal Data Integration
          ↓
Fire / Non-Fire Dataset
          ↓
Feature Engineering
          ↓
Random Forest Training
          ↓
Fire Probability Estimation
          ↓
Risk Classification
          ↓
India Fire Risk Map
          ↓
Streamlit Dashboard
```

---

## 🗺️ Fire Risk Visualization

ClimateGuard AI generates a geographic visualization showing model-estimated fire probability across the analyzed observations.

Generated output:

```text
results/climateguard_fire_risk_map.png
```

---

## 💻 Interactive Dashboard

The Streamlit dashboard provides:

- Dataset overview
- Fire-risk distribution
- India fire-risk visualization
- Highest-risk observations
- Weather and location inputs
- Interactive ML prediction
- Fire probability
- LOW / MODERATE / HIGH / EXTREME risk display
- Model information

---

## 📁 Project Structure

```text
ClimateGuard-AI/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── climateguard_random_forest.pkl
│
├── notebooks/
│
├── results/
│   ├── climateguard_fire_risk_predictions.csv
│   └── climateguard_fire_risk_map.png
│
├── src/
│   ├── load_fire_data.py
│   ├── preprocess_fire_data.py
│   ├── download_weather_data.py
│   ├── download_full_weather.py
│   ├── check_weather_data.py
│   ├── preprocess_weather.py
│   ├── merge_fire_weather.py
│   ├── build_ml_dataset.py
│   ├── train_fire_model.py
│   ├── predict_fire_risk.py
│   └── fire_risk_prediction_map.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 🚀 Run the Dashboard

From the project root directory:

```bash
python -m streamlit run dashboard/app.py
```

Then open the local address displayed by Streamlit.

---

## ⚠️ Limitations

ClimateGuard AI is currently a research/educational prototype.

Current limitations include:

- Training currently focuses on 2024 data.
- Fire occurrence is derived from satellite hotspot observations.
- Random train/test splitting may overestimate generalization.
- The model does not yet provide operational wildfire forecasting.
- Risk thresholds are project-defined visualization categories.
- Human activity, vegetation, fuel moisture, topography and other important fire drivers are not yet fully modeled.
- The system is not connected to an official emergency-warning service.

---

## 🔮 Future Development

Future versions can include:

- Multi-year fire and weather datasets
- Spatial holdout validation
- Temporal forecasting evaluation
- Vegetation and NDVI information
- Soil moisture
- Land-cover information
- Elevation and terrain
- Drought indicators
- Live weather integration
- Explainable AI
- Real-time risk maps
- Location search
- Automated alerts
- Cloud deployment

---

## ⚠️ Disclaimer

ClimateGuard AI is an experimental academic and research project.

Predictions generated by the system must **not** be used as official wildfire warnings, emergency instructions, or public-safety decisions.

---

## 🔥 ClimateGuard AI

**Satellite Data + Climate Data + Machine Learning + Geospatial Intelligence**