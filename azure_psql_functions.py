# File containing all functions that facilitate interaction between azure functions and the Postgres database.
import psycopg2
import logging
import bcrypt
import database_utility as dbu

def create_user(name, email, password):
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None
    try:
        cur = conn.cursor()
        # check table exists, if not create table
        if dbu.check_table("users"):
            query = "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s)"
        else:
            dbu.create_table("users")
            query = "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s)"
        # hash password
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        values = (name, email, hashed_password)
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
    conn = dbu.database_connection()
    if conn is None:
        logging.info("Failed to connect to database.")
        return None

    try:
        cur = conn.cursor()
        # check table exists, if not create table
        if dbu.check_table("test_users"):
            query = "INSERT INTO public.test_users (name, email, password) VALUES (%s, %s, %s)"
        else:
            dbu.create_table("test_users")
            query = "INSERT INTO public.test_users (name, email, password) VALUES (%s, %s, %s)"
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
        print(f"User with email {email} deleted successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_user(email):
    conn = dbu.database_connection()
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
            print(f"User with email {email} not found/password is not correct.")
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

## UTILITY FUNCTIONS

    