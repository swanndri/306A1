#!/usr/bin/env python


import roslib
import rospy
import rosgraph_msgs

import std_msgs.msg

class Resident:
	
	def __init__(self):
		self.fullness = 100
		
	
	def pub_sub(self):
		sub = rospy.Subscriber("clock", std_msgs.msg.String, self.callback)
		rospy.Subscriber("scheduler", std_msgs.msg.String, self.process_event)
		self.pub = rospy.Publisher('human', std_msgs.msg.String, \
		queue_size=10)
		
	def callback(self, msg):
		
		#pulls the secs value from the Clock object
		if int(str(msg).split()[2]) % 42 == 0:
			if self.fullness > 0:
				self.fullness -= 1
				print ("fullness is:", self.fullness)
				self.pub.publish("Fullness: " + str(self.fullness))
			else:
				pass
		
	

	def process_event(self, action_msg):
		#print('test')
		message = str(action_msg).split("data: ")[1]
		if ("Resident.eat" in message):
			self.fullness += 30
		#self.pub.publish(message)	
		print(message)

if __name__ == '__main__':
	rospy.init_node('resident', anonymous=True)
	
	# Set up the controller
	resident = Resident()
	resident.pub_sub()

    # Hand control over to ROS
	rospy.spin()
