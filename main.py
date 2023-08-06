import time
from EdgeServer import Edge_Server
from LightDevice import Light_Device
from ACDevice import AC_Device

WAIT_TIME = 0.25  

print("\nSmart Home Simulation started.")
# Creating the edge-server for the communication with the user

edge_server_1 = Edge_Server('edge_server_1')
time.sleep(WAIT_TIME)  

# Creating the light_device
print("Intitate the device creation and registration process." )
print("\nCreating the Light devices for their respective rooms.")
light_device_1 = Light_Device("light_1", "Kitchen")
light_device_2 = Light_Device("light_2", "DR")
light_device_3 = Light_Device("light_3", "BR1")

time.sleep(WAIT_TIME) 

# print(edge_server_1.get_registered_device_list())

# Creating the ac_device  
print("\nCreating the AC devices for their respective rooms. ")
ac_device_1 = AC_Device("ac_1", "BR1")
ac_device_2 = AC_Device("ac_2", "DR")
time.sleep(WAIT_TIME)  

#Comand ID
# 1- device id, 2-device type, 3-room type, 4-all
edge_server_1.get_status("all")
time.sleep(WAIT_TIME) 

# switch = ON\OFF, req = device id,device type,room type,all, responds
edge_server_1.set_status("ON", "switch/Kitchen/LIGHT/light_1")
time.sleep(WAIT_TIME) 

# 1- device id, 2-device type, 3-room type, 4-all
edge_server_1.get_status("light_1")
time.sleep(WAIT_TIME) 
 
print("\nSmart Home Simulation stopped.")
edge_server_1.terminate()