import sys
import inspect
from flask import Flask, request
from simulator import Simulation
from simulator.parse_sim import parse_sim
from xml.etree import ElementTree as ET

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    # Test content-type
    if request.content_type != 'application/json':
        return 'Request must have Content-Type of application/json', 400

    # Test body content
    json_body = request.get_json()
    if 'simulation' not in json_body:
        return 'Request body must contain the key "simulation"', 400

    # Extract nodes and edges from the provided XML so we can instantiate the
    # nodes
    try:
        nodes, edges = parse_sim(json_body['simulation'])

        print(nodes)
        print(edges)
    except:
        return 'Value associated with "simulation" must be valid XML', 400

    # A valid simulation has:
    # - at lease one Exit and at least one Source nodes
    # - a path of edges leading from the Source node to the Exit node
    if not nodes and not edges:
        return 'Invalid Simulation: Simulation is empty', 400
    elif not nodes:
        return 'Invalid Simulation: Simulation should contain at least one \
                Source and one Exit', 400
    elif not edges:
        return 'Invalid Simulation: Simulation should contain edges', 200


    # Simulation(json_body['simulation'])

    return 'Some details!', 200

if __name__ == '__main__':
    app.run()
