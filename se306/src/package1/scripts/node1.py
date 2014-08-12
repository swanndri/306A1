#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import std_msgs.msg
import nav_msgs.msg
import math
import tf

def shutdown():
	print "Shutting down node1.py."

roslib.load_manifest('package1')

rospy.init_node('node1', anonymous=False)
rospy.on_shutdown(shutdown)
rate = rospy.Rate(20)

# Set the parameters for the target square
goal_distance = rospy.get_param("~goal_distance", 1.0) # meters
goal_angle = rospy.get_param("~goal_angle", math.radians(90)) # degrees converted to radians
linear_speed = rospy.get_param("~linear_speed", 0.2) # meters per second
angular_speed = rospy.get_param("~angular_speed", 0.7) # radians per second
angular_tolerance = rospy.get_param("~angular_tolerance", math.radians(2)) # degrees to radians

cmd_vel = rospy.Publisher('/robot_0/cmd_vel', geometry_msgs.msg.Twist, queue_size=1000)

def bla(msg):
	print msg

my_bot = rospy.Subscriber('/robot_0/odom', nav_msgs.msg.Odometry, bla)

# The base frame is base_footprint for the TurtleBot but base_link for Pi Robot
#base_frame = rospy.get_param('~base_frame', '/base_link')

# The odom frame is usually just /odom
#odom_frame = rospy.get_param('~odom_frame', '/odom')

#listener = tf.TransformListener()

# Set the odom frame
#odom_frame = '/odom'

# Find out if the robot uses /base_link or /base_footprint
#try:
#		listener.waitForTransform(odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
#		base_frame = '/base_footprint'
#except (tf.Exception, tf.ConnectivityException, tf.LookupException):
#	try:
#		listener.waitForTransform(odom_frame, '/base_link', rospy.Time(), rospy.Duration(1.0))
#		base_frame = '/base_link'
#	except (tf.Exception, tf.ConnectivityException, tf.LookupException):
#		rospy.loginfo("Cannot find transform between /odom and /base_link or /base_footprint")
#		rospy.signal_shutdown("tf Exception")

while not rospy.is_shutdown():
	try:
		move_cmd = geometry_msgs.msg.Twist()
		move_cmd.linear.x = linear_speed
		cmd_vel.publish(move_cmd)
		rate.sleep()
	except rospy.exceptions.ROSInterruptException:
		print "Quitting."
		break
