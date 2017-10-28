cp $PWD/AnySense /etc/init.d
chmod 755 /etc/init.d/AnySense
/etc/init.d/AnySense enable

block detect > /etc/config/fstab
echo "	option	enabled	'1'" >> /etc/config/fstab
reboot
