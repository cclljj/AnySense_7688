import mraa
import time
import string
import os

from threading import Timer
from datetime import datetime

import APP_Harvard_TX_config as Conf

fields = Conf.fields
values = Conf.values

def upload_data():
	Timer(Conf.MQTT_interval,upload_data,()).start()
	timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	pairs = timestamp.split(" ")
	values["device_id"] = Conf.DEVICE_ID
	values["date"] = pairs[0]
	values["time"] = pairs[1]
	msg = ""
	for item in values:
		if Conf.num_re_pattern.match(str(values[item])):
			msg = msg + "|" + item + "=" + str(values[item]) + ""
		else:
			tq = values[item]
			tq = tq.replace('"','')
			msg = msg + "|" + item + "=" + tq 
	#MQTT = mqtt.mqtt(Conf.MQTT_broker,Conf.MQTT_port,Conf.MQTT_topic + "/" + Conf.DEVICE_ID)
	#MQTT.pub(msg)

	restful_str = "wget -O /tmp/last_upload.log \"" + Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&msg=" + msg + "\""
	os.system(restful_str)

	print restful_str

	with open(Conf.FS_SD + "/" + values["date"], "a") as f:
		f.write(msg + "\n")
	print msg

def display_data(disp):
	Timer(5, display_data, {disp}).start()
	timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
	pairs = timestamp.split(" ")
	empty_str = "                    "
        disp.setCursor(0,0)                                                                
	disp.write(empty_str)
        disp.setCursor(0,0)                                                                
	disp.write("ID: " + Conf.DEVICE_ID)
        disp.setCursor(1,0)                                                                
	disp.write(empty_str)
        disp.setCursor(1,0)                                                                
	disp.write("Date: " + pairs[0])
        disp.setCursor(2,0)                                                                
	disp.write(empty_str)
        disp.setCursor(2,0)                                                                
	disp.write("Time: " + pairs[1])
        disp.setCursor(3,0)                                                                
	disp.write(empty_str)
        disp.setCursor(3,0)                                                                
        disp.write('Temp = %.2f C' % values["s_t0"])                                           
        disp.setCursor(4,0)                                                                
	disp.write(empty_str)
        disp.setCursor(4,0)                                                                
        disp.write('rH = %.2f \%' % values["s_h0"])
        disp.setCursor(5,0)                                                                
	disp.write(empty_str)
        disp.setCursor(5,0)                                                                
        disp.write('PM2.5 = %d ug/m3' % values["s_d0"])                                             
        disp.setCursor(6,0)                                                                
	disp.write(empty_str)
        disp.setCursor(6,0)                                                                
        disp.write('TVOC = %d ppb' % values["s_gg"])

def reboot_system():
	os.system("reboot")

if __name__ == '__main__':
	if Conf.Reboot_Time > 0:
		Timer(Conf.Reboot_Time, reboot_system,()).start()
	if Conf.Sense_PM==1:
		pm_data = '1'
		pm = Conf.pm_sensor.sensor(Conf.pm_q)
		pm.start()
	if Conf.Sense_Tmp==1:
		tmp_data = '2'
		tmp = Conf.tmp_sensor.sensor(Conf.tmp_q)
		tmp.start()
		tmp_data = {'Tmp':0.0, 'RH':0}
	if Conf.Sense_Light==1:
		light_data = '3'
		light = Conf.light_sensor.sensor(Conf.light_q)
		light.start()
	if Conf.Sense_Gas==1:
		gas_data = '4'
		gas = Conf.gas_sensor.sensor(Conf.gas_q)
		gas.start()

	disp = Conf.upmLCD.SSD1306(0, 0x3C)
	disp.clear()

	upload_data()

	values["s_d0"] = 0
	values["s_gg"] = 0
	values["s_t0"] = 0
	values["s_h0"] = 0
	display_data(disp)

	while True:
		if Conf.Sense_PM==1 and not Conf.pm_q.empty():
			while not Conf.pm_q.empty():
				pm_data = Conf.pm_q.get()
			for item in pm_data:
				if item in fields:
					values[fields[item]] = pm_data[item]
					if Conf.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
				else:
					values[item] = pm_data[item]
		if Conf.Sense_Tmp==1 and not Conf.tmp_q.empty():
			while not Conf.tmp_q.empty():
				tmp_data = Conf.tmp_q.get()
                        for item in tmp_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = tmp_data[item]                                     
					if Conf.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
                                else:                                                                             
                                        values[item] = tmp_data[item]
		if Conf.Sense_Light==1 and not Conf.light_q.empty():
			while not Conf.light_q.empty(): 
				light_data = Conf.light_q.get()
                        for item in light_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = light_data[item]                                     
					if Conf.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
                                else:                                                                             
                                        values[item] = light_data[item]                                             
		if Conf.Sense_Gas==1 and not Conf.gas_q.empty():
			while not Conf.gas_q.empty():
				gas_data = Conf.gas_q.get()
                        for item in gas_data:                                                                 
                                if item in fields:                                                                
                                        values[fields[item]] = gas_data[item]                                     
					if Conf.float_re_pattern.match(str(values[fields[item]])):
						values[fields[item]] = round(float(values[fields[item]]),2)
                                else:                                                                             
                                        values[item] = gas_data[item]                                             

		#disp.clear()                                             
        	#disp.setCursor(0,0)                                      
        	#disp.write('PM2.5 = %5d' % values["s_d0"])               
        	#disp.setCursor(1,0)                                      
        	#disp.write('TVOC = %5d' % values["s_gg"])                                               
        	#disp.setCursor(2,0)                                      
        	#disp.write('Temp = %4.2f' % values["s_t0"])              
        	#disp.setCursor(3,0)                                      
        	#disp.write('rH = %4.2f' % values["s_h0"]) 
		#time.sleep(5)
