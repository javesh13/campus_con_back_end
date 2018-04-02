#!/usr/bin/python3

#HARDCODING DATA STRING TO SEND

import socket,sys
import time
from threading import Thread
HOST = str(sys.argv[1])
PORT = int(sys.argv[2])

print("Connecting to "+str(HOST)+":"+ str(PORT))

ADDR = (HOST,PORT)
BUFSIZE = 4096

roll_num = input("Enter your Roll Number : ")
#group = input("Enter your Group : ")
group = "random"
#name = input("Enter you Name : ")
name="random"
#email = input("Enter your Email : ")
email = "random"
#number = input("Enter you Mobile Number : ")
number="random"

registeration_request = "281001"+roll_num+name+","+email+","+group+","+number+"29"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print ("Registering on server......: ")
client.send(registeration_request.encode())
status = client.recv(1024)
print(status)

def get_message():
    try:
        while True:
            check_msg = "281004"+roll_num+"29"
            client.send(check_msg.encode())
            #print("Sending request for message\n"+ "Waiting for reply from server")
            #reply = client.recv(2048)
            #print("got reply \n")
            reply = reply.decode()
            if len(reply) > 6:
                print(reply + "\n")
            else:
                #print("No Message \n")
            time.sleep(2)
    except Exception as e:
        print(e.message)

t1 = Thread(target = get_message, args = ())
t1.start()

while True:
    todo = input("Press 1 to chat \n")
    if (str(todo) == "1"):
        roll = input("Enter the roll number of ther person you want to chat with: ")
        message = input("Wnter the message you want to send: ")
        message_request = "283001" + roll_num+roll + "," + message + ",29"
        client.send(message_request.encode())
   	

client.close()
