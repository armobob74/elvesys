import json
import time
from flask import Flask, render_template, jsonify
from dist_control import dist_state_control
from mux_control import mux_state_control
from ob1_control import ob1_state_control
from flowmeter_control import *
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import pdb

AURORA_PUMP_URL = 'http://127.0.0.1:5109'
def pmanPOST(url, args):
    """ communicate with PMAN servers """
    response = requests.post(url, json={'args':args})
    return response

def aurora_custom_cmd(cmdstr):
    response = pmanPOST(f"{AURORA_PUMP_URL}/pman/aurora-pump/custom", [cmdstr])
    return response

def read_config(file_path='config2.json'):
    with open(file_path, 'r') as file:
        config_data = json.load(file)
    return config_data


def aurora_is_busy():
    resp = pmanPOST(f'{AURORA_PUMP_URL}/pman/aurora-pump/is-busy', [])
    return resp.json()['status']

def wait_for_aurora():
    loop = True
    print("waiting for aurora")
    while loop:
        loop = aurora_is_busy()
        time.sleep(0.5)
    print("aurora is done")
    return

def vol_to_steps(vol):
    factor = 6000 / 25 # steps/ mL
    return int(factor * vol)

def clean_all():
    # Reading the port configuration of all elvesys devices 
    config = read_config()

    # step 1 : Load Clean_All_new.mxcfg on Charles bridge on COM? - valve 1, 3, 6, 7, 8 - ON
    mux_state_control( config['devices']['elvesys']['charles_bridge'], [0,0,0,0,0,0,0,0], [0,0,0,0,0,1,0,0])

    # step 2 : Set SH on COM? to valve 1. Assume Dist locking position is at valve 12
    dist_state_control(config['devices']['elvesys']['SH'], 12, 1) 

    # step 3 : Operate Aurora Pump to push DCM
    # opening up the way to axf --> do it using Aurora
    # Suck from DCM port 1 --- 15 ml at 15 mL/min (60 steps per sec)
        # Push to port 4 ---- 15 ml
    aurora_steps = vol_to_steps(5)
    aurora_custom_cmd(cmdstr=f"V60I1A{aurora_steps}O4A0R")
    wait_for_aurora()

    # step 4 : Set VH on COM? to valve 3. Assume Dist locking position is at valve 12
    dist_state_control(config['devices']['elvesys']['VH'], 11, 3) 
    
    # step 5 : Delay for 5 s 10 ms
    time.sleep(5.01)

    # step 6 : Load Clean_All_new.mxcfg on Charles bridge on COM? - valve 1, 3, 6, 7, 8 - ON
    mux_state_control( config['devices']['elvesys']['charles_bridge'], [0,0,0,0,0,1,0,0], [1,0,0,0,0,1,1,1])
    
    # step 7 : Delay for 5 s 10 ms
    time.sleep(10.01)
    mux_state_control( config['devices']['elvesys']['charles_bridge'], [1,0,0,0,0,1,1,1], [0,0,0,0,0,1,0,1])
    
    # step 8 : Delay for 20 s 10 ms
    time.sleep(20.01)

    # step 9 : Load All_valves_open_new.mxcfg on Charles bridge on COM? - all valve - OFF
    mux_state_control( config['devices']['elvesys']['charles_bridge'], [0,0,0,0,0,1,0,1], [0,0,0,0,0,0,0,0])

    # step 10: Set SH on COM? to valve 12. Assume Dist locking position is at valve 12
    dist_state_control(config['devices']['elvesys']['SH'], 1, 12) 

    # Set Aurora to 10
    aurora_custom_cmd(cmdstr=f"I10R")
    wait_for_aurora()
   
    # step 11: Set VH on COM? to valve 2. Assume Dist locking position is at valve 12
    dist_state_control(config['devices']['elvesys']['VH'], 3, 11) 


@app.route('/')
def home():
    return render_template('index_clean.html')

@app.route('/clean', methods=['POST'])
def clean():
    clean_all()
    return jsonify({"success": True, "message": "Cleaning process completed."})

if __name__ == '__main__':
    app.run(port=5005)