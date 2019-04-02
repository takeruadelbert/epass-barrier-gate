install:
	sudo python3 service.py
uninstall:
	sudo python3 uninstall-service.py
run:
	sudo chmod 644 /lib/systemd/system/epass.service
	sudo systemctl daemon-reload
	sudo systemctl enable epass.service
	sudo systemctl start epass.service
	sudo systemctl status epass.service