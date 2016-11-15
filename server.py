import sys
from flask import Flask, request
from simulator import Simulation

app = Flask(__name__)

@app.route('/', methods=['POST'])
def hello_world():
    json_body = request.get_json()

    print(json_body)

    # incoming post request should be json
    # json_body['simulation'] should (1) exist and (2) be valid XML
    Simulation(json_body['simulation'])

    return 'Some details!'

if __name__ == '__main__':
    app.run()
