#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import std_msgs.msg
import nav_msgs.msg
import sensor_msgs.msg
import math
import time
import random

def shutdown():
	print "Shutting down node1.py."

roslib.load_manifest('package1')

rospy.init_node('node1', anonymous=False)
rospy.on_shutdown(shutdown)
rate = rospy.Rate(10)

rospy.set_param("~linear_speed_x", 1)
rospy.set_param("~linear_speed_y", 1)

debug_level = 1

cmd_vel = rospy.Publisher('/robot_0/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)

buffer = []

def base_pose_ground_truth_received(msg):
	if debug_level > 2:
		print("Got bgpgt message at %s" % time.time())
	buffer.append(('bpgt', msg))

def cmd_vel_received(msg):
	if debug_level > 2:
		print("Got cv message at %s" % time.time())
	buffer.append(('cv', msg))

rospy.Subscriber('/robot_0/base_pose_ground_truth', nav_msgs.msg.Odometry, base_pose_ground_truth_received)
#rospy.Subscriber('/robot_0/cmd_vel', geometry_msgs.msg.Twist, cmd_vel_received)
#rospy.Subscriber('/robot_0/base_scan',sensor_msgs.msg.LaserScan, bla)

while not rospy.is_shutdown():
	try:
		if len(buffer) > 0:
			if debug_level > 2:
				print("We have %s messages to process." % len(buffer))
			while buffer:
				(message_type, message) = buffer.pop(0)
				if debug_level > 2:
					print("Popped %s message (%d more in the queue)" % (message_type, len(buffer)))
				
				if message_type == 'bpgt':
					# check if the robot is stuck
					if message.twist.twist.linear.x == 0:
						if debug_level > 0:
								print("Robot hit an obstacle.")
						rospy.set_param('~linear_speed_x', rospy.get_param('~linear_speed_x') * -1)
						rospy.set_param('~angular_z', random.uniform(0, 2))
						rospy.set_param('~angular_iterations', random.randint(0, 6))
				elif message_type == 'cv':
					pass
				
				move_cmd = geometry_msgs.msg.Twist()
				move_cmd.linear.x = rospy.get_param('~linear_speed_x')
				move_cmd.linear.y = rospy.get_param('~linear_speed_y')
				
				if rospy.get_param('~angular_iterations') > 0:
					move_cmd.angular.z = rospy.get_param('~angular_z')
					rospy.set_param('~angular_iterations', rospy.get_param('~angular_iterations')-1)
				cmd_vel.publish(move_cmd)
		
		rate.sleep()
	except rospy.exceptions.ROSInterruptException:
		print "Quitting."
		break
