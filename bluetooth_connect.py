#!/usr/bin/env python
import serial, glob, time, requests, string


## TODO if already connected, it goes infinite loop in conn_serial
#					eject USB or send something client reset


class slave_connection (object) :

	def __init__(self) :
		
		# set connection_to_bluetooth_module
		self.conn_state = 0
		
		# 0 set after module connection_to_bluetooth_module()
		self.serial = None
		self.port = None	
		self.number_of_bluetooth_client = None
		
		# 1 set after query for slaves
		self.slave = None
		
	# it searches active modules and test each of them by sending phrase "AT" 
	# and wait for the return "OK"
	def conn_serial(self):
		
		# list of active interfaces
		interface_arr = glob.glob("/dev/ttyUSB*")
		print "Active serial interfaces are : "
		for interface in interface_arr:
			print interface

		serial_bt_conn = 0
		while serial_bt_conn == 0 :
			for interface in interface_arr:
				print "interface " + interface + " is being tested for connection..."
				ser = serial.Serial(interface)
				ser.baudrate = 9600;
				ser.timeout = 3;
		#		print "ser.portstr : " + ser.portstr
				# AT+RESET to drop current connections
				ser.write("AT+RESET\r\n")
				print "SENT TO MODULE : AT+RESET"
				print "---"
				read = ser.read(10)
				print "---"
				read_arr = string.split(read, '\n')
				if len(read_arr) == 2 :
	#			if read_arr[1] == "OK" :
					print "Connection with bluetooth module has been established on serial port " + interface
					serial_bt_conn = 1
			
					self.serial = ser
					self.port = interface
					self.conn_state = 1
					break
				else :
					self.conn_state = 0
					print "Connection attempt for " + interface + " failed!"
				time.sleep(1)

				# reload the the interfaces
				interface_arr = glob.glob("/dev/ttyUSB*")
				
# search for slave bluetooth clients	
	def query_slaves(self, no_try) :
		
		if not self.conn_state > 0 :
			print "cant perform query before bluetooth connection"
			return
		
		# re-configure as master
		self.serial.write("AT+ROLE1\r\n")
		print "SENT TO MODULE : AT+ROLE1"
		read = self.serial.read(30)
		print "---"
		print read
		print "---"

		# query for slave devices
		self.serial.write("AT+INQ\r\n")
		print "SENT TO MODULE : AT+INQ"
		
		time.sleep(5)
		read = self.serial.read(100)
		print "---"
		print read
		print "---"
		conn_query_arr = string.split(read, '\n')
		
		
		# search for slave devices
		self.number_of_bluetooth_client = -1
		no_query = 0
		while not self.number_of_bluetooth_client == "1":
			# when no device found, bluetooth module gives 6 lines of return
			if len(conn_query_arr) == 5 :
				# that line gives says number of clients; 0 
				line_arr = string.split(conn_query_arr[3])
				self.number_of_bluetooth_client =  line_arr[2]
				print "No client found!"

			# when one device found, bluetooth module gives 7 lines of return
			elif len(conn_query_arr) == 6 :
				# that line gives says number of clients; 1 
				line_arr = string.split(conn_query_arr[4])
				self.number_of_bluetooth_client = line_arr[2]
				self.slave = string.split(conn_query_arr[2])[1]
				self.conn_state = 2
				print "One client has been found with MAC addr : " + self.slave 
				
			else :
				self.number_of_bluetooth_client == "undefined condition"

			if not self.number_of_bluetooth_client == "1" :
				time.sleep(1)
				no_query += 1
				print "Searching for bluetooth clients again..." , no_query

				# query for slave devices
				self.serial.write("AT+INQ\r\n")
				print "SENT TO MODULE : AT+INQ"
				time.sleep(5)
				read = self.serial.read(100)
				print "---"
				print read
				print "---"
				conn_query_arr = string.split(read, '\n')

				# try for 6 times
				if no_query > no_try-1 :
					break

# connect to slave client that founded
	def connect_slave(self, no_try) :
		
		if not self.conn_state > 1 :
			print "Cant perform connection before query"
			return
		
		## try to connect
		connect_slave_state = False
		try_cntr = 0
	
		while not connect_slave_state == True :
			try_cntr += 1
			if self.number_of_bluetooth_client == "1" :
				self.serial.write("AT+CONN1\r\n")
				print "SENT TO MODULE : AT+CONN1"
				time.sleep(5)
				read = self.serial.read(100)
				print "---"
				print read
				print "---"
				conn_arr = string.split(read, '\n')
				if len(conn_arr) == 3 :
					connected_arr = string.split(conn_arr[1])
					if connected_arr[0] == "+Connected" :
						print "Connection established!"
						connect_slave_state = True
						self.conn_state = 2
				else :
					print "still trying to connect... ", try_cntr
					time.sleep(2)

				if try_cntr > no_try-1 :
					print "Number of try limit exceed for connection attempt for bluetooth client :" + self.slave
					connect_slave_state = False
					self.conn_state = 1
					break