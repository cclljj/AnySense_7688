import mraa
import mqtt
import time
import string
import os

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

	print t.year, t.month, t.day, t.weekday(), t.hour, t.minute, t.second
	tyear = t.year
	tweek = dec2bcd(t.weekday())
	tmon = dec2bcd(t.month)
	tday = dec2bcd(t.day)
	thour = dec2bcd(t.hour)
	tmin = dec2bcd(t.minute)
	tsec = dec2bcd(t.second)
	tyear_s = dec2bcd(t.year - 2000)

	rtc.writeByte(DS3231_TIME_CAL_ADDR)
	time.sleep(0.1)
	rtc.writeByte(tsec)
	rtc.writeByte(tmin)
	rtc.writeByte(thour)
	rtc.writeByte(tweek)
	rtc.writeByte(tday)
	rtc.writeByte(tmon)
	rtc.writeByte(tyear_s)


def rtc_get_time():
	rtc = mraa.I2c(0)
        rtc.address(DS3231_I2C_ADDR)
	rtc.writeByte(DS3231_TIME_CAL_ADDR)
	time.sleep(0.3)

	tsec = bcd2dec(rtc.readByte())
	tmin = bcd2dec(rtc.readByte())
	thour = bcd2dec(rtc.readByte())
	tweek = bcd2dec(rtc.readByte())
	tday = bcd2dec(rtc.readByte())
	tmon = bcd2dec(rtc.readByte())
	tyear_s = bcd2dec(rtc.readByte())
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


if __name__ == '__main__':
	t = datetime.strptime("2018-01-02 03:04:05", "%Y-%m-%d %H:%M:%S")
	rtc_set_time(t)

	t = rtc_get_time()
	print t.strftime("%Y-%m-%d %H:%M:%S")

	t = datetime.strptime("2019-01-02 03:04:05", "%Y-%m-%d %H:%M:%S")
	rtc_set_time(t)

	t = rtc_get_time()
	print t.strftime("%Y-%m-%d %H:%M:%S")

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

