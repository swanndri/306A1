#!/usr/bin/python

import rospy
import node
import database


class Resident(node.Human):
	''' 
	Resident class for resident robot.
	Inherits from Human class.
	This and all other robot/human classes are similar as they all work
	through inheritance
	'''
	
	def __init__(self, name):
		super(Resident, self).__init__(name)


	''' 
	If the message published by the scheduler corresponds to this class
	add it to it's jobs list and perform the appropriate action
	'''
	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.append(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_1')
	resident = Resident('robot_1')
