#!/usr/bin/python3
# The script connects to the mqtt broker and suscribe to topics that start
# With it's message ID

import paho.mqtt.client as mqtt
import os
from subprocess import Popen

broker_address = os.environ.get('MQTT_BROKER')
client_id = os.environ.get('MQTT_CLIENT')
username = os.environ.get('MQTT_USERNAME')
password = os.environ.get('MQTT_PASSWORD')

# This should be used to execute commands on the computer
commands = {
            'suspend': 'systemctl suspend',
            'shutdown': 'shutdown now',
            'reboot': 'reboot now',
            'lock': 'i3lock',
            'lock_standby': 'i3lock && xset dpms force off'
            }

# This should be used to send status information
status = {
        'status': 'uptime'
        }


def on_connect(client, userdata, flags, rc):
    rc = str(rc)
    print(f"Connected with {client_id} and result code {rc}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(client_id + '/#')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(msg.topic+" " + payload)

    if msg.topic == f"{client_id}/cmnd":
        print("Matches cmnd")
        if payload in commands:
            client.publish(f"{client_id}/stat", payload=payload)
            print(f"Executing {payload}")
            os.system(commands[payload])

    elif msg.topic == f"{client_id}/status":
        print("Matches stat")
        if payload in status:
            print(f"Executing {payload}")
            get_uptime = Popen(status[payload])
            uptime = get_uptime.read()
            client.publish(f"{client_id}/stat", payload=uptime)


client = mqtt.Client(client_id=client_id)
client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)
client.loop_forever()
