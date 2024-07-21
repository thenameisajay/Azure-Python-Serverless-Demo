import logging
import secrets
import base64
from datetime import datetime, timedelta


def generate_auth_object(length=32, expiry_hours=8):
    # Generate a secure random byte string
    token_bytes = secrets.token_bytes(length)
    # Encode the byte string to a URL-safe base64 format
    token = base64.urlsafe_b64encode(token_bytes).rstrip(b"=").decode("utf-8")

    # Get the current time
    now = datetime.now()

    # Calculate the expiry time
    expiry = now + timedelta(hours=expiry_hours)

    return {
        "token": token,
        "issued_at": now.isoformat(),
        "expires_at": expiry.isoformat(),
    }


def create_auth_table(cur, conn):
    try:
        # logging.info("Establishing database connection...")
        # conn = create_client()
        # conn.autocommit = False  # Manage transactions manually
        # cur = conn.cursor()

        logging.info("Creating table query...")
        create_table_query = """
            CREATE TABLE "auth_table" (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                token VARCHAR(255) NOT NULL,
                expires_at TIMESTAMPTZ
            );
        """
        logging.info("Executing table creation query...")
        logging.info(create_table_query)
        cur.execute(create_table_query)
        conn.commit()
        logging.info("Auth Table created successfully.")

    except Exception as e:
        logging.error(f"Error creating table: {e}")
