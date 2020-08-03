import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_DBNAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
)

