#!/bin/bash
source /etc/pc_mqtt_control/env.app
printf "Off" | /bin/nc -q 1 127.0.0.1 $SOCKET_PORT
