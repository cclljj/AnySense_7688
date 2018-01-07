import mraa
import time
import string
import os
import random
import sys,getopt
import hmac
import hashlib
import base64

from threading import Timer
from datetime import datetime

TimeURL = "https://pm25.lass-net.org/util/timestamp.php"

DS3231_I2C_ADDR = 0x68
DS3231_TIME_CAL_ADDR = 0x00

def dec2bcd(v):
	return ((v/10*16)+(v%10))

def bcd2dec(v):
	return ((v/16*10)+(v%16))

def rtc_set_time(t):
	rtc = mraa.I2c(0)
        rtc.address(DS3231_I2C_ADDR)

	tyear = t.year
	tweek = dec2bcd(t.weekday())
	tweek = t.weekday()
	tmon = dec2bcd(t.month)
	tday = dec2bcd(t.day)
	thour = dec2bcd(t.hour)
	tmin = dec2bcd(t.minute)
	tsec = dec2bcd(t.second)
	tyear_s = dec2bcd(t.year - 2000)

	rtc.writeReg(0x00, tsec & 0xff)
	rtc.writeReg(0x01, tmin & 0xff)
	rtc.writeReg(0x02, thour & 0xff)
	rtc.writeReg(0x03, tweek & 0xff)
	rtc.writeReg(0x04, tday & 0xff)
	rtc.writeReg(0x05, tmon & 0xff)
	rtc.writeReg(0x06, tyear_s & 0xff)


def rtc_get_time():
	rtc = mraa.I2c(0)
        rtc.address(DS3231_I2C_ADDR)

	tsec = bcd2dec(rtc.readReg(0x00))
	tmin = bcd2dec(rtc.readReg(0x01))
	thour = bcd2dec(rtc.readReg(0x02))
	tweek = rtc.readReg(0x03)
	tday = bcd2dec(rtc.readReg(0x04))
	tmon = bcd2dec(rtc.readReg(0x05))
	tyear_s = bcd2dec(rtc.readReg(0x06))
	tyear = 2000 + tyear_s

	t = str(tyear) + "-" + str(tmon) + "-" + str(tday) + " " + str(thour) + ":" + str(tmin) + ":" + str(tsec)
	t = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
	return t

def ntp_is_running():
	try:
		command = "wget -O /tmp/time1 " + TimeURL
		os.system(command)
		fh = open("/tmp/time1","r")
		time1 = fh.read()
		time1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
	except:
		time1 = datetime.utcnow()
		return 0 , time1

	time2 = datetime.utcnow()

	delta_time = time2 - time1
	if abs(delta_time.seconds) < 30:
		return 1, time2
	else:
		return -1, time1

def set_key(key):
	mac = open('/sys/class/net/eth0/address').readline().upper().strip()
	DEVICE_ID = mac.replace(':','')
	dig = hmac.new(key, msg=DEVICE_ID, digestmod=hashlib.sha256).digest()
	key = base64.b64encode(dig).decode()      # py3k-mode
	#print "key =", key[:7]

	# use the first 7 bytes as the secure key
	rtc = mraa.I2c(0)
        rtc.address(DS3231_I2C_ADDR)
	rtc.writeReg(0x07, ord(key[0]) & 0xff)
	rtc.writeReg(0x08, ord(key[1]) & 0xff)
	rtc.writeReg(0x09, ord(key[2]) & 0xff)
	rtc.writeReg(0x0A, ord(key[3]) & 0xff)
	rtc.writeReg(0x0B, ord(key[4]) & 0xff)
	rtc.writeReg(0x0C, ord(key[5]) & 0xff)
	rtc.writeReg(0x0D, ord(key[6]) & 0xff)

	# for debug usage: print out the 7 bytes
	#print chr(rtc.readReg(0x07))
	#print chr(rtc.readReg(0x08))
	#print chr(rtc.readReg(0x09))
	#print chr(rtc.readReg(0x0A))
	#print chr(rtc.readReg(0x0B))
	#print chr(rtc.readReg(0x0C))
	#print chr(rtc.readReg(0x0D))


def main(argv):
	Valid_Command = " -k <key> -d <delay>"
	DELAY = random.random()*60

	try:
		opts, args = getopt.getopt(argv,"hd:k:",["delay=","key="])
	except getopt.GetoptError:
		print str(os.path.basename(__file__)) + Valid_Command
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print str(os.path.basename(__file__)) + Valid_Command
			sys.exit()
		elif opt in ("-k", "--key"):
			set_key(arg)
		elif opt in ("-d", "--delay"):
			DELAY = arg

	return DELAY



if __name__ == '__main__':
	delay = main(sys.argv[1:])
	time.sleep(float(delay))
	
	t = rtc_get_time()
	print "RTC time: ", t

	status, t = ntp_is_running()
	if status == 1:
		rtc_set_time(t)
	elif status == -1:
		t = t.strftime("%Y-%m-%d %H:%M:%S")
		command = "date -u -s \"" + t + "\""
		os.system(command)
	elif status == 0:
		t = rtc_get_time()
		t = t.strftime("%Y-%m-%d %H:%M:%S")
		command = "date -u -s \"" + t + "\""
		os.system(command)
	else:
		print "Error in RTC"

