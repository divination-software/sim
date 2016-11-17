"""Simulation server"""

from flask import Flask, request
from simulator import Simulation
from simulator.parse_sim import parse_sim
from simulator.errors import SimParseError

app = Flask(__name__)

@app.route('/', methods=['POST'])
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
        nodes, edges = parse_sim(json_body['simulation'])

        print(nodes)
        print(edges)
    except SimParseError as error:
        return error.message, 400
    except:
        return 'Invalid Simulation', 400

    # TODO: can we optimize this by moving the loop into Simulation's __init__?
    for i in range(3):
        Simulation(nodes, edges)

    return 'Some details!', 200

if __name__ == '__main__':
    app.run()
