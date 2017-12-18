import pm_g5t as pm_sensor
import th_htu21d as tmp_sensor
import light_bh1750fvi as light_sensor
import tvoc_sgp30 as gas_sensor
import pyupm_i2clcd as upmLCD

Version = 0.3

Sense_PM = 1                          
Sense_Tmp = 0
Sense_Light = 0
Sense_Gas = 1

GPS_LAT = 25.1933
GPS_LON = 121.7870
APP_ID = "Harvard_TX"
DEVICE = "LinkIt_Smart_7688"
DEVICE_ID = "DEVICE_ID1234"

MQTT_broker = 'gpssensor.ddns.net'
MQTT_port = 1883                  
MQTT_topic = 'LASS/Test/PM25/AnySense'
MQTT_interval = 60			# interval between every two MQTT messages (seconds)

Reboot_Time = 86400			# interval to reboot (seconds); 0 for no-rebooting

Restful_URL = "https://data.lass-net.org/Upload/MAPS.php?"
Restful_interval = 60

FS_SD = "/mnt/mmcblk0p1"

#################################
# don't make any changes in the following codes

import uuid
import re
from multiprocessing import Queue

float_re_pattern = re.compile("^-?\d+\.\d+$")                                                                                               
num_re_pattern = re.compile("^-?\d+\.\d+$|^-?\d+$")

mac = str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])).upper()
DEVICE_ID = mac.replace(':','')                                                                           

pm_q = Queue(maxsize=5)                                                                                                                     
tmp_q = Queue(maxsize=5)                                                                                                                     
light_q = Queue(maxsize=5)                                                                                                                   
gas_q = Queue(maxsize=5)  
tvoc_q = Queue(maxsize=5)

fields ={       "Tmp"   :       "s_t0",           
                "RH"    :       "s_h0",           
                "PM1.0" :       "s_d2",           
                "PM2.5" :       "s_d0",           
                "PM10"  :       "s_d1",              
                "Lux"   :       "s_l0",              
                "CO2"   :       "s_g8e",              
		"TVOC"	:	"s_gg",
        }                                            
values = {      "app"           :       APP_ID,      
                "device_id"     :       DEVICE_ID,                  
                "device"        :       DEVICE,                     
                "ver_format"    :       3,                        
                "fmt_opt"       :       0,                        
                "gps_lat"       :       GPS_LAT,                    
                "gps_lon"       :       GPS_LON,                    
                "FAKE_GPS"      :       1,                        
                "gps_fix"       :       1,                        
                "gps_num"       :       100,                      
                "date"          :       "1900-01-01",                        
                "time"          :       "00:00:00",                          
        }                       
