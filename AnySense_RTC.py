import mraa
import mqtt
import time
import string
import os

from threading import Timer
from datetime import datetime

def rtc_set_time():
	print "Ya 1"

def rtc_get_time():
	print "Ya 2"

def ntp_is_running():
	print "Ya"
	return 0

if __name__ == '__main__':
	if ntp_is_running():
		rtc_set_time()
	else:
		rtc_get_time()
