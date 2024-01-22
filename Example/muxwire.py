#tested with Python 3.11.6 (IDE VS Code V1.84.0 + Elvesys SDK V3.8.01)
#add python_xx and python_xx/DLL to the project path

import sys
from _ast import Load
sys.path.append('C:/dev/SDK/Python_64/DLL64')#add the path of the library here
sys.path.append('C:/dev/SDK/Python_64')#add the path of the LoadElveflow.py

from ctypes import *
from array import array
from Elveflow64 import *

# Main loop : Display the density and flow of the liquid flowing through the flow meter

#while True:
# Initialization of BFS ( ! ! ! REMEMBER TO USE .encode('ascii') ! ! ! )
Instr_ID=c_int32()
# error=BFS_Initialization("COM19".encode('ascii'),byref(Instr_ID))

# See User Guide to determine regulator types and NIMAX to determine the instrument name 
error = MUX_Initialization('COM28'.encode('ascii'),byref(Instr_ID)) 

# All functions will return error codes to help you to debug your code, for further information refer to User Guide
print('error:%d' % error)
print("OB1 ID: %d" % Instr_ID.value)

valve_state=(c_int32*16)(0)
valve_state[0]=c_int32(0)
valve_state[1]=c_int32(0)
valve_state[2]=c_int32(0)
valve_state[3]=c_int32(0)
valve_state[4]=c_int32(0)
valve_state[5]=c_int32(0)
valve_state[6]=c_int32(0)
valve_state[7]=c_int32(0)
error=MUX_Wire_Set_all_valves(Instr_ID.value, valve_state, 16)  
error=MUX_Destructor(Instr_ID.value)