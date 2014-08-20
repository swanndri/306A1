#!/usr/bin/env python

import rospy
import roslib
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

class Resident(constants.Paths, navigation.Navigation):

	def process_event(self, action_msg):
		#print('test')
		message = str(action_msg).split("data: ")[1]
		if (message == 'Resident.wakeup'):
			self.navigate.current_path = list(self.bedroom_to_living_room)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		if (message == 'Resident.eat_breakfast'):
			self.navigate.current_path = list(self.living_room_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		if (message == 'Resident.take_meds'):
			self.navigate.current_path = list(self.kitchen_to_cupboard)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		if (message == 'Resident.eat_lunch'):
			self.navigate.current_path = list(self.cupboard_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		if (message == 'Resident.eat_dinner'):
			self.navigate.current_path = list(self.living_room_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		if (message == 'Resident.sleep'):
			self.navigate.current_path = list(self.kitchen_to_bedroom)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		if (message == 'Resident.idle'):
			self.navigate.current_path = list(self.kitchen_to_idle)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

	def __init__(self):		
		self.rate = rospy.Rate(20)
		self.navigate = navigation.Navigation("robot_1")		
		rospy.Subscriber("scheduler", String, self.process_event)

		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)
			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('resident_robot')
	resident = Resident()
	