"""Create and send the daily Telegram briefing."""
import os
import requests
from telegram import Bot
from briefing.news import get_current_news
from briefing.weather import get_weather

def generate_message(city="Berlin", language="de", sources="tagesschau.de", unit="metric"):
    symbol = {"metric": "°C", "imperial": "°F", "standard": "K"}.get(unit, "°C")
    try:
        data = get_weather(city, units=unit, lang=language)
        main = data.get("main", {})
        lines = []
        description = (data.get("weather") or [{}])[0].get("description", "")
        if description:
            lines.append("Conditions: " + description)
        for label, key in (("Current temperature", "temp"), ("Today's maximum", "temp_max"), ("Today's minimum", "temp_min")):
            value = main.get(key)
            lines.append(f"{label}: {value}{symbol}" if value is not None else f"{label}: unavailable")
    except (RuntimeError, ValueError, KeyError, requests.RequestException) as exc:
        lines = [f"Weather information is unavailable: {exc}"]
    articles = get_current_news(language=language, domains=sources)
    message = ["Good morning! ☀️", "Here is your daily briefing:", "", f"--- Weather in {city} ---", *lines, "", "--- Current News ---"]
    if articles:
        for article in articles:
            source = (article.get("source") or {}).get("name")
            message.extend([f"• [{'{}] '.format(source) if source else ''}{article.get('title', 'Untitled article')}", article.get("url", ""), ""])
    else:
        message.append("No news articles are available right now.")
    return "\n".join(message).strip()[:4000]

async def send_daily_briefing(city="Berlin", language="de", news_sources="tagesschau.de", unit="metric"):
    token, chat_id = os.getenv("TELEGRAM_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set.")
    message = generate_message(city, language, news_sources, unit)
    async with Bot(token=token) as bot:
        await bot.send_message(chat_id=chat_id, text=message)
