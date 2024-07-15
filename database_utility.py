# utility functions for database connection and table creation
import psycopg2
import logging
import bcrypt


# declare database variables
POSTGRES_DB="base1_test" 
POSTGRES_USER="kevon" 
POSTGRES_PASSWORD="password" 
DB_HOST="172.111.11.10"

def database_connection():
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=DB_HOST
        )
        logging.info("Connected to the database successfully!")
        print("Connected to the database successfully!")
        return conn
    
    except psycopg2.Error as e:
        logging.info("Failed to connect to database.")
        print(f"Error connecting to the database: {e}")
        return None

def create_table(name):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None
    try:
        cur = conn.cursor()
        query = f"CREATE TABLE {name} (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password TEXT(255));"
        cur.execute(query)
        conn.commit()
        logging.info("Table Created.")
        return True
    except psycopg2.Error as e:
        logging.info("Failed to create table.")
        return False
    finally:
        cur.close()
        conn.close()

def check_table(name):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None
    try:
        cur = conn.cursor()
        query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)"
        cur.execute(query,)
        conn.commit()
        print(f"Table exists.")
        logging.info("Table exists.")
        return True
    except psycopg2.Error as e:
        print(f"Table {name} does not exist.")
        return False

def drop_table(name):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None
    try:
        cur = conn.cursor()
        query = f"DROP TABLE {name};"
        cur.execute(query)
        conn.commit()
        logging.info("Table dropped.")
        return True
    except psycopg2.Error as e:
        logging.info("Failed to drop table.")
        return False
    finally:
        cur.close()
        conn.close()

## Password checking

def password_check(plain_password, stored_password):
    if bcrypt.checkpw(plain_password.encode('utf-8'), stored_password.encode('utf-8')):
        return True
    else:
        False