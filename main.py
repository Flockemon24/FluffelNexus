# --- Imports ---
import dotenv

from gui import start_gui
from database import init_db

# load .env and db
dotenv.load_dotenv()
init_db()

# starting the ui
start_gui()