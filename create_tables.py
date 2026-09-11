import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", "5432"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    sslmode="require"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers
(
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(20),
    age INTEGER,
    gender VARCHAR(20),
    city VARCHAR(20),
    churn INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions
(
    subcription_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    plan_type VARCHAR(20),
    monthly_charges DECIMAL(10,2),
    tenure_months INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS payments
(
    payment_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    payment_method VARCHAR(20)
);
""")

connection.commit()

cursor.close()
connection.close()

print("All 3 PostgreSQL tables created successfully")