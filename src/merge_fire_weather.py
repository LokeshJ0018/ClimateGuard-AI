import pandas as pd
import numpy as np

print("🔥🌦️ CLIMATEGUARD AI - FIRE + WEATHER MERGE")
print("=" * 55)

# Files
fire_file = "data/processed/india_viirs_fires_2024.csv"
weather_file = "data/processed/india_weather_2024.csv"
output_file = "data/processed/climateguard_ml_dataset_2024.csv"

print("\nLoading NASA fire data...")
fire = pd.read_csv(fire_file)

print("Fire rows:", len(fire))

print("\nLoading ERA5-Land weather data...")
weather = pd.read_csv(weather_file)

print("Weather rows:", len(weather))

# -------------------------------------------------
# 1. Prepare dates
# -------------------------------------------------

fire["date"] = pd.to_datetime(fire["acq_date"]).dt.normalize()

# Weather date column came from ERA5 valid_time
weather["date"] = pd.to_datetime(weather["valid_time"]).dt.normalize()

# -------------------------------------------------
# 2. Match NASA coordinates to ERA5 0.1° grid
# -------------------------------------------------

fire["latitude_grid"] = (fire["latitude"] * 10).round() / 10
fire["longitude_grid"] = (fire["longitude"] * 10).round() / 10

weather["latitude_grid"] = weather["latitude"].round(1)
weather["longitude_grid"] = weather["longitude"].round(1)

# Keep only required weather features
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

print("\nMerging fire observations with weather...")

merged = fire.merge(
    weather,
    on=["date", "latitude_grid", "longitude_grid"],
    how="left"
)

# -------------------------------------------------
# 3. Check matching quality
# -------------------------------------------------

matched = merged["temperature_c"].notna().sum()
total = len(merged)

match_rate = (matched / total) * 100

print(f"Matched fire records: {matched:,}/{total:,}")
print(f"Weather match rate: {match_rate:.2f}%")

# Remove unmatched rows
merged = merged.dropna(
    subset=[
        "temperature_c",
        "relative_humidity",
        "precipitation_mm",
        "wind_speed_ms"
    ]
)

# -------------------------------------------------
# 4. Create ML fire-risk target
# -------------------------------------------------

if "confidence" in merged.columns:

    confidence_numeric = pd.to_numeric(
        merged["confidence"],
        errors="coerce"
    )

    merged["fire_risk"] = np.select(
        [
            confidence_numeric < 50,
            (confidence_numeric >= 50) & (confidence_numeric < 70),
            (confidence_numeric >= 70) & (confidence_numeric < 90),
            confidence_numeric >= 90
        ],
        [
            "LOW",
            "MODERATE",
            "HIGH",
            "EXTREME"
        ],
        default="UNKNOWN"
    )

else:
    merged["fire_risk"] = "FIRE"

# -------------------------------------------------
# 5. Save ML-ready dataset
# -------------------------------------------------

merged.to_csv(output_file, index=False)

print("\n✅ FIRE + WEATHER MERGE COMPLETED")
print(f"Final rows: {len(merged):,}")
print(f"Saved to: {output_file}")

print("\nRisk distribution:")
print(merged["fire_risk"].value_counts())