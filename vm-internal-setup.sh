#!/usr/bin/env bash

apt-get update
apt-get install -y git lxterminal xfce4 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11 gdm3 firefox apt-transport-https ca-certificates curl software-properties-common ruby python-pip

gem install bundle-audit brakeman
pip install bandit

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
apt-get update
apt install -y docker-ce
usermod -aG docker vagrant
