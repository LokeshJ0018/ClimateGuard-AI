import geopandas as gpd
import pandas as pd

input_file = "data/raw/fire_archive_SV-C2_804514.shp"
output_file = "data/processed/india_viirs_fires_2024.csv"

print("Loading NASA FIRMS data...")

data = gpd.read_file(input_file)

# Standardize column names
data.columns = data.columns.str.lower()

# Convert date
data["acq_date"] = pd.to_datetime(data["acq_date"])

# Create useful date features
data["year"] = data["acq_date"].dt.year
data["month"] = data["acq_date"].dt.month
data["day"] = data["acq_date"].dt.day
data["day_of_year"] = data["acq_date"].dt.dayofyear

# Remove geometry because latitude/longitude already exist
data = data.drop(columns=["geometry"])

# Sort chronologically
data = data.sort_values(["acq_date", "acq_time"])

# Save processed dataset
data.to_csv(output_file, index=False)

print("\nProcessed dataset created! 🔥")
print("Rows:", len(data))
print("Columns:", len(data.columns))
print("Saved to:", output_file)