#!/usr/bin/env python

import rospy
import roslib
import geometry_msgs.msg
import std_msgs.msg
import nav_msgs.msg
import sensor_msgs.msg
import time
import navigation

from std_msgs.msg import String

class Resident(navigation.Navigation):


	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		
		if ("Resident" in message):
			self.task_list.append(message)


	def perform_task(self, task):

		self.status = "active"

		if (task == 'Resident.wakeup'):
			self.navigate.current_path = list(self.bedroom_to_living_room)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

		if (task == 'Resident.eat_breakfast'):
			self.navigate.current_path = list(self.living_room_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

		if (task == 'Resident.take_meds'):
			self.navigate.current_path = list(self.kitchen_to_cupboard)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.eat_lunch'):
			self.navigate.current_path = list(self.cupboard_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.eat_dinner'):
			self.navigate.current_path = list(self.living_room_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.sleep'):
			self.navigate.current_path = list(self.kitchen_to_bedroom)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.idle'):
			self.navigate.current_path = list(self.kitchen_to_idle)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

	
	def __init__(self):
		self.rate = rospy.Rate(20)
		self.task_list = []
		self.status = "idle"
		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up. 
		#Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_1")		
		rospy.Subscriber("scheduler", String, self.process_event)

		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)
			print (self.task_list, self.status, self.navigate.target_coordinate)
			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"


			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))


			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('resident_robot')
	resident = Resident()
	