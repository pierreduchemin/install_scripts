#!/bin/bash

# Removes potential old installs
sudo apt-get purge "lxc-docker*"
sudo apt-get purge "docker.io*"

# Install required packages for docker
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates linux-image-extra-$(uname -r) linux-image-extra-virtual

# Add docker repo
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
sudo apt-get update

# Install docker
sudo apt-get install docker-engine docker-compose
sudo service docker start

# Add current user to docker group
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
newgrp docker
