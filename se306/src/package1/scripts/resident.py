#!/usr/bin/python

import rospy
import node
import database

class Resident(node.Human):
	
	def __init__(self, name):
		super(Resident, self).__init__(name)

	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			priority,task_name,duration,destination = tuple(msg.data.split())

			if "status" in new_job[1]:
				task_name = task_name[:-4]

			#For every job in the queue:
				#If the job name contains that same status_*** of the new job: Ie there is a status_eat of any value in the queue
					#  If the job priorities are the same:
						#Do nothing, we dont need to replace the job, as it is the same job/priority
					# Else if the priority is lower in the new job than in the original job (the one in the queue):
						#Delete the old job
						#Insert the new job
				#Else they are different job types:
					#Do not replace

			self.jobs.put()

if __name__ == '__main__':
	rospy.init_node('robot_1')
	resident = Resident('robot_1')