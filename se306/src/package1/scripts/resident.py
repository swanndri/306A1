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
			priority,task_name,duration,destination = tuple(msg.data.split())

			appended = False

			if "status" in task_name:
				task_name = task_name[:-4]

			#For every job in the queue:
			for job in self.jobs:
				print "A job: %s" % str(job)
				#If the job name contains that same status_*** of the new job: Ie there is a status_eat of any value in the queue
				if(task_name in job[1]):
					print "The task name is in job %s == %s" % (task_name, job[1])
					#  If the job priorities are the same:
					if(int(priority) < int(job[0])):
						print "Priority is lower"
						#Delete the old job
						#Insert the new job
						appended = True
						self.jobs.remove(job)
						self.jobs.append((priority,task_name,duration,destination))
						break
				
			#Else they are different job types:
			if not appended:
				print "Appended is false, do not replace"
				#Do not replace
				self.jobs.append((priority,task_name,duration,destination))

if __name__ == '__main__':
	rospy.init_node('robot_1')
	resident = Resident('robot_1')
