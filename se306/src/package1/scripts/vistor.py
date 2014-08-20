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

class Visitor(constants.Paths, navigation.Navigation):
	def __init__(self, robot_name):
		navigate = navigation.Navigation(robot_name)
		rate = rospy.Rate(40)


	def process_event(action_msg):
		message = str(action_msg).split("data: ")[1]
		if (message == 'Visitor.visit'):
			self.current_path = list(self.door_to_living_room) + (list(self.door_to_living_room[::-1]))
			self.target_coordinate = self.current_path.pop(0)


if __name__ == '__main__':
	rospy.init_node('visitor_robot')
	navigate = Visitor("visitor_robot")
	rospy.Subscriber("scheduler", String, process_event)

	move_cmd = geometry_msgs.msg.Twist()
	target = math.pi/2
	while not rospy.is_shutdown():
		navigate.rate.sleep()
	