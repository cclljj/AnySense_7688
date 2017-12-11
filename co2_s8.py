import mraa
import time

from multiprocessing import Queue,Process

import move_avge

CO2_BYTE = 9
NUM_INCOME_BYTE = 13
S8_message = b"\xFE\x04\x00\x00\x00\x04\xE5\xC6"

class sensor(Process):
	def __init__(self, q):
		Process.__init__(self)
		self.q = q

		self.u=mraa.Uart(1)
		self.u.setBaudRate(9600)
		self.u.setMode(8, mraa.UART_PARITY_NONE, 1)
		self.u.setFlowcontrol(False, False)

		self.co2_avg = move_avge.move_avg(1)		

	def data_log(self, dstr):
		bytedata = bytearray(dstr)
		if self.checksum(dstr) is True:
			CO2 = bytedata[CO2_BYTE]*256 + bytedata[CO2_BYTE+1]
			self.co2_avg.add(CO2)
		else:
			return


	def checksum(self, dstr):
		return True


	def get_data(self):
		CO2 = self.co2_avg.get()
		ret = {	'CO2': CO2
			}
		return ret

	def run(self):
		count = 0

		while True:
			self.u.writeStr(S8_message)
			self.u.flush()
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

	q = Queue(maxsize=5)
	p = sensor(q)
	p.start()


	while True:
		print('co2: '+ str(q.get()))

