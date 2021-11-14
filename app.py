from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World 123"

@app.route("/test")
def hello_world():
    return "It works."
