#!/usr/bin/python

import rospy
import node

class Friend(node.Robot):
	''' 
	Class for Relative robot.
	Inherits from Human class.
	This and all other robot/human classes are similar as they all work
	through inheritance

	Friend is a friend of the resident. This is shown by the fact that the
	Friend robot always turns up to visit alone
	'''	

	def __init__(self, name):
		super(Friend, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.append(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_9')
	relative = Relative('robot_9')