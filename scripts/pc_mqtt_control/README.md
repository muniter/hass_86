# MQTT pc Control

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
