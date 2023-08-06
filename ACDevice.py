import json
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
    
class AC_Device():
    
    _MIN_TEMP = 18  
    _MAX_TEMP = 32  

    def __init__(self, device_id, room):
        
        self._device_id = device_id
        self._room_type = room
        self._temperature = 22
        self._device_type = "AC"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)  
        self.client.on_connect = self._on_connect  
        self.client.on_message = self._on_message  
        self.client.on_disconnect = self._on_disconnect  
        self.client.connect(HOST, PORT, keepalive=60)  
        self.client.loop_start()  
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    # calling registration method to register the device
    def _register_device(self, device_id, room_type, device_type):
        msg = {"id": device_id, "room": room_type, "d_type": device_type}
        self.client.publish("device"+'/'+room_type+"/"+device_type +
                            "/"+device_id, json.dumps(msg))

    # Connect method to subscribe to various topics. 
    def _on_connect(self, client, userdata, flags, result_code):
        print("Connected with result code "+str(result_code))
        self.client.subscribe(self._device_id)
        self.client.subscribe("status")
        self.client.subscribe("switch/"+self._room_type+"/"+self._device_type+"/"+self._device_id)

    def _on_disconnect(client, userdata, rc):
        print("Disconnected with result code "+str(rc))

    # method to process the recieved messages and publish them on relevant topics 
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg): 
        if msg.topic == "status":
            s_report = self._status(json.loads(msg.payload)["req"])
            if s_report != None:
                # print("S_report", s_report)
                self.client.publish("s_report", json.dumps(s_report))
        elif msg.topic == "switch":
            res = json.loads(msg.payload)['req']
            swt = json.loads(msg.payload)['switch']
            print("\nProcesing switch request for "+res+" to "+swt)
            self._set_switch_status(swt)
            
        else:
            if(json.loads(msg.payload)['register']):
                self._device_registration_flag = True
                print("AC-DEVICE Register : ",self._device_registration_flag)
            return self

    # Getting the current switch status of devices 
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        self._switch_status = switch_state
        return self

    # Getting the temperature for the devices
    def _get_temperature(self):
        return self._temperature        

    # Setting up the temperature of the devices
    def _set_temperature(self, temperature):
        self._temperature = temperature
        return self

    def _status(self, req):
        if req == self._device_id:
            return {"device id": self._device_id,
                    "switch": self._switch_status,
                    "Temperature": self._get_temperature()}
        elif req == self._device_type:
            return {"device id": self._device_id,
                    "switch": self._switch_status,
                    "temperature": self._get_temperature()}
        elif req == self._room_type:
            return {"device_type": self._device_type,
                    "device id": self._device_id,
                    "switch": self._switch_status,
                    "temperature": self._get_temperature()}
        elif req == "all":
            return {"room": self._room_type,
                    "device_type": self._device_type,
                    "device id": self._device_id,
                    "switch": self._switch_status,
                    "temperature": self._get_temperature()}
        else:
            return None
    
    # def _switch_status(self, switch, req):
    #     data = self._status(req)
    #     if data != None:
    #         self._set_switch_status(switch)
    #         data = self._self._status(req)
    #         self.client.publish("s_switch", json.dumps(
    #             {"res": req, "data": data}))