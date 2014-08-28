#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import sensor_msgs.msg
import std_msgs.msg
import nav_msgs.msg

import math
import database
import tf.transformations
import utils


""" This class handles all navigation for robots.
It is meant to supplement other robot classes and provide them with the navigation
functionality. It utilises the `constants.Paths` class for its path variables.
"""

class Navigation(object):
	
	''' -----------------------------Call Backs-----------------------------'''
	def process_range_data(self, lazer_beamz):
		#If we are headed somewhere and we are facing the correct direction.
		if (self.target_coordinate != [] and self.facing_correct_direction == True) or self.collision_mode == True:

			if(self.collision_mode == False):				
				angle_list = list(range(45, 135))
				collision_imminent = False
				for angle in angle_list:
					distance_to_collision = lazer_beamz.ranges[angle]
					if (distance_to_collision < 0.4):	
						collision_imminent = True
						break
				self.collision_mode = collision_imminent
			print(self.collision_mode)
			if(self.collision_mode == True):
				all_clear = True
				angle_list = list(range(55, 125))
				for angle in angle_list:
					distance_to_collision = lazer_beamz.ranges[angle]
					if (distance_to_collision < 0.5):	
						all_clear = False
						break
				print("all clear" + str (all_clear))
				if(all_clear):
					theta = self.normalize(int(math.degrees(self.current_direction)))
					x_adjust = math.cos(math.radians(theta)) * 0.7
					y_adjust = math.sin(math.radians(theta)) * 0.7

					x1 = self.current_coordinates[0]
					y1 = self.current_coordinates[1]

					new_coord = [x1 + x_adjust, y1 + y_adjust]

					place = None

					for name, (p1, p2) in database.Database.OBJECTS.iteritems():
						if utils.Rectangle(p1, p2).contains(new_coord):
							place = name
							break
					if(place == None):
						place = "visitor_idle"

					current_place = self.get_current_position()

					self.current_path.insert(0,self.target_coordinate)
					print(self.current_col_nodes_added)
					print(self.original_path)

					if(self.current_col_nodes_added == 0):
						self.original_path = list(self.current_path)					
					
					print("CURRENT")
					print(self.current_path)
					print(self.target_coordinate)
					print("END LOOP")
					
					if(str(current_place) == str(place)):		
						if(self.current_col_nodes_added == 3):
							self.current_path = self.original_path
							self.target_coordinate = self.current_path.pop(0)
							self.current_col_nodes_added = 0
						else:			
							self.target_coordinate = new_coord							
							self.current_col_nodes_added += 1

						self.collision_mode = False
					else:
						self.target_coordinate = self.current_path.pop(0)

	# Process current position and move if neccessary
	def process_position(self, position_data):
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
				self.facing_correct_direction = False
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
				self.rotate_to_direction(self.target_direction)

				self.move_to_target()

		if(self.waypoint_blocked == True):
			self.move_cmd.linear.x = 0	

	def rotate_to_direction(self, ros_angle):
		# Find optimal direction to rotate
		clockwise = utils.Angle(self.current_direction, self.target_direction).check()
		# Finding optimal speed to rotate
		rotation_speed = self.get_rotation_speed()

		# Rotation
		if(abs(self.current_direction - self.target_direction) >  math.radians(2)):
			self.move_cmd.angular.z = clockwise * rotation_speed
			self.facing_correct_direction = False
		else:
			self.move_cmd.angular.z = 0
			self.facing_correct_direction = True
			
		if(self.collision_mode):
			self.move_cmd.angular.z = 0.5

	def move_to_target(self):
		# Linear movement
		if(self.facing_correct_direction and self.collision_mode == False):
			self.movement_speed = self.movement_speed_constant
		else:
			self.movement_speed = 0

		if (self.not_at_target == True):
			self.move_cmd.linear.x = self.movement_speed
		else:
			self.move_cmd.linear.x = 0

	''' -----------------------------Helper Methods-----------------------------'''

	def get_consecutive_good_angles(self, intersects, angle_list):
		consecutive_count = 0
		iteration_count = 0

		for truth in intersects:
			if(truth):
				consecutive_count += 1
				if(consecutive_count > 30):
					return angle_list[iteration_count - 30]
			else:
				consecutive_count = 0
			iteration_count += 1
		return None

	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if (new_angle > 360):
    			new_angle = new_angle - 360
    		if new_angle < 0:
				new_angle += 360;
		return new_angle

	#returns current heading in ros coordinates
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
		#returns a distance from targetx, targety to current coordinates
		x_squared = pow((targetx - self.current_coordinates[0]), 2)
		y_squared = pow((targety - self.current_coordinates[1]), 2)
		return math.sqrt(x_squared + y_squared)

	def get_rotation_speed(self):
		""" This method is used to let a robot rotate at a high speed when it is not 
		close to the target angle it is rotating to, while also allowing it to slow
		down as it approaches its target.
		"""

		old_max = 180
		old_min = 1
		new_max = 6
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

		for name, (p1, p2) in database.Database.OBJECTS.iteritems():
			if utils.Rectangle(p1, p2).contains(pt):
				return name
		return "visitor_idle"

	''' ----------------------------------Init----------------------------------'''
	''' Robots are initialized with a name which is passed in as a parameter. This allows us
	to use this class to publish and subscribe with many different robots inheriting from this
	class
	'''
	def __init__(self, robot_name):

		#init all our used variables
		self.robot_name = robot_name		
		self.movement_speed_constant = 0.6

		self.current_path 			= []
		self.current_direction		= None
		self.target_coordinate 		= []
		self.target_direction 		= None
		self.current_coordinates 	= [0,0]		
		self.original_path 			= []

		self.current_col_nodes_added = 0
		self.waypoint_blocked 		= False
		self.collision_mode 		= False
		self.not_at_target 			= True		
		self.facing_correct_direction = False

		#init publishers and subscribesr
		self.move_cmd = geometry_msgs.msg.Twist()
		subscribe_to = "/" + robot_name + "/base_pose_ground_truth"
		self.test = rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, self.process_position)

		publish_to = "/" + robot_name + "/cmd_vel"		
		self.movement_publisher = rospy.Publisher(publish_to, geometry_msgs.msg.Twist, queue_size=10)		
		
		subscribe_to = "/" + robot_name + "/base_scan"
		rospy.Subscriber(subscribe_to, sensor_msgs.msg.LaserScan, self.process_range_data)

	def move(self, room):		
		self.facing_correct_direction = False
		current_node = self.get_current_position()
		s = utils.Search()

		nodes_path = s.find_path(current_node, room)
		self.current_path = self.convert_path(nodes_path)
		self.target_coordinate = self.current_path.pop(0)

	def convert_path(self, nodes_path):
		path = []
		for i in nodes_path:
			path.append(database.Database.POINTS[i])
		return path

	def has_arrived(self):
		return not self.target_coordinate
		
