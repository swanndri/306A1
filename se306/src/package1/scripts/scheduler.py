#!/usr/bin/env python

import roslib
import rospy

def shutdown():
	print "Shutting down node1.py."

roslib.load_manifest('package1')
rospy.init_node('node1', anonymous=False)
rospy.on_shutdown(shutdown)
