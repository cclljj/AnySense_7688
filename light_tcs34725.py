import mraa
import time
from multiprocessing import Queue,Process

TCS34725_ADDRESS = 0x29
TCS34725_ID = 0x12			# 0x44 = TCS34721/TCS34725, 0x4D = TCS34723/TCS34727
TCS34725_COMMAND_BIT = 0x80

#TCS34725_INTEGRATIONTIME = 0xFF  # /**<  2.4ms - 1 cycle    - Max Count: 1024  */
#TCS34725_INTEGRATIONTIME = 0xF6  # /**<  24ms  - 10 cycles  - Max Count: 10240 */
TCS34725_INTEGRATIONTIME = 0xEB   #/**<  50ms  - 20 cycles  - Max Count: 20480 */   => default
#TCS34725_INTEGRATIONTIME = 0xD5  # /**<  101ms - 42 cycles  - Max Count: 43008 */
#TCS34725_INTEGRATIONTIME = 0xC0  # /**<  154ms - 64 cycles  - Max Count: 65535 */
#TCS34725_INTEGRATIONTIME = 0x00  #  /**<  700ms - 256 cycles - Max Count: 65535 */

#TCS34725_GAIN = 0x00    #/**<  No gain  */
TCS34725_GAIN = 0x01    #/**<  4x gain  */   => default
#TCS34725_GAIN = 0x02    #/**<  16x gain */
#TCS34725_GAIN = 0x03    #/**<  60x gain */


class sensor(Process):


        def __init__(self,q):
		Process.__init__(self)
		self.q = q
                self.tmp = 0
                self.sensor = mraa.I2c(0)
                self.sensor.address(TCS34725_ADDRESS)

		self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_ID)
                d = self.sensor.read(1)
		if d!= 0x44 and d!= 0x10:
			self.Initialised = 0
		else:
			self.Initialised = 1

			self.sensor.writeByte(TCS34725_COMMAND_BIT | TCS34725_ID)
write8(TCS34725_ATIME, _tcs34725IntegrationTime)
write8(TCS34725_CONTROL, _tcs34725Gain)
  write8(TCS34725_ENABLE, TCS34725_ENABLE_PON);
  delay(3);
  write8(TCS34725_ENABLE, TCS34725_ENABLE_PON | TCS34725_ENABLE_AEN);		

	def run(self):
		R, G, B, C = self.getRGBC()
		send_data = {
		#	'Lux':L,
			'RGB_R':R,
			'RGB_G':G,
			'RGB_B':B,
			'RGB_C':C,
		}
		self.q.put(send_data)


		while True:
			R, G, B, C = self.getRGBC()
			send_data = {
	                #       'Lux':L,                     
	                        'RGB_R':R,                   
	                        'RGB_G':G,       
	                        'RGB_B':B,       
	                        'RGB_C':C,       
	                }                  
			self.q.put(send_data)
			time.sleep(5)
			

        def getRGBC(self):
		

		self.sensor.writeByte(0)  # make sure device is in a clean state
		self.sensor.writeByte(1)  # power up
		self.sensor.writeByte(mode)  # set measurement mode
		time.sleep(DELAY_LMODE if mode == OP_SINGLE_LRES else DELAY_HMODE)

                d = self.sensor.read(2)
		bdata = bytearray(d)
		
		L = ((bdata[0]<<24) | (bdata[1]<<16)) // 78642
		self.sensor.writeByte(0)  # power again

		return L


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
		


