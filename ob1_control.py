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
        sets the air/vacuum pressure to one of the 4 channels (depending on method args) in the OB1 
    Args: 
        1. com_port (type : str) - com port assigned to OB1
        2. channel_to_initialize (type : int) - value ranging from 1 to 4. Channel 1 and 2 are for setting air pressure. Channel 3 and 4 are for setting vacuum pressure
        3. pressure_to_set (type : float) - Air/vacuum pressure to be set on the channel number given by previous arg (channel_to_initialize) 
"""

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
    time.sleep(1)
    
# def main():
#     ob1_state_control('COM25', 2, 0)

# if __name__ == "__main__":
#     main()
