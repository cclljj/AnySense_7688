import mraa
import time

from multiprocessing import Queue,Process

import move_avge

NUM_INCOME_BYTE = 8
CHAR_PRELIM     = 0x40
NUM_DATA_BYTE   = 7
CHECK_BYTE      = 7
PM1_BYTE        = -1
PM25_BYTE       = 3
PM10_BYTE       = 5

class sensor(Process):
	def __init__(self, q):
		Process.__init__(self)
		self.q = q

		self.u=mraa.Uart(0)
		self.u.setBaudRate(9600)
		self.u.setMode(8, mraa.UART_PARITY_NONE, 1)
		self.u.setFlowcontrol(False, False)
		self.u.flush()
		cmd = bytearray([0x68,0x01,0x02,0x95])
		#cmd = bytearray([0x68,0x01,0x04,0x96])
		self.u.write(cmd)
		self.u.flush()
		time.sleep(0.1)
		if self.u.dataAvailable():                                                                                   
			ready = False
			while ready is False:
				getstr = self.u.readStr(2) 
				bytedata = bytearray(getstr)
				if bytedata[0]==165 and bytedata[1]==165:
					ready = True
				else:
					time.sleep(0.1)
			self.u.flush()
		cmd = bytearray([0x68,0x01,0x01,0x96])
                self.u.write(cmd)
                self.u.flush()
                time.sleep(0.1)
                if self.u.dataAvailable():
                        ready = False
                        while ready is False:
                                getstr = self.u.readStr(2)
                                bytedata = bytearray(getstr)
                                for i in range (0,2,1):
                                        print (int)(bytedata[i])
                                if bytedata[0]==165 and bytedata[1]==165:
                                        ready = True
                                else:
                                        time.sleep(0.1)
                        self.u.flush()
		

		self.pm1_0_avg = move_avge.move_avg(1)		
		self.pm2_5_avg = move_avge.move_avg(1)		
		self.pm10_avg = move_avge.move_avg(1)		

	def data_log(self, dstr):
		bytedata = bytearray(dstr)
		if self.checksum(dstr) is True:
			PM1_0 = -1
			PM2_5 = bytedata[PM25_BYTE]*256 + bytedata[PM25_BYTE+1]
			PM10 = bytedata[PM10_BYTE]*256 + bytedata[PM10_BYTE+1]
	
			self.pm1_0_avg.add(PM1_0)
			self.pm2_5_avg.add(PM2_5)
			self.pm10_avg.add(PM10)
			return True
		else:
			return False


	def checksum(self, dstr):
		bytedata = bytearray(dstr)
		if bytedata[0]!=64 or bytedata[1]!=5 or bytedata[2]!=4:
			return False
		calcsum = 0
		calcsum = bytedata[0] + bytedata[1] + bytedata[2] + 256 * bytedata[3] + bytedata[4] + 256 * bytedata[5] + bytedata[6]
		calcsum = (65536 - calcsum) % 256
		exptsum = bytedata[CHECK_BYTE]
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
			self.u.flush()
			cmd = bytearray([0x68,0x01,0x04,0x93])
			self.u.write(cmd)
			self.u.flush()
			time.sleep(1)
			if self.u.dataAvailable():
				getstr = self.u.readStr(NUM_INCOME_BYTE)

				if len(getstr) == NUM_INCOME_BYTE:
					if self.data_log(getstr) is True:
						g = self.get_data()
						self.q.put(g)
					
					


if __name__ == '__main__':

	q = Queue()
	p = sensor(q)
	p.start()


	while True:
		print('air: '+ str(q.get()))

