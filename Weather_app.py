import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

#Function to get weather data for the UK
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 51.5085,
	"longitude": -0.1257,
	"hourly": ["temperature_2m"],
	"models": "ukmo_seamless",
	"timezone": "auto"
}
responses = openmeteo.weather_api(url, params=params)
#process the UK weather data
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m

hourly_dataframe = pd.DataFrame(data = hourly_data)
print("You can search for a maximum of 7 days, how many days would you like to see?")
user_dates=int(input())
# Check if the user input is within the allowed range
while True:
    if user_dates <= 7:
        user_dates = user_dates * 24
        for i in range(user_dates):
            print(f"Date: {hourly_dataframe['date'][i]:.%Y-%m-%d %H:%M}:\n Temperature: {hourly_dataframe['temperature_2m'][i]:.2f}°C")
        break
    else:
        print("You can only search for a maximum of 7 days, please try again.")