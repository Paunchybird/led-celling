#!/bin/bash

sudo apt-get update && sudo apt-get upgrade
#Install docker
echo "isolcpus=3" | sudo tee -a /boot/cmdline.txt
sudo sed -i -e 's/dtparam=audio=on/dtparam=audio=off/' /boot/config.txt

curl -sSL https://get.docker.com | sh

sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip

sudo pip3 install docker-compose

sudo systemctl enable docker

sudo docker pull portainer/portainer-ce:latest

sudo docker run -d -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest

git clone https://github.com/Paunchybird/led-celling.git

cd led-celling/

sudo ./restart.sh

