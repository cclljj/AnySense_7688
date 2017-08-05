import mraa
import mqtt
import time
from datetime import datetime

import pm_g3 as air_sensor
import th_htu21d as tmp_sensor
import light_bh1750fvi as light_sensor
from multiprocessing import Queue


if __name__ == '__main__':

	air_data = ''
	tmp_data = ''
	light_data = ''

	air_q = Queue()
	tmp_q = Queue()
	light_q = Queue()

	air = air_sensor.sensor(air_q)
	tmp = tmp_sensor.sensor(tmp_q)
	light = light_sensor.sensor(light_q)

	air.start()
	tmp.start()
	light.start()

	pat = 'PM1.0={pm1_0},PM2.5={pm2_5},PM10={pm10},Tmp={tmp:5.3f},RH={rh},Lux={lux}'
	#pat = 'Tmp={tmp:5.3f},RH={rh},Lux={lux}'
	#pat = 'PM1.0={pm1_0},PM2.5={pm2_5},PM10={pm10},Tmp={tmp:5.3f},RH={rh}'

	tmp_data = {'Tmp':0.0, 'RH':0}

	sn = 1
	while True:
		flag = 0
		if not air_q.empty():
			air_data = air_q.get()
			flag = flag + 1
		if not light_q.empty():
			light_data = light_q.get()
			flag = flag + 1
		if not tmp_q.empty():
			tmp_data = tmp_q.get()
			flag = flag + 1
		if flag==3:
			send_str = pat.format(
			    pm1_0=air_data['PM1.0'],
			    pm2_5=air_data['PM2.5'],
		   	    pm10=air_data['PM10'],
			    tmp=tmp_data['Tmp'],
			    rh=tmp_data['RH'],
			    lux = light_data['Lux'],
			    )

			#mqtt.mqtt().pub(send_str)
			print send_str
			print sn
			print datetime.utcnow()
			sn = sn + 1
		time.sleep(2)

