import time
import schedule
import asyncio
import sys

from briefing.generator import send_daily_briefing

time_str = sys.argv[1]
city = sys.argv[2]
language = sys.argv[3]
news_sources = sys.argv[4]
weather_unit = sys.argv[5]

def run_daily_briefing(city="Berlin", language="de", news_sources="tagesschau.de", unit="metric"):
    asyncio.run(send_daily_briefing(city=city, language=language, news_sources=news_sources, unit=unit))
    time.sleep(1)

if __name__ == '__main__':
    schedule.every().day.at(time_str).do(run_daily_briefing, city=city, language=language, news_sources=news_sources, unit=weather_unit)
    while True:
        schedule.run_pending()
        time.sleep(5)
        