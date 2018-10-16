import mraa
import time

from multiprocessing import Queue,Process

class sensor(Process):
  def __init__(self, q):
    Process.__init__(self)
    self.q = q

    self.u=mraa.Uart(1)
    self.u.setBaudRate(9600)
    self.u.setMode(8, mraa.UART_PARITY_NONE, 1)
    self.u.setFlowcontrol(False, False)

    self.gpstime    = 0
    self.sat_num      = 0
    self.lat   = 0
    self.lon  = 0
    self.gps_stat = 0
    self.alt   = 0

  def data_parse(self, dstr):
    darr = dstr.split(',')
    if   darr[0] == '$GPGSV':
      self.sat_num = darr[3]
    elif darr[0] == '$GPGGA':
      self.gps_stat = int(darr[6])
      if self.gps_stat != 0:
        self.gpstime   = darr[1]
        self.lat   = float(darr[2]) if darr[3] == 'N' else -float(darr[2])
        self.lon  = float(darr[4]) if darr[5] == 'E' else -float(darr[4])
        self.alt   = float(darr[9])

  def get_data(self):
    res = {
      'gpstime': self.gpstime,
      'lat': self.lat,
      'lon': self.lon,
      'gps_stat': self.gps_stat,
      'alt': self.alt,
      'sat_num': self.sat_num,
    }
    return res

  def run(self):
    getstr=''
    while True:
      if self.u.dataAvailable():
        time.sleep(0.05)
        getstr += self.u.read(32).decode()
      else:
        g = self.get_data()
        self.q.put(g)
        time.sleep(5)
        getstr=''
					


if __name__ == '__main__':

	q = Queue(maxsize=10)
	p = sensor(q)
	p.start()


	while True:
		print(q.get())

