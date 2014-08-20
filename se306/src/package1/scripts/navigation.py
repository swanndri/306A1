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

from std_msgs.msg import String
from tf.transformations import euler_from_quaternion

class Navigation(constants.Paths):
	def process_position(self, position_data):
		self.current_coordinates[0] = position_data.pose.pose.position.x
		self.current_coordinates[1] = position_data.pose.pose.position.y
		
		quaternion = position_data.pose.pose.orientation
		quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
		self.current_direction = euler_from_quaternion(quaternionlist)[2]

		#Setup target direction
		if (self.target_coordinate is not None):			
			if(abs(self.current_coordinates[0] - self.target_coordinate[0]) > 0.5):
				self.not_at_target = True
				if (self.current_coordinates[0] > self.target_coordinate[0]):
					self.target_direction = self.west
				else:
					self.target_direction = self.east
			else:
				if(abs(self.current_coordinates[1] - self.target_coordinate[1]) > 0.5):
					self.not_at_target = True
					if (self.current_coordinates[1] > self.target_coordinate[1]):
						self.target_direction = self.south
					else:
						self.target_direction = self.north
				else:
					self.not_at_target = False
					if(len(self.current_path) > 0):
						self.target_coordinate = self.current_path.pop(0)
						self.not_at_target = True

			# Use clockwise object instead of -1 in move_cmd.angular.z after it has been implemented fully
			clockwise = TurnHelp.Angle(self.current_direction, self.target_direction).check()
			
			max_speed = 1
			rotation_speed = (abs(self.current_direction - self.target_direction) / 180) * max_speed * 100
			print(rotation_speed)
			#ROTATION
			if(abs(self.current_direction - self.target_direction) >  math.radians(4)):
				#self.move_cmd.angular.z = clockwise * math.pi / 25
				self.move_cmd.angular.z = clockwise * rotation_speed
				self.facing_correct_direction = False
			else:
				self.move_cmd.angular.z = 0
				self.facing_correct_direction = True

			#LINEAR MOVEMENT
			if (self.facing_correct_direction == True and self.not_at_target == True):
				self.move_cmd.linear.x = 1
			else:
				self.move_cmd.linear.x = 0

	def __init__(self, robot_name):
		self.target_coordinate = None
		self.target_direction = self.west
		self.robot_name = robot_name
		
		self.current_path = self.door_to_kitchen
		self.facing_correct_direction = False

		self.not_at_target = True
		self.current_coordinates = [0,0]
		self.current_direction	= self.north
		
		self.move_cmd = geometry_msgs.msg.Twist()

		subscribe_to = "/" + robot_name + "/base_pose_ground_truth"
		rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, self.process_position)

		publish_to = "/" + robot_name + "/cmd_vel"		
		self.movement_publisher = rospy.Publisher(publish_to, geometry_msgs.msg.Twist, queue_size=10)		
		
	def move (self, room):
		self.current_path = list(self.door_to_living_room) + (list(self.door_to_living_room[::-1]))
		self.target_coordinate = self.current_path.pop(0)
	