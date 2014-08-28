#!/usr/bin/python

import rospy
import node

class Cook(node.Robot):
	
	def __init__(self, name):
		super(self.__class__.__bases__[0], self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.startswith(self.__class__.__name__):
			self.jobs.put(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_0')
	cook = Cook('robot_0')