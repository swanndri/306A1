#!/usr/bin/env python

import roslib
import rospy

def shutdown():
	print "Shutting down scheduler.py."

roslib.load_manifest('package1')
rospy.init_node('scheduler')
rospy.on_shutdown(shutdown)

