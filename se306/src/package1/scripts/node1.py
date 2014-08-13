#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import std_msgs.msg
import nav_msgs.msg
import sensor_msgs.msg
import math
import time

def shutdown():
	print "Shutting down node1.py."

roslib.load_manifest('package1')

rospy.init_node('node1', anonymous=False)
rospy.on_shutdown(shutdown)
rate = rospy.Rate(10)

linear_speed = rospy.get_param("~linear_speed", 50.0)

cmd_vel = rospy.Publisher('/robot_0/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)

buffer = []

def base_pose_ground_truth_received(msg):
	print("Got bgpt message at %s" % time.time())
	buffer.append(('bpgt', msg))

def cmd_vel_received(msg):
	print("Got cv message at %s" % time.time())
	buffer.append(('cv', msg))

rospy.Subscriber('/robot_0/base_pose_ground_truth', nav_msgs.msg.Odometry, base_pose_ground_truth_received)
#rospy.Subscriber('/robot_0/cmd_vel', geometry_msgs.msg.Twist, cmd_vel_received)
#rospy.Subscriber('/robot_0/base_scan',sensor_msgs.msg.LaserScan, bla)

while not rospy.is_shutdown():
	try:
		if len(buffer) > 0:
			print("We have %s messages to process." % len(buffer))
			while buffer:
				(message_type, message) = buffer.pop(0)
				#print("Popped %s message (%d more in the queue)" % (message_type, len(buffer)))
				
				if message_type == 'bpgt':
					# check if the robot is stuck
					if message.twist.twist.linear.x == 0:
						linear_speed *= -1
				elif message_type == 'cv':
					pass
				
				move_cmd = geometry_msgs.msg.Twist()
				move_cmd.linear.x = linear_speed
				cmd_vel.publish(move_cmd)
		
		rate.sleep()
	except rospy.exceptions.ROSInterruptException:
		print "Quitting."
		break
