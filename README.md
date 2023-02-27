# IoT-Gateway
This project contains 2 gateways designed for an IoT Conference Project. Assuming that each participant has a beacon attached on his/her wrist (like a watch) or around his/her neck (like a necklace), the gateways are designed to scan for Bluetooth LE Advertisement Data and handle them in order to offer the following services:
## Room Gateway
1) Saves the viewers that are present in a conference talk and the duration of their stay
2) When a viewer presses the "question" button on their beacon, the gateway sends a question request to the server
## Hall Gateway
1) When someone approaches a kiosk, the people behind the kiosk can see the person's data (authorized beacon)
2) Saves requests for personal data exchange. Those requests are initiated by a button on the beacon

# Installation
This project only runs on Linux devices, and it needs to be run as root (in order to access the BLE adapter).
Both gateways require the installation of 3 python libraries ([bluepy](https://github.com/IanHarvey/bluepy), [dotenv](https://pypi.org/project/python-dotenv/), requests).  
Before running a gateway, you have to add a dotenv file including the IP where the IoT server is hosted.
## Docker
Both gateways are stored in the docker hub and can be found in the following links:  
https://hub.docker.com/r/fchalantzoukas/room-gtw  
https://hub.docker.com/r/fchalantzoukas/hall-gtw  
In order to run a docker image that is already pulled, run `docker run -ti --net=host --privileged NAME:latest`. The `--net=host` and `privileged` options are needed in order to have access to the Bluetooth adapter of the host machine.
