#!/usr/bin/env python

import rospy
from sensor_msgs.msg import String

class StatusPrinter:
	
	def __init__(self):
		self.activity = "Idle"
			
	def print_activity(self):
		print " [ Activity  : " + activity + " "*len(activity-10) + " ]"
		
	def display_status(self):
		print_activity()
		
	def data_received(self, data):
		self.activity = data
			
		self.display_status()
		
		
		
		
		
def callback(data):
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.data)
    
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
	rospy.init_node('status')
	
	rospy.Subscriber('', String, callback)
	
    listener()

