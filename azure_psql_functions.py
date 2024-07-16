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
        cur = conn.cursor()
        # create table
        dbu.create_table("users")
        # create user
        if get_user(email,"users"):
            logging.info(f"Create User: User with email {email} already exists.")
            return False
        else:
            query = "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s)"
            # hash password
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
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        conn = dbu.database_connection()
        if conn is None:
            logging.info("Create User: Failed to connect to database.")
            return None
        try:
        # check table exists, if not create table def create_user(name, email, password):
            cur = conn.cursor()
            # create table (function will check if table exists)
            return dbu.create_table("users")
            # create user
            if get_user(email,"users"):
                logging.info(f"Create User: User with email {email} already exists.")
                return False
        except:
            logging.info("Create User: Error creating table.")
            return False
        else:
            query = "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s)"
            # hash password
            password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt)
            now = datetime.now()

            # values = (name, email, hashed_password)/
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
        logging.info("Encoding password...")
        password = password.encode('utf-8')
        logging.info("Generating salt...")
        salt = bcrypt.gensalt()
        logging.info(f"salt = {salt}")
        logging.info("Hashing password...")
        hashed_password = bcrypt.hashpw(password, salt)
        values = (name, email, hashed_password.decode('utf-8'))
        # values = (name, email, password)
        cur.execute(query, values)
        conn.commit()
        print(f"User with email {email} created successfully.")
        return True   
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

def fixed_create_user(name, email, password):
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Create User: Failed to connect to database.")
        return None
    try:
        cur = conn.cursor()
        # create table
        dbu.create_table("users")
        # create user
        if get_user(email,"users"):
            logging.info(f"Create User: User with email {email} already exists.")
            return False
        else:
            query = "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s)"
            # query = "INSERT INTO public.users (username, roles, password, email, created_by, updated_by, created_at, updated_at, nicename, gdpr, last_login, confirmation_token, password_requested_at, invite_sent, disabled_date, auth_code, successful_logins, disable_mfa, profile_image_id, avatar, language, chat_open) VALUES (%s, %s, %s, %s, %s, %s %s, %s, %s, %s, %s, %s  %s, %s, %s, %s, %s, %s, %s)"
            # query = "INSERT INTO public.users ()"
            # hash password
            password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt)
            now = datetime.now()

            # values = (name, "ROLE_ADMIN", hashed_password, email, updated_by, now, datetime.now(), nicename, gdpr, last_login, confirmation_token)
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