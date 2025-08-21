from django.test import TestCase

import psycopg2

try:
    conn = psycopg2.connect(
        dbname="room_booking_db_wy7c",
        user="jinsa_0",
        password="GmZGCKRmtkWuZEIW3s8sX3OwGvpN9YZr",
        host="dpg-d2iu2jh5pdvs7393fp30-a.oregon-postgres.render.com",
        port="5432",
        sslmode="require"
    )
    print("✅ Successfully connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
