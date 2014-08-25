#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import sensor_msgs.msg
import std_msgs.msg
import nav_msgs.msg

import math
import TurnHelp
import constants

from std_msgs.msg import String
from tf.transformations import euler_from_quaternion

''' This class handles all navigation for robots. It is meant to supplement
other robot classes and provide them with the navigation functionality.
It uses the constants.Paths for it's path variables to keep things tidy and
minimize possible duplication
'''

class Navigation(constants.Paths):

	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if new_angle < 0:
			new_angle += 360;
		return new_angle

	''' This method is used to let a robot rotate at a high speed when it is not 
	close to the target angle it is rotating to, while also allowing it to slow
	down as it approaches it's target
	'''	
	def get_rotation_speed(self):
		old_max = 180
		old_min = 1
		new_max = 4
		new_min = 0.1

		target_angle 	= 	self.normalize(int(math.degrees(self.target_direction)))
		current_angle 	=	self.normalize(int(math.degrees(self.current_direction)))

		difference = abs(target_angle -  current_angle)
		difference = abs((difference + 180) % 360 - 180)

		old_range = (old_max - old_min)  
		new_range = (new_max - new_min)  

		rotation_speed = (((difference - old_min) * new_range) / old_range) + new_min
		return rotation_speed

	def process_range_data(self, lazer_beamz):
		distance_infront = min(lazer_beamz.ranges[85:96])
		if(distance_infront < 0.05):
			self.collision = True
		else:
			self.collision = False
		print(distance_infront)

	# Process current position and move if neccessary
	def process_position(self, position_data):
		self.current_coordinates[0] = position_data.pose.pose.position.x
		self.current_coordinates[1] = position_data.pose.pose.position.y
		
		quaternion = position_data.pose.pose.orientation
		quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
		self.current_direction = euler_from_quaternion(quaternionlist)[2]

		# Setup target direction
		if (len(self.target_coordinate) > 0):			
			if(abs(self.current_coordinates[0] - self.target_coordinate[0]) > 0.2):
				self.not_at_target = True
				if (self.current_coordinates[0] > self.target_coordinate[0]):
					self.target_direction = self.west
				else:
					self.target_direction = self.east
			else:
				if(abs(self.current_coordinates[1] - self.target_coordinate[1]) > 0.2):
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
					else:
						self.target_coordinate = []

			# Find optimal direction to rotate
			clockwise = TurnHelp.Angle(self.current_direction, self.target_direction).check()
			# Finding optimal speed to rotate
			rotation_speed = self.get_rotation_speed()
			# print(rotation_speed)

			# Rotation
			if(abs(self.current_direction - self.target_direction) >  math.radians(2)):
				#self.move_cmd.angular.z = clockwise * math.pi / 25
				self.move_cmd.angular.z = clockwise * rotation_speed
				self.facing_correct_direction = False
			else:
				self.move_cmd.angular.z = 0
				self.facing_correct_direction = True

			# Linear movement
			if (self.facing_correct_direction == True and self.not_at_target == True):
				self.move_cmd.linear.x = self.movement_speed
			else:
				self.move_cmd.linear.x = 0

		if(self.collision == True):
			self.move_cmd.linear.x = 0	
	''' Robots are initialized with a name which is passed in as a parameter. This allows us
	to use this class to publish and subscribe with many different robots inheriting from this
	class
	'''
	def __init__(self, robot_name):
		self.robot_name = robot_name		
		self.movement_speed = 0.5

		self.collision = False
		# Default path and direction
		self.current_path = self.door_to_kitchen
		self.current_direction	= self.north

		# Default target path and direction
		self.target_coordinate = []
		self.target_direction = self.west

		self.current_coordinates = [0,0]

		self.not_at_target = True		
		self.facing_correct_direction = False

		self.move_cmd = geometry_msgs.msg.Twist()

		subscribe_to = "/" + robot_name + "/base_pose_ground_truth"
		rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, self.process_position)

		publish_to = "/" + robot_name + "/cmd_vel"		
		self.movement_publisher = rospy.Publisher(publish_to, geometry_msgs.msg.Twist, queue_size=10)		
		
		subscribe_to = "/" + robot_name + "/base_scan"
		rospy.Subscriber(subscribe_to, sensor_msgs.msg.LaserScan, self.process_range_data)

	# Method currently is unused and has no real function yet. Need current position for this method
	# to be useful
	def move (self, room):
		self.current_path = list(self.door_to_living_room) + (list(self.door_to_living_room[::-1]))
		self.target_coordinate = self.current_path.pop(0)
	