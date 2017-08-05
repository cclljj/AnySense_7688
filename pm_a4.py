import mraa
import time

from multiprocessing import Queue,Process

import move_avge

NUM_INCOME_BYTE = 32
CHAR_PRELIM     = 0x32
NUM_DATA_BYTE   = 29
CHECK_BYTE      = 30
PM1_BYTE        = 4
PM25_BYTE       = 6
PM10_BYTE       = 8

class sensor(Process):
	def __init__(self, q):
		Process.__init__(self)
		self.q = q

		self.u=mraa.Uart(0)
		self.u.setBaudRate(9600)
		self.u.setMode(8, mraa.UART_PARITY_NONE, 1)
		self.u.setFlowcontrol(False, False)

		self.pm1_0_avg = move_avge.move_avg(1)		
		self.pm2_5_avg = move_avge.move_avg(1)		
		self.pm10_avg = move_avge.move_avg(1)		

	def data_log(self, dstr):
		bytedata = bytearray(dstr)
		if self.checksum(dstr) is True:
			PM1_0 = bytedata[PM1_BYTE]*256 + bytedata[PM1_BYTE+1]
			PM2_5 = bytedata[PM25_BYTE]*256 + bytedata[PM25_BYTE+1]
			PM10 = bytedata[PM10_BYTE]*256 + bytedata[PM10_BYTE+1]
	
			self.pm1_0_avg.add(PM1_0)
			self.pm2_5_avg.add(PM2_5)
			self.pm10_avg.add(PM10)
		else:
			return


	def checksum(self, dstr):
		bytedata = bytearray(dstr)
		calcsum = 0
		for i in range(0,NUM_DATA_BYTE,1):
			calcsum = calcsum + bytedata[i]
		exptsum = bytedata[CHECK_BYTE] * 256 + bytedata[CHECK_BYTE+1]
		if calcsum==exptsum:
			return True
		else:
			return False


	def get_data(self):
		PM1_0 = self.pm1_0_avg.get()
		PM2_5 = self.pm2_5_avg.get()
		PM10 = self.pm10_avg.get()

		ret = {	
			'PM1.0': PM1_0,
			'PM2.5': PM2_5,
			'PM10': PM10
			}

		return ret

	def run(self):
		count = 0

		while True:
			if self.u.dataAvailable():
				time.sleep(0.05)
				getstr = self.u.readStr(NUM_INCOME_BYTE)

				if len(getstr) == NUM_INCOME_BYTE:
					self.data_log(getstr)

					if count == 0:
						g = self.get_data()
						self.q.put(g)
					count = (count+1)%10
					


if __name__ == '__main__':

	q = Queue()
	p = sensor(q)
	p.start()


	while True:
		print('air: '+ str(q.get()))

