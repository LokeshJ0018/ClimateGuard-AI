import cdsapi

print("Connecting to Copernicus Climate Data Store...")

client = cdsapi.Client()

dataset = "reanalysis-era5-land"

request = {
    "variable": [
        "2m_temperature"
    ],
    "year": "2024",
    "month": "01",
    "day": ["01"],
    "time": [
        "00:00",
        "06:00",
        "12:00",
        "18:00"
    ],
    "data_format": "netcdf",
    "download_format": "unarchived",

    # North, West, South, East
    "area": [
        38,
        68,
        6,
        98
    ]
}

output_file = "data/raw/weather/era5land_test_2024_01_01.nc"

print("Requesting test ERA5-Land temperature data...")

client.retrieve(
    dataset,
    request,
    output_file
)

print("Weather test download completed! 🌦️")
print("Saved to:", output_file)