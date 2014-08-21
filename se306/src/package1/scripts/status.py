#!/usr/bin/env python


import roslib; roslib.load_manifest('package1')
import std_msgs.msg
import rospy
from Tkinter import *

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(40)


def callback(msg):
	cur_health = int(msg.data.split()[1])
	if cur_health <= 0:
		#not low
		mlabellow["bg"] = "grey"
		mlabelmid["bg"] = "grey"
		mlabelhigh["bg"] = "grey"
		mlabelfull["bg"] = "grey"
		print ("0/100")
	else:
		if cur_health <= 75 and cur_health > 50:
			#not full
			mlabellow["bg"] = "red"
			mlabelmid["bg"] = "red"
			mlabelhigh["bg"] = "red"
			mlabelfull["bg"] = "grey"
		elif cur_health <= 50 and cur_health > 25:
			#not high
			mlabellow["bg"] = "orange"
			mlabelmid["bg"] = "orange"
			mlabelhigh["bg"] = "grey"
			mlabelfull["bg"] = "grey"
		elif cur_health <= 25 and cur_health > 0:
			#not mid
			mlabellow["bg"] = "yellow"
			mlabelmid["bg"] = "grey"
			mlabelhigh["bg"] = "grey"
			mlabelfull["bg"] = "grey"
		print (msg.data + "/100")

def scheduler_callback(msg):
	msg = str(msg)
	status = ''
	if (msg == 'data: Resident.wakeup'):
		status = "Resident is currently waking up"
		print(status)
	elif (msg == 'data: Resident.eat_breakfast'):
		status = "Resident is walking to the kitchen to eat breakfast"
		print(status)
	elif (msg == 'data: Resident.take_meds'):
		status = "Resident is walking to the cupboard to get and take their medication"
		print(status)
	elif (msg == 'data: Resident.eat_lunch'):
		status = "Resident is walking to the kitchen to eat lunch"
		print(status)
	elif (msg =='data: Resident.eat_dinner'):
		status = "Resident is walking to the kitchen to eat dinner"
		print(status)
	elif (msg =='data: Resident.sleep'):
		status = "Resident is walking to the bedroom to go to sleep"
		print(status)

	if (msg == 'data: Cook.cook_breakfast'):
		status = "Cook robot is moving to the kitchen to cook breakfast"
		print(status)
	elif (msg == 'data: Cook.cook_lunch'):
		status = "Cook robot is moving to the kitchen to cook lunch"
		print(status)
	elif (msg =='data: Cook.cook_dinner'):
		status = "Cook robot is moving to the kitchen to cook dinner"
		print(status)
		
	if (msg == 'data: Visitor.visit'):
		status = "Visitor is visiting the residents house"
		print(status)
	mstatus_bar["text"] = status
	#print msg


sub = rospy.Subscriber("human", std_msgs.msg.String, callback)
sub = rospy.Subscriber("scheduler", std_msgs.msg.String, scheduler_callback)
mGui = Tk()

mGui.geometry("450x450+700+100")

mGui.title("Status")

mlabel = Label(text="hunger: ")
mlabellow = Label(bg="red",width="5")
mlabelmid = Label(bg="red",width="5")
mlabelhigh = Label(bg="red",width="5")
mlabelfull = Label(bg="red",width="5")
mlabel2 = Label(text="health: ")
mlabel3 = Label(text="bladder: ")
mstatus = Label(text="Status: ")
mstatus_bar = Label(width="40")

# button = Button(text="OK",command=decrease).grid(row=3,column=0)

mlabel.grid(row=0,column=0,sticky=W)

mlabellow.grid(row=0,column=2)
mlabelmid.grid(row=0,column=3)
mlabelhigh.grid(row=0,column=4)
mlabelfull.grid(row=0,column=5)
mlabel2.grid(row=1,column=0)
mlabel3.grid(row=2,column=0)
mstatus.place(x=0,y=100)
mstatus_bar.place(x=50,y=100)

mGui.mainloop()

while not rospy.is_shutdown():
	rate.sleep()






