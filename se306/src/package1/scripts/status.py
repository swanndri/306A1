#!/usr/bin/env python

import rospy
import roslib
import std_msgs.msg

roslib.load_manifest('package1')

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(10)


def callback(msg):
	print msg.data + "/100"




sub = rospy.Subscriber("human", std_msgs.msg.String, callback)

while not rospy.is_shutdown():
	rate.sleep()






