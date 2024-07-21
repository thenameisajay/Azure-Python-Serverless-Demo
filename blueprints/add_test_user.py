import azure.functions as func
import logging
from services.db_connection import create_client
import bcrypt
import json

bp = func.Blueprint("add_test_user")


@bp.route("add_test_user", methods=["GET"])
def add_test_user(req: func.HttpRequest) -> func.HttpResponse:
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

        if not table_exists:
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

        # Check if the test user already exists
        check_user_query = 'SELECT 1 FROM "user" WHERE email = %s'
        cur.execute(check_user_query, ["test@test.com"])
        user_exists = cur.fetchone() is not None

        if not user_exists:
            # No existing user found, insert the test user
            hashed_password = bcrypt.hashpw(
                "test".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            insert_user_query = """
                INSERT INTO "user" (username, roles, password, email, created_by, updated_by, created_at, updated_at, nicename, gdpr, last_login, confirmation_token, password_requested_at, invite_sent, disabled_date, auth_code, successful_logins, disable_mfa, profile_image_id, avatar, language, chat_open)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(
                insert_user_query,
                [
                    "testuser",
                    json.dumps(["ROLE_ADMIN"]),
                    hashed_password,  # Use the hashed password
                    "test@test.com",
                    "system",
                    "system",
                    "now",
                    "now",
                    "Test User",
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
                ],
            )

        conn.commit()  # Commit the transaction
        print("Test user added successfully")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

        # Return an error response
        return func.HttpResponse(
            "An error occurred. Please try again.", status_code=500
        )

    finally:
        if conn:
            conn.close()  # Close the database connection

            # Return a success response

    return func.HttpResponse("Test user added successfully", status_code=200)
