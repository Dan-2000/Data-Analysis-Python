import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"


def city():
	user_city = input("Please enter your city: ")
	# Use the Open-Meteo API to get the coordinates of the user's city
	geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
	geocode_params = {
		"name": user_city,
		"latitude": 0,  # Placeholder, will be replaced by actual coordinates
		"longitude": 0,  # Placeholder, will be replaced by actual coordinates
		"count": 1,  # Limit to one result
		"format": "json"
		}
	response = openmeteo.weather_api(geocode_url, params=geocode_params)
	if response:
		location = response[0]
		return user_params(lon= location.Latitude(), lat=location.Longitude())
	else:
		print("City not found. Please try again.")
		return city()
#Function to change the URL of the Open-Meteo API to the user's city of choice
def user_params(lon, lat):
	# Set the parameters for the Open-Meteo API request
	# The parameters include latitude, longitude, hourly temperature data, model, and timezone
	params = {
		"latitude": lon,
		"longitude": lat,
		"hourly": ["temperature_2m"],
		"models": "ukmo_seamless",
		"timezone": "auto"
	}

responses = openmeteo.weather_api(url, params=params)
#process the Users City weather data
response = responses[0]
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

def menu():
	print("Welcome to the Weather App! Please select an option: \n1. Get current weather \n2. Get weather forecast \n3. Exit")
	get_user_choice_logic()

# Function to print weather data and convert user input to hours
def print_weather_data(user_dates:int):
	user_dates = user_dates * 24  # Convert days to hours
	for i in range(user_dates):
		print(f"Date: {hourly_dataframe['date'][i]:%Y-%m-%d %H:%M}, Temperature: {hourly_dataframe['temperature_2m'][i]:.2f}°C")
	print("Returning to main menu...")
	menu()
# Function to handle user choice and logic
def get_user_choice_logic():
	while True:
		user_choice = int(input())
		if user_choice == 1:
			print("You selected option 1: Get current weather")
			print_weather_data(1)  # Default to 1 day for current weather
		elif user_choice == 2:
			print("You selected option 2: Get weather forecast")
			user_dates = int(input("How many days of forecast would you like to see? (max 7): "))
			if user_dates > 7:
				print("You can only search for a maximum of 7 days, setting to 7 days.")
				print_weather_data(7)
			elif user_dates <= 7:
				print_weather_data(user_dates)
			elif user_dates <= 0:
				print("You have selected 0 days, we have defaulted you to 1 day.")
				print_weather_data(1)
		elif user_choice == 3:
			print("Exiting the Weather App. Goodbye!")
			exit()
			break
		else:
			print("Invalid choice. Please try again.")
			return menu()

def main():
	city()
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
	menu()
main()
