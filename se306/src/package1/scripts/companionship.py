#!/usr/bin/python

import rospy
import node
import database

class Companionship(node.Robot):
	"""

	"""
	def __init__(self, name):
		super(Companionship, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.put(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_8')
	companionship = Companionship('robot_8')