#!/usr/bin/python3
# The script connects to the mqtt broker and suscribe to topics that start
# With it's message ID

import os
import json
import time
import threading
import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

from subprocess import check_output as check_o
from subprocess import CalledProcessError

import paho.mqtt.client as mqtt


def pub_status(client, state='On'):
    '''Poll the status from system and return it as a json'''

    '''
    TODO: Add support for idle status (use swayidle)
    '''
    p = {}
    with open('/proc/uptime', 'r') as up, open('/proc/loadavg') as la:
        uptime = up.read().split()[0]
        la = la.read().strip().split()[:3]

    p['state'] = state
    p['uptime'] = uptime
    p['users'] = check_o(['who', '-q'],
                         encoding='utf-8').strip().split('=')[-1]
    p['l1'], p['l5'], p['l15'] = la
    try:
        p['lock'] = 1 if check_o(['pgrep', '-c', 'i3lock']) else 0
    except CalledProcessError:
        p['lock'] = 0

    payload = json.dumps(p)
    print(payload)

    return client.publish(topic=_TOPIC_TELE_, payload=payload)


def on_connect(client, userdata, flags, rc):
    '''Callback function to execute on connect/reconnect'''

    print(f'Connected with result code {str(rc)}')

    client.subscribe(_TOPIC_CMND_)
    pub_status(client)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    '''Callback function to execute on message and send a json payload'''
    # TODO instead of executing the command here, call another function
    # to do so.

    payload = msg.payload.decode('utf-8')
    print('recieved:', msg.topic, payload, sep=' ')

    if payload in commands:  # commands is a dictionary
        print(f'Executing {payload}')
        os.system(commands[payload])


def state_thread(interval=60):
    '''Thread function to preiodically send payload'''
    while True:
        pub_status(client)
        time.sleep(interval)

def handle_sleep(dbus_object):
    if dbus_object.numerator == 1:
        print('Recieved system sleep signal, setting off state')
        return client.publish(topic=_TOPIC_TELE_, payload='{"state": "Off"}')
    else:
        print('System Waking up, setting Online state')
        return pub_status(client)



if __name__ == '__main__':
    _NAME_ = os.environ.get('NAME')
    _TOPIC_TELE_ = f"{_NAME_}/tele"
    _TOPIC_CMND_ = f"{_NAME_}/cmnd"

    '''The key is the payload that must be recieved, to execute the value
    which is the command to execute'''
    COMMANDS = os.environ.get('COMMANDS').split(',')
    commands = dict(map(lambda x: x.split(':', 1), COMMANDS))

    client = mqtt.Client()
    client.username_pw_set(os.environ.get('MQTT_USERNAME'),
                           os.environ.get('MQTT_PASSWORD'))
    client.on_connect = on_connect
    client.on_message = on_message
    client.will_set(topic=_TOPIC_TELE_, payload='{"state": "Off"}', qos=1, retain=True)
    client.connect(os.environ.get('MQTT_BROKER'))
    # Thread that sends a messge every 60 seconds with the status
    state_thread = threading.Thread(target=state_thread, args=(60,))
    state_thread.start()
    client.loop_start()

    DBusGMainLoop(set_as_default=True)     # integrate into gobject main loop
    bus = dbus.SystemBus()                 # connect to system wide dbus
    bus.add_signal_receiver(               # define the signal to listen to
        handle_sleep,                      # callback function
        'PrepareForSleep',                 # signal name
        'org.freedesktop.login1.Manager',  # interface
        'org.freedesktop.login1'           # bus name
    )
    
    loop = GLib.MainLoop()
    loop.run()
