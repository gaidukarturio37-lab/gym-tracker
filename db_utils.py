from db_init import get_connection
engine = get_connection()
from sqlalchemy import text
import streamlit as st

@st.cache_data
def execute_query(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params or {})
        connection.commit()
        return result

@st.cache_data
def get_consumed_calories(date, user_id):
        query = "SELECT SUM(f.amount * p.calories / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = :date AND f.user_id = :user_id"
        res = execute_query(query, {"date": date, "user_id": user_id},).fetchone()[0] or 0
        return res

@st.cache_data
def get_consumed_protein(date, user_id):
        query = "SELECT SUM(f.amount * p.protein / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = :date AND f.user_id = :user_id"
        res = execute_query(query, {"date": date, "user_id": user_id}).fetchone()[0] or 0
        return res


@st.cache_data
def get_consumed_fat(date, user_id):
        query = "SELECT SUM(f.amount * p.fat / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = :date AND f.user_id = :user_id"
        res = execute_query(query, {"date": date, "user_id": user_id}).fetchone()[0] or 0
        return res


@st.cache_data
def get_consumed_carbs(date, user_id):
        query = "SELECT SUM(f.amount * p.carbs / 100.0) FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = :date AND f.user_id = :user_id"
        res = execute_query(query, {"date": date, "user_id": user_id}).fetchone()[0] or 0
        return res



@st.cache_data
def last_date(user_id):
        query = "SELECT MAX(date) FROM body_metrics WHERE user_id = :user_id"
        last_date = execute_query(query, {"user_id": user_id}).fetchone()[0]
        return last_date


@st.cache_data
def get_weight(user_id):
        query = "SELECT AVG(weight) FROM(SELECT weight FROM body_metrics WHERE user_id = :user_id ORDER BY date DESC LIMIT 7)"
        weight = execute_query(query, {"user_id": user_id}).fetchone()[0]
        return weight


def add_food_entry(date, product_name, amount, user_id):
        query = "SELECT product_id FROM products WHERE name = :product_name AND user_id = :user_id"
        product_id = execute_query(query, {"product_name": product_name, "user_id": user_id}).fetchone()[0]
        query = "INSERT INTO food_diary (date, product_id, amount, user_id) VALUES (:date, :product_id, :amount, :user_id)"
        execute_query(query, {"date": date, "product_id": product_id, "amount": amount, "user_id": user_id})

def check_product_exists(product_name, user_id):
        query = "SELECT product_id FROM products WHERE name = :product_name AND user_id = :user_id"
        product = execute_query(query, {"product_name": product_name, "user_id": user_id}).fetchone()
        return product is not None





def add_product_entry(name, protein, fat, carbs, calories, user_id):
        query = "INSERT INTO products (name, protein, fat, carbs, calories, user_id) VALUES (:name, :protein, :fat, :carbs, :calories, :user_id)"
        execute_query(query, {"name": name, "protein": protein, "fat": fat, "carbs": carbs, "calories": calories, "user_id": user_id})





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
        query = "INSERT INTO body_metrics (date, weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck, user_id) VALUES (:date, :weight, :fat_weight, :lean_body_mass, :body_fat_mass, :body_fat_percentage, :waist_clean, :waist_dirty, :hips, :one_hip, :chest, :arm, :shoulder, :neck, :user_id)"
        execute_query(query, {
            "date": date,
            "weight": weight,
            "fat_weight": fat_weight,
            "lean_body_mass": lean_body_mass,
            "body_fat_mass": body_fat_mass,
            "body_fat_percentage": body_fat_percentage,
            "waist_clean": waist_clean,
            "waist_dirty": waist_dirty,
            "hips": hips,
            "one_hip": one_hip,
            "chest": chest,
            "arm": arm,
            "shoulder": shoulder,
            "neck": neck,
            "user_id": user_id
        })

@st.cache_data
def food_diary_check(date, user_id):
        query = "SELECT f.food_id, p.name, f.amount, f.amount * p.calories / 100.0 AS calories, f.amount * p.protein / 100.0 AS protein, f.amount * p.fat / 100.0 AS fat, f.amount * p.carbs / 100.0 AS carbs FROM food_diary f JOIN products p ON f.product_id = p.product_id WHERE f.date = :date AND f.user_id = :user_id"
        entries = execute_query(query, {"date": date, "user_id": user_id}).fetchall()
        return entries


def delete_food_entry_by_id(food_id, user_id):
        query = "DELETE FROM food_diary WHERE food_id = :food_id AND user_id = :user_id"
        execute_query(query, {"food_id": food_id, "user_id": user_id})

@st.cache_data
def get_products(user_id):
        query = "SELECT product_id, name, protein, fat, carbs, calories FROM products WHERE user_id = :user_id"
        products = execute_query(query, {"user_id": user_id}).fetchall()
        return products

@st.cache_data
def get_body_metrics(period, user_id):
    query = "SELECT date, weight, fat_weight, lean_body_mass, body_fat_mass, body_fat_percentage, waist_clean, waist_dirty, hips, one_hip, chest, arm, shoulder, neck FROM body_metrics WHERE user_id = :user_id ORDER BY date DESC LIMIT :period"
    metrics = execute_query(query, {"user_id": user_id, "period": period}).fetchall()
    return metrics

def change_product_entry(product_id, name, protein, fat, carbs, calories, user_id):
    query = "UPDATE products SET name = :name, protein = :protein, fat = :fat, carbs = :carbs, calories = :calories WHERE product_id = :product_id AND user_id = :user_id"
    execute_query(query, {"name": name, "protein": protein, "fat": fat, "carbs": carbs, "calories": calories, "product_id": product_id, "user_id": user_id})

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
    query = "UPDATE body_metrics SET weight = :weight, fat_weight = :fat_weight, lean_body_mass = :lean_body_mass, body_fat_mass = :body_fat_mass, body_fat_percentage = :body_fat_percentage, waist_clean = :waist_clean, waist_dirty = :waist_dirty, hips = :hips, one_hip = :one_hip, chest = :chest, arm = :arm, shoulder = :shoulder, neck = :neck WHERE date = :date AND user_id = :user_id"
    execute_query(query, {
        "weight": weight,
        "fat_weight": fat_weight,
        "lean_body_mass": lean_body_mass,
        "body_fat_mass": body_fat_mass,
        "body_fat_percentage": body_fat_percentage,
        "waist_clean": waist_clean,
        "waist_dirty": waist_dirty,
        "hips": hips,
        "one_hip": one_hip,
        "chest": chest,
        "arm": arm,
        "shoulder": shoulder,
        "neck": neck,
        "date": date,
        "user_id": user_id
    })

@st.cache_data
def get_user_id(username, pin_code):
    query = "SELECT user_id FROM users WHERE user_name = :u AND pin_code = :p"
    user_id = execute_query(query, {"u": username, "p": pin_code}).fetchone()
    return user_id[0] if user_id else None

@st.cache_data
def reg_new_user(username, pin_code, join_key):
    query = "UPDATE users SET user_name = :u, pin_code = :p WHERE join_key = :j AND user_name IS NULL AND pin_code IS NULL"
    res = execute_query(query, {"u": username, "p": pin_code, "j": join_key})
    return get_user_id(username, pin_code)