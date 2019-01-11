
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

print "start"

time.sleep(5)

print "OK go"

#port.write("AT")
#time.sleep(1)
#rcv = readlineCR(port)
#print(rcv)

#print "check OK"

port.write("AT$I=11\r\n")
time.sleep(0.5)
rcv = readlineCR(port)
print(rcv)

port.write("AT$I=10\r\n")
time.sleep(0.5)
rcv = readlineCR(port)
print(rcv)
 

port.write("AT$RC\r\n")
time.sleep(0.5)
rcv = readlineCR(port)
print(rcv)

port.write("AT$GI?\r\n")
time.sleep(0.5)
rcv = readlineCR(port)
print(rcv)

port.write("AT$SF=310608233051013504400000\r\n")
time.sleep(5)
rcv = readlineCR(port)
print(rcv)



