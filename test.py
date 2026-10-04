from briefing.generator import send_daily_briefing
import dotenv
import asyncio

dotenv.load_dotenv()

asyncio.run(send_daily_briefing("Hattingen"))