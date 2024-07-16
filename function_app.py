import azure.functions as func

# Routes Imported
from blueprints.hello import bp as hello
from blueprints.add_People import bp as add_people
from blueprints.people import bp as people
from blueprints.drop_people import bp as drop_people
from blueprints.add_test_user import bp as add_test_user
from blueprints.validate_user import bp as validate_user

# Set the auth level to anonymous for now ,
# (https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python-v2
# %2Cisolated-process%2Cnodejs-v4%2Cfunctionsv2&pivots=programming-language-python#authorization-keys)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# All Routes must be declared here
app.register_blueprint(hello)
app.register_blueprint(add_people)
app.register_blueprint(people)
app.register_blueprint(drop_people)
app.register_blueprint(add_test_user)
app.register_blueprint(validate_user)
