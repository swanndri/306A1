#!/usr/bin/python

import rospy
import node
import database

class Resident(node.Human):
	
	def __init__(self, name):
		super(Resident, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		print "this is pee pee %s" % msg
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.put(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_1')
	resident = Resident('robot_1')