#!/bin/bash

sudo mkdir -p /opt/play
cd /opt/play
wget https://downloads.typesafe.com/play/1.4.4/play-1.4.4.zip -O /tmp/play-1.4.4.zip
unzip /tmp/play-1.4.4.zip -d /tmp
rm /tmp/play-1.4.4.zip
sudo mv /tmp/play-1.4.4 /opt/play/play-1.4.4
sudo chmod +x /opt/play/play-1.4.4/play

sudo update-alternatives --remove-all play
sudo update-alternatives --install /usr/bin/play play /opt/play/play-1.4.4/play 1

touch ~/.bashrc && echo "export PLAY_HOME=/opt/play/play-1.4.4" >> ~/.bashrc
touch ~/.bashrc && echo "export PATH=$PATH:$PLAY_HOME" >> ~/.bashrc
