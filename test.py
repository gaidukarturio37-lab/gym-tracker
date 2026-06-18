import sqlite3
from db_init import get_connection
connection = get_connection()

import sqlite3
db_path = "C:/MyPythonProjects/gym_tracker/tracker.db"
conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()


cursor.execute("Select * from users")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

conn.commit()
conn.close()
