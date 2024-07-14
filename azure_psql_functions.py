# File containing all functions that facilitate interaction between azure functions and the Postgres database.
import psycopg2
import logging
import bcrypt

# declare database variables
POSTGRES_DB="base1_test" 
POSTGRES_USER="kevon" 
POSTGRES_PASSWORD="password" 
DB_HOST="172.111.11.10"

# function to connect to database
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

def create_user(name, email, password):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        # hash password
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        values = (name, email, hashed_password.decode('utf-8'))
        # values = (name, email, password)
        cur.execute(query, values)
        conn.commit()
        print(f"User with email {email} created successfully.")
        logging.info("User created successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error creating user: {e}")
        logging.info("Failed to create user.")
        return False
    finally:
        cur.close()
        conn.close()

def create_test_user(name, email, password):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "INSERT INTO test_users (name, email, password) VALUES (%s, %s, %s)"
        # hash password
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        values = (name, email, hashed_password.decode('utf-8'))
        # values = (name, email, password)
        cur.execute(query, values)
        conn.commit()
        print(f"User with email {email} created successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def delete_user(email):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "DELETE FROM users WHERE email = %s"
        values = (email,)
        cur.execute(query, values)
        conn.commit()
        print(f"User with email {email} deleted successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_user(email):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        values = (email,)
        cur.execute(query, values)
        user = cur.fetchone()
        if user:
            print(f"User with email {email} retrieved successfully.")
            return user
        else:
            print(f"User with email {email} not found.")
            return None
    except psycopg2.Error as e:
        print(f"Error retrieving user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def validate_user(email,password):
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        values = (email,) # comma wraps value in tuple
        cur.execute(query, values)
        user = cur.fetchone()
        if user:
            print(f"User with email {email} retrieved successfully.")
            if password_check(password, user[2]):
                print("Password is correct.")
                return True
        else:
            print(f"User with email {email} not found.")
            return False
    except psycopg2.Error as e:
        print(f"Error retrieving user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_all_users():
    conn = database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "SELECT * FROM users"
        cur.execute(query)
        users = cur.fetchall()
        print("Users retrieved successfully.")
        return users
    except psycopg2.Error as e:
        print(f"Error retrieving users: {e}")
        return None
    finally:
        cur.close()
        conn.close()

## UTILITY FUNCTIONS

# def password_check(password, hashed_password):
#     salt = bcrypt.gensalt()
#     pw_input = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return bcrypt.checkpw(pw_input, hashed_password)

def password_check(plain_password, stored_password):
    # Convert the hashed_password to bytes if it is in string format
    # encoded_password = plain_password.encode('utf-8')
    # salt = bcrypt.gensalt()
    # password = bcrypt.hashpw(encoded_password, salt)
    # plain_password = bcrypt.hashpw(password, salt)
    if bcrypt.checkpw(plain_password.encode('utf-8'), stored_password.encode('utf-8')):
        return True
    # Function to check if the plain password matches the hashed password
    # if (plain_password == hashed_password):
    #     return True
    else:
        False
    