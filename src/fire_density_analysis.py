import pandas as pd
import matplotlib.pyplot as plt

# Load processed fire dataset
file_path = "data/processed/india_viirs_fires_2024.csv"

print("Loading ClimateGuard fire data...")

data = pd.read_csv(file_path)

print("Total detections:", len(data))

# Create fire density heatmap
plt.figure(figsize=(8, 10))

plt.hexbin(
    data["longitude"],
    data["latitude"],
    gridsize=80,
    bins="log",
    mincnt=1,
    cmap="hot"
)

plt.colorbar(label="Log Fire Detection Density")

plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.title(
    "ClimateGuard AI - Fire Hotspot Density\nIndia VIIRS 2024"
)

plt.xlim(68, 98)
plt.ylim(6, 38)

plt.tight_layout()

# Save result
plt.savefig(
    "results/india_fire_density_2024.png",
    dpi=300
)

plt.show()

print("Fire density analysis completed! 🔥")