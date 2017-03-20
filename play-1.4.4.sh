#!/bin/bash

sudo mkdir -p /opt/play
cd /opt/play
wget https://github.com/playframework/play1/archive/1.4.4.tar.gz -O /tmp/play-1.4.4.tar.gz
tar -xf /tmp/play-1.4.4.tar.gz -C /tmp
rm /tmp/play-1.4.4.tar.gz
sudo mv /tmp/play1-1.4.4 /opt/play/play-1.4.4
sudo chmod +x /opt/play/play-1.4.4/play

sudo update-alternatives --remove-all play
sudo update-alternatives --install /usr/bin/play play /opt/play/play-1.4.4/play 1

touch ~/.bashrc && echo "export PLAY_HOME=/opt/play/play-1.4.4" >> ~/.bashrc
