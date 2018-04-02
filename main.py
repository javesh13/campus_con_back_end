#!/usr/bin/python3

import socket
from threading import Thread
import second as rc

tcpSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
tcpSocket.bind(("0.0.0.0", 12345))
tcpSocket.listen(10000)



while True:
    (client, (ip, port)) = tcpSocket.accept()
    client.settimeout(120)
    t1 = Thread(target = rc.process_client, args = (client, ip, port, rc.dm.dc.debug[1]))
    print ("Client Connected \n")
    t1.start()


#The main task this file is doing that it is accepting the connections and
#calling save_client function from record clients to save the clients 
#I thinkthis file is almost complete

