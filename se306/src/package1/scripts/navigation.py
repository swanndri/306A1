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

from std_msgs.msg import String
from tf.transformations import euler_from_quaternion

class Navigate:
	def __init__(self):
		self.east = 0.0
		self.west = math.pi
		self.north = math.pi / 2.0
		self.south = -math.pi / 2.0

		self.cupboard 		=	[-11,12]
		self.bedroom 		=	[-11,6]
		self.bathroom		=	[-10,-11]
		self.hallway_top	=	[-4,6]
		self.hallway_mid	=	[-4,1]
		self.hallway_bot	=	[-4,-11]
		self.door			=	[-4,-14]
		self.kitchen		=	[6,11]
		self.living_room	=	[6,1]
		self.idle			=	[12,4]

		self.door_to_kitchen				=	[self.door, self.hallway_mid, self.living_room, self.kitchen]
		self.bedroom_to_living_room			=	[self.bedroom, self.hallway_top, self.hallway_mid, self.living_room, self.idle]
		self.living_room_to_kitchen			=	[self.living_room, self.kitchen]
		self.kitchen_to_bedroom				=	[self.kitchen, self.living_room, self.hallway_mid, self.hallway_top, self.bedroom]
		self.kitchen_to_cupboard			=	[self.kitchen, self.living_room, self.hallway_mid, self.hallway_top, self.bedroom, self.cupboard, self.bedroom]
		self.cupboard_to_kitchen			=	[self.bedroom, self.hallway_top, self.hallway_mid, self.living_room, self.kitchen]
		self.door_to_living_room			=	[self.door, self.hallway_mid, self.living_room]
		self.kitchen_to_idle				=	[self.kitchen, self.living_room, self.idle]
		
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
				clockwise = TurnHelp.Angle(self.current_direction, self.target_direction).check()
				print "TurnHelp.Angle == %d" % clockwise
				
				#ROTATION
				if(abs(self.current_direction - self.target_direction) >  math.radians(4)):
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

		rospy.Subscriber('/robot_1/base_pose_ground_truth', nav_msgs.msg.Odometry, process_position)
		robot_0_movement_publisher = rospy.Publisher('/robot_1/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
		rate = rospy.Rate(40)

		
		move_cmd = geometry_msgs.msg.Twist()
		target = math.pi/2

		while not rospy.is_shutdown():
			robot_0_movement_publisher.publish(move_cmd)
			rate.sleep()

	def move (self, room):
		self.current_path = list(self.door_to_living_room) + (list(self.door_to_living_room[::-1]))
		self.target_coordinate = self.current_path.pop(0)

if __name__ == '__main__':
	rospy.init_node('resident_prototype')
	navigate = Navigate()
	
