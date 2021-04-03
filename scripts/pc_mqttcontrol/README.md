# MQTT pc Control

TODO:Fix this docs since this is not running as root anymore

This program simply allows integration of the pc using mqtt into any system, parituclary this time into Home Assistant. Is done over MQTT to avoid having ssh-keys in the Home Assistant server that can execute commands.


## Requirements

- Python 3
- paho-mqtt (Install for root user) ```sudo su && umask 022 && pip3 install paho-mqtt```

## To Use

**Fill env.bak and rename to env.app**, then run as root ```bash ./install.sh```

Now to trigger suspend, reboot, shutdown, etc. send an MQTT message as:
```
# The client-id is defined in env.app
mosquito_pub -t {client-id}/cmnd -m suspend
```

## Check status
```
systemctl pc_mqtt_service status
```

# Check Logs
```
journalctl -u pc_mqtt_control
```

# Integrate into Home Assistant

The program will send an mqtt message every 60 seconds that looks like this:
```{"state": "On", "uptime": "20003.26", "users": "10", "l1": "0.47", "l5": "0.42", "l15": "0.38", "lock": 0}```

All this data can be used to create an mqtt switch, and sensors.

# Configuration Example

## env.app

DISPLAY=:0 
NAME="office_pc"
USERNAME="cool"
MQTT_BROKER="192.168.1.100"
MQTT_USERNAME="mqtt"
MQTT_PASSWORD="mqtt"
# name_of_command:what_should_be_executed
COMMANDS="status::,suspend:systemctl suspend,shutdown:shutdown now,reboot:reboot now"
# Avoid common ports
SOCKET_PORT="62132"

