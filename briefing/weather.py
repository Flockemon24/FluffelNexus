"""OpenWeatherMap API helper."""
import os
import requests
URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, units="metric", lang="en"):
    key = os.getenv("WEATHER_API_KEY")
    if not key:
        raise RuntimeError("WEATHER_API_KEY is not set in .env.")
    if not city or not city.strip():
        raise ValueError("A city is required.")
    if units not in {"standard", "metric", "imperial"}:
        raise ValueError("Unsupported weather unit.")
    response = requests.get(URL, params={"q": city.strip(), "appid": key, "units": units, "lang": lang}, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict) or str(data.get("cod")) != "200":
        raise RuntimeError(data.get("message", "Invalid weather API response") if isinstance(data, dict) else "Invalid weather API response")
    return data
