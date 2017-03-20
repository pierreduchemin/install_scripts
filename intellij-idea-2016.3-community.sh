#!/bin/bash

COMMUNITY_DOWNLOAD_URL="https://download.jetbrains.com/idea/ideaIC-2016.3.5.tar.gz"

# Download IntelliJ community edition
COMMUNITY_PACKAGE_NAME=${COMMUNITY_DOWNLOAD_URL##*/}
wget $COMMUNITY_DOWNLOAD_URL -O /tmp/$COMMUNITY_PACKAGE_NAME

echo "Verifying sha-256 checksum for community edition..."
wget $COMMUNITY_DOWNLOAD_URL.sha256 -O /tmp/$COMMUNITY_PACKAGE_NAME.sha256
COMMUNITY_SHA256_SOURCE="$(sudo sha256sum /tmp/$COMMUNITY_PACKAGE_NAME | cut -d ' ' -f 1)"
COMMUNITY_SHA256_TARGET="$(cat /tmp/$COMMUNITY_PACKAGE_NAME.sha256 | cut -d ' ' -f 1)"
if [ ! $COMMUNITY_SHA256_SOURCE = $COMMUNITY_SHA256_TARGET ]; then
  echo "Invalid sha256 for community edition. Check download url and try running this script again."
  exit 1
fi

echo "Extract community edition..."
tar -xvf /tmp/$COMMUNITY_PACKAGE_NAME -C /tmp
rm /tmp/$COMMUNITY_PACKAGE_NAME
sudo mkdir -p /opt/idea-IC
sudo mv /tmp/idea-IC-*/* /opt/idea-IC

if [ -d plugins ]; then
  echo "Copying plugins..."
  sudo cp -R plugins/* /opt/idea-IC/plugins/
fi

echo ""
echo "================================="
echo "Please follow wizard instructions"
echo "================================="
sh /opt/idea-IC/bin/idea.sh &
