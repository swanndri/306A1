#!/usr/bin/env python

import roslib
import rospy
import geometry_msgs.msg
import math

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

cmd_vel = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=1000)
