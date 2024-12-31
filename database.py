import sqlite3

conn = sqlite3.connect('states_of_the_world.db')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    capital TEXT,
    population INTEGER,
    density REAL,
    area REAL,
    neighbors TEXT,
    language TEXT,
    timezone TEXT,
    regime TEXT
)''')

conn.commit()
