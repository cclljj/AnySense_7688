import time, string, os, subprocess
from datetime import datetime
import APP_LASS7688_config as Conf
fields = Conf.fields
values = Conf.values

def upload_data():
	pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
	values["device_id"] = Conf.DEVICE_ID
	values["ver_app"] = Conf.Version
	values["date"] = pairs[0]
	values["time"] = pairs[1]
	values["tick"] = 0
	with open('/proc/uptime', 'r') as f:
		values["tick"] = float(f.readline().split()[0])
	msg = ""
	for item in values:
		if Conf.num_re_pattern.match(str(values[item])):
			msg = msg + "|" + item + "=" + str(values[item]) + ""
		else:
			tq = values[item].replace('"','')
			msg = msg + "|" + item + "=" + tq 
	restful_str = "wget -O /tmp/last_upload.log \"" + Conf.Restful_URL + Conf.APP_ID + "/" + Conf.DEVICE_ID + "/" + msg + "\""
	os.system(restful_str)
	msg = ""
	for item in Conf.CSV_items:
		if item in values:
			msg = msg + str(values[item]) + '\t'
		else:
			msg = msg + "N/A" + '\t'
	with open(Conf.FS_SD + "/" + values["date"] + ".txt", "a") as f:
		f.write(msg + "\n")

def display_data(disp):
	pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
	disp.setCursor(0,0)
	disp.write('{:16}'.format("ID: " + Conf.DEVICE_ID))
        disp.setCursor(1,0)                                                                
        disp.write('{:16}'.format("Date: " + pairs[0]))
	disp.setCursor(2,0)                                                                
        disp.write('{:16}'.format("Time: " + pairs[1]))
	disp.setCursor(3,0)                                                                                                                              
        disp.write('{:16}'.format('Temp: %.2fC' % values["s_t0"]))
	disp.setCursor(4,0)                                                                
        disp.write('{:16}'.format('  RH: %.2f%%' % values["s_h0"]))
	disp.setCursor(5,0)                                                                                                            
        disp.write('{:16}'.format('PM2.5: %dug/m3' % values["s_d0"]))
	disp.setCursor(6,0)                                                                                                            
        disp.write('{:16}'.format('PM10: %dug/m3' % values["s_d1"]))
	
def reboot_system():
	items = subprocess.Popen(['uptime'], stdout = subprocess.PIPE).communicate()[0].split(",")
	items = items[-3].split(" ")
	k = float(items[-1])
	if k>1.5:
		os.system("echo b > /proc/sysrq-trigger")

if __name__ == '__main__':
	if Conf.Sense_PM==1:
		pm_data = '1'
		pm = Conf.pm_sensor.sensor(Conf.pm_q)
		pm.start()
	disp = Conf.upmLCD.SSD1306(0, 0x3C)
	disp.clear()
	count = 0
	values["s_d0"] = 0
	values["s_d1"] = 0
	values["s_d2"] = 0
	values["s_t0"] = 0
	values["s_h0"] = 0
	while True:
		reboot_system()
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
		display_data(disp)
		if count == 0:
			upload_data()
		count = (count + 1) % (Conf.Restful_interval / Conf.Interval_LCD)
		time.sleep(Conf.Interval_LCD)
