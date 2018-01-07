import pm_g3 as pm_sensor
import th_htu21d as tmp_sensor
import light_tcs34725 as light_sensor
#import tvoc_sgp30 as gas_sensor
import co2_s8 as gas_sensor
import pyupm_i2clcd as upmLCD


Version = 0.1

Sense_PM = 1                          
Sense_Tmp = 1
Sense_Light = 1
Sense_Gas = 1
Use_RTC_DS3231 = 1

GPS_LAT = 25.1933
GPS_LON = 121.7870
APP_ID = "Harvard_IAQ"
DEVICE = "LinkIt_Smart_7688"
DEVICE_ID = "DEVICE_ID1234"

Interval_LCD = 5
Interval_Upload = 60			# 60 seconds

Restful_URL = "https://data.lass-net.org/Upload/MAPS-secure.php?"
Restful_interval = 60

SecureKey = "NoKey"

FS_SD = "/mnt/mmcblk0p1"

#################################
# don't make any changes in the following codes

import uuid
import re
from multiprocessing import Queue

float_re_pattern = re.compile("^-?\d+\.\d+$")                                                                                               
num_re_pattern = re.compile("^-?\d+\.\d+$|^-?\d+$")

mac = open('/sys/class/net/eth0/address').readline().upper().strip()
DEVICE_ID = mac.replace(':','') 

if Use_RTC_DS3231 == 1:
	import mraa
	import hmac
	import hashlib
	import base64

	DS3231_I2C_ADDR = 0x68
	rtc = mraa.I2c(0)
	rtc.address(DS3231_I2C_ADDR)
	SecureKey = chr(rtc.readReg(0x07)) + chr(rtc.readReg(0x08)) + chr(rtc.readReg(0x09)) + chr(rtc.readReg(0x0A)) + chr(rtc.readReg(0x0B)) + chr(rtc.readReg(0x0C)) + chr(rtc.readReg(0x0D))
	print "SecureKey = " , SecureKey

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
		"RGB_R"	:	"s_lr",
		"RGB_G"	:	"s_lg",
		"RGB_B"	:	"s_lb",
		"RGB_C"	:	"s_lc",
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
