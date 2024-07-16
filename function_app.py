import azure.functions as func
import logging
import azure_psql_functions as db
import bcrypt
import json
 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
 
@app.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
 
    # Check if name is provided in query parameters
    name = req.params.get('name')
 
    # If not found in query parameters, check if it's in the body of a POST request
    if not name:
        content_type = req.headers.get('Content-Type', '')
        
        if 'application/x-www-form-urlencoded' in content_type:
            # Access form data
            form_data = req.form
            name = form_data.get('name')
        else:
            # Handle JSON data
            try:
                req_body = req.get_json()
                name = req_body.get('name')
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass
 
    # If still no name, use the default value
    if not name:
        name = 'World'
 
    # Respond with a personalized greeting
    # json object with Hello World as value and key as message
    response = {'message': f"Hello, {name}!"}
    return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json"
        )
    # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")

@app.route(route="addUser")
def AddUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('AddUser: Python HTTP trigger function processed a request.')

    # Check if name is provided in query parameters
    name = req.params.get('name')
    email = req.params.get('email')
    password = req.params.get('password')

    # If not found in query parameters, check if it's in the body of a POST request
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
            # add more fields as required

            # pass parameters into function that adds email to database
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
                logging.info("AddUser: Invalid JSON data in request body.")
                logging.info("AddUser: No request information found. PLease try again.")
                return func.HttpResponse("No request information found. Please try again.")
                
    # database interaction
    try:
        created_user = db.create_user(name, email, password)
        if not created_user:
            logging.info(f"AddUser: User with email {email} already exists.")
    except Exception as e:
        return func.HttpResponse(f"User has not been added to database. Please try again.")
    
    # Respond with a personalized greeting
    return func.HttpResponse(f"Hello, {name}. Your email is {email}.")

@app.route(route="addTestUser", auth_level=func.AuthLevel.FUNCTION)
def AddTestUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if name is provided in query parameters
    name = req.params.get('name')
    email = req.params.get('email')
    password = req.params.get('password')

    # If not found in query parameters, check if it's in the body of a POST request
    if not name:
        content_type = req.headers.get('Content-Type', '')

        if 'application/x-www-form-urlencoded' in content_type:
            # Access form data
            form_data = req.form
            name = form_data.get('name')
            email = form_data.get('email')
            password = form_data.get('password')
            # add more fields as requried
            # pass parameters into function that adds email to database
        else:
            # Handle JSON data
            try:
                req_body = req.get_json()
                name = req_body.get('name')
                email = req_body.get('email')
                password = req_body.get('password')
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass
    # database interaction
    try:
        db.create_test_user(name, email, password)
    except Exception as e:
        print(f"Error creating user: {e}")
        return func.HttpResponse(f"Test user has not been added to database. Please try again.")

    # If still no name, use the default value
    if not name:
        name = 'World'
        email = "default@gmail.com"
        password = "password"
        return func.HttpResponse(f"Your email has not been added. Please try again.")

    # Respond with a personalized greeting
    return func.HttpResponse(f"Test User: {name} Account created. Your email is {email}.")

@app.route(route="deleteUser", auth_level=func.AuthLevel.FUNCTION)
def DeleteUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

     # Check if name is provided in query parameters
    email = req.params.get('email')

    # If not found in query parameters, check if it's in the body of a POST request
    if not email:
        content_type = req.headers.get('Content-Type', '')

        if 'application/x-www-form-urlencoded' in content_type:
            # Access form data
            form_data = req.form
            email = form_data.get('email')
            # add more fields as requried
            # pass parameters into function that adds email to database
        else:
            # Handle JSON data
            try:
                req_body = req.get_json()
                email = req_body.get('email')
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass

    # database interaction
    db.delete_user(email)

    # If still no name, use the default value
    if not email:
        return func.HttpResponse(f"Please input a user to delete.")

    # Respond with a personalized greeting
    return func.HttpResponse(f"User with email: \"{email}\" has been deleted.")

@app.route(route="getUser", auth_level=func.AuthLevel.FUNCTION)
def GetUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

     # Check if name is provided in query parameters
    email = req.params.get('email')
    # If not found in query parameters, check if it's in the body of a POST request
    if not email:
        content_type = req.headers.get('Content-Type', '')

        if 'application/x-www-form-urlencoded' in content_type:
            # Access form data
            form_data = req.form
            email = form_data.get('email')
            # add more fields as requried
            # pass parameters into function that adds email to database
        else:
            # Handle JSON data
            try:
                req_body = req.get_json()
                email = req_body.get('email')
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass

    # database interaction
    table_name = "users"
    if table_name:
        pass
    else:
        table_name = "users"
    user = db.get_user(email,table_name)

    # If still no name, use the default value
    if not email:
        return func.HttpResponse(f"User does not exist.")

    # Respond with a personalized greeting
    return func.HttpResponse(f"User with email: \"{email}\" exists.")


@app.route(route="validateUser", auth_level=func.AuthLevel.FUNCTION)
def ValidateUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if name is provided in query parameters
    email = req.params.get('email')
    password = req.params.get('password')

    # If not found in query parameters, check if it's in the body of a POST request
    if not email:
        logging.info("Email not provided.")
        content_type = req.headers.get('Content-Type', '')

        if 'application/x-www-form-urlencoded' in content_type:
            # Access form data
            form_data = req.form
            email = form_data.get('email')
            password = form_data.get('password')
            # add more fields as requried
            # pass parameters into function that adds email to database
        else:
            # Handle JSON data
            try:
                logging.info("Trying to get JSON data.")
                req_body = req.get_json()
                email = req_body.get('email')
                password = req_body.get('password')
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass

    # database interaction
    try:
        if db.validate_user(email, password):
            return func.HttpResponse(f"User has been validated.")
        elif None:
            return func.HttpResponse(f"User does not exist.")
        else:
            return func.HttpResponse(f"User has not been validated.")
    except Exception as e:
        print(f"Error validating user: {e}")
        return func.HttpResponse(f"User has not been validated. Please try again.")

    # If still no name, use the default value
    if not email:
        email = 'test@test.com'
        password = "password"
        return func.HttpResponse(f"Welcome!")

    # Respond with a personalized greeting
    return func.HttpResponse(f"Your email is {email}. Your password is {password}.")

