import sqlite3

conn = sqlite3.connect("janitri.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    device_id TEXT,
    sdp REAL,
    status TEXT,
    waveform TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")