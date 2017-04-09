# IoT-Gateway-BLE-CC41a
IoT Gateway for Bluetooth Module (BLE-CC41a)

This is simple Gateway Python software which handles serial communication with Bluetooth modules (BLE-CC41A) and cloud server through ethernet interface. This project is not tested on real IoT application. It was one my project that ended on half way.  There still lot to be done. 

A. Requirements :
1. A linux machine able to run Python 2.7. I have developed and tested this gateway on Ubuntu 14.04 machine. 
2. Gateway hardware should have at least one ethernet (to cloud server) and one serial USB port (for BLE-CC41A module).
3. A cloud server: I have used my own cloudserver. 
3.1. You can go with thingspeak.com and update the code accordingly. 
3.2. Wait for me to upload my cloudserver code to handle http requests.  
3.3. Write your own servercode.
4. Couple of BLE-CC41A modules. It is clone of HM10. 

B. What this Gateway do? :
1. This Gateway automatically searches for BLE-CC41A module on each serial port.
2. Configures the serially connected BLE-CC41A module as master.
3. Searches for availible slave modules around.
4. Establishes connection between master and slaves.
5. Sends requests of slaves to cloud server.

C. Configuration :
1. You must modify server_url and api_key variables in main.py.
server_url = "http://1.2.3.4/server.php" 
api_key = "NBIWUCM0DHGTLMX"

![alt tag](https://github.com/kerematam/IoT-Gateway-BLE-CC41a/blob/master/iot-gateway-bluetooth.png)

