#!/usr/bin/python

import rospy
import node

class Relative(node.Robot):
	''' 
	Class for Relative robot.
	Inherits from Human class.
	This and all other robot/human classes are similar as they all work
	through inheritance

	Relative is a relative human, this along with the Visitor class
	are the relatives/family of the resident. They show that they are
	the family by always turning up to visit together
	'''	

	def __init__(self, name):
		super(Relative, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith("Visitor.visit"):
			self.jobs.append(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_8')
	relative = Relative('robot_8')