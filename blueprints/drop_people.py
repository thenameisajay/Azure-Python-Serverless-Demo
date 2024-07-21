import logging
import azure.functions as func
from services.db_connection import create_client

bp = func.Blueprint("drop_people")


@bp.route("drop_people", methods=["DELETE"])
def delete_people(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Create a database connection
        conn = create_client()
        logging.info("Database connection created.")

        # Drop the 'people' table if it exists
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS people")
            conn.commit()
            logging.info("Table 'people' deleted successfully.")

        # Close the database connection
        conn.close()

        # Return a success response
        return func.HttpResponse("Table 'people' deleted successfully", status_code=200)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

        # Return an error response
        return func.HttpResponse(
            "An error occurred while deleting the table", status_code=500
        )
