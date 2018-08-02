#!/usr/bin/env bash

vagrant --version > /dev/null || \
  { echo 'Vagrant not found.  You can install it with the command "brew cask install vagrant"'; exit; }
vboxmanage --version > /dev/null || \
  { echo 'Virtualbox not found.  You can install it with the command "brew cask install virtualbox"'; exit; }

set -e

echo 'Type a name for the new machine and press Enter: '
read MACHINE_NAME

mkdir -p vagrant_data

if [ ! -f vagrant-ubuntu.ova ]; then
  vagrant up
  vagrant halt
  VM_NAME=$(vboxmanage list vms | grep -o '".*"' | sed 's/"//g' | tail -n1)
  vboxmanage export "$VM_NAME" --output vagrant-ubuntu.ova
  vagrant destroy
fi

vboxmanage import vagrant-ubuntu.ova -vsys 0 --cpus 4 --memory 8196 --vmname $MACHINE_NAME
vboxmanage modifyvm $MACHINE_NAME --accelerate3d off

DISK_ID=$(vboxmanage showvminfo "$MACHINE_NAME" | grep -E '(SCSI|SATA).*UUID' | head -n 1 | sed 's/^.*UUID: \(.*\))/\1/')
echo "Please create an entry for the disk encryption password in this project's password vault, and paste it below:"
vboxmanage encryptmedium $DISK_ID --newpassword - --newpasswordid "disk-encryption" --cipher "AES-XTS256-PLAIN64"

echo "Encrypted VM successfully created"
