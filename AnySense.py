import mraa
import mqtt
import time
import string
from threading import Timer
from datetime import datetime

import AnySense_config

fields = AnySense_config.fields
values = AnySense_config.values

def upload_data():
	Timer(AnySense_config.MQTT_interval,upload_data,()).start()
	timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	pairs = timestamp.split(" ")
	values["device_id"] = AnySense_config.DEVICE_ID
	values["date"] = pairs[0]
	values["time"] = pairs[1]
	msg = ""
	for item in values:
		if AnySense_config.num_re_pattern.match(str(values[item])):
			msg = msg + "|" + item + "=" + str(values[item]) + ""
		else:
			tq = values[item]
			tq = tq.replace('"','')
			msg = msg + "|" + item + "=" + tq 
	MQTT = mqtt.mqtt(AnySense_config.MQTT_broker,AnySense_config.MQTT_port,AnySense_config.MQTT_topic + "/" + AnySense_config.DEVICE_ID)
	MQTT.pub(msg)
	print msg

if __name__ == '__main__':
	if AnySense_config.Sense_PM==1:
		pm_data = '1'
		pm = AnySense_config.pm_sensor.sensor(AnySense_config.pm_q)
		pm.start()
	if AnySense_config.Sense_Tmp==1:
		tmp_data = '2'
		tmp = AnySense_config.tmp_sensor.sensor(AnySense_config.tmp_q)
		tmp.start()
		tmp_data = {'Tmp':0.0, 'RH':0}
	if AnySense_config.Sense_Light==1:
		light_data = '3'
		light = AnySense_config.light_sensor.sensor(AnySense_config.light_q)
		light.start()
	if AnySense_config.Sense_Gas==1:
		gas_data = '4'
		gas = AnySense_config.gas_sensor.sensor(AnySense_config.gas_q)
		gas.start()
	upload_data()
	while True:
		if AnySense_config.Sense_PM==1 and not AnySense_config.pm_q.empty():
			pm_data = AnySense_config.pm_q.get()
			for item in pm_data:
				if item in fields:
					values[fields[item]] = pm_data[item]
					if AnySense_config.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
				else:
					values[item] = pm_data[item]
		if AnySense_config.Sense_Tmp==1 and not AnySense_config.tmp_q.empty():
			tmp_data = AnySense_config.tmp_q.get()
                        for item in tmp_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = tmp_data[item]                                     
					if AnySense_config.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
                                else:                                                                             
                                        values[item] = tmp_data[item]
		if AnySense_config.Sense_Light==1 and not AnySense_config.light_q.empty():
			light_data = AnySense_config.light_q.get()
                        for item in light_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = light_data[item]                                     
					if AnySense_config.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
                                else:                                                                             
                                        values[item] = light_data[item]                                             
		if AnySense_config.Sense_Gas==1 and not AnySense_config.gas_q.empty():
			gas_data = AnySense_config.gas_q.get()
                        for item in gas_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = gas_data[item]                                     
					if AnySense_config.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
                                else:                                                                             
                                        values[item] = gas_data[item]                                             
