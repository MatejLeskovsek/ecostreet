from flask import Flask
from flask import request
import requests

app = Flask(__name__)

service_name = "ecostreet_core_service"
service_ip = "34.159.194.58:5000"

database_core_service = "34.96.72.77"
configuration_core_service = "192.168.1.121"

@app.route("/")
def hello_world():
    return "Login microservice."
    
@app.route('/login', methods = ['POST'])
def login():
    login_data = request.form
    url = 'http://' + database_core_service + '/authenticate'
    response = requests.post(url, data=login_data)
    return response.text

@app.route("/update_ip")
def update_ip():
    data = {"name": service_name, "ip": service_ip}
    url = 'http://' + configuration_core_service + '/update'
    response = requests.post(url, data=data)
    return response.text

@app.route("/config", methods = ['POST'])
def config_update():
    try:
        microservice = request.form["name"]
        ms_ip = request.form["ip"]
        if microservice == "database_core_service":
            database_core_service = ms_ip
        if microservice == "configuration_core_service":
            configuration_core_service = ms_ip
        service_name = "neki_druga"
        return service_name
    except Exception as err:
        return err

@app.route("/getconfig")
def get_config():
    return str([database_core_service, configuration_core_service, service_name])