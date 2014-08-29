#!/usr/bin/env python

import roslib; roslib.load_manifest('package1')
import std_msgs.msg
import rospy
import Tkinter as tk
import ttk
import database

class StatusGUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#sets the dimensions and settings of thw window
		self.geometry("380x380+700+100")
		self.title("Resident status")

		self.build_frames()

		self.combobox_set_up()
		self.cb.pack()

		#build the GUI components:
		self.build_gui_components()
		
		#position the GUI components:
		self.position_frames_and_components()

		#initialize progress bar values
		self.initialize_status_bars()

	def build_frames(self):
		self.all_bars_frame = tk.Frame(self)
		self.horizontal_bars_frame = tk.Frame(self.all_bars_frame)
		self.satisfaction_frame = ttk.Labelframe(self.horizontal_bars_frame,text="Satisfaction",padding=(0,0,10,10))
		self.leisure_frame = ttk.Labelframe(self.horizontal_bars_frame,text="Leisure",padding=(0,0,10,10))
		self.cleanliness_frame = ttk.Labelframe(self.horizontal_bars_frame,text="Cleanliness",padding=(0,0,10,10))
		self.vital_frame = ttk.Labelframe(self.all_bars_frame,text="Vitals",padding=(0,10,0,10))
		self.status_frame = ttk.Labelframe(self,text="Status")
		self.combo_frame = ttk.Labelframe(self,text="Generate event")

	def build_gui_components(self):
		#Satisfaction levels
		self.fullness_label = ttk.Label(self.satisfaction_frame,text="Fullness")
		self.fullness_progress = ttk.Progressbar(self.satisfaction_frame, orient="horizontal", 
										length=150, mode="determinate")
		self.hydration_label = ttk.Label(self.satisfaction_frame,text="Hydration")
		self.hydration_progress = ttk.Progressbar(self.satisfaction_frame, orient="horizontal", 
										length=150, mode="determinate")

		#Cleanliness levels
		self.hygiene_label = ttk.Label(self.cleanliness_frame, text="Hygiene")
		self.hygiene_progress = ttk.Progressbar(self.cleanliness_frame, orient="horizontal", 
										length=150, mode="determinate")
		self.relief_label = ttk.Label(self.cleanliness_frame,text="Relief")
		self.relief_progress = ttk.Progressbar(self.cleanliness_frame,orient="horizontal", 
										length=150, mode="determinate")

		#Leisure levels
		self.entertainment_label = ttk.Label(self.leisure_frame,text="Enjoyment")	#this is entertainment
		self.entertainment_progress = ttk.Progressbar(self.leisure_frame,orient="horizontal", 
										length=150, mode="determinate")		
		self.fitness_label = ttk.Label(self.leisure_frame,text="Fitness")
		self.fitness_progress = ttk.Progressbar(self.leisure_frame,orient="horizontal", 
										length=150, mode="determinate")

		#Vital levels
		self.health_label = ttk.Label(self.vital_frame,text="Health")
		self.health_progress = ttk.Progressbar(self.vital_frame, orient="vertical", 
										length=180, mode="determinate")
		self.sanity_label = ttk.Label(self.vital_frame,text="Sanity")
		self.sanity_progress = ttk.Progressbar(self.vital_frame, orient="vertical", 
										length=180, mode="determinate")

		#Status updates
		self.status_info = ttk.Label(self.status_frame,width="40",wraplength=320)

	def position_frames_and_components(self):
		#set up frames
		self.all_bars_frame.pack()
		self.horizontal_bars_frame.pack(side="left")
		self.satisfaction_frame.pack(padx=(0,10),pady=10)
		self.cleanliness_frame.pack(padx=(0,10),pady=10)
		self.leisure_frame.pack(padx=(0,10),pady=10)
		self.vital_frame.pack(side="left",padx=10,pady=5)
		self.combo_frame.pack()
		self.status_frame.pack()

		#Satisfaction frame
		self.satisfaction_frame.grid_columnconfigure(0,minsize=75)
		self.fullness_label.grid(row=0)
		self.fullness_progress.grid(row=0,column=1)
		self.hydration_label.grid(row=1)
		self.hydration_progress.grid(row=1,column=1)

		#Cleanliness frame
		self.cleanliness_frame.grid_columnconfigure(0,minsize=75)
		self.hygiene_label.grid(row=0)
		self.hygiene_progress.grid(row=0,column=1)
		self.relief_label.grid(row=1)
		self.relief_progress.grid(row=1,column=1)

		#Leisure frame
		self.leisure_frame.grid_columnconfigure(0,minsize=75)
		self.entertainment_label.grid(row=0)
		self.entertainment_progress.grid(row=0,column=1)
		self.fitness_label.grid(row=1)
		self.fitness_progress.grid(row=1,column=1)

		#Vital levels frame
		self.health_label.grid(row=1,padx=(5,1))
		self.health_progress.grid(row=0,padx=(5,1))
		self.sanity_label.grid(row=1,column=1,padx=(1,5))
		self.sanity_progress.grid(row=0,column=1,padx=(1,5))

		#status frame
		self.status_info.grid(row=0,rowspan=2, columnspan=2, padx=10, pady=10)

	def initialize_status_bars(self):
		self.fullness_progress["value"] = 100
		self.health_progress["value"] = 100
		self.entertainment_progress["value"] = 100
		self.sanity_progress["value"] = 100
		self.fitness_progress["value"] = 100
		self.hydration_progress["value"] = 100
		self.hygiene_progress["value"] = 100
		self.relief_progress["value"] = 100

	def handle_selected(self, event):
		print("generating event")
		index = self.cb.current()
		selected_event = self.events[index]
		print(selected_event)
		if selected_event == "Heart Attack":
			#publish new message to robots
			task = database.Database.EVENTS.get('Resident.heart_attack')
			event_priority = task.get('priority')
			event_name = 'Resident.heart_attack'
			event_duration = task.get('duration')
			event_destination = task.get('destination')
			event_pub.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
			print("Should publish new event - doctor.doctor.emergency")		#example
		elif selected_event == "Eat":
			#publish new message to robots
			task = database.Database.EVENTS.get('Resident.eat_snack')
			event_priority = task.get('priority')
			event_name = 'Resident.eat_snack'
			event_duration = task.get('duration')
			event_destination = task.get('destination')
			event_pub.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
			print("Should publish new event - ",selected_event)
		elif selected_event == "Exercise":
			task = database.Database.EVENTS.get('Resident.gym')
			event_priority = task.get('priority')
			event_name = 'Resident.gym'
			event_duration = task.get('duration')
			event_destination = task.get('destination')
			event_pub.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
			#publish new message to robots
			print("Should publish new event - ",selected_event)
		elif selected_event == "Bath":
			task = database.Database.EVENTS.get('Resident.bath')
			event_priority = task.get('priority')
			event_name = 'Resident.bath'
			event_duration = task.get('duration')
			event_destination = task.get('destination')
			event_pub.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
			#publish new message to robots
			print("Should publish new event - ",selected_event)
		elif selected_event == "Toilet":
			task = database.Database.EVENTS.get('Resident.toilet')
			event_priority = task.get('priority')
			event_name = 'Resident.toilet'
			event_duration = task.get('duration')
			event_destination = task.get('destination')
			event_pub.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
			#publish new message to robots
			print("Should publish new event - ",selected_event)
		elif selected_event == "Sleep":
			task = database.Database.EVENTS.get('Resident.sleep')
			event_priority = task.get('priority')
			event_name = 'Resident.sleep'
			event_duration = task.get('duration')
			event_destination = task.get('destination')
			event_pub.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
			#publish new message to robots
			print("Should publish new event - ",selected_event)

	def combobox_set_up(self):
		self.events = ('Heart Attack','Eat','Exercise','Sleep','Bath','Toilet')
		self.cb = ttk.Combobox(self.combo_frame, values=self.events, state='readonly')
		self.cb.bind("<<ComboboxSelected>>", self.handle_selected)

	def update_status_level(self,status_type,status_value):
		if status_type == "Fullness":
			self.fullness_progress["value"] = status_value
		elif status_type == "Health":
			self.health_progress["value"] = status_value
		elif status_type == "Entertainment":
			self.entertainment_progress["value"] = status_value
		elif status_type == "Sanity":
			self.sanity_progress["value"] = status_value
		elif status_type == "Fitness":
			self.fitness_progress["value"] = status_value
		elif status_type == "Hydration":
			self.hydration_progress["value"] = status_value
		elif status_type == "Hygiene":
			self.hygiene_progress["value"] = status_value
		elif status_type == "Relief":
			self.relief_progress["value"] = status_value

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(40)


def callback(msg):
	status_name, status_value = msg.data.split()

	if (status_value>80):
		pass
	elif(status_value>50):
		stat_pub.publish("%s %s" % (status_name, 'med'))
	elif(status_value>20):
		stat_pub.publish("%s %s" % (status_name, 'low'))
	elif(status_value>0):
		stat_pub.publish("%s %s" % (status_name, 'dan'))
	else:
		print "Something has gone terribly wrong"


	# if status_value > 100:		entering this loop for some reason
	# 	status_value = 100

	status_type = status_name[:-1]
	mGui.update_status_level(status_type,status_value)
	if status_value <= 0:
		print ("0/100")
	else:
		print (msg.data + "/100")
	

		
def scheduler_callback(msg):	
	print(msg)
	if ("status" in msg.data):
		task = msg.data[:-4]
	else:
		task = msg.data

	status = ''
	#Search the dictionary (resident_statuses) in the Constants file for the correct status
	print(task.split())
	temp = database.Database.EVENTS.get(task.split()[1])
	print(temp)
	status = temp.get('explanation')
	mGui.status_info["text"] = status
	

sub = rospy.Subscriber("human", std_msgs.msg.String, callback)
sub = rospy.Subscriber("scheduler", std_msgs.msg.String, scheduler_callback)

stat_pub = rospy.Publisher("human_status", std_msgs.msg.String, queue_size = 10)
event_pub = rospy.Publisher('scheduler', std_msgs.msg.String, queue_size=10)

mGui = StatusGUI()
mGui.mainloop()

while not rospy.is_shutdown():
	rate.sleep()






