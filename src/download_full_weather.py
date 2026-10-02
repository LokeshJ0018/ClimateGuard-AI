import cdsapi
import os
import calendar

client = cdsapi.Client()

output_dir = "data/raw/weather"
os.makedirs(output_dir, exist_ok=True)

dataset = "reanalysis-era5-land"

# Weather features useful for wildfire-risk modelling
variables = [
    "2m_temperature",
    "2m_dewpoint_temperature",
    "total_precipitation",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind"
]

year = "2024"

# India bounding box:
# North, West, South, East
area = [37.5, 68.0, 6.5, 97.5]

times = [f"{hour:02d}:00" for hour in range(24)]

print("CLIMATEGUARD AI - ERA5-LAND WEATHER DOWNLOAD")
print("Downloading 2024 weather data month-by-month...")

for month in range(1, 13):

    month_str = f"{month:02d}"
    days_in_month = calendar.monthrange(int(year), month)[1]
    days = [f"{day:02d}" for day in range(1, days_in_month + 1)]

    output_file = os.path.join(
        output_dir,
        f"era5land_india_{year}_{month_str}.nc"
    )

    if os.path.exists(output_file):
        print(f"\nMonth {month_str} already exists - skipping.")
        continue

    print(f"\nDownloading {year}-{month_str}...")

    request = {
        "variable": variables,
        "year": year,
        "month": month_str,
        "day": days,
        "time": times,
        "area": area,
        "data_format": "netcdf",
        "download_format": "unarchived"
    }

    try:
        client.retrieve(
            dataset,
            request,
            output_file
        )

        print(f"Completed: {output_file}")

    except Exception as error:
        print(f"ERROR downloading month {month_str}:")
        print(error)
        print("Stopping download. You can run the script again later.")
        break

print("\nClimateGuard weather download process finished.")