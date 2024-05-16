#!/bin/bash

if mount | grep -q "/media/usb_log_volume/"; then
    echo "/media/usb_log_volume/ is already mounted."
else
    echo "/media/usb_log_volume/ is not mounted. Mounting now..."
    mount -t vfat /dev/sda1 /media/usb_log_volume/ -o rw,umask=0000
    if [ $? -eq 0 ]; then
        echo "Mount successful."
    else
        echo "Failed to mount /dev/sda1 to /media/usb_log_volume/."
        exit 1
    fi
fi
