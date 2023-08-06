
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
WAIT_TIME = 0.25


class Edge_Server:
    def __init__(self, instance_name):
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        print("Connected with result code "+str(result_code))
        self.client.subscribe("device/#")
        self.client.subscribe("s_report")

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        if msg.topic == "s_report":
            status_list = []
            status_list.append(json.loads(msg.payload))
            print(status_list)
        
        elif msg.topic == "s_switch":
            print("Here is the switch status for ",
                  json.loads(msg.payload)["res"], " : ", 
                  json.loads(msg.payload)["data"])
            print("Request Executed")

        else:
            item = {"topic": msg.topic, "payload": {
                "room": json.loads(msg.payload)['room'],
                "device_id": json.loads(msg.payload)['id'],
                "type": json.loads(msg.payload)["d_type"]}
            }
            print('Registration is acknowledge for device ',
                  json.loads(msg.payload)['id'])
            self._registered_list.append(item)
            self.client.publish(json.loads(msg.payload)[
                'id'], json.dumps({"register": True}))

    def _on_disconnect(client, userdata, rc):
        print("Disconnected with result code "+str(rc))

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self, req):
        print("\nRequesting status for ", req)
        self.client.publish("status", json.dumps(
            {'req': req}))

    # Controlling and performing the operations on the devices
    # based on the request received
    def set(self):
        pass

    def set_status(self, switch, req):
        print(req)
        self.client.publish(req, json.dumps(
            {"switch": switch, "req": req}))
