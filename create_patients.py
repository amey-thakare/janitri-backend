import sqlite3

conn = sqlite3.connect("janitri.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gestational_week INTEGER
)
""")

patients = [
    ("P123", "Anita Sharma", 28, 32),
    ("P124", "Priya Singh", 30, 35),
    ("P125", "Sarah Khan", 26, 29)
]

cursor.executemany("""
INSERT OR IGNORE INTO patients
VALUES (?, ?, ?, ?)
""", patients)

conn.commit()
conn.close()

print("Patients table created")