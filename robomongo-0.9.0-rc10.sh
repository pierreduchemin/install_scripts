#/bin/bash

wget https://download.robomongo.org/0.9.0-rc10/linux/robomongo-0.9.0-rc10-linux-x86_64-33c89ea.tar.gz -O /tmp/robomongo-0.9.0-rc10-linux-x86_64-33c89ea.tar.gz

# Delete previous installs
sudo rm -rf /opt/robomongo
tar -xf /tmp/robomongo-0.9.0-rc10-linux-x86_64-33c89ea.tar.gz robomongo-0.9.0-rc10-linux-x86_64-33c89ea -C /tmp
sudo mv /tmp/robomongo-0.9.0-rc10-linux-x86_64-33c89ea /opt/robomongo
