#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs

from std_msgs.msg import String

#time_publisher = rospy.Publisher('/clock', rosgraph_msgs.msg.Clock, queue_size=100)

simulation_time = 0
pub = rospy.Publisher('scheduler', String, queue_size=10)

scheduled_tasks = { 480: 'Resident.wakeup', 
				 	540: 'Resident.eat_breakfast',
				 	660: 'Resident.take_meds',
				 	750: 'Resident.eat_lunch',
				 	1080:'Resident.eat_dinner',
				 	1320:'Resident.sleep',

				 	510: 'Cook.cook_breakfast',
					720: 'Cook.cook_lunch',
					1050:'Cook.cook_dinner'	}

def publish(actionmsg):        
        pub.publish(actionmsg)
        print(actionmsg)


def schedule_events(time):
	#1440 because there are 1440 minutes in a day therefore 1 minute simulation = 1 second real time
	#0 = 12:00am (midnight). 
	#480 = 8:00am
	simulation_time  = time.clock.secs % 1440
	actionmsg = None
	if ( time.clock.nsecs == 100000000 ):
		actionmsg = scheduled_tasks.get(simulation_time)
		print(simulation_time)
		
		if (actionmsg is not None):
			publish(actionmsg)
		

roslib.load_manifest('package1')
rospy.init_node('scheduler')

rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock, schedule_events)
rospy.spin()