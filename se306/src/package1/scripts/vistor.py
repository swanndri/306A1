#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
import navigation
import constants

from std_msgs.msg import String

class Visitor(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		if ("Visitor" in message):
			
			self.task_list.append(message)

			

	def perform_task(self, task):

		self.status = "active" 

		if task =="Visitor.visit":
			self.navigate.move("living_room_middle")
			self.at_idle = False



	def __init__(self):		
		self.rate = rospy.Rate(constants.RosConstants.robot_rate)
		self.task_list = []
		self.status = "idle"
		self.at_idle = True

		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up.

		#Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_0")		
		rospy.Subscriber("scheduler", String, self.process_event)

		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)

			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"

			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))
			elif len(self.navigate.current_path) < 1 and self.navigate.not_at_target == False and self.at_idle == False:
				# print("elif statement")
				self.navigate.move("visitor_idle")
				self.at_idle = True

			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('visitor_robot')
	visit = Visitor()
	