import mraa
import time
from multiprocessing import Queue,Process


class sensor(Process):
        def __init__(self,q):
		Process.__init__(self)
		self.q = q
                self.tmp = 0
                self.sensor = mraa.I2c(0)
                self.sensor.address(0x50) #this is for i2c<=>adc
		self.DBcmd = 0x00

		self.sensor.writeByte(self.DBcmd)

	def run(self):
		DB = self.getDB()
		send_data = {
			'DB':DB
		}
		self.q.put(send_data)


		while True:
			send_data['DB'] = self.getDB()
			#time.sleep(0.1)
			
			self.q.put(send_data)
			time.sleep(0.1)
			

        def getDB(self):
		#self.sensor.writeByte(self.DBcmd)  #fix from here
		#time.sleep(0.1)
                d = self.sensor.read(2)
		bdata = bytearray(d)
		
		analog = bdata[0]*256+bdata[1]
                #dbVlaue = analog * 3.3 * 2 / 4096 * 50
		
                #return dbVlaue
		return analog



if __name__ == '__main__':

	q = Queue(maxsize=3)
        sen = sensor(q)
	sen.start()

	while True:
		if not q.empty():
			print(str(q.get()))
		else:	
			print('wait...')
			time.sleep(0.1)
		


