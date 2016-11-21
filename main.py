"""Simulation server"""

import json
import sqlite3
import threading
from sim_worker import run_oldest_sim
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/', methods=['POST'])
def store_simulation():
    """Run a simulation and send the results back."""
    conn = sqlite3.connect('simulations.db')
    cursor = conn.cursor()

    print(request.url)

    # Test content-type
    if request.content_type != 'application/json':
        return 'Request must have Content-Type of application/json', 400

    # Test body content
    json_body = request.get_json()
    if 'simulation' not in json_body:
        return 'Request body must contain the key "simulation"', 400
    if 'user_id' not in json_body:
        return 'Request body must contain the key "user_id"', 400

    if 'board_name' in json_body:
        sql = """
            INSERT INTO simulations(simulation, user_id, board_name)
            VALUES (?, ?, ?)"""
        cursor.execute(sql, (
            json_body['simulation'],
            json_body['user_id'],
            json_body['board_name']))
    else:
        sql = '''
            INSERT INTO simulations(simulation, user_id)
            VALUES (?, ?)'''
        cursor.execute(sql, (
            json_body['simulation'],
            json_body['user_id']))
    conn.commit()
    conn.close()

    threading.Thread(target=run_oldest_sim, args=(), kwargs={})

    response_content = {
        'message': 'Simulation received'}
    return Response(json.dumps(response_content), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)
    