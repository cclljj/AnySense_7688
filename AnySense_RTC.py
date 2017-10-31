import mraa
import mqtt
import time
import string
import os

from threading import Timer
from datetime import datetime

TimeURL = "https://pm25.lass-net.org/util/timestamp.php"

def rtc_set_time():
	print "Ya 1"

def rtc_get_time():
	print "Ya 2"

def ntp_is_running():
	command = "wget -O /tmp/time1 " + TimeURL
	os.system(command)
	fh = open("/tmp/time1","r")
	time1 = fh.read()

	time2 = datetime.utcnow()
	time2 = time2.strftime("%Y-%m-%d %H:%M:%S")

	print time1
	print time2
	print "Ya"
	return 0

if __name__ == '__main__':
	if ntp_is_running():
		rtc_set_time()
	else:
		rtc_get_time()
