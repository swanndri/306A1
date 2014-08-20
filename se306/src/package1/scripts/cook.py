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

class Navigate(constants.Paths):
	def __init__(self):
		self.target_coordinate = None
		self.target_direction = self.west
		
		self.current_path = self.door_to_kitchen

		self.facing_correct_direction = False

		self.not_at_target = True
		self.current_coordinates = [0,0]
		self.current_direction	= self.north
		
		#self.target_coordinate = self.current_path.pop(0)

		def process_position(position_data):
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
				#clockwise = TurnHelp.Angle(self.current_direction, self.target_direction).check()
				#print clockwise

				clockwise = TurnHelp.Angle(self.current_direction, self.target_direction).check()

				#ROTATION
				if(abs(self.current_direction - self.target_direction) >  math.radians(3)):
					move_cmd.angular.z = clockwise * math.pi / 25
					self.facing_correct_direction = False
				else:
					move_cmd.angular.z = 0
					self.facing_correct_direction = True

				#LINEAR MOVEMENT
				if (self.facing_correct_direction == True and self.not_at_target == True):
					move_cmd.linear.x = 1
				else:
					move_cmd.linear.x = 0

		def process_event(action_msg):
			#print('test')
			message = str(action_msg).split("data: ")[1]
			if ('Cook.cook_' in message):
				self.current_path = list(self.cook_path)
				self.target_coordinate = self.current_path.pop(0)
			# if (message == 'Cook.cook_lunch'):
			# 	self.current_path = self.door_to_kitchen + self.kitchen_to_door
			# 	self.target_coordinate = self.current_path.pop(0)
			# if (message == 'Cook.cook_dinner'):
			# 	self.current_path = self.door_to_kitchen + self.kitchen_to_door
			# 	self.target_coordinate = self.current_path.pop(0)

		rospy.Subscriber('/robot_2/base_pose_ground_truth', nav_msgs.msg.Odometry, process_position)
		rospy.Subscriber("scheduler", String, process_event)
		robot_0_movement_publisher = rospy.Publisher('/robot_2/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
		rate = rospy.Rate(40)

		
		move_cmd = geometry_msgs.msg.Twist()
		target = math.pi/2

		while not rospy.is_shutdown():
			robot_0_movement_publisher.publish(move_cmd)
			rate.sleep()

if __name__ == '__main__':
	rospy.init_node('cook_robot')
	navigate = Navigate()