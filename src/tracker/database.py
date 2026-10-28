import sqlite3

DEFAULT_DB = "applications.db"

def get_connection(db_path=DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DEFAULT_DB):
    conn=get_connection(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'applied',
            job_url TEXT,
            contact TEXT,
            notes TEXT,
            follow_up_date TEXT,
            date_applied TEXT
        )
    """)
    conn.commit()
    conn.close()
    