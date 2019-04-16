import threading as thd
import time
import serial


mac = open('/sys/class/net/eth0/address').readline().upper().strip()
DEVICE_ID = mac.replace(':','')


def formatStrToInt(target):
    kit = ""
    for i in range(len(target)):
        temp=ord(target[i])
        temp=hex(temp)[2:]
        kit=kit+str(temp)+" "
        #print(temp,)
    return kit

#===Start here===
try:
    print("I'm here")
    port = serial.Serial("/dev/ttyUSB0",baudrate=57600, timeout=3.0)
    sigfox_flag = " "
except:
    print ("there is no NBIOT on the board!!!")
    sigfox_flag = "!"


connect_pack_pre = "10 28 00 06 4D 51 49 73 64 70 03 C2 00 3C 00 0C "
Client_ID = formatStrToInt(DEVICE_ID)
connect_pack_post = " 00 04 6D 61 70 73 00 06 69 69 73 6E 72 6C "
connect_pack = connect_pack_pre + Client_ID + connect_pack_post
cycle = 0

prifix = "MAPS/IAQ_TW/NBIOT/"+DEVICE_ID


#===Start regular event===
def fn():
    global cycle
    #global msg
    
    #====================NBIOT======================#
    msg = "This is:" + str(cycle) + " cycle."

    msg = prifix + msg
    payload_len = len(msg) #remember to add tpoic length (2 byte in this case)
    payload_len = payload_len + 2
    #MQTT Remaining Length calculate
    #currently support range 0~16383(1~2 byte)
    if(payload_len<128):
        payload_len_hex = hex(payload_len).split('x')[-1]
    else:
        a = payload_len % 128
        b = payload_len // 128
        a = hex(a+128).split('x')[-1]
        b = hex(b).split('x')[-1]
        b = b.zfill(2)
        payload_len_hex = str(a) + " " +  str(b)    

    a = formatStrToInt(msg)

    add_on = "30 " + str(payload_len_hex.upper()) +" 00 1E "
    end_line = "1A"
    message_package = add_on + a + end_line

    #===Timer===#

    print("Start T:",time.time())
    print('Thread number{}'.format(thd.activeCount()))
    thd.Timer(30,fn).start()
    #===Timer===#

    port.write("AT+CIPCLOSE\r".encode())
    time.sleep(1)

    port.write("AT+CIPSENDHEX=1\r\n".encode())
    time.sleep(1)

    port.write("AT+CSTT=\"nbiot\"\r\n".encode())
    time.sleep(1)

    port.write("AT+CIICR\r\n".encode())
    time.sleep(1)

    port.write("AT+CIFSR\r\n".encode())
    time.sleep(1)

    port.write("AT+CIPSTART=\"TCP\",\"35.162.236.171\",\"8883\"\r\n".encode())
    time.sleep(1)

    port.write("AT+CIPSEND\r\n".encode())
    time.sleep(1)

    port.write(connect_pack.encode())
    time.sleep(1)

    port.write(message_package.upper().encode())
    time.sleep(1)

    port.write("AT+CIPCLOSE\r\n".encode())
    time.sleep(1)

    cycle = cycle + 1

    print("done")
    print("msg is:",msg)
    print("connect_pack:",connect_pack)
    print("message_package:",message_package)


fn()
