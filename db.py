import sqlite3
import os

DB_PATH = "database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payment_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contractor TEXT,
            description TEXT,
            work_period TEXT,
            amount REAL,
            status TEXT,
            submitted_by TEXT
        )
    """)
    conn.commit()
    conn.close()

def submit_payment_request(contractor, description, work_period, amount, email, files):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO payment_requests (contractor, description, work_period, amount, status, submitted_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (contractor, description, work_period, amount, "Pending", email))
    conn.commit()
    conn.close()

    # Save files locally
    os.makedirs("uploads", exist_ok=True)
    for f in files:
        with open(f"uploads/{f.name}", "wb") as out:
            out.write(f.read())

init_db()
