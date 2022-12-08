# Poweron/poweroff Onkyo A-9010 receiver on librespot event
## Works on a Raspberry pi 3

## Install

 - sudo mkdir /opt/onkyo
 - sudo chmod -R 0755 /opt/onkyo
 - cd /opt/onkyo
 - sudo git clone https://github.com/aperfectcypher/onkyo-ri-librespot.git .
 - sudo apt install python3-pip
 - pip install pigpio
 - sudo apt install pigpio
 - sudo systemctl start pigpiod.service
 - sudo systemctl enable pigpiod.service
 - sudo mv onkyo-ri.service /lib/systemd/system
 - sudo systemctl daemon-reload
 - sudo systemctl enable onkyo-ri
 - sudo systemctl start onkyo-ri


Add this to librespot's cmd line: 
- /usr/bin/librespot __--onevent /opt/onkyo/spothook.sh__

- [ ] TODO write a setup
