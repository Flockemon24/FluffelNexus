import requests
import os

def get_weather(city, units="metric", lang="en"):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}"
    response = requests.get(url)
    return response.json()