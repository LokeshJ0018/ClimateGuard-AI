import geopandas as gpd

file_path = "data/raw/fire_archive_SV-C2_804514.shp"

print("Loading NASA FIRMS wildfire data...")

data = gpd.read_file(file_path)

print("\nDataset loaded successfully! 🔥🌍")

print("\nNumber of fire detections:")
print(len(data))

print("\nColumns:")
print(data.columns.tolist())

print("\nFirst 5 records:")
print(data.head())
