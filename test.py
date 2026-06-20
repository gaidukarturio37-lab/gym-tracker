import sqlite3
from db_init import get_connection
connection = get_connection()


cursor = connection.cursor()


cursor.execute("Select * from users")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

connection.commit()
connection.close()
