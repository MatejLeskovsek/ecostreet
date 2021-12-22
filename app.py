from flask import Flask
from flask import request
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Login microservice."
    
@app.route('/login', methods = ['POST'])
def login():
    login_data = request.form
    url = 'http://34.96.72.77/authenticate'
    response = requests.post(url, data=login_data)
    return response.text
