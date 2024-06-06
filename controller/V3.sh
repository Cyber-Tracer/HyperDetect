#!/bin/bash

if mount | grep -q "/media/usb_log_volume"; then
    echo "/media/usb_log_volume/ is already mounted."
else
    echo "/media/usb_log_volume/ is not mounted. Mounting now..."
    mount -t exfat /dev/sda /media/usb_log_volume/ -o rw,umask=0000
    if [ $? -eq 0 ]; then
        echo "Mount successful."
    else
        echo "Failed to mount /dev/sda to /media/usb_log_volume/."
        exit 1
    fi
fi

cd /home/logger/HyperDetect/controller/input

python3 to_zipped.py --directory V3/ --output_directory ../input_zipped/V3/

cd ..

mkdir -p /media/usb_log_volume/V3

su - logger -c "cd HyperDetect/controller && python3 start_server.py --input input_zipped/V3/ --log_dir /media/usb_log_volume/V3"

echo "Done logging!"

echo "Unmounting /dev/sda..."
sleep 5


umount /dev/sda/