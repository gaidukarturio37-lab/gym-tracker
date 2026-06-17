import sqlite3
from db_init import get_connection
connection = get_connection()

import sqlite3

connection = sqlite3.connect("tracker.db")
cursor = connection.cursor()

# Удаляем записи, где дата не похожа на формат даты (например, состоит из цифр и точек)
# Это удалит все, где в дате записан вес
cursor.execute("DELETE FROM body_metrics WHERE date LIKE '%91.19%' OR date LIKE '%.%'")

# Если ты хочешь вообще видеть, что там происходит:
cursor.execute("SELECT * FROM body_metrics")
print("Осталось в базе:", cursor.fetchall())

connection.commit()
connection.close()
