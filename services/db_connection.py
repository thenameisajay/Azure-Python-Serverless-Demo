import psycopg2
import os
import logging
from dotenv import load_dotenv, find_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = 5432


def create_client():
    logger.info("create client is running")
    try:
        client = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            host='localhost'
        )
        logger.info("Connected to PostgreSQL")
        return client
    except Exception as err:
        logging.error(f"Error connecting to PostgreSQL: {err}")
        raise
