#!/bin/bash
source /etc/pc_mqtt_control/env.app

case $1 in
  pre)
    printf "Sleep" | /bin/nc -q 1 127.0.0.1 $SOCKET_PORT
    ;;
  post)
    printf "On" | /bin/nc -q 1 127.0.0.1 $SOCKET_PORT
    ;;
esac
