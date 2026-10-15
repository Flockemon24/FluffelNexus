"""FluffelNexus entry point."""
from pathlib import Path
from dotenv import load_dotenv
from database import init_db
from gui import start_gui

def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")
    init_db()
    start_gui()

if __name__ == "__main__":
    main()
