#!/usr/bin/env python

import roslib
import rospy
import tf


if __name__ == '__main__':
	roslib.load_manifest('robot_setup_tf')
	rospy.init_node('tf_broadcaster')
	rospy.spin()


