#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs
import constants

from std_msgs.msg import String

#time_publisher = rospy.Publisher('/clock', rosgraph_msgs.msg.Clock, queue_size=100)

simulation_time = 0
pub = rospy.Publisher('scheduler', String, queue_size=10)

def publish(actionmsg):        
        pub.publish(actionmsg)
        print(actionmsg)


def schedule_events(time):
	#1440 because there are 1440 minutes in a day therefore 1 minute simulation = 1 second real time
	#0 = 12:00am (midnight). 
	#480 = 8:00am
	simulation_time  = time.clock.secs % 420
	actionmsg = None
	if ( time.clock.nsecs == 100000000 ):
		actionmsg = constants.Tasks.scheduled_tasks.get(simulation_time)
		print(simulation_time)
		
		if (actionmsg is not None):
			publish(actionmsg)
		
def schedule_status_event(event):
	#print  constants.Tasks.status_based_tasks[event.data]
	
	task = constants.Tasks.status_based_tasks[event.data]
	if (task is not None):
		publish(task)

	
roslib.load_manifest('package1')
rospy.init_node('scheduler')

rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock, schedule_events)
rospy.Subscriber('human_status', String, schedule_status_event)

rospy.spin()



#jak gittest