from flask import Blueprint, redirect, request, render_template
from functools import wraps
import json
from ob1_control import ob1_state_control
from mux_control import mux_half_control, mux_state_control
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
        print(args)
        return f(*args)
    return decorated_function

@pman.get("/mux")
def muxPage():
    import pdb
    device_names = [k for k in name_to_port.keys() if 'Bridge' in k]
    return render_template('mux_pman.html', device_names=device_names)

@pman.post("/mux-UI")
def muxUI():
    """ Handles requests from the pman mux UI """
    device_name = request.form['device_name']
    desired_states = [0] * 8
    for i in range(1,9):
        s = f"state_{i}"
        if s in request.form:
            state = int(request.form[s])
            desired_states[i-1] = state
    com_port = name_to_port[device_name]
    mux_half_control(com_port, desired_state=desired_states)
    return redirect('/pman/mux')


@pman.post("/mux")
@extract_pman_args
def mux(device_name, curr_state, desired_state):
    com_port = name_to_port[device_name]
    mux_state_control(com_port, curr_state, desired_state)
    return {'state':'ok','message':'Mux'}

@pman.route("/ob1", methods=["POST"])
@extract_pman_args
def ob1(device_name, channel_to_initialize, pressure_to_set):
    com_port = name_to_port[device_name]
    ob1_state_control(com_port, int(channel_to_initialize), float(pressure_to_set))
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
