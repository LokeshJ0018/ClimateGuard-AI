import pandas as pd
import matplotlib.pyplot as plt

file_path = "data/processed/india_viirs_fires_2024.csv"

print("Loading ClimateGuard fire data...")

data = pd.read_csv(file_path)

print("Total detections:", len(data))

plt.figure(figsize=(8, 10))

plt.scatter(
    data["longitude"],
    data["latitude"],
    s=1,
    alpha=0.25
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("VIIRS Fire/Hotspot Detections in India - 2024")

plt.xlim(68, 98)
plt.ylim(6, 38)

plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    "results/india_fire_hotspots_2024.png",
    dpi=300
)

plt.show()

print("Hotspot map created successfully! 🔥🗺️")