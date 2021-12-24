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

# HEALTH PAGE
@app.route("/")
def health():
    return "200"

# HOME PAGE
@app.route("/lg")
def hello_world():
    return "Login microservice."

# EXTERNAL API CONNECTION
@app.route("/lgexternal")
def external_test():
    print("/lgexternal accessed")
    response = requests.get("http://www.atremic.com/login")
    return response.text
    
# CONNECTION TO ANOTHER MICROSERVICE - AUTHENTICATION MS
@app.route('/lglogin', methods = ['POST'])
def login():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    print("/lglogin accessed")
    
    login_data = request.form
    url = 'http://' + database_core_service + '/dblogin'
    response = requests.post(url, data=login_data)
    access_token = response.text
    return response.text

# EXECUTION OF A GAME COMMAND - MOCKUP
@app.route("/lgcommand", methods=["POST"])
def game_command():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    print("/lgcommand accessed")
    
    url = 'http://' + database_core_service + '/dbauthenticate'
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
@app.route("/lgupdate_ip", methods = ['POST'])
def update_ip():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    print("/update_ip accessed")
    
    
    service_ip = request.form["ip"]
    data = {"name": service_name, "ip": service_ip}
    url = 'http://' + configuration_core_service + '/cfupdate'
    response = requests.post(url, data=data)
    return response.text

# FUNCTION TO UPDATE IP'S OF OTHER SERVICES
@app.route("/lgconfig", methods = ['POST'])
def config_update():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    print("/lgconfig accessed")
    
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
@app.route("/lggetconfig")
def get_config():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    print("/lggetconfig accessed")
    
    return str([database_core_service, configuration_core_service])

# METRICS FUNCTION
@app.route("/lgmetrics")
def get_health():
    print("/lgmetrics accessed")
    start = datetime.datetime.now()
    try:
        url = 'http://' + configuration_core_service + '/cfhealthcheck'
        response = requests.get(url)
    except Exception as err:
        return "METRIC CHECK FAIL: configuration unavailable"
    end = datetime.datetime.now()
    
    start2 = datetime.datetime.now()
    try:
        url = 'http://' + database_core_service + '/dbhealthcheck'
        response = requests.get(url)
    except Exception as err:
        return "METRIC CHECK FAIL: login service unavailable"
    end2 = datetime.datetime.now()
    
    delta1 = end-start
    crt = delta1.total_seconds() * 1000
    delta2 = end2-start2
    lrt = delta2.total_seconds() * 1000
    health = {"metric check": "successful", "configuration response time": crt, "authentication response time": lrt}
    return str(health)

# HEALTH CHECK
@app.route("/lghealthcheck")
def send_health():
    print("/lghealthcheck accessed")
    return "200 OK"