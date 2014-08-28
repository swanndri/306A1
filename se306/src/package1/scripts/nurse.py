#!/usr/bin/env python


import roslib
import rospy
import rosgraph_msgs
import std_msgs.msg
import navigation
import constants
import os

from std_msgs.msg import String

class Nurse(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		
		#checks for the heart attack message, if found schedules the event. Needs to be implemented in the resident first
		if ("Nurse.heart_attack" in message):
			self.task_list.append(message)
		
		#gets in the sick message i.e health under 30
		if ("Nurse.sick" in message):
			self.task_list.append(message)


	def perform_task(self, task):
		self.status = "active"

		if (task == 'Nurse.heart_attack'):
			self.navigate.current_path = list(self.bedroom_to_living_room)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)


	def __init__(self):

		self.task_list = []
		self.status = "idle"

		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up. 
		# Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_Nurse")		
		rospy.Subscriber("scheduler", String, self.process_event)
		sub = rospy.Subscriber("clock", rosgraph_msgs.msg.Clock, self.callback)
		subRes = rospy.Subscriber("human", rosgraph_msgs.String, self.callback)
		self.pub = rospy.Publisher('nurse', std_msgs.msg.String, queue_size=10)

		#runs through the task list when not idle
		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)
			# print statement for debugging path
			# print (self.task_list, self.status, self.navigate.target_coordinate)
			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"


			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))

			self.rate.sleep()	



	def callback(self, msg):
		
		#need to set callback methods up
		pass


				
if __name__ == '__main__':
	rospy.init_node('nurse_robot')
	nurse = Nurse()