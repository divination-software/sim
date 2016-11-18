"""Simulation server"""

import json
from flask import Flask, request, Response
from simulator import Simulation
from simulator.build_sim import build_sim
from simulator.errors import SimBuildError

APP = Flask(__name__)

@APP.route('/', methods=['POST'])
def run_simulation():
    """Run a simulation and send the results back."""
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
        nodes, edges = build_sim(json_body['simulation'])

        #print(nodes)
        #print(edges)
    except SimBuildError as error:
        return error.message, 400
    except:
        return 'Something went wrong when building or running your \
            Simulation', 400

    sim = Simulation(nodes, edges)
    statistics = sim.run()

    return Response(json.dumps(statistics), mimetype='application/json')

if __name__ == '__main__':
    APP.run()
