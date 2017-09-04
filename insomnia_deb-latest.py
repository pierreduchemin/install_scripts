#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os
import subprocess

print("Downloading Insomnia...")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
request = urllib.request.Request("https://builds.insomnia.rest/downloads/ubuntu/latest", None, headers)
with urllib.request.urlopen(request) as response:
   installerBytes = response.read()

print("Writing install files...")

with open("/tmp/insomnia.deb", 'wb') as file:
    file.write(installerBytes)
    file.close()

print("Installing Insomnia...")

os.chmod("/tmp/insomnia.deb", 755)
subprocess.call(["sudo", "-S", "dpkg", "-i", "/tmp/insomnia.deb"])
os.remove("/tmp/insomnia.deb")
