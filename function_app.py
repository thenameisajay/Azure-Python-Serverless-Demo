import azure.functions as func
from blueprints.hello_blueprint import bp as hello
from blueprints.add_People_blueprint import bp as add_people

 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


app.register_blueprint(hello)
app.register_blueprint(add_people)
 
