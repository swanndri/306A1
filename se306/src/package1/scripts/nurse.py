#!/usr/bin/python

import rospy
import node
import database

class Nurse(node.Robot):
	''' 
	Class for Nurse robot.
	Inherits from Human class.
	This and all other robot/human classes are similar as they all work
	through inheritance
	'''	

	def __init__(self, name):
		super(Nurse, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.append(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_3')
	nurse = Nurse('robot_3')