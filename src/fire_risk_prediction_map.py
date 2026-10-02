import pandas as pd
import matplotlib.pyplot as plt
import os

print("🔥 CLIMATEGUARD AI - FIRE RISK MAP")
print("=" * 50)

# ---------------------------------------
# 1. Load prediction results
# ---------------------------------------

input_file = "results/climateguard_fire_risk_predictions.csv"

print("\nLoading fire-risk predictions...")

data = pd.read_csv(input_file)

print(f"Records loaded: {len(data):,}")

# ---------------------------------------
# 2. Reduce points for faster plotting
# ---------------------------------------

# Plot at most 100,000 points so the map remains manageable
if len(data) > 100000:
    plot_data = data.sample(
        n=100000,
        random_state=42
    )
else:
    plot_data = data.copy()

print(f"Points plotted: {len(plot_data):,}")

# ---------------------------------------
# 3. Create risk map
# ---------------------------------------

plt.figure(figsize=(9, 10))

scatter = plt.scatter(
    plot_data["longitude_grid"],
    plot_data["latitude_grid"],
    c=plot_data["fire_probability_percent"],
    cmap="YlOrRd",
    s=6,
    alpha=0.65,
    vmin=0,
    vmax=100
)

colorbar = plt.colorbar(scatter)

colorbar.set_label(
    "Predicted Fire Probability (%)"
)

plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.title(
    "ClimateGuard AI\n"
    "Predicted Fire-Risk Distribution - India 2024"
)

plt.xlim(68, 98)
plt.ylim(6, 38)

plt.grid(
    alpha=0.2
)

plt.tight_layout()

# ---------------------------------------
# 4. Save map
# ---------------------------------------

os.makedirs("results", exist_ok=True)

output_file = "results/climateguard_fire_risk_map.png"

plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

print("\n✅ FIRE RISK MAP CREATED")
print("Saved to:", output_file)

plt.show()