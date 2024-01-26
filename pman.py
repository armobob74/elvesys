from flask import Blueprint, request, render_template
from functools import wraps
import json
from ob1_control import ob1_state_control
from mux_control import mux_state_control
from flowmeter_control import get_density_and_flow
from dist_control import dist_state_control
import pdb

config = {}
with open('config.json') as f:
    config = json.load(f)

name_to_port = config['name_to_port']


pman = Blueprint('pman', __name__)

def extract_pman_args(f):
    """
    Extract the pman args from the request and plug them into the decorated function
    Use as a decorator if desired
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = json.loads(request.data)
        args = data.get('args',[])
        return f(*args)
    return decorated_function

@pman.route("/mux", methods=["POST"])
@extract_pman_args
def mux(device_name, curr_state, desired_state):
    com_port = name_to_port[device_name]
    mux_state_control(com_port, curr_state, desired_state)
    return {'state':'ok','message':'Mux'}

@pman.route("/ob1", methods=["POST"])
@extract_pman_args
def ob1(device_name, channel_to_initialize, pressure_to_set):
    com_port = name_to_port[device_name]
    ob1_state_control(com_port, channel_to_initialize, pressure_to_set)
    return {'state':'ok','message':'OB1'}

@pman.route("/density-and-flow/<string:device_name>", methods=["GET"])
def densityAndFlow(device_name):
    com_port = name_to_port[device_name]
    density, flow = get_density_and_flow(com_port)
    return {'state':'ok','message':{'density':density,'flow':flow}}

@pman.route("/dist", methods=["POST"])
@extract_pman_args
def dist(device_name, initial_set_valveID, desired_set_valveID):
    com_port = name_to_port[device_name]
    dist_state_control(com_port, initial_set_valveID, desired_set_valveID)
    return {'state':'ok','message':'Valving'}
