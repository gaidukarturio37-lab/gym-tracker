import sqlite3
from db_init import get_connection

connection = get_connection()
cursor = connection.cursor()
try:
    cursor.execute(
        """ INSERT INTO products (name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?) """,
        ("Куриная грудка сырая", 23.0, 1.7, 0.5, 110.0),
    )
    cursor.execute(
        """ INSERT INTO products (name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?) """,
        ("Сироп сахарный с наполнителями", 0.0, 0.0, 64.0, 255.0),
    )
    cursor.execute(
        """ INSERT INTO products (name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?) """,
        ("Творог брикет 5%", 16.0, 5.0, 3.6, 125.0),
    )
    cursor.execute(
        """ INSERT INTO products (name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?) """,
        ("Желе", 11.7, 0.0, 83.9, 390.0),
    )
    cursor.execute(
        """ INSERT INTO products (name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?) """,
        ("Зефир Стимул", 1.0, 0.09, 83.8, 348.0),
    )
    cursor.execute(
        """INSERT INTO body_metrics (date, weight, fat_weight) VALUES (?, ?, ?) """,
        ("2026-05-17", 90.7, 22.1),
    )
    cursor.execute(
        """INSERT INTO body_metrics (date, weight, fat_weight) VALUES (?, ?, ?) """,
        ("2026-05-18", 91.4, 22.5),
    )
    cursor.execute(
        """INSERT INTO body_metrics (date, weight, fat_weight) VALUES (?, ?, ?) """,
        ("2026-05-19", 91.2, 22.3),
    )
    last_date = cursor.execute("""SELECT MAX(date) FROM body_metrics""").fetchone()[0]
    cursor.execute(
        """INSERT INTO food_diary (date, product_id, amount) VALUES (?, ?, ?) """,
        (
            last_date,
            cursor.execute(
                """SELECT product_id FROM products WHERE name = 'Творог брикет 5%'"""
            ).fetchone()[0],
            360.0,
        ),
    )
    cursor.execute(
        """INSERT INTO food_diary (date, product_id, amount) VALUES (?, ?, ?) """,
        (
            last_date,
            cursor.execute(
                """SELECT product_id FROM products WHERE name = 'Зефир Стимул'"""
            ).fetchone()[0],
            85.0,
        ),
    )
    connection.commit()
    print("Данные успешно добавлены в базу данных.")
except sqlite3.Error as e:
    print(f"Ошибка при добавлении данных: {e}")
finally:
    connection.close()
