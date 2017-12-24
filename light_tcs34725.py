import mraa
import time
from multiprocessing import Queue,Process

TCS34725_ADDRESS 	= 0x29
TCS34725_ID 		= 0x12	# 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727
TCS34725_COMMAND_BIT 	= 0x80
TCS34725_ENABLE 	= 0x00
TCS34725_ATIME		= 0x01	# Integration time
TCS34725_CONTROL	= 0x0F	# Set the gain level for the sensor
TCS34725_ENABLE_PON	= 0x01	# Power on - Writing 1 activates the internal oscillator, 0 disables it
TCS34725_ENABLE_AEN	= 0x02	# RGBC Enable - Writing 1 actives the ADC, 0 disables it

TCS34725_INTEGRATIONTIME = 0xFF  # /**<  2.4ms - 1 cycle    - Max Count: 1024  */
#TCS34725_INTEGRATIONTIME = 0xF6  # /**<  24ms  - 10 cycles  - Max Count: 10240 */
#TCS34725_INTEGRATIONTIME = 0xEB   #/**<  50ms  - 20 cycles  - Max Count: 20480 */   => default
#TCS34725_INTEGRATIONTIME = 0xD5  # /**<  101ms - 42 cycles  - Max Count: 43008 */
#TCS34725_INTEGRATIONTIME = 0xC0  # /**<  154ms - 64 cycles  - Max Count: 65535 */
#TCS34725_INTEGRATIONTIME = 0x00  #  /**<  700ms - 256 cycles - Max Count: 65535 */

TCS34725_GAIN = 0x00    #/**<  No gain  */
#TCS34725_GAIN = 0x01    #/**<  4x gain  */   => default
#TCS34725_GAIN = 0x02    #/**<  16x gain */
#TCS34725_GAIN = 0x03    #/**<  60x gain */

TCS34725_CDATAL	= 0x14	# Clear channel data
TCS34725_CDATAH = 0x15
TCS34725_RDATAL = 0x16	# Red channel data
TCS34725_RDATAH = 0x17
TCS34725_GDATAL = 0x18	# Green channel data
TCS34725_GDATAH = 0x19
TCS34725_BDATAL = 0x1A	# Blue channel data
TCS34725_BDATAH = 0x1B

class sensor(Process):


        def __init__(self,q):
		Process.__init__(self)
		self.q = q
                self.tmp = 0
		self.Initialised = 0
                self.sensor = mraa.I2c(0)
                self.sensor.address(TCS34725_ADDRESS)

		self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_ID)
                d = self.sensor.read(1)
		bdata = bytearray(d)
		d = bdata[0]

		if d!= 0x44 and d!= 0x10:
			self.Initialised = 0
		else:
			self.Initialised = 1

			self.sensor.writeByte(TCS34725_ATIME | TCS34725_INTEGRATIONTIME)
			self.sensor.writeByte(TCS34725_CONTROL | TCS34725_GAIN)
			self.sensor.writeByte(TCS34725_ENABLE | TCS34725_ENABLE_PON)
			time.sleep(0.01)
			self.sensor.writeByte(TCS34725_ENABLE | ( TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN))		

	def run(self):
		R, G, B, C, L = self.getRGBC()
		send_data = {
			'Lux':L,
			'RGB_R':R,
			'RGB_G':G,
			'RGB_B':B,
			'RGB_C':C,
		}
		self.q.put(send_data)


		while True:
			R, G, B, C, L = self.getRGBC()
			send_data = {
	                        'Lux':L,                     
	                        'RGB_R':R,                   
	                        'RGB_G':G,       
	                        'RGB_B':B,       
	                        'RGB_C':C,       
	                }                  
			self.q.put(send_data)
			time.sleep(5)
			

        def getRGBC(self):
		if self.Initialised == 0:
			return -1, -1, -1, -1

                self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_CDATAL)
	        d = self.sensor.read(2)
		bdata = bytearray(d)
		#bdata = self.sensor.readBytesReg(TCS34725_COMMAND_BIT |TCS34725_CDATAL,2)
		#C = ((bdata[0]<<8) | (bdata[1]))


                self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_RDATAL)                                        
                d = self.sensor.read(2)                                                                      
                bdata = bytearray(d)                                                                         
		#bdata = self.sensor.readBytesReg(TCS34725_COMMAND_BIT |TCS34725_RDATAL,2)
                R = ((bdata[0]<<8) | (bdata[1]))                                                             

                self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_GDATAL)
                d = self.sensor.read(2)                                                                      
                bdata = bytearray(d)                                                                         
                G = ((bdata[0]<<8) | (bdata[1]))                                                             
                G = bdata[0]* 256 + bdata[1]

                self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_BDATAL) 
                d = self.sensor.read(2)                                                                      
                bdata = bytearray(d)                                                                         
                B = ((bdata[0]<<8) | (bdata[1]))                                                             

		L = (-0.32466 * R) + (1.57837 * G) + (-0.73191 * B)

		print C, R, G, B, L

		if TCS34725_INTEGRATIONTIME == 0xFF:
			time.sleep(0.003)
		elif TCS34725_INTEGRATIONTIME == 0xF6:
			time.sleep(0.024)
		elif TCS34725_INTEGRATIONTIME == 0xEB:
			time.sleep(0.050)
		elif TCS34725_INTEGRATIONTIME == 0xD5:
			time.sleep(0.101)
		elif TCS34725_INTEGRATIONTIME == 0xC0:
			time.sleep(0.154)
		elif TCS34725_INTEGRATIONTIME == 0x00:
			time.sleep(0.704)
		else:
			time.sleep(1)
		return R, G, B, C, L


if __name__ == '__main__':

	q = Queue(maxsize=5)
        sen = sensor(q)
	sen.start()

	while True:
		if not q.empty():
			print(str(q.get()))
		else:	
			print('wait...')
			time.sleep(1)
		


