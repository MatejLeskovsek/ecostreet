from flask import Flask
from flask import request
import requests

app = Flask(__name__)

service_name = "ecostreet_core_service"
service_ip = "34.159.194.58:5000"

database_core_service = "34.96.72.77"
configuration_core_service = "192.168.1.121"

access_token = "None"

# HOME PAGE
@app.route("/")
def hello_world():
    return "Login microservice."

# EXTERNAL API CONNECTION
@app.route("/external")
def external_test():
    response = requests.get("http://www.atremic.com/login")
    return response.text
    
# CONNECTION TO ANOTHER MICROSERVICE - AUTHENTICATION MS
@app.route('/login', methods = ['POST'])
def login():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    
    login_data = request.form
    url = 'http://' + database_core_service + '/login'
    response = requests.post(url, data=login_data)
    access_token = response.text
    return response.text

# EXECUTION OF A GAME COMMAND - MOCKUP
@app.route("/command")
def game_command():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    
    url = 'http://' + database_core_service + '/authenticate'
    response = requests.post(url, data={"AccessToken": access_token})
    if(response.text == "200 OK"):
        return "You have executed a game command."
    return "401 UNAUTHORIZED"

# SERVICE IP UPDATE FUNCTION
@app.route("/update_ip", methods = ['POST'])
def update_ip():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    
    
    service_ip = request.form["ip"]
    data = {"name": service_name, "ip": service_ip}
    url = 'http://' + configuration_core_service + '/update'
    response = requests.post(url, data=data)
    return response.text

# FUNCTION TO UPDATE IP'S OF OTHER SERVICES
@app.route("/config", methods = ['POST'])
def config_update():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    
    try:
        microservice = request.form["name"]
        ms_ip = request.form["ip"]
        if microservice == "database_core_service":
            database_core_service = ms_ip
        if microservice == "configuration_core_service":
            configuration_core_service = ms_ip
        return "200 OK"
    except Exception as err:
        return err

# FUNCTION TO GET CURRENT CONFIG
@app.route("/getconfig")
def get_config():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    
    return str([database_core_service, configuration_core_service])