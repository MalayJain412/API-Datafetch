import requests
import pandas as pd
from datetime import datetime, timedelta

# Define API Key and Location
API_KEY = "617d22d5b7cf4b05889194950250502"  # Replace with your actual API key
LOCATION = "Delhi,IN"
BASE_URL = "http://api.weatherapi.com/v1/history.json"

# Define start and end dates
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 2, 6)

# API allows a maximum of 35 days per request
chunk_size = 35
current_date = start_date

# List to store data
all_data = []

# Loop to fetch data in 35-day chunks
while current_date <= end_date:
    next_date = min(current_date + timedelta(days=chunk_size - 1), end_date)
    
    # Construct API URL
    url = f"{BASE_URL}?key={API_KEY}&q={LOCATION}&dt={current_date.strftime('%Y-%m-%d')}&end_dt={next_date.strftime('%Y-%m-%d')}"
    
    # Fetch data
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "forecast" in data:
            for day in data["forecast"]["forecastday"]:
                all_data.append({
                    "date": day["date"],
                    "max_temp": day["day"]["maxtemp_c"],
                    "min_temp": day["day"]["mintemp_c"],
                    "humidity": day["day"]["avghumidity"],
                    "precipitation": day["day"]["totalprecip_mm"],
                    "condition": day["day"]["condition"]["text"],
                    "uv_index": day["day"]["uv"]
                })
    else:
        print(f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')} to {next_date.strftime('%Y-%m-%d')}")

    # Move to the next chunk
    current_date = next_date + timedelta(days=1)

# Convert to DataFrame
df = pd.DataFrame(all_data)

# # Output for Power BI
# print(df)

# Save to CSV
df.to_csv("Delhi_Weather_History.csv", index=False)

# Save to Excel
df.to_excel("Delhi_Weather_History.xlsx", index=False)

print("Data saved successfully!")
