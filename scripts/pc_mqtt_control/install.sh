#!/bin/bash

#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

umask 022 && pip3 install paho-mqtt

cp ./pc_mqtt_control.service /etc/systemd/system &&\
    chmod 0644 /etc/systemd/system/pc_mqtt_control.service &&\
    chown root:root /etc/systemd/system/pc_mqtt_control.service 

cp ./pc_mqtt_control.py /usr/bin &&
    chmod 0644 /usr/bin/pc_mqtt_control.py &&\
    chown root:root /usr/bin/pc_mqtt_control.py

cp ./sleep-hook.sh /lib/systemd/system-sleep &&
    chmod 0644 /lib/systemd/system-sleep &&\
    chown root:root /lib/systemd/system-sleep

cp ./shutdown-hook.sh /lib/systemd/system-shutdown &&
    chmod 0644 /lib/systemd/system-shutdown &&\
    chown root:root /lib/systemd/system-shutdown

mkdir /etc/pc_mqtt_control ;\
    cp ./env.app /etc/pc_mqtt_control &&\
    chmod 0777 /usr/bin/pc_mqtt_control.py &&\
    chown root:root /usr/bin/pc_mqtt_control.py

systemctl daemon-reload &&\
    systemctl enable pc_mqtt_control

echo "Install completed"
