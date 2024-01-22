import sys
from email.header import UTF8
import time
from ctypes import *
from array import array
from Elveflow64 import *

# Add ‘dll’ files and ‘Elveflow64.py’ file in the following directories
# edit the following 2 lines to add the path.
sys.path.append('C:/dev/SDK/Python_64/DLL64')#add the path of the dll files here
sys.path.append('C:/dev/SDK/Python_64')#add the path of the Elveflow64.py

"""
    Method: 
        Returns the density and flow of the liquid at the time of execution of this method
    Args: 
        1. com_port - com port assigned to the flowmeter
    Returns:
        1. Density
        2. Flow
"""
def get_density_and_flow(com_port):
    density_response = 0
    flow_response = 0
    while True:
        # Initialization of BFS ( ! ! ! REMEMBER TO USE .encode('ascii') ! ! ! )
        Instr_ID=c_int32()
        error=BFS_Initialization(com_port.encode('ascii'),byref(Instr_ID))
        #all functions will return error codes to help you to debug your code
        print('error:%d' % error)
        print("Instr ID: %d" % Instr_ID.value)
        density=c_double(-1)
        error=BFS_Get_Density(Instr_ID.value,byref(density))
        #print('Density: ',density.value)
        density_response = density.value
        flow=c_double(-1)
        error=BFS_Get_Flow(Instr_ID.value,byref(flow))
        #print('Flow in microliters/min: ',flow.value)
        flow_response = flow.value
        # Calling destructor function
        error=BFS_Destructor(Instr_ID.value)
        return density_response, flow_response

# def main():
#     density_response, flow_response = get_density_and_flow('COM24')
#     print(f'Density: ',density_response)
#     print(f'flow (microliters/min): ',flow_response)

# if __name__ == "__main__":
#     main()