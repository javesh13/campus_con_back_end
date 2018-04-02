import third as dm
from threading import Thread



buffer_one = ""
connection_alive = True
message_list  = []


#make a message list according to their type and then process them
#use dictionary
#cuurently i am using thread per message which may slow down applicatino during heavy usage

def process_messages(con, debug = False):
	global message_list
	global connection_alive

	for message in message_list:
		curr_msg = message_list.pop()
		if connection_alive:
			t1 = Thread(target = dm.process_data, args = (con, curr_msg, dm.dc.debug[2]))
			t1.start()
		


	

		

def process_client(con, i, p, debug = False):
	global connection_alive
	global message_list	
	data = "abcd"
	connection_alive = True
	while len(data) > 0:
		try:
			data = con.recv(4096)
			#this code might lead to message loss but i am leaving it for a while, do it and delete the comment
			#delimiter has been changed from 28 29 to qz jk
			message_list += ([x + "jk" for x in data.decode().split("jk") if len(x) > 2])
			
			process_messages(con, debug)
			
			if debug:
				print([x + "jk" for x in data.decode().split("jk") if len(x) > 2])

		except Exception as e:
			print("Below exception occured also closing socket")
			connection_alive = False
			print(e)
	else:
		connection_alive = False
		if debug:
			print("connection terminated by client")

	
	
			
		

