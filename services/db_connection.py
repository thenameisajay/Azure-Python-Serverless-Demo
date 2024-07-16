import psycopg2
import os
import logging

DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_PORT = 5432

print('DB_NAME', DB_NAME)
print('DB_USER', DB_USER)
print('DB_PASSWORD', DB_PASSWORD)


def create_client():
    try:
        client = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            host='localhost'
        )
        logging.info("Connected to PostgreSQL")
        return client
    except Exception as err:
        logging.error(f"Error connecting to PostgreSQL: {err}")
        raise
