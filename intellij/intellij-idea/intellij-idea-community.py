#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import stat
import argparse
import fileinput
import urllib.request
import hashlib
import tarfile
import shutil
import subprocess
from distutils.dir_util import copy_tree

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--packageUrl", default="https://download.jetbrains.com/idea/ideaIC-2017.3.4.tar.gz", help="a url to get an IntelliJ version")
parser.add_argument("-s", "--sha256Url", default="https://download.jetbrains.com/idea/ideaIC-2017.3.4.tar.gz.sha256", help="a sha256 url to check package integrity")
parser.add_argument("-d", "--destination", default="/opt/idea-IC", help="where IntelliJ must be installed")
parser.add_argument("-f", "--removeDestination", default=False, help="wheather or not the installer should force remove previous installations", action="store_true")
args = parser.parse_args()


def getSha256ForFile(filePath, block_size=65536):
    sha256 = hashlib.sha256()
    try:
        with open(filePath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
    except IOError:
        print("Error: can\'t find file or read data")
        sys.exit(1)
    return sha256.hexdigest()


def untarArchive(source, destination):
    tar = tarfile.open(source)
    tar.extractall(destination)
    tar.close()


def cleanExit(tempPackagePath, tempSha256Path):
    os.remove(tempPackagePath)
    os.remove(tempSha256Path)
    sys.exit(1)


if os.getuid() != 0:
    print("Error: This installer must be executed as root")
    exit(1)

packageName = args.packageUrl.split('/')[-1]
tempPackagePath = "/tmp/" + packageName
tempSha256Path = "/tmp/" + packageName + ".sha256"

if not os.path.isfile(tempPackagePath):
    print("Downloading IntelliJ Community Edition...")
    urllib.request.urlretrieve(args.packageUrl, tempPackagePath)
    os.chmod(tempPackagePath, 0o755)

print("Checking package integrity...")
if not os.path.isfile(tempSha256Path):
    urllib.request.urlretrieve(args.sha256Url, tempSha256Path)

f = open(tempSha256Path, "r")
expectedSha256 = f.readlines()[0].split()[0]
f.close()

computedSha256 = getSha256ForFile(tempPackagePath)

if expectedSha256 != computedSha256:
    print("Error: Invalid sha256 for community edition. Check download url and try again.")
    cleanExit(tempPackagePath, tempSha256Path)

print("Extracting IntelliJ Community Edition...")
untarArchive(tempPackagePath, "/tmp")

print("Checking destination folder...")
if os.path.isdir(args.destination):
    if args.removeDestination:
        print("Removing content of destination folder (" + args.destination + ")...")
        shutil.rmtree(args.destination)
    else:
        print("Error: " + args.destination + " already exists")
        cleanExit(tempPackagePath, tempSha256Path)

print("Copying files to destination folder (" + args.destination + ")...")
for f in os.listdir("/tmp"):
    if f.startswith("idea-IC-"):
        shutil.move("/tmp/" + f, args.destination)

# Deploy plugins
if os.path.isdir("plugins"):
    print("Extracting plusgins...")
    subprocess.Popen(["tar -xf", "plugins.tar.gz"])

    print("Copying plugins...")
    copy_tree("plugins", os.path.join(args.destination, "plugins"))

# Launch install wizard
print("Please follow wizard instructions")
subprocess.Popen(["sh", args.destination + "/bin/idea.sh"])

# Delete downloaded files
os.remove(tempPackagePath)
os.remove(tempSha256Path)
