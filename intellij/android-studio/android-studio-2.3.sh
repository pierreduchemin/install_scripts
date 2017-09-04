#!/bin/bash

# This script can be used offline
# To do so, you can provide 1 or 2 packages of android-studio.zip and android-sdk.tar and put them in the same folder as this script
# If the archives are not found, they will be downloaded
# android-studio.zip is the downloaded archive from google
# android-sdk.tar is an archive of ~/Android from a computer where sdk is already installed. It will simply be extracted to ~

STUDIO_PACKAGE_URL=https://dl.google.com/dl/android/studio/ide-zips/2.3.2.0/android-studio-ide-162.3934792-linux.zip

sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386

# Download
if [ ! -f android-studio.zip ]; then
        wget $STUDIO_PACKAGE_URL -O android-studio.zip
fi

# Extract and install sdk
if [ -f android-sdk.tar ]; then
        tar -xf android-sdk.tar -C ~
fi

# Extract studio package
unzip android-studio.zip
sudo mkdir -p /opt
sudo mv android-studio/ /opt

# Add android studio to path
touch ~/.bashrc

# Add sdk tools to path
echo 'export ANDROID_HOME=$HOME/Android/Sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools' >> ~/.bashrc

# Launch android studio wizard
sh /opt/android-studio/bin/studio.sh &
