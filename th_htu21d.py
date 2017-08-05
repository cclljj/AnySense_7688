import mraa
import time
from multiprocessing import Queue,Process


class sensor(Process):
        def __init__(self,q):
		Process.__init__(self)
		self.q = q
                self.tmp = 0
                self.sensor = mraa.I2c(0)
                self.sensor.address(0x40)
		self.sensor.frequency(0)
		self.Tcmd = 0xE3
		self.RHcmd = 0xE5

	def run(self):
		T = self.getT()
		RH = self.getRH()
		send_data = {
			'Tmp':T,
			'RH':RH
		}
		self.q.put(send_data)


		while True:
			send_data['Tmp'] = self.getT()
			time.sleep(0.3)
			send_data['RH'] = self.getRH()
			self.q.put(send_data)
			time.sleep(0.3)
			

        def getT(self):
		self.sensor.writeByte(self.Tcmd)
		time.sleep(0.2)
                d = self.sensor.read(3)
		bdata = bytearray(d)
		
		if self.crc_check(bdata[0],bdata[1],bdata[2]) is False:
			return -1
		St = (bdata[0] << 8) + bdata[1]
		St = St & 0xFFFC
		T = (175.72*St/65536)-46.85

		return T


	def getRH(self):
		self.sensor.writeByte(self.RHcmd)
		time.sleep(0.2)
		d = self.sensor.read(3)
		bdata = bytearray(d)
		
		if self.crc_check(bdata[0],bdata[1],bdata[2]) is False:
			return -1
		Srh = (bdata[0] << 8) + bdata[1]
		Srh = Srh & 0xFFFC
		RH = (125*Srh/65536)-6

		return RH

    	def crc_check(self, msb, lsb, crc):
        	remainder = ((msb << 8) | lsb) << 8
        	remainder |= crc
        	divsor = 0x988000
        	for i in range(0, 16):
        	    if remainder & 1 << (23 - i):
        	        remainder ^= divsor
        	    divsor >>= 1
        	if remainder == 0:
        	    return True
        	else:
        	    return False

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
		


