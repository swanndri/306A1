#!/usr/bin/env python

import roslib; roslib.load_manifest('package1')
import std_msgs.msg
import rospy
import Tkinter as tk
import ttk

class StatusGUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#sets the dimensions and settings of thw window
		self.geometry("450x250+700+100")
		self.title("Status")

		#build the GUI components
		self.hunger_label = ttk.Label(text="hunger: ")
		self.hunger_progress = ttk.Progressbar(self, orient="horizontal", 
										length=200, mode="determinate")
		self.health_label = ttk.Label(text="health: ")
		self.bladder_label = ttk.Label(text="bladder: ")
		self.status_label = ttk.Label(text="Status: ")
		self.status_info = ttk.Label(width="50")
		
		#position the GUI components 
		self.hunger_progress.grid(row=0,column=2)
		self.hunger_label.grid(row=0,column=0)
		self.health_label.grid(row=1,column=0)
		self.bladder_label.grid(row=2,column=0)
		self.status_label.place(x=0,y=100)
		self.status_info.place(x=50,y=100)

		self.hunger_progress["value"] = 100

	def update_hunger_level(self,cur_health):
		self.hunger_level = cur_health
		self.hunger_progress["value"] = self.hunger_level

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(40)


def callback(msg):
	print (msg)
	cur_health = int(msg.data.split()[1])
	mGui.update_hunger_level(cur_health)
	if cur_health <= 0:
		print ("0/100")
	else:
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
	mGui.status_info["text"] = status
	#print msg


sub = rospy.Subscriber("human", std_msgs.msg.String, callback)
sub = rospy.Subscriber("scheduler", std_msgs.msg.String, scheduler_callback)

mGui = StatusGUI()
mGui.mainloop()

while not rospy.is_shutdown():
	rate.sleep()






