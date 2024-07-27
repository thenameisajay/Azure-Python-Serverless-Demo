import logging
import azure.functions as func
import bcrypt
import json
import pytz
from datetime import datetime
from services.db_connection import create_client
from services.auth_token import generate_auth_object, create_auth_table

bp = func.Blueprint("validate_user")


@bp.route(route="validate_user", methods=["POST"])
def validate_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function (validate_user) processed a request.")

    email = None
    password = None
    conn = None
    auth_object = None

    content_type = req.headers.get("Content-Type", "")

    if "application/x-www-form-urlencoded" in content_type:
        form_data = req.form
        email = form_data.get("email")
        password = form_data.get("password")
    else:
        try:
            req_body = req.get_json()
            email = req_body.get("email")
            password = req_body.get("password")
        except ValueError as e:
            logging.error(f"Error parsing JSON: {e}")
            return func.HttpResponse("Invalid JSON format", status_code=400)

    if not email or not password:
        return func.HttpResponse("Email and password are required", status_code=400)

    try:
        conn = create_client()
        cur = conn.cursor()

        fetch_user_query = 'SELECT password FROM "user" WHERE email = %s'
        cur.execute(fetch_user_query, [email])
        result = cur.fetchone()

        if result is None:
            return func.HttpResponse("User does not exist", status_code=400)

        hashed_password = result[0]

        if not bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        ):
            return func.HttpResponse("Invalid credentials", status_code=403)

        table_exists_query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'auth_table'
            );
        """
        cur.execute(table_exists_query)
        table_exists = cur.fetchone()[0]

        if not table_exists:
            create_auth_table(cur, conn)

        check_query = """
            SELECT expires_at
            FROM auth_table
            WHERE email = %s
        """
        cur.execute(check_query, [email])
        result = cur.fetchone()

        if result:
            expires_at = result[0]
            current_time = datetime.now(pytz.UTC)

            if expires_at > current_time:
                logging.info("Valid auth token found. Generating new token...")
                auth_object = generate_auth_object()
                delete_query = "DELETE FROM auth_table WHERE email = %s"
                insert_query = """
                    INSERT INTO auth_table (email, token, expires_at)
                    VALUES (%s, %s, %s)
                """
                cur.execute(delete_query, [email])
                cur.execute(
                    insert_query,
                    [email, auth_object["token"], auth_object["expires_at"]],
                )
                conn.commit()
            else:
                logging.info("Auth token has expired. Generating new token...")
                auth_object = generate_auth_object()
                delete_query = "DELETE FROM auth_table WHERE email = %s"
                insert_query = """
                    INSERT INTO auth_table (email, token, expires_at)
                    VALUES (%s, %s, %s)
                """
                cur.execute(delete_query, [email])
                cur.execute(
                    insert_query,
                    [email, auth_object["token"], auth_object["expires_at"]],
                )
                conn.commit()
        else:
            logging.info("No auth record found. Generating new token...")
            auth_object = generate_auth_object()
            insert_query = """
                INSERT INTO auth_table (email, token, expires_at)
                VALUES (%s, %s, %s)
            """
            cur.execute(
                insert_query, [email, auth_object["token"], auth_object["expires_at"]]
            )
            conn.commit()

        response_data = {
            "message": "Successfully logged in!",
            "auth_object": auth_object["token"],
        }
        response_headers = {"Content-Type": "application/json"}

        return func.HttpResponse(
            body=json.dumps(response_data),
            status_code=200,
            headers=response_headers,
            mimetype="application/json",
        )

    except Exception as e:
        logging.error(f"Failed to authenticate the credentials: {str(e)}")
        return func.HttpResponse(
            "Failed to authenticate the credentials", status_code=500
        )

    finally:
        if conn:
            conn.close()
