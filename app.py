from flask import Flask, request, render_template
import sys
import time
from ctypes import *
from Elveflow64 import *

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("mux_button"):
            # Redirect to the Mux control page
            return redirect("/mux")
        elif request.form.get("ob1_button"):
            # Redirect to the OB1 control page
            return redirect("/ob1")

    return render_template("index.html")

@app.route("/mux", methods=["GET", "POST"])
def mux():
    if request.method == "POST":
        com_port_mux = request.form["com_port_mux"]
        curr_state = [int(request.form[f"curr_state_{i}"]) for i in range(8)]
        desired_state = [int(request.form[f"desired_state_{i}"]) for i in range(8)]
        mux_state_control(com_port_mux, curr_state, desired_state)

    return render_template("mux.html")

@app.route("/ob1", methods=["GET", "POST"])
def ob1():
    if request.method == "POST":
        com_port_ob1 = request.form["com_port_ob1"]
        channel_to_initialize = int(request.form["channel_to_initialize"])
        pressure_to_set = float(request.form["pressure_to_set"])
        ob1_state_control(com_port_ob1, channel_to_initialize, pressure_to_set)

    return render_template("ob1.html")

def mux_state_control(com_port, curr_state, desired_state):
    # Initialize valve and actuate
    Instr_ID = c_int32()

    # See NIMAX or device manager to determine the instrument name 
    error = MUX_Initialization(com_port.encode('ascii'),byref(Instr_ID)) 

    # All functions will return error codes to help you to debug your code
    print('error:%d' % error)
    print("Mux Wire: %d" % Instr_ID.value)

    # All of the 16 channels are set to LOW state (0) in the following line
    valve_state=(c_int32*16)(0) 

    # Set all valves to curr_state
    for i in range (8):
        valve_state[i] = c_int32(curr_state[i])

    # Set the state of the channels as per new config set in previous lines
    error=MUX_Wire_Set_all_valves(Instr_ID.value, valve_state, 16) 
    time.sleep(2)
    # Set all valves to curr_state
    for i in range (8):
        valve_state[i] = c_int32(desired_state[i])

    # Set the state of the channels as per new config set in previous lines
    error=MUX_Wire_Set_all_valves(Instr_ID.value, valve_state, 16) 
    time.sleep(10)
    # Close the communication with MUX Wire connected on COM24
    error=MUX_Destructor(Instr_ID.value)
    time.sleep(2)

def ob1_state_control(com_port, channel_to_initialize, pressure_to_set):
    # Initialize OB1 
    Instr_ID = c_int32()
    # Initialize channel 2 among 4 channels. (0,2,0,0)
    error = OB1_Initialization(com_port.encode('ascii'),0,channel_to_initialize,0,0,byref(Instr_ID)) 
    # All functions will return error codes to help you to debug your code
    print('error:%d' % error)
    print("OB1 ID: %d" % Instr_ID.value)
    # Always define array this way, calibration should have 1000 elements
    Calib = (c_double*1000)() 
    # Select channel in the controller. Here channel 2 is selected. 
    # User may select any of the 2 channels (1 and 2 for setting pressure,  3 and 4 for setting vacuum
    set_channel=int(channel_to_initialize) # convert to int
    set_channel=c_int32(set_channel) # convert to c_int32
    # Set pressure to 2000 mbar on channel 2
    set_pressure=float(pressure_to_set) 
    # convert to c_double
    set_pressure=c_double(set_pressure)
    error=OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib),1000) 
    time.sleep(2)

if __name__ == "__main__":
    app.run(debug=True, port = 6010)
