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

def process_position(position_data):
	quaternion = position_data.pose.pose.orientation

	quaternionlist = [quaternion.x, quaternion.y, quaternion.z, quaternion.w]
	#print(euler_from_quaternion([0.793,0,-0.608,0]))
	yaw_angle_in_radians = euler_from_quaternion(quaternionlist)[2]

	if(abs(yaw_angle_in_radians - target) >  math.radians(2)):
		move_cmd.angular.z = - 2*math.pi / 25
	else:
		move_cmd.angular.z = 0

rospy.init_node('navigater_robot_0')

robot_0_movement_publisher = rospy.Publisher('/robot_1/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
rate = rospy.Rate(5)

rospy.Subscriber('/robot_1/base_pose_ground_truth', nav_msgs.msg.Odometry, process_position)

move_cmd = geometry_msgs.msg.Twist()
target = math.pi/2

while not rospy.is_shutdown():
	robot_0_movement_publisher.publish(move_cmd)
	rate.sleep()