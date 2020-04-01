# If not used i3, i3lock won't work
DISPLAY=:0 
NAME="ryzen-desktop"
USERNAME="muniter"
MQTT_BROKER="10.3.30.11"
MQTT_USERNAME="hassio"
MQTT_PASSWORD="myhassio"
COMMANDS="status::,suspend:systemctl suspend,shutdown:shutdown now,reboot:reboot now,lock:su -c \"i3lock\" -l $USERNAME,lock_standby:su -c \"i3lock && xset dpms force off\" -l $USERNAME"
SOCKET_PORT="62132"

