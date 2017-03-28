#!/bin/bash

# This script can be used offline
# To do so, you can provide 1 or 2 packages of android-studio.zip and android-sdk.tar and put them in the same folder as this script
# If the archives are not found, they will be downloaded
# android-studio.zip is the downloaded archive from google
# android-sdk.tar is an archive of ~/Android from a computer where sdk is already installed. It will simply be extracted to ~

STUDIO_PACKAGE_URL=https://dl.google.com/dl/android/studio/ide-zips/2.3.0.8/android-studio-ide-162.3764568-linux.zip
STUDIO_SHA256_TARGET=214cee47ef7a628c712ae618f5aab6c2a56a72aa479a50937d4cad5a0abf8435

sudo apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386

# Download
if [ ! -f android-studio.zip ]; then
  wget $STUDIO_PACKAGE_URL -O /tmp/android-studio.zip

  echo "Verifying sha-256 checksum for android studio..."
  STUDIO_SHA256_SOURCE="$(sudo sha256sum /tmp/android-studio.zip | cut -d ' ' -f 1)"
  if [ ! $STUDIO_SHA256_SOURCE = $STUDIO_SHA256_TARGET ]; then
    echo "Invalid sha256 for android studio. Check download url and try running this script again."
    exit 1
  fi
fi

if [ -f android-sdk.tar ]; then
  echo "Extracting android sdk..."
  tar -xf android-sdk.tar -C ~
fi

echo "Extracting android studio..."
unzip /tmp/android-studio.zip -d /tmp
sudo mkdir -p /opt
sudo mv /tmp/android-studio/ /opt

if [ -f ~/.zshrc ]; then
  echo 'export ANDROID_HOME=$HOME/Android/Sdk' >> ~/.zshrc
  echo 'export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools' >> ~/.zshrc
fi

# Add android studio to path
touch ~/.bashrc

# Add sdk tools to path
echo 'export ANDROID_HOME=$HOME/Android/Sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools' >> ~/.bashrc

if [ -d plugins ]; then
  echo "Copying plugins..."
  mkdir -p ~/.AndroidStudio2.3/config/plugins
  sudo cp -R ./plugins/* ~/.AndroidStudio2.3/config/plugins
fi

echo ""
echo "================================="
echo "Please follow wizard instructions"
echo "================================="
# Launch android studio wizard
sh /opt/android-studio/bin/studio.sh &
