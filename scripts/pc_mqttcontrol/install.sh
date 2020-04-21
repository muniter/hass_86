#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

PROGRAM=pc_mqttcontrol.py
SERVICE=pc_mqttcontrol.service
CONFIG_FOLDER=/etc/pc_mqttcontrol
SLEEP=mqtt_sleep
SHUTDOWN=mqtt_off
ENV=env.app

# Import paho if not installed
umask 022 && python3 -c "import paho" || pip3 install paho-mqtt

cp $SERVICE /etc/systemd/system &&\
    chmod 0644 /etc/systemd/system/$SERVICE &&\
    chown root:root /etc/systemd/system/$SERVICE 

cp $PROGRAM -t /usr/bin &&
    chmod 0644 /usr/bin/$PROGRAM &&\
    chown root:root /usr/bin/$PROGRAM

cp $SLEEP -t /lib/systemd/system-shutdown &&
    chmod 0644 /lib/systemd/system-shutdown/$SLEEP &&\
    chown root:root /lib/systemd/system-shutdown/$SLEEP

cp $SHUTDOWN -t /lib/systemd/system-shutdown &&
    chmod 0644 /lib/systemd/system-shutdown/$SHUTDOWN &&\
    chown root:root /lib/systemd/system-shutdown/$SHUTDOWN

mkdir $CONFIG_FOLDER ;\
    cp $ENV -t $CONFIG_FOLDER &&\
    chmod 0600 $CONFIG_FOLDER/$ENV &&\
    chown root:root $CONFIG_FOLDER/$ENV

systemctl daemon-reload &&\
    systemctl enable pc_mqttcontrol && \
    systemctl start pc_mqttcontrol

echo "Install completed"
