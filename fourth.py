#!/usr/bin/python3
import regex as rx
import os
from datetime import datetime as dt

   # Every Method will have their own file , where they will store their data 

   #The Method will be called based on the its codes.

    # MEDIA SENDING IS TO BE SORTED OUT YET BE IT IMAGE/VIDEO/PDF/TXT/AUDIO "

    #Instead of  comma seperated try to use colon seperated

debug = [False, False, True, True]

def send_data(con, prefix_code, data, debug = False):
    """
    prefix_code determines the type of message
    it allows the receiver the differntiate the type of message
    that the user is going to receive.
    Ex. message with multimedia
    Ex. message without multimedia
    """
    """
    you can use the codes here as the prefix codes or you can make them yourself
    prefix code 5000 < 6000 means control messages.
    where the first character denotes the type of message ans the last three digits denote the length of message.

    3000 to 4000 means single user without multimedia messages.

    """
    if(len(prefix_code) != 4):
        if debug:
            print("wrong prefix code returning")
        return

    length = len(data)
    prefix = prefix_code[0] + "0" * (3 - len(str(length))) + str(length) #converting length to four byte like 0002hi
    
    if debug:
        print("Sending " + prefix + data)

    con.send((prefix + data).encode())


registered_users  =  []
got_users  =  False
client_having_pending_message  =  []
message_dic  =  {}





def decode_1001(con, data, debug = False):
    """
    #1 time Registeration of user
    #data = "qz100104414802714,harshit,hkhurana3@gmail.com,99996209642,jk"
    """
    try:

        if debug:
            print("Data: ", data)

        actual = data[2:-2]
        code = actual[0:4]
        sender = actual[4:15]
        details = actual[15:]
        name = details.split(",")[0]
        email = details.split(",")[1]
        group = details.split(",")[2]
        number = details.split(",")[3]
        print ("Registeration request from " + sender)
        #branch_dic  =  {"027":cse, ""...}
        global got_users
        if not got_users:
            try:
                if debug:
                   print("Getting all users")
                with open("users.txt", "r") as f:
                    for line in f.readlines():
                        if(len(line) > 1):
                            registered_users.append(line.rstrip())
                got_users  =  True
            except Exception as e:
                print(e)
                with open("users.txt","w") as f:
                    f.write("")

        if(sender not in registered_users):
            print("new user aya hai bhau")
            with open("registeration_1001.txt","a") as f:
                f.write(sender+":"+ group + ":" + name + ":" + email + ":" + number + "\n")
            with open("users.txt", "a") as f:
                f.write(sender + "\n")
            registered_users.append(sender)
            send_data(con , "1234", "Registered Success Fully", debug)
            if debug:
               print("sent response Registered successfully")
        else:
            send_data(con, "1234", "Already Registered", debug)
            if debug:
                print("sent response Already registered")
    except Exception as e:
        print(e)
        print("unable to register")
        send_data(con, "0000", "one", debug)

    print("Registered_users")
    print(registered_users)




 
def decode_1002(con, data, debug = False):

    
    #Dummy Request for keeping connection alive
    #data = "qz1002,00000000000jk"
    actual = data[2:-2] 
    code = actual[0:4]
    sender = actual[4:]
    print("App connected\n")

def decode_1003(con, data, debug = False):


    #Location Sending via IP of client 
    #data =  "28100304414802714,192.168.120.10329"

    actual = data[2:-2]
    code = actual[0:4]
    sender = actual.split(",")[0][4:]
    IpOfSender = actual.split(",")[1]

    with open("LocationviaIP_1003.txt","a") as f:
    	f.write("Student : "+sender+"\tIP : "+IpOfSender+"\tTime : "+str(str(dt.now()).split(".")[:-1]) + "\n")

def decode_1005(con, data, debug = False):
    #checking for messages for client
    roll_number =  data[6:17]
    tosend_msg  =  []
#    print(roll_number + " requesting for message")
    if roll_number in client_having_pending_message:
        try:
            with open(roll_number+".txt", "r") as f: #this line is unable to open the file
                for line in f.readline():
                    if len(line) < 3:
                        break
                sender   =  line.split(":")[0]
                msg  =  line.split(":")[1]
                tosend.append(sender+":"+msg)
        except:
            print("Unable to open file " + roll_number+".txt\n")
        if len(tosend_msg) > 0:
            for item in tosend_msg:
                try:
                    send_data(con, code, item, debug)
                    tosend_msg.remove(item)
                except:
                    print("There is an exception while sending the message  kind regards 1004")
                    with open(roll_number+".txt", "w") as f:
                        for item in tosend_msg:
                            f.write(item + "\n")
                        return
        client_having_pending_message.remove(roll_number)
    else:
#        print("No message for " + roll_number+ "\n")
        try:
            send_data(con, "1234", "nomsg", debug)#send a random single digit string here
        except:
            print("There is an exception i am returing \n kind regards 1004\n")
            return

def decode_1004(con, data, debug = False):
	#data  =  qz1004,02914802714,jk
    #checking for messages for client
    roll_number =  data.split(",")[1]
    sender  =  roll_number
    tosend_msg  =  []
    global message_dic
    global client_having_pending_message

    print(roll_number + " requesting for message")
    print(message_dic)
    if roll_number in client_having_pending_message:
        for msg in message_dic[sender]:
            try:
                #con.send(msg.encode())
                send_data(con, "1234", msg, debug)
                message_dic[sender].remove(msg)
                print("Message sent to " +  sender)
            except Exception as e:
                print(e.message)
                print("Unable to send messaage to"+ roll_number)
        client_having_pending_message.remove(roll_number)
    else:
        pass
#        print("No message for " + roll_number+ "\n")
#        try:
#        send(con, "0")
#        except:
#            print("There is an exception i am returing \n kind regards 1004\n")
#            return 

#*****************************************FILE WRITING LEFT FOR BELOW METHODS************************************************

def decode_3001(con, data, debug = False):
    #Single user message forward without multimedia
    #data = "qz3001,04414802714,02714802714,Hey buddy how are you \n I am good here \n hope the same for you,jk"
    actual = data[2:-2]
    code = actual[0:4]
    receiver = actual.split(',')[1]
    sender = actual.split(',')[2]
    message = actual.split(',')[3]
    if debug:
        print("Sender is" + sender)
        print("receiver is"+ receiver)
#    print("Message: "+	 message)
    global client_having_pending_message
    global message_dic

    if receiver not in client_having_pending_message:
        client_having_pending_message.append(receiver)
    if receiver not in message_dic:
        message_dic[receiver]  =  []
        message_dic[receiver].append(sender+":"+message)
    else:
        message_dic[receiver].append(message)
    #with open("SingleUserMessages_3001.txt","a")as f:
    #	f.write("Sender: "+sender+"\tReciever: "+reciever+"\tMessage: "+message+"\n")
    with open(receiver+".txt","a") as f:
        print("made file: " + receiver+".txt")
        f.write(sender + ":" + message + "\n")

    print("Client Havig pending message")
    print(client_having_pending_message)



def decode_3003(con, data, debug = False):


    #Message intended for multiple users based on Regex ( 044 027 14)(this shows to reserve 3 3 and 2 characters resp for regex decoding)
    #    ***02714  : Cse of 2014 batch
    #    0C102714  : C1 batch of cse 2014
    #    ***027**  : All cse students of every year
    #data = "28 3003 04414802714 ***02714,Hey student you all are stupid,29"

    actual  =  data[-2:2]
    code = actual[0:4]
    sender = actual.split(',')[0][4:15]
    reciever = actual.split(',')[0][15:]
    message = actual.split[1]
    tosend  =  rx.get_user(receiver)
    for item in tosend:
    	with open(item+".txt","a") as f:
    		f.write("Sender: " + sender+ "\t Message: " + message+"\n")


def decode_3002(con, data, debug = False):


    #Single user message forward with multimedia
    #data = "2830020441480271402902714802714:Hey student you all are stupid:IMAGE/VIDEO/PDF/TXT/AUDIO:29"
    #data = "283002+-+-04414802714+-+-02902714802714+-+-Hey student you all are stupid+-+-IMAGE/VIDEO/PDF/TXT/AUDIO+-+-29"


    #actual  =  data[-2:2]
    #code = actual[0:4]
    #sender = actual.split('+-+-')[0][4:15]
    #reciever = actual.split('+-+-')[0][15:]
    #message = actual.split("+-+-")[-3]
    #media = actual.split("+-+-")[-2] #THIS IS TO BE SORTED OUT YET


    actual  =  data[2:-2]
    print("decode_3002 function called")
    code = actual[0:4]
    print("Actual is : "+actual)
    sender = actual.split("+-+-")[1]
    print("Sendr is: "+sender)
    reciever = actual.split("+-+-")[2]
    message = actual.split("+-+-")[3]
    media = actual.split("+-+-")[4]

    with open("MEDIA FILE.jpg","w")as fw:
        fw.write(media)
    print("Sender : "+sender+"\treciever : "+reciever+"\tMessage: "+message+"\tMedia : "+media+"\n")

#with open("MediaSingleReciever_3002.txt","a")as f:
#f.write("")
   

def decode_3004(con, data, debug = False):


    #Message intended for multiple users based on Regex ( 044 027 14)(this shows to reserve 3 3 and 2 characters resp for regex decoding)
     #   ***02714  : Cse of 2014 batch
     #   0C102714  : C1 batch of cse 2014
     #   ***027**  : All cse students of every year
    #data = "28 3005 04414802714 ***027**,Hey student you all are stupid,IMAGE/VIDEO/PDF/TXT/AUDIO,29"

    actual  =  data[-2:2]
    code = actual[0:4]
    sender = actual.split(',')[0][4:15]
    reciever = actual.split(',')[0][15:]
    message = actual.split[1]
    media = actual.split[2] #THIS IS TO BE SORTED OUT YET

def decode_3005(con, data, debug = False):

    
    # THIS IS SPECIAL CASE OF ASSIGNMENTS(assignments/tutorials by teachers) 
    #Message intended for multiple users based on Regex ( 044 027 14)(this shows to reserve 3 3 and 2 characters resp for regex decoding)
      #  ***02714  : Cse of 2014 batch
     #  0C102714  : C1 batch of cse 2014
      #  ***027**  : All cse students of every year
    #data = "28 3005 04414802714 ***027**,Description of Assignment ,Last date of submission ,IMAGE/VIDEO/PDF/TXT/AUDIO of assignment 29"

    actual  =  data[-2:2]
    code = actual[0:4]
    sender = actual.split(',')[0][4:15]
    reciever = actual.split(',')[0][15:]
    message = actual.split[1]
    last_Date = actual.split[2]
    media = actual.split[3] #THIS IS TO BE SORTED OUT YET

