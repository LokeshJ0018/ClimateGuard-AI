import streamlit as st
import pandas as pd
import joblib
import os

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ClimateGuard AI",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 ClimateGuard AI")
st.subheader("AI-Based Wildfire Risk Analysis System")

st.caption(
    "Machine-learning prototype using ERA5-Land weather data "
    "and VIIRS fire observations."
)

st.divider()

# --------------------------------------------------
# PATHS
# --------------------------------------------------

PREDICTION_FILE = "results/climateguard_dashboard_sample.csv"
MODEL_FILE = "models/climateguard_random_forest_compressed.pkl"
MAP_FILE = "results/climateguard_fire_risk_map.png"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_predictions():
    return pd.read_csv(PREDICTION_FILE)


@st.cache_resource
def load_model():
    saved = joblib.load(MODEL_FILE)
    return saved["model"], saved["features"]


try:
    data = load_predictions()
    model, features = load_model()

except Exception as e:
    st.error(f"Unable to load ClimateGuard data: {e}")
    st.stop()

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

st.header("📊 ClimateGuard Overview")

total_records = len(data)

extreme_count = (data["risk_level"] == "EXTREME").sum()
high_count = (data["risk_level"] == "HIGH").sum()

average_probability = data[
    "fire_probability_percent"
].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{total_records:,}"
)

col2.metric(
    "Extreme Risk",
    f"{extreme_count:,}"
)

col3.metric(
    "High Risk",
    f"{high_count:,}"
)

col4.metric(
    "Average Probability",
    f"{average_probability:.1f}%"
)

st.divider()

# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------

st.header("🔥 Fire Risk Distribution")

risk_order = [
    "LOW",
    "MODERATE",
    "HIGH",
    "EXTREME"
]

risk_counts = (
    data["risk_level"]
    .value_counts()
    .reindex(risk_order, fill_value=0)
)

st.bar_chart(risk_counts)

st.divider()

# --------------------------------------------------
# FIRE RISK MAP
# --------------------------------------------------

st.header("🗺️ India Fire Risk Map")

if os.path.exists(MAP_FILE):

    st.image(
        MAP_FILE,
        caption="ClimateGuard AI - Predicted Fire Risk Distribution",
        use_container_width=True
    )

else:

    st.warning(
        "Fire risk map image was not found."
    )

st.caption(
    "Risk values are experimental model outputs and should not "
    "be interpreted as official wildfire warnings."
)

st.divider()

# --------------------------------------------------
# HIGH RISK LOCATIONS
# --------------------------------------------------

st.header("📍 Highest-Risk Observations")

display_columns = [
    "date",
    "latitude_grid",
    "longitude_grid",
    "temperature_c",
    "relative_humidity",
    "precipitation_mm",
    "wind_speed_ms",
    "fire_probability_percent",
    "risk_level"
]

top_locations = (
    data
    .sort_values(
        "fire_probability_percent",
        ascending=False
    )
    [display_columns]
    .head(20)
)

st.dataframe(
    top_locations,
    use_container_width=True,
    hide_index=True
)

st.divider()

# --------------------------------------------------
# INTERACTIVE PREDICTION
# --------------------------------------------------

st.header("🤖 Fire Risk Predictor")

st.write(
    "Enter weather and location information to obtain "
    "the baseline model's estimated fire-detection probability."
)

col1, col2 = st.columns(2)

with col1:

    temperature = st.number_input(
        "Temperature (°C)",
        value=30.0
    )

    humidity = st.number_input(
        "Relative Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=40.0
    )

    precipitation = st.number_input(
        "Precipitation (mm)",
        min_value=0.0,
        value=0.0
    )

    wind_speed = st.number_input(
        "Wind Speed (m/s)",
        min_value=0.0,
        value=3.0
    )


with col2:

    latitude = st.number_input(
        "Latitude",
        min_value=6.0,
        max_value=38.0,
        value=13.0
    )

    longitude = st.number_input(
        "Longitude",
        min_value=68.0,
        max_value=98.0,
        value=80.0
    )

    month = st.slider(
        "Month",
        1,
        12,
        5
    )

    day_of_year = st.slider(
        "Day of Year",
        1,
        366,
        150
    )

# --------------------------------------------------
# PREDICT BUTTON
# --------------------------------------------------

if st.button(
    "🔥 Predict Fire Risk",
    type="primary"
):

    input_data = pd.DataFrame(
        [{
            "temperature_c": temperature,
            "relative_humidity": humidity,
            "precipitation_mm": precipitation,
            "wind_speed_ms": wind_speed,
            "latitude_grid": latitude,
            "longitude_grid": longitude,
            "month": month,
            "day_of_year": day_of_year
        }]
    )

    input_data = input_data[features]

    probability = model.predict_proba(
        input_data
    )[0][1]

    probability_percent = probability * 100

    if probability < 0.25:
        risk = "LOW"

    elif probability < 0.50:
        risk = "MODERATE"

    elif probability < 0.75:
        risk = "HIGH"

    else:
        risk = "EXTREME"

    st.subheader("Prediction Result")

    st.metric(
        "Estimated Fire Probability",
        f"{probability_percent:.2f}%"
    )

    if risk == "LOW":
        st.success("🟢 LOW RISK")

    elif risk == "MODERATE":
        st.info("🟡 MODERATE RISK")

    elif risk == "HIGH":
        st.warning("🟠 HIGH RISK")

    else:
        st.error("🔴 EXTREME RISK")

    st.caption(
        "This prediction comes from the project's baseline "
        "Random Forest model and is not an official emergency warning."
    )

# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

st.divider()

st.header("🧠 Model Information")

st.write("**Algorithm:** Random Forest Classifier")
st.write("**Training data:** ERA5-Land + VIIRS 2024")
st.write("**Baseline test accuracy:** 90.13%")
st.write("**Baseline recall:** 94.88%")
st.write("**Baseline F1 score:** 92.12%")

st.warning(
    "These metrics come from the project's random train/test split. "
    "Further spatial and temporal validation is required before "
    "interpreting them as real-world forecasting performance."
)

st.divider()

st.caption(
    "ClimateGuard AI | Experimental Wildfire Risk Analysis Project"
)