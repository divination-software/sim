import sys
import inspect
from flask import Flask, request
from simulator import Simulation
from xml.etree import ElementTree as ET

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    if request.content_type != 'application/json':
        return 'Request must have Content-Type of application/json', 400

    json_body = request.get_json()
    if 'simulation' not in json_body:
        return 'Request body must contain the key "simulation"', 400

    try:
        xml = ET.fromstring(json_body['simulation'])
    except:
        return 'Value associated with "simulation" must be valid XML', 400

    # Simulation(json_body['simulation'])

    return 'Some details!'

if __name__ == '__main__':
    app.run()
