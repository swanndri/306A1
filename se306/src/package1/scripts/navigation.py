#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import sensor_msgs.msg
import std_msgs.msg
import nav_msgs.msg

import math
import utils
import database
import tf.transformations

class Navigation(constants.Paths):

	""" This class handles all navigaself.cution for robots.

	It is meant to supplement other robot classes and provide them with the navigation
	functionality. It utilises the `constants.Paths` class for its path variables.
	"""

	def __init__(self, robot_name):
		""" Robots are initialized with a name which is passed in as a parameter. This allows us
		to use this class to publish and subscribe with many different robots inheriting from this class
		"""

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
		# rospy.Subscriber(subscribe_to, sensor_msgs.msg.LaserScan, self.process_range_data)
	
	''' -----------------------------Call Backs-----------------------------'''

	# Process current position and move if neccessary
	def process_position(self, position_data):
		print("Current room:",self.get_current_position())
		print("Current path:",self.current_path)
		print("Current target:", self.target_coordinate)

		self.current_coordinates[0] = position_data.pose.pose.position.x
		self.current_coordinates[1] = position_data.pose.pose.position.y
		
		quaternion = position_data.pose.pose.orientation
		quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
		self.current_direction = tf.transformations.euler_from_quaternion(quaternionlist)[2]

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

			# We are not at target, and there is another target coordinate
			if(self.target_coordinate != []):
				self.target_direction = self.calculate_heading()

				self.rotate_to_direction(self.target_direction)

				self.move_to_target()

		if (self.collision == True):
			self.move_cmd.linear.x = 0

	
	def rotate_to_direction(self, ros_angle):
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


	def move_to_target(self):
		# Linear movement
		if (self.facing_correct_direction == True and self.not_at_target == True):
			self.move_cmd.linear.x = self.movement_speed
		else:
			self.move_cmd.linear.x = 0


	''' -----------------------------Helper Methods-----------------------------'''
	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if (new_angle > 360):
    			new_angle = new_angle - 360
    		if new_angle < 0:
				new_angle += 360;
		return new_angle

	# Returns an angle, with ROS coordinates
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
		# print(pt)
		for object_name, (pt1, pt2) in database.OBJECTS.iteritems():
			if utils.Rectangle(pt1, pt2).contains(pt):
				return object_name
		return "visitor_idle"

	# Enter the room node you wish to go to and this method will create a path using the A* algorithm
	# and put it on as the current_path
	def move (self, room):
		current_node = self.get_current_position()
		s = utils.Search()

		nodes_path = s.find_path(current_node, room)
		self.current_path = self.convert_path(nodes_path)

		self.target_coordinate = self.current_path.pop(0)

	def convert_path(self, nodes_path):
		path = []
		for i in nodes_path:
			path.append(self.points[i])
			# print(i,self.points[i])
		return path


if __name__ == "__main__":
	print "This was not intended to be run directly."
