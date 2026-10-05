import sqlite3

def init_db():
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            briefing_time TEXT NOT NULL, 
            language TEXT NOT NULL,
            news_sources TEXT,
            weather_units TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()