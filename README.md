This is the AnySense project for MediaTek LinkIt 7688 board. The codes are based on MRAA library in Python, so hopefully it will run smoothly on the other MRAA-supported boards.

## Sensors supported
### Temperature and Humidity Sensor
 - HTU21d (I2C)
 - SHT2x (I2C)
### Light Sensor
 - BH1750FVI (I2C)
### Particulate Matter Sensor
 - Plantower PMS3003 (UART0)
 - Plantower PMS5003 (UART0)
 - Plantower PMS7003 (UART0)
 - Plantower PMSA003 (UART0)
### Gas Sensor
 - Senseair S8 (UART1)
 
## How to run this program?
Please login you development board, and change to your working directory. Then, please follow the following steps:
1. Use the coommand to get the latest version of the codes: 
   ```
   git clone https://github.com/cclljj/AnySense_7688
   ```
2. Edit the file AnySense.py and change the configureations
   - Sense_PM: Enable PM sensor (1) or Not (0)
   - Sense_Tmp: Enable Temperature/Humidity sensor (1) or Not (0)
   - Sense_Light: Enable Light sensor (1) or Not (0)
   - Sense_Gas: Enable Gas sensor (1) or Not (0)
   

3. Run the main program by
   ```
   python AnySense.py
   ```
4. 
