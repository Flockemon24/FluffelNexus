import time
import schedule
import asyncio

from briefing.generator import send_daily_briefing

def run_daily_briefing():
    asyncio.run(send_daily_briefing("Hattingen"))

def schedule_daily_briefing(time_str):
    schedule.every().day.at(time_str).do(run_daily_briefing)

    while True:
        schedule.run_pending()
        time.sleep(60)