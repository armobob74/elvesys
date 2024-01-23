from flask import Blueprint, request, render_template
import json
from ob1_control import ob1_state_control
from mux_control import mux_state_control
from flowmeter_control import get_density_and_flow
from dist_control import dist_state_control

pman = Blueprint('pman', __name__)

@pman.route("/mux", methods=["POST"])
def mux():
    d = json.loads(request.data)
    args = d['args']
    com_port = args[0]
    curr_state = args[1]
    desired_state = args[2]
    mux_state_control(com_port, curr_state, desired_state)
    return {'state':'ok','message':'Mux'}

@pman.route("/ob1", methods=["POST"])
def ob1():
    d = json.loads(request.data)
    args = d['args']
    com_port = args[0]
    channel_to_initialize = args[1]
    pressure_to_set = args[2]
    ob1_state_control(com_port, channel_to_initialize, pressure_to_set)
    return {'state':'ok','message':'OB1'}

@pman.route("/density-and-flow", methods=["POST"])
def densityAndFlow():
    d = json.loads(request.data)
    args = d['args']
    com_port = args[0]
    density, flow = get_density_and_flow(com_port)
    return {'state':'ok','message':{'density':density,'flow':flow}}

@pman.route("/dist", methods=["POST"])
def dist():
    d = json.loads(request.data)
    args = d['args']
    com_port = args[0]
    initial_set_valveID = args[1]
    desired_set_valveID = args[2]
    dist_state_control(com_port, initial_set_valveID, desired_set_valveID)
    return {'state':'ok','message':'Valving'}

