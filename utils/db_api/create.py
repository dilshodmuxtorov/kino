import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        username TEXT,
        fullname TEXT,
        registrated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    )
    """)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        video_id TEXT,
        caption TEXT
    )
    ''')

    conn.commit()
    conn.close()