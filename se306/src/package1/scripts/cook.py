#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
import navigation

from std_msgs.msg import String

class Cook(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		if ('Cook.cook_' in message):

			self.task_list.append(message)
			


	def perform_task(self, task):

		self.status = "active" 

		if task =="Cook.cook_":
			self.navigate.current_path = list(self.cook_path)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)


	

	def __init__(self):
		self.rate = rospy.Rate(20)
		self.task_list = []
		self.status = "idle"
		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up. 
		#Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_2")
		rospy.Subscriber("scheduler", String, self.process_event)

		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)

			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"


			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))

			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('cook_robot')
	cook = Cook()
