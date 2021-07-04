# PC MQTT control

This program simply allows integration of a linux desktop pc using mqtt into any system, I use it for Home Assistant. The program sends status reports in a configured interval.

## Requirements

- Python 3
- paho-mqtt (Will be installed by the Makefile)

## How to use

### Installation

First prepare the environment file, `cp env.bak env.app` and modify accordingly

#### Environment file

This file configures the program, the program is run as a systemd service and this values are passed as environment variables.

```
NAME="of your computer"
USERNAME="your username"
MQTT_BROKER="address of your MQTT broker"
MQTT_USERNAME=""
MQTT_PASSWORD=""
# Command format: {{mqtt payload to recevie}}:{{command to execute}} and the differents command
# are separated by a comma
COMMANDS="suspend:systemctl suspend,shutdown:shutdown now,reboot:reboot now,lock:swaylock,unlock:pkill -9 swaylock"
INTERVAL=60
```

#### Running make file

After filling the `env.app` file run `sudo make install`.

If you wan't to reconfigure you can find the configuration file in `/etc/pc_mqttcontrol/env.app`.

This will run the programs as a service aka systemd unit.

#### Uninstall

`sudo make uninstall`

### Usage

The programs sends a payload every `INTERVAL` to the topic `{NAME}/tele`, the payload it send:
```
{
    "state": "On",
    "uptime": "20003.26",
    "users": "10",
    "l1": "0.47",
    "l5": "0.42",
    "l15": "0.38",
    "lock": 0
}
```

The program also listens to systemd sleep and shutdown signals (using dbus) and sends the `{"state": "Off"}` right before the computer goes down.

To run commands configured send a mqtt message to `{NAME}/cmnd` with payload `command name` as configured in `env.app` as `COMMANDS`.

To trigger update the status send the special command `status`

To check the program logs run `journalctl -f -u pc_mqttcontrol.service` one can also restart, stop, disable, the normal systemd commands.

## Integrate into Home Assistant

You can use any mqtt sensor available, soon I'll automatically integrate with Home Assistant auto discovery.
