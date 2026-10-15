"""Daily briefing scheduler."""
import argparse
import asyncio
import logging
import time
from datetime import datetime
from pathlib import Path
import schedule
from dotenv import load_dotenv
from briefing.generator import send_daily_briefing

BASE_DIR = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("fluffelnexus")

def run_daily_briefing(city, language, news_sources, unit):
    try:
        asyncio.run(send_daily_briefing(city=city, language=language, news_sources=news_sources, unit=unit))
        log.info("Briefing sent successfully.")
    except Exception:
        log.exception("Failed to send briefing.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("time", help="Local time HH:MM")
    parser.add_argument("city")
    parser.add_argument("language", choices=("de", "en"))
    parser.add_argument("news_sources")
    parser.add_argument("weather_unit", choices=("metric", "imperial", "standard"))
    args = parser.parse_args()
    try:
        datetime.strptime(args.time, "%H:%M")
    except ValueError:
        parser.error("time must use HH:MM format")
    load_dotenv(BASE_DIR / ".env")
    schedule.every().day.at(args.time).do(run_daily_briefing, city=args.city, language=args.language, news_sources=args.news_sources, unit=args.weather_unit)
    log.info("Daily briefing scheduled for %s local time.", args.time)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
