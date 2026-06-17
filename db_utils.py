import sqlite3
from db_init import get_connection


def get_consumed_calories(date):
    connection = get_connection()
    cursor = connection.cursor()
    consumed_calories = (
        cursor.execute(
            """SELECT SUM(f.amount * p.calories / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ?""",
            (date,),
        ).fetchone()[0]
        or 0
    )
    connection.close()
    return consumed_calories


def get_consumed_protein(date):
    connection = get_connection()
    cursor = connection.cursor()
    consumed_protein = (
        cursor.execute(
            """SELECT SUM(f.amount * p.protein / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ?""",
            (date,),
        ).fetchone()[0]
        or 0
    )
    connection.close()
    return consumed_protein


def get_consumed_fat(date):
    connection = get_connection()
    cursor = connection.cursor()
    consumed_fat = (
        cursor.execute(
            """SELECT SUM(f.amount * p.fat / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ?""",
            (date,),
        ).fetchone()[0]
        or 0
    )
    connection.close()
    return consumed_fat


def get_consumed_carbs(date):
    connection = get_connection()
    cursor = connection.cursor()
    consumed_carbs = (
        cursor.execute(
            """SELECT SUM(f.amount * p.carbs / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ?""",
            (date,),
        ).fetchone()[0]
        or 0
    )
    connection.close()
    return consumed_carbs


def last_date():
    connection = get_connection()
    cursor = connection.cursor()
    last_date = cursor.execute("""SELECT MAX(date) FROM body_metrics""").fetchone()[0]
    connection.close()
    return last_date


def get_weight():
    connection = get_connection()
    cursor = connection.cursor()
    weight = cursor.execute(
        """SELECT AVG(weight) FROM(SELECT weight FROM body_metrics ORDER BY date DESC LIMIT 7)""",
    ).fetchone()[0]
    connection.close()
    return weight


def add_food_entry(date, product_name, amount):
    connection = get_connection()
    cursor = connection.cursor()
    product_id = cursor.execute(
        """SELECT product_id FROM products WHERE name = ?""", (product_name,)
    ).fetchone()[0]
    cursor.execute(
        """INSERT INTO food_diary (date, product_id, amount) VALUES (?, ?, ?)""",
        (date, product_id, amount),
    )
    connection.commit()
    connection.close()


def check_product_exists(product_name):
    connection = get_connection()
    cursor = connection.cursor()
    product = cursor.execute(
        """SELECT product_id FROM products WHERE name = ?""", (product_name,)
    ).fetchone()
    connection.close()
    return product is not None


def add_weight_entry(date, weight, fat_weight):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO body_metrics (date, weight, fat_weight) VALUES (?, ?, ?)""",
        (date, weight, fat_weight),
    )
    connection.commit()
    connection.close()


def add_product_entry(name, protein, fat, carbs, calories):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO products (name, protein, fat, carbs, calories) VALUES (?, ?, ?, ?, ?)""",
        (name, protein, fat, carbs, calories),
    )
    connection.commit()
    connection.close()


def delete_food_entry(date, product_name):
    connection = get_connection()
    cursor = connection.cursor()
    product_id = cursor.execute(
        """SELECT product_id FROM products WHERE name = ?""", (product_name,)
    ).fetchone()[0]
    cursor.execute(
        """DELETE FROM food_diary WHERE date = ? AND product_id = ?""",
        (date, product_id),
    )
    connection.commit()
    connection.close()


def add_body_metrics_entry(
    date,
    weight,
    fat_weight,
    lean_body_mass,
    body_fat_mass,
    body_fat_percentage,
    waist_clean,
    waist_dirty,
    hips,
    one_hip,
    chest,
    arm,
    shoulder,
    neck,
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO body_metrics (date, weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            date,
            weight,
            fat_weight,
            lean_body_mass,
            body_fat_mass,
            body_fat_percentage,
            waist_clean,
            waist_dirty,
            hips,
            one_hip,
            chest,
            arm,
            shoulder,
            neck,
        ),
    )
    connection.commit()
    connection.close()


def food_diary_check(date):
    connection = get_connection()
    cursor = connection.cursor()
    entries = cursor.execute(
        """SELECT f.food_id, p.name, f.amount, f.amount * p.calories / 100.0 AS calories, f.amount * p.protein / 100.0 AS protein, f.amount * p.fat / 100.0 AS fat, f.amount * p.carbs / 100.0 AS carbs FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ?""",
        (date,),
    ).fetchall()
    connection.close()
    return entries

def delete_food_entry_by_id(food_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """DELETE FROM food_diary WHERE food_id = ?""",
        (food_id,),
    )
    connection.commit()
    connection.close()

def get_products():
    connection = get_connection()
    cursor = connection.cursor()
    products = cursor.execute(
        """SELECT * FROM products"""
    ).fetchall()
    connection.close()
    return products

def get_body_metrics(period):
    connection = get_connection()
    cursor = connection.cursor()
    metrics = cursor.execute(
        """SELECT * FROM body_metrics ORDER BY date DESC LIMIT ?""", (period,)
    ).fetchall()
    connection.close()
    return metrics

def change_product_entry(product_id, name, protein, fat, carbs, calories):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE products SET name = ?, protein = ?, fat = ?, carbs = ?, calories = ? WHERE product_id = ?""",
        (name, protein, fat, carbs, calories, product_id),
    )
    connection.commit()
    connection.close()

def change_body_metrics_entry(
    date,
    weight,
    fat_weight,
    lean_body_mass,
    body_fat_mass,
    body_fat_percentage,
    waist_clean,
    waist_dirty,
    hips,
    one_hip,
    chest,
    arm,
    shoulder,
    neck,
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE body_metrics SET weight = ?, fat_weight = ?, lean_body_mass = ?, body_fat_mass = ?, body_fat_percentage = ?, waist_clean = ?, waist_dirty = ?, hips = ?, one_hip = ?, chest = ?, arm = ?, shoulder = ?, neck = ? WHERE date = ?""",
        (weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck, date),
    )
    connection.commit()
    connection.close()