import logging
import azure.functions as func
import bcrypt
from services.db_connection import create_client

bp = func.Blueprint('validate_user')

@bp.route(route="validate_user", methods=['POST'])
def validate_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function (validate_user) processed a request.')

    # Initialize email and password variables
    email = None
    password = None
    conn = None

    # Check if the email and password are in the body of a POST request
    content_type = req.headers.get('Content-Type', '')

    if 'application/x-www-form-urlencoded' in content_type:
        # Access form data
        form_data = req.form()
        email = form_data.get('email')
        password = form_data.get('password')
    else:
        # Handle JSON data
        try:
            req_body = req.get_json()
            email = req_body.get('email')
            password = req_body.get('password')
        except ValueError as e:
            logging.error(f'Error parsing JSON: {e}')
            return func.HttpResponse(
                'Invalid JSON format',
                status_code=400
            )

    if not email or not password:
        return func.HttpResponse(
            'Email and password are required',
            status_code=400
        )

    try:
        # Establish a database connection
        conn = create_client()
        cur = conn.cursor()

        # Fetch user data based on email
        fetch_user_query = 'SELECT password FROM "user" WHERE email = %s'
        cur.execute(fetch_user_query, [email])
        result = cur.fetchone()

        # Handle case where the user does not exist
        if result is None:
            return func.HttpResponse(
                'User does not exist',
                status_code=400
            )

        hashed_password = result[0]

        # Compare the provided password with the stored hashed password
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

        if is_valid:
            return func.HttpResponse(
                'Successfully logged in!',
                status_code=200
            )
        else:
            return func.HttpResponse(
                'Invalid password',
                status_code=401
            )

    except Exception as e:
        logging.error(f'Failed to authenticate the credentials: {str(e)}')
        return func.HttpResponse(
            'Failed to authenticate the credentials',
            status_code=500
        )

    finally:
        if conn:
            conn.close()  # Ensure the database connection is closed
