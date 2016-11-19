"""Set up SQLite3 database to store simulations before they're run."""

import sqlite3

def init_db():
    """Initialize the simulations database

    Fields:
        simulation TEXT
        callback_url TEXT
    """
    conn = sqlite3.connect('simulations.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS simulations(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        simulation TEXT NOT NULL,
        user_id TEXT NOT NULL,
        board_name TEXT)''')

    conn.commit()

    conn.close()

if __name__ == '__main__':
    init_db()
