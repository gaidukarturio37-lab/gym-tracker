import sqlite3

def get_connection():
    # Простой и понятный путь
    db_path = "C:/MyPythonProjects/gym_tracker/tracker.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


connection = get_connection()
cursor = connection.cursor()
connection.executescript("""
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    protein REAL,
    fat REAL,
    carbs REAL,
    calories REAL
);
CREATE TABLE IF NOT EXISTS food_diary (
    food_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    product_id INTEGER,
    amount REAL,
    FOREIGN KEY (date) REFERENCES body_metrics (date) ON DELETE RESTRICT,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS body_metrics (
    date TEXT NOT NULL PRIMARY KEY,
    weight REAL,
    fat_weight REAL,
    lean_body_mass REAL,
    body_fat_mass REAL,
    body_fat_percentage REAL,
    waist_clean REAL,
    waist_dirty REAL,
    hips REAL,
    one_hip REAL,
    chest REAL,
    arm REAL,
    shoulder REAL,
    neck REAL
);
""")
connection.commit()
connection.close()
