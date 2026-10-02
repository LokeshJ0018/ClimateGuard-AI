import pandas as pd
import numpy as np

print("🔥 CLIMATEGUARD AI - BUILDING ML DATASET")
print("=" * 50)

fire_file = "data/processed/climateguard_ml_dataset_2024.csv"
weather_file = "data/processed/india_weather_2024.csv"

output_file = "data/processed/climateguard_training_data.csv"

# --------------------------------------------------
# 1. LOAD FIRE + WEATHER MATCHED DATA
# --------------------------------------------------

print("\nLoading fire observations...")

fire = pd.read_csv(fire_file)

fire["date"] = pd.to_datetime(fire["date"])

fire_samples = fire[
    [
        "date",
        "latitude_grid",
        "longitude_grid",
        "temperature_c",
        "relative_humidity",
        "precipitation_mm",
        "wind_speed_ms"
    ]
].copy()

fire_samples["fire"] = 1

# Remove duplicate fire observations from same grid/day
fire_samples = fire_samples.drop_duplicates(
    subset=["date", "latitude_grid", "longitude_grid"]
)

print("Unique fire samples:", len(fire_samples))

# --------------------------------------------------
# 2. LOAD WEATHER DATA
# --------------------------------------------------

print("\nLoading weather data...")

weather = pd.read_csv(weather_file)

weather["date"] = pd.to_datetime(weather["valid_time"]).dt.normalize()

weather["latitude_grid"] = weather["latitude"].round(1)
weather["longitude_grid"] = weather["longitude"].round(1)

weather = weather[
    [
        "date",
        "latitude_grid",
        "longitude_grid",
        "temperature_c",
        "relative_humidity",
        "precipitation_mm",
        "wind_speed_ms"
    ]
]

# --------------------------------------------------
# 3. REMOVE LOCATIONS/DAYS WHERE FIRE OCCURRED
# --------------------------------------------------

fire_keys = fire_samples[
    ["date", "latitude_grid", "longitude_grid"]
].copy()

fire_keys["has_fire"] = 1

weather = weather.merge(
    fire_keys,
    on=["date", "latitude_grid", "longitude_grid"],
    how="left"
)

non_fire_pool = weather[
    weather["has_fire"].isna()
].drop(columns=["has_fire"])

print("Available non-fire samples:", len(non_fire_pool))

# --------------------------------------------------
# 4. SAMPLE BALANCED NON-FIRE OBSERVATIONS
# --------------------------------------------------

n_non_fire = min(
    len(fire_samples),
    len(non_fire_pool)
)

non_fire_samples = non_fire_pool.sample(
    n=n_non_fire,
    random_state=42
).copy()

non_fire_samples["fire"] = 0

print("Selected non-fire samples:", len(non_fire_samples))

# --------------------------------------------------
# 5. COMBINE FIRE + NON-FIRE
# --------------------------------------------------

dataset = pd.concat(
    [fire_samples, non_fire_samples],
    ignore_index=True
)

# Add useful temporal features
dataset["month"] = dataset["date"].dt.month
dataset["day_of_year"] = dataset["date"].dt.dayofyear

# Remove invalid weather records
dataset = dataset.dropna(
    subset=[
        "temperature_c",
        "relative_humidity",
        "precipitation_mm",
        "wind_speed_ms"
    ]
)

# Shuffle
dataset = dataset.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# --------------------------------------------------
# 6. SAVE
# --------------------------------------------------

dataset.to_csv(output_file, index=False)

print("\n✅ ML TRAINING DATASET CREATED")
print("Total samples:", len(dataset))

print("\nClass distribution:")
print(dataset["fire"].value_counts())

print("\nSaved to:")
print(output_file)