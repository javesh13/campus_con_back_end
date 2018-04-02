#!/usr/bin/python

def get_user(reciever):
	print("Reciever is : "+reciever)
#receiver = ***14814 , 0C214814
	roll_num = reciever[0:3]
	branch = reciever[3:6]
	year = reciever[6:8]
	is_roll_star = roll_num == "***" if True else False
	is_branch_star = branch == "***" if True else False
	is_year_star = year == "***" if True else False
	is_group = False
	tosend = []
	if ("C" in roll_num or "I" in roll_num or "M" in roll_num or "E" in roll_num or "EE" in roll_num):
		is_group = True
	with open ("registeration_1001.txt","r") as f :
		for line in f.readlines():
			if is_group == True:
					curr_roll = line.split(":")[1] #c1
					curr_roll = curr_roll.upper() #C1
			else:
				curr_roll = line.split(":")[0][0:3] #029
			curr_year = line.split(":")[0][-2:] #14
			curr_branch = line.split(":")[6:9] #027
			curr_group = line.split(":")[2] #0C2
			if is_roll_star:
				if is_year_star:
					if is_branch_star:
						tosend.append(line.split(":")[1])
					elif branch == curr_branch:
						tosend.append(line.split(":")[1])
					elif year == curr_year:
						if is_branch_star:
							tosend.append(line.split(":")[1])
						elif branch == curr_branch:
							tosend.append(line.split(":")[1])
				elif roll_num == curr_roll:
					tosend.append(line.split(":")[1])
				if not is_group:
					break
			print ("Line is : " + line + "\t Roll no. is: " + line.split(": ")[1].split("\t")[0])

#For year based regex : 
