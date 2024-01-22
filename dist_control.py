import sys
from email.header import UTF8
# Add ‘dll’ files and ‘Elveflow64.py’ file in the following directories
# edit the following 2 lines to add the path.
import time
from ctypes import *
from array import array
from Elveflow64 import *

sys.path.append('C:/dev/SDK/Python_64/DLL64')#add the path of the dll files here
sys.path.append('C:/dev/SDK/Python_64')#add the path of the Elveflow64.py

"""
    Method: 
        switches the valve in DIST from initial valve ID (ranging from 1 to 12) to desired valve ID
    Args: 
        1. com_port - com port assigned to DIST
        2. initial_set_valveID - integer ranging from 1-12, signifying initial valve that is connected to the output port 
        3. desired_set_valveID - integer ranging from 1-12,, signifying desired valve that should be connected to the output port
"""
def dist_state_control(com_port, initial_set_valveID, desired_set_valveID):
    # Initialize valve and actuate
    Instr_ID = c_int32()

    # See NIMAX or device manager to determine the instrument name 
    error=MUX_DRI_Initialization(com_port.encode('ascii'),byref(Instr_ID))

    # All functions will return error codes to help you to debug your code
    print('error:%d' % error)
    print("Mux DRI ID: %d" % Instr_ID.value)

    Answer=(c_char*40)()

    # Set initial state of the distributor
    set_initial_valve=c_double()
    set_initial_valve=int(initial_set_valveID)
    set_initial_valve=c_int32(set_initial_valve)
    error=MUX_DRI_Set_Valve(Instr_ID.value,set_initial_valve,1) 

    time.sleep(2)

    # Set desired state of the distributor
    to_actuate=c_double()
    to_actuate=int(desired_set_valveID)
    to_actuate=c_int32(to_actuate)
    error=MUX_DRI_Set_Valve(Instr_ID.value,to_actuate,1) 

    error=MUX_DRI_Destructor(Instr_ID.value)
    
    time.sleep(2)
    
# def main():
#     dist_state_control('COM20', 12, 1)

# if __name__ == "__main__":
#     main()
