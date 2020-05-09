PROGRAM=pc_mqttcontrol.py
SERVICE=pc_mqttcontrol.service
CONFIG_FOLDER=/etc/pc_mqttcontrol
ENV=env.app

uninstall:
	rm /usr/bin/$(PROGRAM)
	rm /etc/systemd/system/$(SERVICE)
	rm -r $(CONFIG_FOLDER)
	systemctl stop $(SERVICE)
	systemctl disable $(SERVICE)
	systemctl daemon-reload

install:
	# Import paho if not install it
	@echo "Checking if paho-mqtt is intalled"
	umask 022 && python3 -c "import paho" || pip3 install paho-mqtt
	@echo "Copying the service file"
	cp $(SERVICE) /etc/systemd/system && chmod 0644 /etc/systemd/system/$(SERVICE) && chown root:root /etc/systemd/system/$(SERVICE) 
	@echo "Copying the program"
	cp $(PROGRAM) -t /usr/bin && chmod 0644 /usr/bin/$(PROGRAM) && chown root:root /usr/bin/$(PROGRAM)
	@echo "Setting up the configruation file"
	mkdir $(CONFIG_FOLDER) ; cp $(ENV) -t $(CONFIG_FOLDER) && chmod 0600 $(CONFIG_FOLDER)/$(ENV) && chown root:root $(CONFIG_FOLDER)/$(ENV)
	@echo "Reloading systemd"
	systemctl daemon-reload
	systemctl enable pc_mqttcontrol
	@echo "Starting the service"
	systemctl start pc_mqttcontrol
