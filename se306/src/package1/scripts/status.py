#!/usr/bin/env python


import roslib; roslib.load_manifest('package1')
import std_msgs.msg
import rospy

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(10)


def callback(msg):
	if int(msg.data) <= 0:
		print "0/100"
	else:
		print msg.data + "/100"




sub = rospy.Subscriber("human", std_msgs.msg.String, callback)

while not rospy.is_shutdown():
	rate.sleep()






