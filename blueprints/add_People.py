import logging
import azure.functions as func
from services.db_connection import create_client

bp = func.Blueprint('add_people')

@bp.route('add_people', methods=['GET'])  # Change to POST as it is more appropriate for adding data but for now it is GET
def add_people(req: func.HttpRequest) -> func.HttpResponse:
    people_to_add = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "age": 28,
            "date_of_birth": "1996-05-14",
            "country": "USA",
            "sex": "M",
            "occupation": "Software Engineer",
            "relationship_status": "Single",
            "salary": 85000.0,
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "age": 34,
            "date_of_birth": "1989-08-22",
            "country": "Canada",
            "sex": "F",
            "occupation": "Data Analyst",
            "relationship_status": "Married",
            "salary": 92000.0,
        },
        {
            "first_name": "Alice",
            "last_name": "Johnson",
            "age": 41,
            "date_of_birth": "1982-02-17",
            "country": "UK",
            "sex": "F",
            "occupation": "Project Manager",
            "relationship_status": "Divorced",
            "salary": 105000.0,
        },
        {
            "first_name": "Bob",
            "last_name": "Brown",
            "age": 25,
            "date_of_birth": "1999-11-05",
            "country": "Australia",
            "sex": "M",
            "occupation": "Graphic Designer",
            "relationship_status": "Single",
            "salary": 62000.0,
        },
        {
            "first_name": "Emily",
            "last_name": "Davis",
            "age": 30,
            "date_of_birth": "1993-03-28",
            "country": "New Zealand",
            "sex": "F",
            "occupation": "HR Specialist",
            "relationship_status": "Married",
            "salary": 74000.0,
        },
    ]

    def create_table_if_not_exists(conn):
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                age INTEGER,
                date_of_birth DATE,
                country VARCHAR(50),
                sex CHAR(1),
                occupation VARCHAR(100),
                relationship_status VARCHAR(20),
                salary NUMERIC,
                UNIQUE (first_name, last_name, date_of_birth)  -- Ensure unique combination
            )
            """)
            conn.commit()

    def person_exists(conn, first_name, last_name, date_of_birth):
        with conn.cursor() as cur:
            cur.execute("""
            SELECT 1 FROM people WHERE first_name = %s AND last_name = %s AND date_of_birth = %s
            """, (first_name, last_name, date_of_birth))
            return cur.fetchone() is not None

    def insert_people(conn, people):
        with conn.cursor() as cur:
            for person in people:
                if not person_exists(conn, person['first_name'], person['last_name'], person['date_of_birth']):
                    cur.execute("""
                    INSERT INTO people (first_name, last_name, age, date_of_birth, country, sex, occupation, relationship_status, salary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        person['first_name'], person['last_name'], person['age'], person['date_of_birth'],
                        person['country'],
                        person['sex'], person['occupation'], person['relationship_status'], person['salary']))
            conn.commit()

    try:
        conn = create_client()
        create_table_if_not_exists(conn)
        insert_people(conn, people_to_add)
        conn.close()
        return func.HttpResponse(
            "People added successfully",
            status_code=200
        )
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return func.HttpResponse(
            "An error occurred while adding people",
            status_code=500
        )
