
import serial
import time

def readlineCR(port):
    rv =  ""
    while True:
       ch = port.read()
       rv += ch
       if ch=='\r' or ch=='':
          return rv

port = serial.Serial("/dev/ttyUSB0",baudrate=9600, timeout=3.0)   

port.write("AT\r\n")
time.sleep(0.5)
rcv = readlineCR(port)
print( rcv)


