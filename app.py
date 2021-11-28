from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World 123"

@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        return(user_id)
    if request.method == 'POST':
        """modify/update the information for <user_id>"""
        # you can use <user_id>, which is a str but could
        # changed to be int or whatever you want, along
        # with your lxml knowledge to make the required
        # changes
        data = request.form # a multidict containing POST data
        return(data)
    if request.method == 'DELETE':
        """delete user with ID <user_id>"""
        return("User deleted")
    else:
        # POST Error 405 Method Not Allowed
        return("Error 405: Method Not Allowed")
    
@app.route('/login', methods = ['POST'])
def login():
    data = request.form
    if(data["username"]):
        if(data["username"] == 'matej'):
            return "200 OK"
    return(data) 
