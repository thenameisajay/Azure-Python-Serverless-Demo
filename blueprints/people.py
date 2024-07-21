import json
import azure.functions as func
import logging
from services.db_connection import create_client

bp = func.Blueprint("people")


@bp.route("people", methods=["GET"])
def get_people(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Create a database connection
        conn = create_client()
        logging.info("Database connection created.")

        # Define a function to retrieve data from the database
        def fetch_all_people(conn):
            with conn.cursor() as cur:
                logging.info("Executing query: SELECT * FROM people")
                cur.execute("SELECT * FROM people")
                rows = cur.fetchall()
                # Convert rows to a list of dictionaries
                columns = [desc[0] for desc in cur.description]
                people = [dict(zip(columns, row)) for row in rows]
                return people

        # Fetch all people
        people = fetch_all_people(conn)
        logging.info(f"Fetched {len(people)} records from database.")

        # Close the connection
        conn.close()
        logging.info("Database connection closed.")

        # Return the response with the people data in JSON format
        return func.HttpResponse(
            json.dumps(
                people, default=str
            ),  # Convert datetime objects to string if needed
            status_code=200,
            mimetype="application/json",
        )

    except Exception as e:
        # Log the error and return a 500 response
        logging.error(f"An error occurred while retrieving people: {str(e)}")
        return func.HttpResponse(
            "An error occurred while retrieving people", status_code=500
        )
