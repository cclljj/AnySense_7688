import mraa
import time
from multiprocessing import Queue,Process

OP_SINGLE_HRES1 = 0x20
OP_SINGLE_HRES2 = 0x21
OP_SINGLE_LRES = 0x23
DELAY_HMODE = 0.180  # 180ms in H-mode
DELAY_LMODE = 0.024  # 24ms in L-mode

class sensor(Process):


        def __init__(self,q):
		Process.__init__(self)
		self.q = q
                self.tmp = 0
                self.sensor = mraa.I2c(0)
                self.sensor.address(0x23)

	def run(self):
		L = self.getL()
		send_data = {
			'Lux':L,
		}
		self.q.put(send_data)


		while True:
			send_data['Lux'] = self.getL()
			self.q.put(send_data)
			time.sleep(5)
			

        def getL(self, mode=OP_SINGLE_HRES1):
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

	q = Queue()
        sen = sensor(q)
	sen.start()

	while True:
		if not q.empty():
			print(str(q.get()))
		else:	
			print('wait...')
			time.sleep(1)
		


