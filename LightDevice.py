import json
from re import S
from xmlrpc.client import boolean
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883


class Light_Device():
    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices.
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._register_device(
            self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    def _register_device(self, device_id, room_type, device_type):
        msg = {"id": device_id, "room": room_type, "d_type": device_type}
        self.client.publish("device"+'/'+room_type+"/"+device_type +
                            "/"+device_id, json.dumps(msg))

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        print("Connected with result code "+str(result_code))
        self.client.subscribe(self._device_id)
        self.client.subscribe("status")
        self.client.subscribe("switch/"+self._room_type +
                              "/"+self._device_type+"/"+self._device_id)

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if msg.topic == "status":
            s_report = self._status(json.loads(msg.payload)["req"])
            if s_report != None:
                self.client.publish("s_report", json.dumps(s_report))

        elif msg.topic == "switch/"+self._room_type+"/"+self._device_type+"/"+self._device_id:
            print("HElloooo")
            res = json.loads(msg.payload)['req']
            swt = json.loads(msg.payload)['switch']
            self._set_switch_status(swt)
            print("\nProcesing switch request for "+res+" to "+swt)

        else:
            if(json.loads(msg.payload)['register']):
                self._device_registration_flag = True
                print("LIGHT-DEVICE Register : ",
                      self._device_registration_flag)
            return self

    def _on_disconnect(client, userdata, rc):
        print("Disconnected with result code "+str(rc))

    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        print("Preparing Swtitch")
        self._switch_status = switch_state
        return self

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        self._light_intensity = light_intensity
        return self

    def _status(self, req):
        if req == self._device_id:
            return {"device id": self._device_id,
                    "switch": self._switch_status,
                    "intensity": self._get_light_intensity()}
        elif req == self._device_type:
            return {"device id": self._device_id,
                    "switch": self._switch_status,
                    "intensity": self._get_light_intensity()}
        elif req == self._room_type:
            return {"device_type": self._device_type,
                    "device id": self._device_id,
                    "switch": self._switch_status,
                    "intensity": self._get_light_intensity()}
        elif req == "all":
            return {"room": self._room_type,
                    "device_type": self._device_type,
                    "device id": self._device_id,
                    "switch": self._switch_status,
                    "intensity": self._get_light_intensity()}
        else:
            return None

    # def _switch_status(self, switch, req):
    #     data = self._status(req)
    #     if data != None:
    #         self._set_switch_status(switch)
    #         data = self._self._status(req)
    #         self.client.publish("s_switch", json.dumps(
    #             {"res": req, "data": data}))
