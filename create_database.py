import sqlite3


def create_database():
    """
    Create a SQLite database used for storing the scraped information
    from Wikipedia about countries. A country is represented by a name,
    capital, population, density, area, neighbors, language, timezone and
    regime.
    """
    conn = sqlite3.connect('states_of_the_world.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        capital TEXT,
        population INTEGER,
        density INTEGER,
        area INTEGER,
        neighbors TEXT,
        languages TEXT,
        timezone TEXT,
        regime TEXT
    )''')

    conn.commit()
