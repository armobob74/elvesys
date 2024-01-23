"""
Needs to be run on a machine connected to an ELVESYS setup
Configure the variables in test_config.json
"""
import pytest
import json
from flask import Flask
from pman import pman

with open('test_config.json') as f:
    test_config = json.load(f)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(pman)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_mux_post(client):
    com_port = test_config.get('com-port-mux')
    current_state = test_config.get('current-state-mux')
    desired_state = test_config.get('desired-state-mux')
    data = json.dumps({"args": [com_port, current_state, desired_state]})
    response = client.post('/mux', data=data, content_type='application/json')
    assert response.status_code == 200
    assert 'state' in response.json
    assert response.json['state'] == 'ok'

def test_ob1_post(client):
    com_port = test_config.get('com-port-ob1')
    channel_to_initialize = test_config.get("channel-to-initialize")
    pressure_to_set = test_config.get("pressure-to-set")
    data = json.dumps({'args': [com_port, channel_to_initialize, pressure_to_set]})
    response = client.post('/ob1', data=data, content_type='application/json')
    assert response.status_code == 200
    assert 'state' in response.json
    assert response.json['state'] == 'ok'

def test_density_and_flow_get(client):
    com_port = test_config.get('com-port-flowmeter')
    response = client.get(f'/density-and-flow/{com_port}')
    assert response.status_code == 200
    assert 'state' in response.json
    assert response.json['state'] == 'ok'
    assert 'message' in response.json
    assert 'density' in response.json['message']
    assert 'flow' in response.json['message']

def test_dist_post(client):
    com_port = test_config.get('com_port_dist')
    initial_set_valveID = test_config.get('initial-set-valve-id')
    desired_set_valveID = test_config.get('desired-set-valve-id')
    data = json.dumps({'args': [com_port, initial_set_valveID, desired_set_valveID]})
    response = client.post('/ob1', data=data, content_type='application/json')
    assert response.status_code == 200
    assert 'state' in response.json
    assert response.json['state'] == 'ok'
