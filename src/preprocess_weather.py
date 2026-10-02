import xarray as xr
import pandas as pd
import numpy as np
import glob
import os

print("🌦️ CLIMATEGUARD AI - WEATHER PREPROCESSING")
print("=" * 50)

weather_files = sorted(
    glob.glob("data/raw/weather/era5land_india_2024_*.nc")
)

output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

monthly_results = []

print(f"Weather files found: {len(weather_files)}")

for file in weather_files:

    print(f"\nProcessing: {file}")

    ds = xr.open_dataset(file)

    # Temperature: Kelvin -> Celsius
    temp_c = ds["t2m"] - 273.15

    # Dew point: Kelvin -> Celsius
    dew_c = ds["d2m"] - 273.15

    # Approximate relative humidity from temperature + dew point
    rh = 100 * (
        np.exp((17.625 * dew_c) / (243.04 + dew_c))
        /
        np.exp((17.625 * temp_c) / (243.04 + temp_c))
    )

    rh = rh.clip(min=0, max=100)

    # Wind speed from U/V components
    wind_speed = np.sqrt(ds["u10"] ** 2 + ds["v10"] ** 2)

    # Build weather dataset
    weather = xr.Dataset({
        "temperature_c": temp_c,
        "relative_humidity": rh,
        "precipitation_m": ds["tp"],
        "wind_speed_ms": wind_speed
    })

    # Convert hourly values -> daily values
    daily = xr.Dataset({
    "temperature_c": weather["temperature_c"].resample(valid_time="1D").mean(),
    "relative_humidity": weather["relative_humidity"].resample(valid_time="1D").mean(),
    "precipitation_m": weather["precipitation_m"].resample(valid_time="1D").sum(),
    "wind_speed_ms": weather["wind_speed_ms"].resample(valid_time="1D").mean()
    })
    # Convert precipitation metres -> millimetres
    daily["precipitation_mm"] = daily["precipitation_m"] * 1000
    daily = daily.drop_vars("precipitation_m")

    # Convert to dataframe
    df = daily.to_dataframe().reset_index()

    monthly_results.append(df)

    ds.close()

    print(f"Completed: {len(df):,} daily grid records")

print("\nCombining all months...")

weather_df = pd.concat(monthly_results, ignore_index=True)

output_file = "data/processed/india_weather_2024.csv"

weather_df.to_csv(output_file, index=False)

print("\n✅ WEATHER PREPROCESSING COMPLETED")
print(f"Rows: {len(weather_df):,}")
print(f"Saved to: {output_file}")

print("\nColumns:")
print(weather_df.columns.tolist())
