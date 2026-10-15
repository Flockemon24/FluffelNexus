"""SQLite settings persistence."""
from pathlib import Path
import sqlite3
DB_PATH = Path(__file__).resolve().parent / "db.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL, briefing_time TEXT NOT NULL, language TEXT NOT NULL,
            lang_code TEXT NOT NULL, news_sources TEXT NOT NULL, weather_units TEXT NOT NULL)""")

def load_settings():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT name, city, briefing_time, language, lang_code, news_sources, weather_units FROM user ORDER BY id DESC LIMIT 1").fetchone()
        return dict(row) if row else None

def save_settings(settings):
    fields = ("name", "city", "briefing_time", "language", "lang_code", "news_sources", "weather_units")
    missing = [f for f in fields if f not in settings]
    if missing:
        raise ValueError("Missing settings: " + ", ".join(missing))
    values = tuple(settings[f] for f in fields)
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT id FROM user ORDER BY id DESC LIMIT 1").fetchone()
        if row:
            conn.execute("UPDATE user SET name=?, city=?, briefing_time=?, language=?, lang_code=?, news_sources=?, weather_units=? WHERE id=?", (*values, row[0]))
        else:
            conn.execute("INSERT INTO user (name, city, briefing_time, language, lang_code, news_sources, weather_units) VALUES (?, ?, ?, ?, ?, ?, ?)", values)
