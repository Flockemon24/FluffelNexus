from telegram import Bot
import os

from briefing.news import get_current_news
from briefing.weather import get_weather

def generate_message(city):
    weather_data = get_weather(city)
    temperature = weather_data.get("main", {}).get("temp", "No temperature data")
    max_temperature = weather_data.get("main", {}).get("temp_max", "No max temperature data")
    min_temperature = weather_data.get("main", {}).get("temp_min", "No min temperature data")

    news_articles = get_current_news()

    message = (
        "Good morning Boss ☀️!\n\n"
        f"Here is your daily brifing:\n\n"
        f"--- Weather in {city} ---\n"
        f"Current temperature: {temperature}°C\n"
        f"Maximum temperature for today: {max_temperature}°C\n"
        f"Minimum temperature for today: {min_temperature}°C\n\n"
        "--- Current News ---\n"
    )
    for art in news_articles:
        message += f"- {art['title']}\n - {art['url']}\n\n"
    return message


async def send_daily_briefing(city):
    message = generate_message(city)
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=message)
