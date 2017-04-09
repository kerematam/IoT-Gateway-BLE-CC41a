#!/usr/bin/env python
import bluetooth_connect

ble_con = bluetooth_connect.slave_connection()
while not ble_con.conn_state == 2 :
	ble_con.conn_serial() # infinite try
	ble_con.query_slaves(3) # 3 try
	ble_con.connect_slave(3) # 3 try

	
server_url = "http://1.2.3.4/server-g.php" 
api_key = "NBIWUCM0DHGTLMX"

while True:    
	match_phrase = ser.read()
	print str(match_phrase)
	
	# wait for double # to listen
	if match_phrase == '#':
		match_phrase = ser.read()
		if match_phrase == '#':
			
			user_id = ser.read(3) # user_id
			sensor_id = ser.read(3) # sensor_id
			type_id = ser.read(3) # type_id
			sensor_value = ser.read(3) # sensor_value
			print "notification sent to server"

			request_url = server_url + "?"
			request_url += "api_key=" + api_key
			request_url += "&user_id=" + user_id
			request_url += "&sensor_id=" + sensor_id
			request_url += "&type_id=" + type_id
			request_url += "&sensor_value=" + sensor_value
			r = requests.get(request_url)
