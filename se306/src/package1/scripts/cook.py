#!/usr/bin/python

import rospy
import node

class Cook(node.Robot):
	''' 
	Class for Cook robot.
	Inherits from Human class.
	This and all other robot/human classes are similar as they all work
	through inheritance
	'''	

	def __init__(self, name):
		super(Cook, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.append(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_2')
	cook = Cook('robot_2')
