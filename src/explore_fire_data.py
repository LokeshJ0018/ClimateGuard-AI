import pandas as pd
import matplotlib.pyplot as plt

file_path = "data/processed/india_viirs_fires_2024.csv"

print("Loading processed ClimateGuard data...")

data = pd.read_csv(file_path)

# Count fire detections for each month
monthly_fires = data.groupby("month").size()

print("\n🔥 Fire detections by month:")
print(monthly_fires)

# Create graph
plt.figure(figsize=(10, 5))

plt.bar(monthly_fires.index, monthly_fires.values)

plt.xlabel("Month")
plt.ylabel("Number of Fire Detections")
plt.title("India VIIRS Fire Detections by Month - 2024")

plt.xticks(range(1, 13))

plt.tight_layout()

# Save graph
plt.savefig("results/monthly_fire_detections_2024.png")

plt.show()

print("\nGraph saved successfully! 📊🔥")