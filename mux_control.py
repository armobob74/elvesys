import sys
from email.header import UTF8
import time
from ctypes import *
from array import array
from Elveflow64 import *

# Add ‘dll’ files and ‘Elveflow64.py’ file in the following directories
# edit the following 2 lines to add the path.
sys.path.append('./DLL64')#add the path of the dll files here
sys.path.append('.')#add the path of the Elveflow64.py

"""
    Method: 
        switches the state of Mux 
    Args: 
        1. com_port - com port assigned to mux
        2. curr_state - integer array of size 8 (with 0 and 1 as the elements), signifying current state of all channels in a Mux. 0 - Low, 1- High 
        3. desired_state - integer array of size 8 (with 0 and 1 as the elements), signifying desired state of all channels in a Mux.
"""
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

def main():
    mux_state_control('COM28', [0,0,0,0,0,0,0,0], [1,1,1,0,0,0,0,0])

if __name__ == "__main__":
    main()
