from telegram import Bot
import os

from briefing.news import get_current_news
from briefing.weather import get_weather

def generate_message(city="Berlin", language="de", sources="tagesschau.de", unit="metric"):
    weather_data = get_weather(city, units=unit, lang=language)
    temperature = weather_data.get("main", {}).get("temp", "No temperature data")
    max_temperature = weather_data.get("main", {}).get("temp_max", "No max temperature data")
    min_temperature = weather_data.get("main", {}).get("temp_min", "No min temperature data")

    news_articles = get_current_news(language=language, domains=sources)

    message = (
        "Good morning Boss ☀️!\n\n"
        f"Here is your daily brifing:\n\n"
        f"--- Weather in {city} ---\n"
        f"Current temperature: {temperature}\n"
        f"Maximum temperature for today: {max_temperature}\n"
        f"Minimum temperature for today: {min_temperature}\n\n"
        "--- Current News ---\n"
    )
    for art in news_articles:
        message += f"- {art['title']}\n - {art['url']}\n\n"
    return message


async def send_daily_briefing(city="Berlin", language="de", news_sources="tagesschau.de", unit="metirc"):
    message = generate_message(city=city, language=language, sources=news_sources, unit=unit)
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=message)
