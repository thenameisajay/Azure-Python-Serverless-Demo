# File containing all functions that facilitate interaction between azure functions and the Postgres database.
import psycopg2
import logging
import bcrypt
import database_utility as dbu
import datetime


def create_user(name, email, password):
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Create User: Failed to connect to database.")
        return None
    try:
        logging.info("Create User: Setting cursor...")
        cur = conn.cursor()
        # create table
        logging.info("Create User: Creating table...")
        dbu.create_table("users", conn)
        # create user
        logging.info("Create User: Checking if user already exists...")
        if get_user(email,"users"):
            logging.info(f"Create User: User with email {email} already exists.")
            return False
        else:
            logging.info("Create User: User does not exist. Creating user...")
            # create user
            query = "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s)"
            # hash password
            logging.info("Create User: Hashing password...")
            password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt)

            # values = (name, "ROLE_ADMIN", hashed_password, email, updated_by, now, datetime.now(), NotImplemented, None, last_login, confirmation_token)
            values = (name, email, hashed_password)
            # values = (name, email, password)
            cur.execute(query, values)
            conn.commit()
            print(f"Create User: User with email \"{email}\" created successfully.")
            logging.info("Create User: User created successfully.")
            return True
        return False
    except psycopg2.Error as e:
        logging.info(f"Create User: Error creating user: {e}.")
        return False
    finally:
        cur.close()
        conn.close()

def create_test_user(name, email, password):
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Create Test User: Failed to connect to database.")
        return None
    try:
        logging.info("Create Test User: Setting cursor...")
        cur = conn.cursor()
        # create table
        logging.info("Create Test User: Creating table...")
        dbu.create_table("users", conn)
        # create user
        logging.info("Create Test User: Checking if user already exists...")
        if get_user(email,"test_users"):
            logging.info(f"Create Test User: User with email {email} already exists.")
            return False
        else:
            logging.info("Create Test User: User does not exist. Creating user...")
            # create user
            query = "INSERT INTO public.test_users (name, email, password) VALUES (%s, %s, %s)"
            # hash password
            logging.info("Create User: Hashing password...")
            password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt)

            # values = (name, "ROLE_ADMIN", hashed_password, email, updated_by, now, datetime.now(), NotImplemented, None, last_login, confirmation_token)
            values = (name, email, hashed_password)
            # values = (name, email, password)
            cur.execute(query, values)
            conn.commit()
            print(f"Create User: User with email \"{email}\" created successfully.")
            logging.info("Create User: User created successfully.")
            return True
        return False
    except psycopg2.Error as e:
        logging.info(f"Create User: Error creating user: {e}.")
        return False
    finally:
        cur.close()
        conn.close()

def delete_user(email):
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        query = "DELETE FROM users WHERE email = %s"
        values = (email,)
        cur.execute(query, values)
        conn.commit()
        print(f"Delete User: User with email {email} deleted successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Delete User: Error deleting user: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_user(email, table_name="users"):
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Get User: Failed to connect to database.")
        return None
    if table_name is None:
        table_name = "users"
    try:
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE email = %s"
        values = (email,)
        cur.execute(query, values)
        user = cur.fetchone()
        if user:
            print(f"Get User: User with email {email} retrieved successfully.")
            return user
        else:
            print(f"Get User: User with email {email} not found.")
            return None
    except psycopg2.Error as e:
        print(f"Get User: Error retrieving user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def validate_user(email,password):
    conn = dbu.database_connection()
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
            print(f"Checking password...")
            if dbu.password_check(password, user[2]):
                print("Password is correct.")
                return True
        else:
            print(f"User with email {email} not found or password is not correct.")
            return False
    except psycopg2.Error as e:
        print(f"Error retrieving user: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_all_users():
    conn = dbu.database_connection()
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

## FIXED FUNCTIONS
