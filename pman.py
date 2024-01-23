from flask import Blueprint, request, render_template
from ob1_control import ob1_state_control
from mux_control import mux_state_control
from flowmeter_control import get_density_and_flow

pman = Blueprint('pman', __name__)

@pman.route("/mux", methods=["POST"])
def mux():
    com_port_mux = request.form["com_port_mux"]
    curr_state = [int(request.form[f"curr_state_{i}"]) for i in range(8)]
    desired_state = [int(request.form[f"desired_state_{i}"]) for i in range(8)]
    mux_state_control(com_port_mux, curr_state, desired_state)
    return {'state':'ok','message':'Mux'}

@pman.route("/ob1", methods=["POST"])
def ob1():
    com_port_ob1 = request.form["com_port_ob1"]
    channel_to_initialize = int(request.form["channel_to_initialize"])
    pressure_to_set = float(request.form["pressure_to_set"])
    ob1_state_control(com_port_ob1, channel_to_initialize, pressure_to_set)
    return {'state':'ok','message':'OB1'}

@pman.route("/density-and-flow", methods=["POST"])
def densityAndFlow():
    com_port = ''
    density, flow = get_density_and_flow(com_port)
    return {'state':'ok','message':{'density':density,'flow':flow}}
