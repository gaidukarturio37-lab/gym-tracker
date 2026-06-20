from db_init import get_connection
engine = get_connection()

def get_consumed_calories(date, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        consumed_calories = (
            cursor.execute(
                """SELECT SUM(f.amount * p.calories / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ? AND f.user_id = ?""",
                (date, user_id),
            ).fetchone()[0]
            or 0
        )
        connection.close()
        return consumed_calories


def get_consumed_protein(date, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        consumed_protein = (
            cursor.execute(
                """SELECT SUM(f.amount * p.protein / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ? AND f.user_id = ?""",
                (date, user_id),
            ).fetchone()[0]
            or 0
        )
        connection.close()
        return consumed_protein


def get_consumed_fat(date, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        consumed_fat = (
            cursor.execute(
                """SELECT SUM(f.amount * p.fat / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ? AND f.user_id = ?""",
                (date, user_id),
            ).fetchone()[0]
            or 0
        )
        connection.close()
        return consumed_fat


def get_consumed_carbs(date, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        consumed_carbs = (
            cursor.execute(
                """SELECT SUM(f.amount * p.carbs / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ? AND f.user_id = ?""",
                (date, user_id),
            ).fetchone()[0]
            or 0
        )
        connection.close()
        return consumed_carbs


def last_date(user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        last_date = cursor.execute("""SELECT MAX(date) FROM body_metrics WHERE user_id = ?""", (user_id,)).fetchone()[0]
        connection.close()
        return last_date


def get_weight(user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        weight = cursor.execute(
            """SELECT AVG(weight) FROM(SELECT weight FROM body_metrics WHERE user_id = ? ORDER BY date DESC LIMIT 7)""",
            (user_id,)
        ).fetchone()[0]
        connection.close()
        return weight


def add_food_entry(date, product_name, amount, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        product_id = cursor.execute(
            """SELECT product_id FROM products WHERE name = ? and user_id = ?""", (product_name, user_id)
        ).fetchone()[0]
        cursor.execute(
            """INSERT INTO food_diary (date, product_id, amount, user_id) VALUES (?, ?, ?, ?)""",
            (date, product_id, amount, user_id),
        )
        connection.commit()
        connection.close()


def check_product_exists(product_name, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        product = cursor.execute(
            """SELECT product_id FROM products WHERE name = ? and user_id = ?""", (product_name, user_id)
        ).fetchone()
        connection.close()
        return product is not None





def add_product_entry(name, protein, fat, carbs, calories, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO products (name, protein, fat, carbs, calories, user_id) VALUES (?, ?, ?, ?, ?, ?)""",
            (name, protein, fat, carbs, calories, user_id),
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
    user_id,
):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO body_metrics (date, weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
                user_id
            ),
        )
        connection.commit()
        connection.close()


def food_diary_check(date, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        entries = cursor.execute(
            """SELECT f.food_id, p.name, f.amount, f.amount * p.calories / 100.0 AS calories, f.amount * p.protein / 100.0 AS protein, f.amount * p.fat / 100.0 AS fat, f.amount * p.carbs / 100.0 AS carbs FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = ? AND f.user_id = ?""",
            (date, user_id),
        ).fetchall()
        connection.close()
        return entries

def delete_food_entry_by_id(food_id, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """DELETE FROM food_diary WHERE food_id = ? AND user_id = ?""",
            (food_id, user_id),
        )
        connection.commit()
        connection.close()

def get_products(user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        products = cursor.execute(
            """SELECT product_id, name, protein, fat, carbs, calories FROM products WHERE user_id = ?""", (user_id,)
        ).fetchall()
        connection.close()
        return products

def get_body_metrics(period, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        metrics = cursor.execute(
            """SELECT date, weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck FROM body_metrics WHERE user_id = ? ORDER BY date DESC LIMIT ?""", (user_id, period)
        ).fetchall()
        connection.close()
        return metrics

def change_product_entry(product_id, name, protein, fat, carbs, calories, user_id):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE products SET name = ?, protein = ?, fat = ?, carbs = ?, calories = ? WHERE product_id = ? AND user_id = ?""",
            (name, protein, fat, carbs, calories, product_id, user_id),
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
    user_id
):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE body_metrics SET weight = ?, fat_weight = ?, lean_body_mass = ?, body_fat_mass = ?, body_fat_percentage = ?, waist_clean = ?, waist_dirty = ?, hips = ?, one_hip = ?, chest = ?, arm = ?, shoulder = ?, neck = ? WHERE date = ? AND user_id = ?""",
            (weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck, date, user_id),
        )
        connection.commit()
        connection.close()

def get_user_id(username, pin_code):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        user_id = cursor.execute(
            """SELECT user_id FROM users WHERE user_name = ? AND pin_code = ?""", (username, pin_code)
        ).fetchone()
        connection.close()
        return user_id[0] if user_id else None

def reg_new_user(username, pin_code, join_key):
    with engine.raw_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO users (user_name, pin_code) VALUES (?, ?) WHERE join_key = ?""", (username, pin_code, join_key)
        )
        connection.commit()
        connection.close()
        return get_user_id(username, pin_code)