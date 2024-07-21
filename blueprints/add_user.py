import logging
import bcrypt
import json
import azure.functions as func
from services.db_connection import create_client

bp = func.Blueprint('add_user')


@bp.route(route="add_user", methods=['POST'])
def add_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Attempting to retrieve parameters from URL...")
    name = req.params.get('name')
    email = req.params.get('email')

    if not name:
        logging.info("AddUser: Name not found in HTTP request. Checking form data...")
        content_type = req.headers.get('Content-Type', '')

        if 'application/x-www-form-urlencoded' in content_type:
            logging.info("AddUser: Form data detected. Parsing...")
            # Access form data
            form_data = req.form
            name = form_data.get('name')
            email = form_data.get('email')
            password = form_data.get('password')

        else:
            # Handle JSON data
            try:
                logging.info("AddUser: No form data provided. Trying to parse JSON data...")
                req_body = req.get_json()
                name = req_body.get('name')
                email = req_body.get('email')
                password = req_body.get('password')
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass
                name = None
                email = None
                password = None
                logging.info("AddUser: Invalid JSON data in request body.")
                logging.info("AddUser: No request information found. PLease try again.")
                return func.HttpResponse("No request information found. Please try again.")
    # perform checks for credentials
    if not name:
        logging.info("AddUser: Name not provided.")
        return func.HttpResponse("Name not provided.", status_code=400)

    if not email:
        logging.info("AddUser: Email not provided.")
        return func.HttpResponse("Email not provided.", status_code=400)

    if not password:
        logging.info("AddUser: Password not provided.")
        return func.HttpResponse("Password not provided.", status_code=400)

    try:
        conn = create_client()
        conn.autocommit = False  # Manage transactions manually
        cur = conn.cursor()

        # Check if the table exists and create it if it doesn't
        table_exists_query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'user'
            );
        """

        cur.execute(table_exists_query)
        table_exists = cur.fetchone()[0]
        logging.info(f"Table exists: {table_exists}")

        if not table_exists:
            logging.info("Table doesn't exist. Creating...")
            create_table_query = """
                CREATE TABLE "user" (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(180) NOT NULL UNIQUE,
                    roles JSON NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    created_by VARCHAR(255),
                    updated_by VARCHAR(255),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    nicename VARCHAR(255) NOT NULL,
                    gdpr BOOLEAN DEFAULT FALSE,
                    last_login TIMESTAMPTZ,
                    confirmation_token VARCHAR(255),
                    password_requested_at TIMESTAMPTZ,
                    invite_sent BOOLEAN DEFAULT FALSE,
                    disabled_date TIMESTAMPTZ,
                    auth_code VARCHAR(255),
                    successful_logins INT DEFAULT 0,
                    disable_mfa BOOLEAN DEFAULT FALSE,
                    profile_image_id INT,
                    avatar INT,
                    language VARCHAR(256),
                    chat_open BOOLEAN DEFAULT TRUE
                );
            """
            cur.execute(create_table_query)
            logging.info("Table created successfully.")

        # Check if the test user already exists
        logging.info("Checking if test user already exists...")
        logging.info(f"Name: {name}")
        logging.info(f"Email: {email}")
        check_user_query = f"""SELECT 1 FROM "user" WHERE email = '{email}'"""
        logging.info(f"Executing query: {check_user_query}")
        cur.execute(check_user_query, email)
        logging.info("Query executed.")
        user_exists = cur.fetchone() is not None
        logging.info(f"User exists: {user_exists}")

        if user_exists:
            logging.info(f"User '{name}' already exists. Skipping insertion.")
            return func.HttpResponse(
                f"User '{name}' already exists.",
                status_code=200
            )

        if not user_exists:
            # No existing user found, insert the test user
            logging.info("No existing user found. Inserting user...")
            logging.info("Hashing password...")
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            insert_user_query = """
                INSERT INTO "user" (username, roles, password, email, created_by, updated_by, created_at, updated_at, nicename, gdpr, last_login, confirmation_token, password_requested_at, invite_sent, disabled_date, auth_code, successful_logins, disable_mfa, profile_image_id, avatar, language, chat_open)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_user_query, [
                name,
                json.dumps(['ROLE_ADMIN']),
                hashed_password,  # Use the hashed password
                email,
                "system",
                "system",
                "now",
                "now",
                "User",
                False,
                None,
                None,
                None,
                False,
                None,
                None,
                0,
                False,
                None,
                None,
                "en",
                True,
            ])

        conn.commit()  # Commit the transaction
        logging.info(f"User {name} added successfully.")
        print(f"User {name} added successfully")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

        # Return an error response
        return func.HttpResponse(
            'An error occurred. Please try again.',
            status_code=500
        )

    finally:
        if conn:
            conn.close()  # Close the database connection
            # Return a success response

    return func.HttpResponse(
        'User added successfully',
        status_code=200
    )