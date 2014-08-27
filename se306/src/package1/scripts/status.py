#!/usr/bin/env python

import roslib; roslib.load_manifest('package1')
import std_msgs.msg
import rospy
import Tkinter as tk
import ttk
import constants

class StatusGUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#sets the dimensions and settings of thw window
		self.geometry("380x350+700+100")
		self.title("Resident status")
		self.satisfaction_frame = tk.Frame(self,bd=5)
		self.leisure_frame = tk.Frame(self,bd=5)
		self.cleanliness_frame = tk.Frame(self,bd=5)
		self.vital_frame = tk.Frame(self,bd=5)
		self.status_frame = tk.Frame(self,bd=10,highlightbackground="black")

		#build the GUI components:
		#Satisfaction levels
		self.satisfaction_title = ttk.Label(self.satisfaction_frame,text="Satisfaction",font="bold")
		self.hunger_label = ttk.Label(self.satisfaction_frame,text="Hunger")
		self.hunger_progress = ttk.Progressbar(self.satisfaction_frame, orient="horizontal", 
										length=150, mode="determinate")
		self.thirst_label = ttk.Label(self.satisfaction_frame,text="Thirst")
		self.thirst_progress = ttk.Progressbar(self.satisfaction_frame, orient="horizontal", 
										length=150, mode="determinate")

		#Cleanliness levels
		self.cleanliness_title = ttk.Label(self.cleanliness_frame, text="Cleanliness",font="bold")
		self.hygiene_label = ttk.Label(self.cleanliness_frame, text="Hygiene")
		self.hygiene_progress = ttk.Progressbar(self.cleanliness_frame, orient="horizontal", 
										length=150, mode="determinate")
		self.bladder_label = ttk.Label(self.cleanliness_frame,text="Bladder")
		self.bladder_progress = ttk.Progressbar(self.cleanliness_frame,orient="horizontal", 
										length=150, mode="determinate")

		#Leisure levels
		self.leisure_title = ttk.Label(self.leisure_frame,text="Leisure",font="bold")
		self.entertainment_label = ttk.Label(self.leisure_frame,text="Enjoyment")
		self.entertainment_progress = ttk.Progressbar(self.leisure_frame,orient="horizontal", 
										length=150, mode="determinate")		
		self.fitness_label = ttk.Label(self.leisure_frame,text="Fitness")
		self.fitness_progress = ttk.Progressbar(self.leisure_frame,orient="horizontal", 
										length=150, mode="determinate")

		#Vital levels
		self.vital_title = ttk.Label(self.vital_frame,text="Vitals system",font="bold")
		self.health_label = ttk.Label(self.vital_frame,text="Health")
		self.health_progress = ttk.Progressbar(self.vital_frame, orient="vertical", 
										length=180, mode="determinate")
		self.sanity_label = ttk.Label(self.vital_frame,text="Sanity")
		self.sanity_progress = ttk.Progressbar(self.vital_frame, orient="vertical", 
										length=180, mode="determinate")

		#Status updates
		self.status_label = ttk.Label(self.status_frame,text="Status:",font="bold")
		self.status_info = ttk.Label(self.status_frame,width="100")
		
		#position the GUI components:
		#set up frames
		self.satisfaction_frame.place(x=0,y=0,width=230,height=80)
		self.cleanliness_frame.place(x=0,y=80,width=230,height=80) 
		self.leisure_frame.place(x=0,y=160,width=230,height=80)
		self.vital_frame.place(x=230,y=0,width=120,height=240)
		self.status_frame.place(x=0,y=240,width=370,height=80)

		#Satisfaction frame
		self.satisfaction_frame.grid_columnconfigure(0,minsize=75)
		self.satisfaction_title.grid(row=0,columnspan=2,sticky="w",pady=(0,5))
		self.hunger_label.grid(row=1)
		self.hunger_progress.grid(row=1,column=1)
		self.thirst_label.grid(row=2)
		self.thirst_progress.grid(row=2,column=1)

		#Cleanliness frame
		self.cleanliness_frame.grid_columnconfigure(0,minsize=75)
		self.cleanliness_title.grid(row=0,columnspan=2,sticky="w",pady=(0,5))
		self.hygiene_label.grid(row=1)
		self.hygiene_progress.grid(row=1,column=1)
		self.bladder_label.grid(row=2)
		self.bladder_progress.grid(row=2,column=1)

		#Leisure frame
		self.leisure_frame.grid_columnconfigure(0,minsize=75)
		self.leisure_title.grid(row=0,columnspan=2,sticky="w",pady=(0,5))
		self.entertainment_label.grid(row=1)
		self.entertainment_progress.grid(row=1,column=1)
		self.fitness_label.grid(row=2)
		self.fitness_progress.grid(row=2,column=1)

		#Vital levels frame
		self.vital_title.grid(row=0,columnspan=2,pady=(0,5),padx=(10,0))
		self.health_label.grid(row=2,padx=(10,0))
		self.health_progress.grid(row=1,padx=(10,0))
		self.sanity_label.grid(row=2,column=1)
		self.sanity_progress.grid(row=1,column=1)

		#status frame
		self.status_label.grid(row=0,sticky="w")
		self.status_info.grid(row=1,rowspan=2, padx=10)

		self.hunger_progress["value"] = 100
		self.health_progress["value"] = 100
		self.entertainment_progress["value"] = 100
		self.sanity_progress["value"] = 100
		self.fitness_progress["value"] = 100
		self.thirst_progress["value"] = 100
		self.hygiene_progress["value"] = 100
		self.bladder_progress["value"] = 100

	def update_hunger_level(self,status_value):
		self.hunger_level = status_value
		self.hunger_progress["value"] = self.hunger_level

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(40)


def callback(msg):
	#print (msg)

	status_value = int(msg.data.split()[1])
	status_type = msg.data.split()[0][:-1]

	if (status_value>80):
		pass
	elif(status_value>50):
		stat_pub.publish(constants.Statuses.mid[status_type])
	elif(status_value>20):
		stat_pub.publish(constants.Statuses.low[status_type])
	elif(status_value>0):
		stat_pub.publish(constants.Statuses.dangerous[status_type])
	else:
		print "Something has gone terribly wrong"


	if status_value> 100:
		status_value = 100
	mGui.update_hunger_level(status_value)
	if status_value <= 0:
		print ("0/100")
	else:
		print (msg.data + "/100")
	

		
def scheduler_callback(msg):	
	status = ''
	#Search the dictionary (resident_statuses) in the Constants file for the correct status
	status = constants.Statuses.resident_statuses[msg.data]
	mGui.status_info["text"] = status


sub = rospy.Subscriber("human", std_msgs.msg.String, callback)
sub = rospy.Subscriber("scheduler", std_msgs.msg.String, scheduler_callback)

stat_pub = rospy.Publisher("human_status", std_msgs.msg.String, queue_size = 10)

mGui = StatusGUI()
mGui.mainloop()

while not rospy.is_shutdown():
	rate.sleep()






