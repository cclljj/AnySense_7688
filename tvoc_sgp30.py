import mraa
import time
from multiprocessing import Queue,Process


class sensor(Process):
        def __init__(self,q):
		Process.__init__(self)
		self.q = q
                self.sensor = mraa.I2c(0)
                self.sensor.address(0x58)

		self.IAQInitCmd = bytearray(b'\x20\x03')
		self.IAQMeasureCmd = bytearray(b'\x20\x08')
		#self.IAQMeasureCmd = bytearray(b'\x20\x32')
		#self.Tcmd = 0xF3
		#self.RHcmd = 0xF5

	def run(self):
		self.sensor.write(self.IAQInitCmd)
		time.sleep(0.5)

		co2_eq_ppm, tvoc_ppb = self.getIAQMeasure()
		send_data = {
			'TVOC'	: tvoc_ppb,
			'CO2'	: co2_eq_ppm
		}
		self.q.put(send_data)


		while True:
			co2_eq_ppm, tvoc_ppb = self.getIAQMeasure()
			send_data['TVOC'] = tvoc_ppb
			send_data['CO2'] = co2_eq_ppm
		
			self.q.put(send_data)
			time.sleep(5)
			

        def getIAQMeasure(self):
		self.sensor.write(self.IAQMeasureCmd)
		time.sleep(1)
                d = self.sensor.read(6)
		bdata = bytearray(d)

		v1 = bdata[0] * 256 + bdata[1]
		v2 = bdata[3] * 256 + bdata[4]


		return v1, v2


if __name__ == '__main__':

	q = Queue()
        sen = sensor(q)
	sen.start()

	while True:
		if not q.empty():
			print(str(q.get()))
		else:	
			print('wait...')
			time.sleep(1)
		


