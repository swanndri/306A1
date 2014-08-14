#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs


#time_publisher = rospy.Publisher('/clock', rosgraph_msgs.msg.Clock, queue_size=100)

def reset_time_to_zero(time):
	print(time.clock.secs % 300)
		#t=rospy.Time(0)
		#time_publisher.publish(t)


roslib.load_manifest('package1')
rospy.init_node('scheduler')


rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock, reset_time_to_zero)


rospy.spin()