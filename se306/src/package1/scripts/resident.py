#!/usr/bin/env python


import roslib
import rospy
import rosgraph_msgs

from std_msgs.msg import String

def process_event(data):
    print(data)
    
def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scheduler", String, process_event)

    rospy.spin()

if __name__ == '__main__':
    listener()