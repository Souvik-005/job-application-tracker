import sqlite3
from .models import Application, Status

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

def add_application(app, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cursor = conn.execute(
        """
        INSERT INTO applications
            (company, title, status, job_url, contact, notes, follow_up_date, date_applied)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            app.company,
            app.title,
            app.status.value,
            app.job_url,
            app.contact,
            app.notes,
            app.follow_up_date,
            app.date_applied,
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def _row_to_application(row):
    return Application(
        id=row["id"],
        company=row["company"],
        title=row["title"],
        status=Status(row["status"]),
        job_url=row["job_url"],
        contact=row["contact"],
        notes=row["notes"],
        follow_up_date=row["follow_up_date"],
        date_applied=row["date_applied"],
    )

def get_all_applications(db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM applications ORDER BY id").fetchall()
    conn.close()
    return [_row_to_application(row) for row in rows]

def get_application(app_id, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    row = conn.execute(
        "SELECT * FROM applications WHERE id = ?", (app_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return _row_to_application(row)

def update_status(app_id, new_status, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cursor = conn.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (new_status.value, app_id),   
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def delete_application(app_id, db_path=DEFAULT_DB):
    conn = get_connection(db_path)
    cursor = conn.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,),
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted