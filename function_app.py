import azure.functions as func
from blueprints.hello import bp as hello
from blueprints.add_People import bp as add_people
from blueprints.people import bp as people
from blueprints.drop_people import bp as drop_people

 
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


app.register_blueprint(hello)
app.register_blueprint(add_people)
app.register_blueprint(people)
app.register_blueprint(drop_people)
