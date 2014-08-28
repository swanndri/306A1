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
import tf.transformations
import Rectangle

from tf.transformations import euler_from_quaternion

""" This class handles all navigation for robots.

It is meant to supplement other robot classes and provide them with the navigation
functionality. It utilises the `constants.Paths` class for its path variables.
"""

class Navigation(constants.Paths):
	
	''' -----------------------------Call Backs-----------------------------'''

	def process_range_data(self, lazer_beamz):
		if (self.target_coordinate != [] and self.facing_correct_direction == True):
			adjust_distance = 0.7

			targetx = self.target_coordinate[0]
			targety = self.target_coordinate[1]

			distance_infront = min(lazer_beamz.ranges[89:92])	
			immediate_infront = min(lazer_beamz.ranges[45:136])		
			distance_to_waypoint = self.get_distance_to_target(targetx, targety)

			if(distance_infront < distance_to_waypoint / 2 and self.col_other_robot == False):
				self.current_path.insert(0,self.target_coordinate)

				perp = self.normalize(math.degrees(self.current_direction))
				perp = perp + 90
				perp = self.normalize(perp)

				x_adjust = math.cos(math.radians(perp)) * adjust_distance
				y_adjust = math.sin(math.radians(perp)) * adjust_distance

				x1 = ((targetx - self.current_coordinates[0]) / 2) + self.current_coordinates[0]
				y1 = ((targety - self.current_coordinates[1]) / 2) + self.current_coordinates[1]

				new_coord = [x1 + x_adjust, y1 + y_adjust]
				self.target_coordinate = new_coord 
				self.facing_correct_direction = False
				self.col_other_robot = True

			if(immediate_infront == min(lazer_beamz.ranges[45:136]) < 0.2):
				print("still to implement")
				self.collision = True
			else:
				self.collision = False			
			

	# Process current position and move if neccessary
	def process_position(self, position_data):
		# print(self.get_current_position())

		self.current_coordinates[0] = position_data.pose.pose.position.x
		self.current_coordinates[1] = position_data.pose.pose.position.y
		
		quaternion = position_data.pose.pose.orientation
		quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
		self.current_direction = euler_from_quaternion(quaternionlist)[2]

		# Setup target direction
		if (len(self.target_coordinate) > 0):		
			# Check to see if we have reached our target or not.
			if(abs(self.current_coordinates[0] - self.target_coordinate[0]) > 0.2 or
				abs(self.current_coordinates[1] - self.target_coordinate[1]) > 0.2):
				self.not_at_target = True

			#We have reached our target. 
			else:
				self.not_at_target = False
				self.col_other_robot = False
				self.move_cmd.linear.x = 0
				self.move_cmd.angular.z = 0

				#Check if there are any more way points to go to.
				if(len(self.current_path) > 0):
					self.target_coordinate = self.current_path.pop(0)
					self.not_at_target = True
				else:
					self.target_coordinate = []

			if(self.target_coordinate != []):
				self.target_direction = self.calculate_heading()
				# Find optimal direction to rotate
				clockwise = TurnHelp.Angle(self.current_direction, self.target_direction).check()
				# Finding optimal speed to rotate
				rotation_speed = self.get_rotation_speed()

				# Rotation
				if(abs(self.current_direction - self.target_direction) >  math.radians(2)):
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
	''' -----------------------------Helper Methods-----------------------------'''
	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if (new_angle > 360):
    			new_angle = new_angle - 360
    		if new_angle < 0:
				new_angle += 360;
		return new_angle

	def calculate_heading(self):
		x_diff = self.target_coordinate[0] - self.current_coordinates[0]
		y_diff = self.target_coordinate[1] - self.current_coordinates[1]

		if(x_diff > -0.01 and x_diff < 0.01):
			x_diff = 0.01
		if(y_diff > -0.01 and y_diff < 0.01):
			y_diff = 0.01

		angle = math.degrees(math.atan(y_diff / x_diff))

		if(x_diff < 0 and y_diff < 0):
			angle = angle + 180
		elif(x_diff < 0 and y_diff > 0):
			angle = angle + 180
		elif(x_diff > 0 and y_diff < 0):
			angle = angle + 360

		''' De normalize Angle '''
		if angle > 180:
			angle -= 360;

		angle = math.radians(angle)
		return angle

	def get_distance_to_target(self, targetx, targety):
		x_squared = pow((targetx - self.current_coordinates[0]), 2)
		y_squared = pow((targety - self.current_coordinates[1]), 2)
		return math.sqrt(x_squared + y_squared)

	''' This method is used to let a robot rotate at a high speed when it is not 
	close to the target angle it is rotating to, while also allowing it to slow
	down as it approaches it's target
	'''	
	def get_rotation_speed(self):
		""" This method is used to let a robot rotate at a high speed when it is not 
		close to the target angle it is rotating to, while also allowing it to slow
		down as it approaches its target.
		"""

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


	def get_current_position(self):
		xcurrent = self.current_coordinates[0]
		ycurrent = self.current_coordinates[1]
		pt = [xcurrent, ycurrent]
		print(pt)
		for rect in self.rect_list:
			if(rect.contains(pt)):
				return rect.name
		return "Outside"

	''' ----------------------------------Init----------------------------------'''

	''' Robots are initialized with a name which is passed in as a parameter. This allows us
	to use this class to publish and subscribe with many different robots inheriting from this
	class
	'''
	def __init__(self, robot_name):
		self.robot_name = robot_name		
		self.movement_speed = 0.7

		self.col_other_robot = False
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

if __name__ == "__main__":
	print "This was not intended to be run directly."
