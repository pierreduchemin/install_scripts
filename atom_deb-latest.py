#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import os, stat
import subprocess

print("Downloading atom...")
urllib.request.urlretrieve("https://atom.io/download/deb", "/tmp/atom-amd64.deb")
os.chmod("/tmp/atom-amd64.deb", 755)
subprocess.call(["sudo", "-S", "dpkg", "-i", "/tmp/atom-amd64.deb"])
os.remove("/tmp/atom-amd64.deb")

print("Installing atom plugins...")
subprocess.call(["apm", "install", "pretty-json"])
subprocess.call(["apm", "install", "platformio-ide-terminal"])
subprocess.call(["apm", "install", "pandoc-convert"])
subprocess.call(["apm", "install", "language-javascript-jsx"])
subprocess.call(["apm", "install", "atom-typescript"])
subprocess.call(["apm", "install", "intellij-idea-keymap"])
