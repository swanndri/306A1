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

from std_msgs.msg import String
from tf.transformations import euler_from_quaternion

#Rotates robot in direction of current target.

north 	= 0.0
south 	= math.pi
west 	= math.pi / 2.0
east 	= -math.pi / 2.0

target_coordinates = [6,0]
target_direction = west

facing_correct_direction = False
at_target = False

current_coordinates = [0,0]
current_direction	= north

def process_position(position_data):
	current_coordinates[0] = position_data.pose.pose.position.x
	current_coordinates[0] = position_data.pose.pose.position.y
	
	quaternion = position_data.pose.pose.orientation
	quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
	current_direction = euler_from_quaternion(quaternionlist)[2]
	
	if(abs(current_direction - target_direction) >  math.radians(2)):
		move_cmd.angular.z = -2 * math.pi / 25
	else:
		move_cmd.angular.z = 0
		facing_correct_direction = True

def process_linear_velocity(velocity_data):
	pass


rospy.init_node('navigater_robot_0')
robot_0_movement_publisher = rospy.Publisher('/robot_1/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
rate = rospy.Rate(10)

rospy.Subscriber('/robot_1/base_pose_ground_truth', nav_msgs.msg.Odometry, process_position)

move_cmd = geometry_msgs.msg.Twist()
target = math.pi/2

while not rospy.is_shutdown():
	robot_0_movement_publisher.publish(move_cmd)
	rate.sleep()