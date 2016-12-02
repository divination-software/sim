"""Run the oldest simulation in the db and respond."""

import sqlite3
import requests
import json
import configparser
from simulator import Simulation
from simulator.build_sim import build_sim
from simulator.errors import SimBuildError

def run_oldest_sim():
    """Run the oldest simulation we have received and respond with the results."""
    conn = sqlite3.connect('simulations.db')
    cursor = conn.cursor()

    config = configparser.ConfigParser()
    config.read('config.ini')

    cursor.execute('''
                   SELECT id, simulation, user_id, board_name
                   FROM simulations
                   ORDER BY created_at DESC
                   LIMIT 1''')

    record = cursor.fetchone()
    if record is not None:
        sim_id = record[0]
        simulation = record[1]
        user_id = record[2]
        board_name = record[3]

        error_message = None
        try:
            nodes, edges, resources = build_sim(simulation)
        except SimBuildError as error:
            error_message = error.message
        except:
            error_message = 'Something went wrong when building your Simulation'

        url = config['Respond']['url']
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        if error_message is None:
            sim = Simulation(nodes, edges, resources)
            statistics = sim.run()

            response_data = {
                'data': {
                    'statistics': statistics,
                    'user_id': user_id
                }}

            if board_name is not None:
                response_data['data']['board_name'] = board_name

            requests.post(
                url,
                headers=headers,
                data=json.dumps(response_data),
                verify=False)
            print('Response disabled for testing')
            print(json.dumps(response_data))
        else:
            requests.post(
                url,
                headers=headers,
                data=json.dumps({'error': {'message': error_message}}),
                verify=False)
            print('Response disabled for testing')
            print(error_message)

        cursor.execute('DELETE FROM simulations WHERE id = ?', (str(sim_id)))
        conn.commit()
    conn.close()

if __name__ == '__main__':
    run_oldest_sim()
