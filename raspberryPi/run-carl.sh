# @Author: djvolz
# @Date:   2016-11-15 22:26:01
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 22:26:21
#!/bin/bash

while true; do
	python /home/pi/djvolz/dev/CarlLights/raspberryPi/main.py
done

#put this in your crontab as root (sudo crontab -e)
#@reboot /home/pi/djvolz/dev/CarlLights/raspberryPi/main.py
