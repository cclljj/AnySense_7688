## Hardware

* MediaTek LinkIt Smart 7688
* MediaTek LinkIt Smart 7688 Breakout v2.0
* TVOC sensor: Sensirion SGP30
* T/H/PM sensor: Plantower PMS5003T
* RTC: DS3231
* 0.96" LCD
* SD card

## How to re-install the codes?

Please use the designated account/password to login the system, and remove the existing project source codes:

## How to install the codes (for new LinkIt Smart 7688 boards)?

Please login you 7688 board, and change the working directory to /root. Then, please follow the following steps:

1. Use the coommand to get the latest version of the codes: 
   ```
   git clone https://github.com/cclljj/AnySense_7688
   ```
2. Run the setup script:
   ```
   /root/AnySense_7688/APP/Harvard_TX/setup.sh
   ```

Then, the script will install and configure everything. The system will reboot after the installation is done, and hopefully the system will start to upload data to the backend database.
