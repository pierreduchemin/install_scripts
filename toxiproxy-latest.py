#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import os
import git
import shutil

def getLatestTag(repoUrl):
    repo_path = os.path.join('/tmp', 'cerebro_source')

    if os.access(repo_path, os.F_OK):
        shutil.rmtree(repo_path)

    empty_repo = git.Repo.init(repo_path)
    origin = empty_repo.create_remote('origin', repoUrl)

    origin.fetch()

    tags = sorted(empty_repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = tags[-1]

    if os.access(repo_path, os.F_OK):
        shutil.rmtree(repo_path)

    return latest_tag

if os.getuid() != 0:
    print("This application must be executed as root")
    exit(1)

appDirectory = "/opt/toxiproxy"
tempDirectory = "/tmp"

cliName = "toxiproxy-cli"
serverName = "toxiproxy-server"

cliPath = appDirectory + "/" + cliName
serverPath = appDirectory + "/" + serverName

cliTemp = tempDirectory + "/" + cliName
serverTemp = tempDirectory + "/" + serverName

if not os.access(appDirectory, os.F_OK):
    os.makedirs(appDirectory)

print("Checking Cerebro latest version...")

latestVersion = str(getLatestTag("https://github.com/Shopify/toxiproxy.git"))

print("Downloading Toxiproxy...")
urllib.request.urlretrieve("https://github.com/Shopify/toxiproxy/releases/download/" + latestVersion + "/toxiproxy-cli-linux-amd64", cliTemp)
urllib.request.urlretrieve("https://github.com/Shopify/toxiproxy/releases/download/" + latestVersion + "/toxiproxy-server-linux-amd64", serverTemp)

print("Installing Toxiproxy...")
os.rename(cliTemp, cliPath)
os.chmod(cliPath, 755)

os.rename(serverTemp, serverPath)
os.chmod(serverPath, 755)

# Add to path
if not os.access("/usr/local/bin/" + cliName, os.F_OK):
    os.symlink(cliPath, "/usr/local/bin/" + cliName)

if not os.access("/usr/local/bin/" + serverName, os.F_OK):
    os.symlink(serverPath, "/usr/local/bin/" + serverName)
