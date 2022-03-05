# import flask dependency
from flask import Flask

# Create a new Flask app instance
# __name__ is a variable that denotes the name of the current function
app = Flask(__name__)

#create flask routes

#starting point/root:
@app.route("/")
#create a function, which will appear in the route above.
def hello_world():
    return "Hello World"

#to run a flask app, use command line/anaconda, navigate to folder, 
# run the name of the flask file to be run (or set FLASK_APP=app.py, then flask run)