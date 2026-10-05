import dotenv

from gui import start_gui
from briefing_scheduler import schedule_daily_briefing
from database import init_db

dotenv.load_dotenv()
init_db()

start_gui()