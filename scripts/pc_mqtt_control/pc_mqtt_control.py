#!/usr/bin/python3
# The script connects to the mqtt broker and suscribe to topics that start
# With it's message ID

import os
import json
import time
import threading
import socket

import paho.mqtt.client as mqtt
from subprocess import check_output as check_o
from subprocess import CalledProcessError


def get_status(state='On'):
    '''Get the status of the system and send it back as json'''
    p = {}
    with open('/proc/uptime', 'r') as up, open('/proc/loadavg') as la:
        uptime = up.read().split()[0]
        la = la.read().strip().split()[:3]

    p['state'] = state
    p['uptime'] = uptime
    p['users'] = check_o(['who', '-q'],
                         encoding="utf-8").strip().split('=')[-1]
    p['l1'], p['l5'], p['l15'] = la[0], la[1], la[2]
    try:
        p['lock'] = 1 if check_o(['pgrep', '-c', 'i3lock']) else 0
    except CalledProcessError:
        p['lock'] = 0

    return json.dumps(p)


def on_connect(client, userdata, flags, rc):
    '''Callback function to execute on connect/reconnect'''
    print(f"Connected with result code {str(rc)}")

    client.subscribe(_TOPIC_CMND_)
    payload = get_status()
    client.publish(topic=_TOPIC_TELE_, payload=payload)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    '''Callback function to execute on message and send a json payload'''
    payload = msg.payload.decode("utf-8")
    print(msg.topic+" " + payload)

    if payload in commands:  # commands is a dictionary
        print(f"Executing {payload}")
        command = payload
        payload = get_status()
        print(payload)  # For log keeping
        os.system(commands[command])
        client.publish(_TOPIC_TELE_, payload=payload)


def state_thread(interval=60):
    '''Thread function to preiodically send payload'''
    while True:
        payload = get_status()
        client.publish(_TOPIC_TELE_, payload=payload)
        print(payload)
        time.sleep(interval)


def socket_processing(client):
    HOST = '127.0.0.1'
    PORT = int(os.environ.get('SOCKET_PORT'))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                state = conn.recv(1024).decode("utf-8")
                print(f'received:{state} from:{addr}')
                payload = get_status(state)
                client.publish(_TOPIC_TELE_, payload=payload)


if __name__ == "__main__":
    _NAME_ = os.environ.get('NAME')
    _TOPIC_TELE_ = _NAME_ + "/tele"
    _TOPIC_CMND_ = _NAME_ + "/cmnd"

    # This should be used to execute commands on the computer
    # The key is the payload that must be sent, and the list has
    # The command to execute and the state to report
    COMMANDS = os.environ.get('COMMANDS').split(',')
    commands = {i.split(':', 1)[0]: i.split(':', 1)[1] for i in COMMANDS}

    # This should be used to send status information
    status = {
        'status': get_status(),
    }

    client = mqtt.Client()
    client.username_pw_set(os.environ.get('MQTT_USERNAME'),
                           os.environ.get('MQTT_PASSWORD'))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.environ.get('MQTT_BROKER'))
    client.loop_start()

    state_thread = threading.Thread(target=state_thread, args=(60,))
    state_thread.start()
    socket_processing(client=client)
