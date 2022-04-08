#!/bin/bash

sudo apt update
sudo apt install net-tools

ipaddr=`ip a | grep 172.31 | xargs | cut -d" " -f 2 | cut -d"/" -f1`

sudo docker swarm init --advertise-addr ${ipaddr}
sudo docker service create --name registry --publish 5000:5000 registry:2