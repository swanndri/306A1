#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import std_msgs.msg
import nav_msgs.msg
import sensor_msgs.msg
import math
import time
import tf
import TurnHelp
import constants
import navigation

from std_msgs.msg import String
from tf.transformations import euler_from_quaternion

class Cook(constants.Paths, navigation.Navigation):

	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		if ('Cook.cook_' in message):
			self.navigate.current_path = list(self.cook_path)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

	def __init__(self):
		self.rate = rospy.Rate(20)
		self.navigate = navigation.Navigation("robot_2")
		rospy.Subscriber("scheduler", String, self.process_event)

		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)
			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('cook_robot')
	cook = Cook()
