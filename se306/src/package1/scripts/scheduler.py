#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs

from std_msgs.msg import String

#time_publisher = rospy.Publisher('/clock', rosgraph_msgs.msg.Clock, queue_size=100)

simulation_time = 0
pub = rospy.Publisher('scheduler', String, queue_size=10)

scheduled_tasks = { 100: 'Resident.wakeup', 
				 	900: 'Resident.eat_breakfast',
				 	1100: 'Resident.take_meds',
				 	1850: 'Resident.eat_lunch',
				 	2210: 'Resident.idle',
				 	3000:'Resident.eat_dinner',
				 	3750:'Resident.sleep',

				 	600: 'Cook.cook_breakfast',
					1570:'Cook.cook_lunch',
					2650:'Cook.cook_dinner',	

					300: 'Visitor.visit',
					2450: 'Visitor.visit'}

def publish(actionmsg):        
        pub.publish(actionmsg)
        print(actionmsg)


def schedule_events(time):
	#1440 because there are 1440 minutes in a day therefore 1 minute simulation = 1 second real time
	#0 = 12:00am (midnight). 
	#480 = 8:00am
	simulation_time  = time.clock.secs % 4320
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



#jak gittest