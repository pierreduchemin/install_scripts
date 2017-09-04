#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import os
import subprocess
import shutil
import git

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

print("Checking Cerebro latest version...")

latestVersion = str(getLatestTag("https://github.com/KELiON/cerebro.git"))[1:]
downloadUrl = "https://github.com/KELiON/cerebro/releases/download/v" + latestVersion + "/cerebro_" + latestVersion + "_amd64.deb"

print("Downloading Cerebro...")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
request = urllib.request.Request(downloadUrl, None, headers)
with urllib.request.urlopen(request) as response:
   installerBytes = response.read()

print("Writing install files...")

with open("/tmp/cerebro.deb", 'wb') as file:
    file.write(installerBytes)
    file.close()

print("Installing Cerebro...")

os.chmod("/tmp/cerebro.deb", 755)
subprocess.call(["sudo", "-S", "dpkg", "-i", "/tmp/cerebro.deb"])

os.remove("/tmp/cerebro.deb")
