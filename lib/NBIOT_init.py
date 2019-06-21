import searal


AT+CNMP=38  #set to LTE only

AT+CMNB=2   #set to NB-IOT

#AT+CGDCONT=1,"IP","nbiot"

AT+CGDCONT=1,"IP",""

AT+CSQ

#AT+COPS=1,2,"46692"


AT+CSTT="nbiot"

AT+CIICR

AT+CIFSR

AT+CIPSHUT