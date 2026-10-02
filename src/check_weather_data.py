import xarray as xr

file_path = "data/raw/weather/era5land_india_2024_01.nc"

print("Loading ERA5-Land weather data...")

data = xr.open_dataset(file_path)

print("\n🌦️ CLIMATEGUARD AI - WEATHER DATA CHECK 🌦️")
print(data)

print("\nVariables:")
for variable in data.data_vars:
    print("-", variable)

print("\nCoordinates:")
for coordinate in data.coords:
    print("-", coordinate)

print("\nWeather data loaded successfully! ✅")