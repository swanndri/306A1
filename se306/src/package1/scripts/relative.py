#!/usr/bin/python

import rospy
import node

class Relative(node.Robot):
	
	def __init__(self, name):
		super(Relative, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith("Visitor.visit"):
			self.jobs.put(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_8')
	relative = Relative('robot_8')