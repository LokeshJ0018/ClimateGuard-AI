import geopandas as gpd

file_path = "data/raw/fire_archive_SV-C2_804514.shp"

print("Loading NASA FIRMS data...")
data = gpd.read_file(file_path)

print("\n🔥 CLIMATEGUARD AI - DATA QUALITY REPORT 🔥")

print("\n1. Dataset shape:")
print(data.shape)

print("\n2. Missing values:")
print(data.isnull().sum())

print("\n3. Duplicate rows:")
print(data.duplicated().sum())

print("\n4. Date range:")
print("Start:", data["ACQ_DATE"].min())
print("End:", data["ACQ_DATE"].max())

print("\n5. Confidence distribution:")
print(data["CONFIDENCE"].value_counts())

print("\n6. Day/Night distribution:")
print(data["DAYNIGHT"].value_counts())

print("\n7. FRP statistics:")
print(data["FRP"].describe())

print("\n8. Brightness statistics:")
print(data["BRIGHTNESS"].describe())

print("\nAnalysis completed! 🌍🔥")