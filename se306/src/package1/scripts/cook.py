#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
import navigation
import constants

class Cook(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''

	def __init__(self):
		self.rate = rospy.Rate(constants.RosConstants.robot_rate)
		self.task_list = []
		self.status = "idle"

		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Pass the robot's name so that the publisher 
		# and subscribers for its navigation can be set up.
		self.navigate = navigation.Navigation("robot_2")

		rospy.Subscriber("scheduler", std_msgs.msg.String, self.process_event)

		self.loop()

	def loop(self):
		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)

			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"

			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))

			self.rate.sleep()

	def process_event(self, action_msg):
		if ('Cook.cook_' in action_msg.data):
			self.task_list.append(action_msg.data)

	def perform_task(self, task):
		self.status = "active" 

		if ("Cook.cook_" in task):
			self.navigate.current_path = list(self.cook_path)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

if __name__ == '__main__':
	rospy.init_node('cook_robot')
	cook = Cook()
