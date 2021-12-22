from flask import Flask
from flask import request
import requests
import datetime

app = Flask(__name__)

service_name = "ecostreet_core_service"
service_ip = "34.159.194.58:5000"

database_core_service = "34.159.211.186:5000"
configuration_core_service = "34.141.19.56:5000"

access_token = "None"

# HOME PAGE
@app.route("/")
def hello_world():
    return "Login microservice."

# EXTERNAL API CONNECTION
@app.route("/external")
def external_test():
    print("/external accessed")
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
    print("/login accessed")
    
    login_data = request.form
    url = 'http://' + database_core_service + '/login'
    response = requests.post(url, data=login_data)
    access_token = response.text
    return response.text

# EXECUTION OF A GAME COMMAND - MOCKUP
@app.route("/command", methods=["POST"])
def game_command():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    print("/command accessed")
    
    url = 'http://' + database_core_service + '/authenticate'
    response = requests.post(url, data={"AccessToken": access_token})
    if(response.text == "200 OK"):
        # additional functionalities could be implemented
        try:
            response = requests.post("http://www.atremic.com/join", data={"gameCode": "9328"})
        except:
            response = "200 OK"
        return "You have successfully joined the game."
    return "401 UNAUTHORIZED"

# SERVICE IP UPDATE FUNCTION
@app.route("/update_ip", methods = ['POST'])
def update_ip():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    print("/update_ip accessed")
    
    
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
    print("/config accessed")
    
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
    print("/getconfig accessed")
    
    return str([database_core_service, configuration_core_service])

# HEALTH CHECK
@app.route("/health")
def get_health():
    print("/health accessed")
    start = datetime.datetime.now()
    try:
        url = 'http://' + configuration_core_service + '/healthcheck'
        response = requests.get(url)
    except Exception as err:
        return "HEALTH CHECK FAIL: configuration unavailable"
    end = datetime.datetime.now()
    
    start2 = datetime.datetime.now()
    try:
        url = 'http://' + database_core_service + '/healthcheck'
        response = requests.get(url)
    except Exception as err:
        return "HEALTH CHECK FAIL: login service unavailable"
    end2 = datetime.datetime.now()
    
    delta1 = end-start
    crt = delta1.total_seconds() * 1000
    delta2 = end2-start2
    lrt = delta2.total_seconds() * 1000
    health = {"health check": "successful", "configuration response time": crt, "authentication response time": lrt}
    return str(health)

@app.route("/healthcheck")
def send_health():
    print("/healthcheck accessed")
    return "200 OK"