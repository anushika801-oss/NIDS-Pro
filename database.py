import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("nids.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        alert TEXT,
        severity TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()


def save_alert(alert, severity="Medium"):
    conn = sqlite3.connect("nids.db")
    cursor = conn.cursor()
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO alerts (time, alert, severity) VALUES (?, ?, ?)",
        (time_str, alert, severity)
    )
    conn.commit()
    conn.close()