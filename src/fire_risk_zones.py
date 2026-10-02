import pandas as pd

# Load processed NASA FIRMS data
file_path = "data/processed/india_viirs_fires_2024.csv"

print("Loading ClimateGuard fire data...")

data = pd.read_csv(file_path)

print("Total detections:", len(data))

# --------------------------------
# Create geographic grid cells
# --------------------------------

grid_size = 0.5

data["lat_grid"] = (
    data["latitude"] / grid_size
).round() * grid_size

data["lon_grid"] = (
    data["longitude"] / grid_size
).round() * grid_size

# Count detections in each grid
risk_zones = (
    data.groupby(["lat_grid", "lon_grid"])
    .size()
    .reset_index(name="fire_count")
)

# Sort highest fire-density areas first
risk_zones = risk_zones.sort_values(
    "fire_count",
    ascending=False
)
# Calculate thresholds
q50 = risk_zones["fire_count"].quantile(0.50)
q75 = risk_zones["fire_count"].quantile(0.75)
q90 = risk_zones["fire_count"].quantile(0.90)

# Assign risk level
def assign_risk(count):
    if count <= q50:
        return "LOW"
    elif count <= q75:
        return "MODERATE"
    elif count <= q90:
        return "HIGH"
    else:
        return "EXTREME"

risk_zones["risk_level"] = risk_zones["fire_count"].apply(assign_risk)

print("\n🔥 TOP 10 FIRE HOTSPOT ZONES 🔥\n")

print(risk_zones.head(10).to_string(index=False))

# Save result
output_file = "data/processed/fire_risk_zones_2024.csv"

risk_zones.to_csv(output_file, index=False)

print("\nRisk-zone dataset created successfully!")
print("Saved to:", output_file)