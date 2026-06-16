# check_db.py

import sqlite3

conn = sqlite3.connect("janitri.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM predictions")

for row in cursor.fetchall():
    print(row)

conn.close()