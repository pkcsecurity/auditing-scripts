# Miscellaneous scripts for use during code audits

As a reminder, any client-specific information, names, code, keys, passwords, and exploits should **not** go in this repo.

To create an encrypted vm:
- Install virtualbox and vagrant, both of which can be installed with `brew cask install virtualbox vagrant`.
- `sh create-encrypted-vm.sh` - that script will prompt you for a name for your new vm, as well as the new password you will create in 1password.  Provisioning the VM will take around 30 minutes if you are running the script for the first time, or about 1 minute if you already have the base image (`vagrant-ubuntu.ova`) cached.
- In the virtualbox GUI, a new VM with the name you entered should appear.  Double click to boot into it.
- The default username and password are both "vagrant".  Once you log in, create a new password in 1password and change the login password within the VM.
