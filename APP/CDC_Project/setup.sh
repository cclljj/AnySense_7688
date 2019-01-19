cp /root/AnySense_7688/APP/CDC_Project/AnySense /etc/init.d
chmod 755 /etc/init.d/AnySense
/etc/init.d/AnySense enable


opkg update
opkg install wget block-mount kmod-fs-ext4 kmod-usb-storage-extras e2fsprogs fdisk kmod-usb-serial kmod-usb-serial-cp210x kmod-usb-serial-pl2303 usbutils
mkfs.ext4 /dev/mmcblk0p1

block detect > /etc/config/fstab
echo "	option	enabled	'1'" >> /etc/config/fstab

python /root/AnySense_7688/AnySense_RTC.py -d 0 -k $1
crontab /root/AnySense_7688/APP/CDC_Project/RTC_cron

reboot

