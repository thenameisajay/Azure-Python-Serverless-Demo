import logging
import json
import azure.functions as func

bp = func.Blueprint("hello")


@bp.route(route="hello", methods=["GET", "POST"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Check if name is provided in query parameters
    name = req.params.get("name")

    # If not found in query parameters, check if it's in the body of a POST request
    if not name:
        content_type = req.headers.get("Content-Type", "")

        if "application/x-www-form-urlencoded" in content_type:
            # Access form data
            form_data = req.form
            name = form_data.get("name")
        else:
            # Handle JSON data
            try:
                req_body = req.get_json()
                name = req_body.get("name")
            except ValueError:
                # Handle the case where the body is not valid JSON or is empty
                pass

    # If still no name, use the default value
    if not name:
        name = "World"

    # Respond with a personalized greeting
    # json object with Hello World as value and key as message
    response = {"message": f"Hello, {name}!"}
    return func.HttpResponse(json.dumps(response), mimetype="application/json")
    # return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
