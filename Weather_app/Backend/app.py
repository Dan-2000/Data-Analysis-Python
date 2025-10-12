from flask import Flask, request, jsonify,render_template
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# --- Setup the Open-Meteo API client (same as your code) ---
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://api.open-meteo.com/v1/forecast"

app = Flask(__name__)

# --- Function to get city coordinates ---
def get_city_coords(city_name):
    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "format": "json"}
    response = retry_session.get(geocode_url, params=params)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        loc = data["results"][0]
        return loc["latitude"], loc["longitude"]
    return None, None

# --- Function to fetch weather data (from your user_params) ---
def get_weather_data(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m"],
        "models": "ukmo_seamless",
        "timezone": "auto",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "temperature_2m": hourly_temperature_2m,
    }

    df = pd.DataFrame(data=hourly_data)
    return df, response


# --- Flask API route ---
@app.route("/api/weather")
def home():
    return(render_template("index.html"))

def weather_api():
    # Get parameters from the URL: /api/weather?city=London&days=3
    city = request.args.get("city")
    days = int(request.args.get("days", 1))  # default = 1 day

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    lat, lon = get_city_coords(city)
    if lat is None:
        return jsonify({"error": "City not found"}), 404

    df, response = get_weather_data(lat, lon)

    # Limit results to requested number of days
    hours = days * 24
    df = df.head(hours)

    # Convert to JSON
    result = {
        "city": city,
        "coordinates": {"lat": lat, "lon": lon},
        "elevation": response.Elevation(),
        "timezone": response.Timezone(),
        "timezone_abbr": response.TimezoneAbbreviation(),
        "utc_offset": response.UtcOffsetSeconds(),
        "forecast": [
            {"date": str(df["date"][i]), "temperature": float(df["temperature_2m"][i])}
            for i in range(len(df))
        ],
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
