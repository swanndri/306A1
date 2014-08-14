#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs

from std_msgs.msg import String

#time_publisher = rospy.Publisher('/clock', rosgraph_msgs.msg.Clock, queue_size=100)

simulation_time = 0
pub = rospy.Publisher('scheduler', String, queue_size=10)

def publish(actionmsg):        
        pub.publish(actionmsg)

def wakeup():
	actionmsg = 'wakeup'
	publish(actionmsg)

def schedule_events(time):
	#1440 because there are 1440 minutes in a day therefore 1 minute simulation = 1 second real time
	#0 = 12:00am (midnight). 
	#480 = 8:00am

	simulation_time  = time.clock.secs % 1440
	if ( time.clock.nsecs == 100000000 ):
		print(simulation_time)
	if ( simulation_time == 480 and time.clock.nsecs == 100000000):
		wakeup()
		print('Sent wake up message')
		

roslib.load_manifest('package1')
rospy.init_node('scheduler')

rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock, schedule_events)
rospy.spin()