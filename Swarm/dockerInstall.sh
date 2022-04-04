#!/bin/bash

sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
sudo apt-cache policy docker-ce wget
sudo apt install -y docker-ce

sudo apt install -y python3
wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

cd /home/ubuntu
git clone https://github.com/graboskyc/MongoDBScaleTester.git

#sudo docker pull graboskyc/mongodb-locust-scale:v1.0.10