#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import std_msgs.msg
import nav_msgs.msg
import math
import TurnHelp
import constants

class Navigation(constants.Paths):
	""" This class handles all navigation for robots.

	It is meant to supplement other robot classes and provide them with the navigation
	functionality. It utilises the `constants.Paths` class for its path variables.
	"""

	def __init__(self, robot_name):
		""" Robots are initialized with a name which is passed in as a parameter."""
		self.robot_name = robot_name
		
		self.movement_speed = 0.5
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

	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if new_angle < 0:
			new_angle += 360;
		return new_angle

	def get_rotation_speed(self):
		""" This method is used to let a robot rotate at a high speed when it is not 
		close to the target angle it is rotating to, while also allowing it to slow
		down as it approaches its target.
		"""

		old_max = 180
		old_min = 1
		new_max = 4
		new_min = 0.1

		target_angle = self.normalize(int(math.degrees(self.target_direction)))
		current_angle = self.normalize(int(math.degrees(self.current_direction)))
	
		difference = abs(target_angle - current_angle)

		old_range = (old_max - old_min)  
		new_range = (new_max - new_min)  

		rotation_speed = (((difference - old_min) * new_range) / old_range) + new_min
		return rotation_speed
	
	def process_position(self, position_data):
		""" This method processes the current position and initiates a move if necessary."""

		self.current_coordinates[0] = position_data.pose.pose.position.x
		self.current_coordinates[1] = position_data.pose.pose.position.y
		
		quaternion = position_data.pose.pose.orientation
		quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
		self.current_direction = tf.transformations.euler_from_quaternion(quaternionlist)[2]

		# Set up target direction
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

			print(rotation_speed)

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
		print(self.target_coordinate)
			
		
	# Method currently is unused and has no real function yet	
	def move(self, room):
		self.current_path = list(self.door_to_living_room) + (list(self.door_to_living_room[::-1]))
		self.target_coordinate = self.current_path.pop(0)

if __name__ == "__main__":
	print "This was not intended to be run directly."