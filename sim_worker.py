"""Run the oldest simulation in the db and respond."""

import sqlite3
import requests
import json
from simulator import Simulation
from simulator.build_sim import build_sim
from simulator.errors import SimBuildError

def run_oldest_sim():
    """Run the oldest simulation we have received and respond with the results."""
    conn = sqlite3.connect('simulations.db')
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT id, simulation, user_id, board_name
                   FROM simulations
                   ORDER BY created_at DESC
                   LIMIT 1''')
    sim_id, simulation, user_id, board_name = cursor.fetchone()

    print(sim_id)
    print(simulation)
    print(user_id)
    print(board_name)

    error_message = None
    try:
        nodes, edges = build_sim(simulation)
    except SimBuildError as error:
        error_message = error.message
    except:
        error_message = 'Something went wrong when building your Simulation'

    url = 'http://someurltobedetermined'

    if error_message is None:
        sim = Simulation(nodes, edges)
        statistics = sim.run()

        response_data = {
            'data': {
                'statistics': statistics,
                'id': sim_id
            }}

        if board_name is not None:
            response_data['data']['board_name'] = board_name

        requests.post(
            url,
            data=json.dumps(response_data))
    else:
        requests.post(
            url,
            data=json.dumps({'error': {'message': error_message}}))

    cursor.execute('DELETE FROM simulations WHERE id = ?', (str(sim_id)))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_oldest_sim()