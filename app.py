from flask import Flask
from flask import request
import requests
import datetime
import grequests
from gevent import monkey
from webargs import fields
from flask_apispec import use_kwargs, marshal_with
from flask_apispec import FlaskApiSpec
from marshmallow import Schema
monkey.patch_all()

app = Flask(__name__)
app.config.update({
    'APISPEC_SWAGGER_URL': '/lgopenapi',
    'APISPEC_SWAGGER_UI_URL': '/lgswaggerui'
})
docs = FlaskApiSpec(app, document_options=False)

service_name = "ecostreet_core_service"
service_ip = "34.96.72.77"

database_core_service = "34.96.72.77"
configuration_core_service = "34.96.72.77"

access_token = "None"
class NoneSchema(Schema):
        pass

# HEALTH PAGE
@app.route("/")
@marshal_with(NoneSchema, description='200 OK', code=200)
def health():
    return "200", 200
docs.register(health)

# HOME PAGE
@app.route("/lg")
@marshal_with(NoneSchema, description='200 OK', code=200)
def hello_world():
    return "Login microservice.", 200
docs.register(hello_world)

# EXTERNAL API CONNECTION
@app.route("/lgexternal")
@marshal_with(NoneSchema, description='200 OK', code=200)
@marshal_with(NoneSchema, description='INTERNAL SERVER ERROR', code=500)
def external_test():
    print("/lgexternal accessed")
    try:
        response = requests.get("http://www.atremic.com/login")
        return response.text, 200
    except:
        return "INTERNAL SERVER ERROR", 500
docs.register(external_test)
    
# CONNECTION TO ANOTHER MICROSERVICE - AUTHENTICATION MS
@app.route('/lglogin', methods = ['POST'])
@use_kwargs({'username': fields.Str(), 'password': fields.Str()})
@marshal_with(NoneSchema, description='200 OK', code=200)
@marshal_with(NoneSchema, description='UNAUTHORIZED', code=401)
def login():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    print("/lglogin accessed")
    
    login_data = request.form
    try:
        url = 'http://' + database_core_service + '/dblogin'
        response = requests.post(url, data=login_data)
        access_token = response.text
        return response.text, 200
    except:
        return "UNAUTHORIZED", 401
docs.register(login)

# EXECUTION OF A GAME COMMAND - MOCKUP
@app.route("/lgcommand", methods=["POST"])
@use_kwargs({'AccessToken': fields.Str()})
@marshal_with(NoneSchema, description='200 OK', code=200)
@marshal_with(NoneSchema, description='UNAUTHORIZED', code=401)
def game_command():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    global access_token
    print("/lgcommand accessed")
    
    # asynchronously send data to a outside statistic server (also on www.atremic.com/statistics)
    try:
        url = [
        'www.atremic.com/statistics'
        ]
        rs = (grequests.get(u) for u in url)
        grequests.map(rs)
        print("Asynchronous call: successful.")
    except Exception as err:
        print("Asynchronous call: failed.")
    
    url = 'http://' + database_core_service + '/dbauthenticate'
    response = requests.post(url, data={"AccessToken": access_token})
    if(response.text == "200 OK"):
        # additional functionalities could be implemented
        try:
            response = requests.post("http://www.atremic.com/join", data={"gameCode": "9328"})
        except:
            response = "200 OK"
        return "You have successfully joined the game.", 200
    return "401 UNAUTHORIZED", 401
docs.register(game_command)

# SERVICE IP UPDATE FUNCTION
@app.route("/lgupdate_ip", methods = ['POST'])
@use_kwargs({'name': fields.Str(), 'ip': fields.Str()})
@marshal_with(NoneSchema, description='200 OK', code=200)
@marshal_with(NoneSchema, description='Something went wrong.', code=500)
def update_ip():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    print("/update_ip accessed")
    
    
    service_ip = request.form["ip"]
    data = {"name": service_name, "ip": service_ip}
    try:
        url = 'http://' + configuration_core_service + '/cfupdate'
        response = requests.post(url, data=data)
        return response.text, 200
    except:
        return "Something went wrong.", 500
docs.register(update_ip)

# FUNCTION TO UPDATE IP'S OF OTHER SERVICES
@app.route("/lgconfig", methods = ['POST'])
@use_kwargs({'name': fields.Str(), 'ip': fields.Str()})
@marshal_with(NoneSchema, description='200 OK', code=200)
@marshal_with(NoneSchema, description='Something went wrong', code=500)
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
        return "200 OK", 200
    except Exception as err:
        return "Something went wrong.", 500
docs.register(config_update)

# FUNCTION TO GET CURRENT CONFIG
@app.route("/lggetconfig")
@marshal_with(NoneSchema, description='200 OK', code=200)
def get_config():
    global database_core_service
    global configuration_core_service
    global service_ip
    global service_name
    print("/lggetconfig accessed")
    
    return str([database_core_service, configuration_core_service]), 200
docs.register(get_config)

# METRICS FUNCTION
@app.route("/lgmetrics")
@marshal_with(NoneSchema, description='200 OK', code=200)
@marshal_with(NoneSchema, description='METRIC CHECK FAIL', code=500)
def get_health():
    print("/lgmetrics accessed")
    start = datetime.datetime.now()
    try:
        url = 'http://' + configuration_core_service + '/cfhealthcheck'
        response = requests.get(url)
    except Exception as err:
        return "METRIC CHECK FAIL: configuration unavailable", 500
    end = datetime.datetime.now()
    
    start2 = datetime.datetime.now()
    try:
        url = 'http://' + database_core_service + '/dbhealthcheck'
        response = requests.get(url)
    except Exception as err:
        return "METRIC CHECK FAIL: login service unavailable", 500
    end2 = datetime.datetime.now()
    
    delta1 = end-start
    crt = delta1.total_seconds() * 1000
    delta2 = end2-start2
    lrt = delta2.total_seconds() * 1000
    health = {"metric check": "successful", "configuration response time": crt, "authentication response time": lrt}
    return str(health), 200
docs.register(get_health)

# HEALTH CHECK
@app.route("/lghealthcheck")
@marshal_with(NoneSchema, description='200 OK', code=200)
def send_health():
    print("/lghealthcheck accessed")
    return "200 OK", 200
docs.register(send_health)