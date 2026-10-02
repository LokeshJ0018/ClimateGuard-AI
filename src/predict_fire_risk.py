import pandas as pd
import joblib
import os

print("🔥 CLIMATEGUARD AI - FIRE RISK PREDICTION")
print("=" * 50)

# ---------------------------------------
# 1. Load trained model
# ---------------------------------------

model_file = "models/climateguard_random_forest.pkl"

saved = joblib.load(model_file)

model = saved["model"]
features = saved["features"]

print("Model loaded successfully! ✅")

# ---------------------------------------
# 2. Load ML dataset
# ---------------------------------------

data_file = "data/processed/climateguard_training_data.csv"

print("\nLoading prediction data...")

data = pd.read_csv(data_file)

print(f"Records loaded: {len(data):,}")

# ---------------------------------------
# 3. Prepare features
# ---------------------------------------

X = data[features]

# ---------------------------------------
# 4. Predict probability
# ---------------------------------------

print("\nCalculating fire probabilities...")

data["fire_probability"] = model.predict_proba(X)[:, 1]

# Convert 0-1 probability to percentage
data["fire_probability_percent"] = (
    data["fire_probability"] * 100
).round(2)

# ---------------------------------------
# 5. Convert probability into risk level
# ---------------------------------------

def get_risk_level(probability):

    if probability < 0.25:
        return "LOW"

    elif probability < 0.50:
        return "MODERATE"

    elif probability < 0.75:
        return "HIGH"

    else:
        return "EXTREME"


data["risk_level"] = data["fire_probability"].apply(
    get_risk_level
)

# ---------------------------------------
# 6. Sort highest risk first
# ---------------------------------------

data = data.sort_values(
    "fire_probability",
    ascending=False
)

# ---------------------------------------
# 7. Save predictions
# ---------------------------------------

os.makedirs("results", exist_ok=True)

output_file = "results/climateguard_fire_risk_predictions.csv"

data.to_csv(
    output_file,
    index=False
)

# ---------------------------------------
# 8. Display summary
# ---------------------------------------

print("\n🔥 RISK DISTRIBUTION")
print(data["risk_level"].value_counts())

print("\n🔥 TOP 10 HIGHEST-RISK LOCATIONS")

columns = [
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

print(
    data[columns]
    .head(10)
    .to_string(index=False)
)

print("\n✅ FIRE RISK PREDICTION COMPLETED")
print("Saved to:", output_file)