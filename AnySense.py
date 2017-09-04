import mraa
import mqtt
import time
import uuid
import string
import re
from threading import Timer
from datetime import datetime
from multiprocessing import Queue

import pm_g5 as pm_sensor
import th_htu21d as tmp_sensor
import light_bh1750fvi as light_sensor
import co2_s8 as gas_sensor

Sense_PM = 1
Sense_Tmp = 1
Sense_Light = 1
Sense_Gas = 1

MQTT_broker = 'gpssensor.ddns.net'
MQTT_port = 1883
MQTT_topic = 'LASS/Test/PM25/AnySense'
GPS_LAT = 25.1933
GPS_LON = 121.7870
APP_ID = "AnySense"
DEVICE = "LinkIt Smart 7688"
DEVICE_ID = "DEVICE_ID1234"
num_re_pattern = re.compile("^-?\d+\.\d+$|^-?\d+$")

fields ={ 	"Tmp"	:	"s_t0",
		"RH"	:	"s_h0",
		"PM1.0"	:	"s_d2",
		"PM2.5"	:	"s_d0",
		"PM10"	:	"s_d1",
		"Lux"	:	"s_l0",
		"CO2"	:	"s_g8",
	}
values = {	"app"		:	APP_ID,
		"device_id"	:	DEVICE_ID,
		"device"	:	DEVICE,
		"ver_format"	:	"3",
		"fmt_opt"	:	"0",
		"ver_app"	:	"0.1",
		"gps_lat"	:	GPS_LAT,
		"gps_lon"	:	GPS_LON,
		"FAKE_GPS"	:	"1",
		"gps_fix"	:	"1",
		"gps_num"	:	"100",
		"date"		:	"1900-01-01",
		"time"		:	"00:00:00",
	}

def upload_data():
	# setup a timer, in seconds, to trigger the next upload_data
	Timer(10,upload_data,()).start()
	timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	pairs = timestamp.split(" ")
	values["device_id"] = DEVICE_ID
	values["date"] = pairs[0]
	values["time"] = pairs[1]
	msg = ""
	for item in values:
		if num_re_pattern.match(str(values[item])):
			msg = msg + "|" + item + "=" + str(values[item]) + ""
		else:
			tq = values[item]
			tq = tq.replace('"','')
			msg = msg + "|" + item + "=" + tq 
	#MQTT = mqtt.mqtt(MQTT_broker,MQTT_port,MQTT_topic + "/" + DEVICE_ID)
	#MQTT.pub(msg)
	print msg
	

if __name__ == '__main__':

	pm_q = Queue()
	tmp_q = Queue()
	light_q = Queue()
	gas_q = Queue()

	if Sense_PM==1:
		pm_data = '1'
		pm = pm_sensor.sensor(pm_q)
		pm.start()

	if Sense_Tmp==1:
		tmp_data = '2'
		tmp = tmp_sensor.sensor(tmp_q)
		tmp.start()
		tmp_data = {'Tmp':0.0, 'RH':0}

	if Sense_Light==1:
		light_data = '3'
		light = light_sensor.sensor(light_q)
		light.start()

	if Sense_Gas==1:
		gas_data = '4'
		gas = gas_sensor.sensor(gas_q)
		gas.start()

	pat = 'PM1.0={pm1_0},PM2.5={pm2_5},PM10={pm10},Tmp={tmp:5.3f},RH={rh},Lux={lux}'

	mac = str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()
	DEVICE_ID = mac.replace(':','')
	
	upload_data()
	sn = 1
	while True:
		flag = 0
		if Sense_PM==1 and not pm_q.empty():
			pm_data = pm_q.get()
			for item in pm_data:
				if item in fields:
					values[fields[item]] = pm_data[item]
				else:
					values[item] = pm_data[item]

		if Sense_Tmp==1 and not tmp_q.empty():
			tmp_data = tmp_q.get()
                        for item in tmp_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = tmp_data[item]                                     
                                else:                                                                             
                                        values[item] = tmp_data[item]

		if Sense_Light==1 and not light_q.empty():
			light_data = light_q.get()
                        for item in light_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = light_data[item]                                     
                                else:                                                                             
                                        values[item] = light_data[item]                                             

		if Sense_Gas==1 and not gas_q.empty():
			gas_data = gas_q.get()
                        for item in gas_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = gas_data[item]                                     
                                else:                                                                             
                                        values[item] = gas_data[item]                                             


