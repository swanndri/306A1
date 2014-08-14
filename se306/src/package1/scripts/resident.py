#!/usr/bin/env python


import roslib
import rospy
import rosgraph_msgs

from std_msgs.msg import String

def process_event(action_msg):
	#print('test')
	message = str(action_msg).split("data: ")[1]
	print(message)
    
def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scheduler", String, process_event)

    rospy.spin()

if __name__ == '__main__':
    listener()