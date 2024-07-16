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
        logging.info("Database Connection: Connected to the database successfully!")
        return conn
    
    except psycopg2.Error as e:
        logging.info(f"Database Connection: Error connecting to the database: {e}")
        return None

def check_table(name):
    conn = database_connection()
    if conn is None:
        logging.info("Check Table: Failed to connect to database.")
        return None
    try:
        cur = conn.cursor()
        query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)"
        cur.execute(query)
        conn.commit()
        print(f"Table exists.")
        logging.info("Check Table: Table exists.")
        return True
    except psycopg2.Error as e:
        print(f"Table {name} does not exist.")
        return False

def create_table(name):
    conn = database_connection()
    if conn is None:
        logging.info("Create Table: Failed to connect to database.")
        return None
    try:
        if not check_table(name):
            logging.info(f"Create Table: Creating table '{name}'...")
            cur = conn.cursor()
            logging.info(f"Create Table: Cursor created.")
            logging.info(f"Create Table: Connection objec - {conn.info}")
            query = f"CREATE TABLE {name} (name VARCHAR(255), email VARCHAR(255), password VARCHAR(255));"
            logging.info(f"Create Table: Query: \"{query}\"")
            logging.info("Create Table: Executing query...")
            cur.execute(query)
            logging.info("Create Table: Query executed. Committing changes...")
            conn.commit()
            logging.info("Create Table: Table Created.")
            return True
        else:
            logging.info("Create Table: Table already exists.")
            return True
    except psycopg2.Error as e:
        logging.info(f"Create Table: Error creating table: {e}")
        logging.info("Create Table: Failed to create table.")
        return False
    finally:
        cur.close()
        conn.close()


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

# ## fixed statement
# def create_table(name):
#     conn = database_connection()
#     if conn is None:
#         logging.info("Create Table: Failed to connect to database.")
#         return None
#     try:
#         if not check_table(name):
#             logging.info(f"Create Table: Creating table '{name}'...")
#             cur = conn.cursor()
#             logging.info(f"Create Table: Cursor created.")
#             logging.info(f"Create Table: Connection objec - {conn.info}")
#             query = f"CREATE TABLE {name} (
#             name VARCHAR(255), 
#             email VARCHAR(255), 
#             password VARCHAR(255)
#             );"
#             query = f"CREATE TABLE {name} (
#                 id SERIAL PRIMARY KEY,
#                 username VARCHAR(180) NOT NULL UNIQUE,
#                 roles JSON NOT NULL,
#                 password VARCHAR(255) NOT NULL,
#                 email VARCHAR(255) NOT NULL,
#                 created_by VARCHAR(255),
#                 updated_by VARCHAR(255),
#                 created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
#                 updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
#                 nicename VARCHAR(255) NOT NULL,
#                 gdpr BOOLEAN DEFAULT FALSE,
#                 last_login TIMESTAMPTZ,
#                 confirmation_token VARCHAR(255),
#                 password_requested_at TIMESTAMPTZ,
#                 invite_sent BOOLEAN DEFAULT FALSE,
#                 disabled_date TIMESTAMPTZ,
#                 auth_code VARCHAR(255),
#                 successful_logins INT DEFAULT 0,
#                 disable_mfa BOOLEAN DEFAULT FALSE,
#                 profile_image_id INT,
#                 avatar INT,
#                 language VARCHAR(256),
#                 chat_open BOOLEAN DEFAULT TRUE
#                 );"
#             logging.info(f"Create Table: Query: \"{query}\"")
#             logging.info("Create Table: Executing query...")
#             cur.execute(query)
#             logging.info("Create Table: Query executed. Committing changes...")
#             conn.commit()
#             logging.info("Create Table: Table Created.")
#             return True
#         else:
#             logging.info("Create Table: Table already exists.")
#             return True
#     except psycopg2.Error as e:
#         logging.info(f"Create Table: Error creating table: {e}")
#         logging.info("Create Table: Failed to create table.")
#         return False
#     finally:
#         cur.close()
#         conn.close()