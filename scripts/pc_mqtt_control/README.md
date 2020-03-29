# MQTT pc Control

This program simply allows integration of the pc using mqtt into any system, parituclary this time into Home Assistant. Is done over MQTT to avoid having ssh-keys in the Home Assistant server that can execute commands.

**Right now it runs as user, therefore suspend or reboot won't work unless modified in the system**

## Requirements

- Python 3
- paho-mqtt ```pip3 install paho-mqtt```

## To Use

Fill env.app, systemd service, and move the program to $HOME/bin
```
# Move the script to the proper path
mkdir -p $HOME/bin/pc_mqtt_control
mv pc_mqtt_control.py env.app -t $HOME/bin/pc_mqtt_control
# Move the systemd unit file to the proper path
mkdir -p $HOME/.config/systemd/user
mv pc_mqtt_control.service $HOME/.config/systemd/user
# Start the service
systemctl --user daemon-reload
systemctl --user start pc_mqtt_control
```

Now to trigger suspend, send an MQTT message as:
```
# The client-id is defined in env.app
mosquito_pub -t {client-id}/cmnd -m suspend
```

## Check status
```
systemctl --user pc_mqtt_service status
```

# Check Logs
```
journalctl --user -u pc_mqtt_control
```
