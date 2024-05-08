# This script is used to setup the controller node
# It is assumed the controller node is still connected to the internet
# requires to be run with sudo

# Update and upgrade the system
apt update
apt upgrade
reboot

# Add logger user
adduser logger
cd /home/logger
git clone https://github.com/Cyber-Tracer/HyperDetect.git

# IP address of the controller node
cp ./01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml
netplan apply

# Cron task to start log server on reboot

# Restrict firewall to only allow connections from the logger nodes
ufw default deny incoming
ufw allow 8989/tcp
ufw allow 9090/tcp
ufw enable

# Mount usb drive
mount -t vfat /dev/sda1 /media/usb_log_volume/ -o rw,umask=0000
