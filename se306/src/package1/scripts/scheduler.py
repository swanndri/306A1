#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs
import std_msgs.msg
import database

class Scheduler(object):
	"""
	The scheduler handles event scheduling for all the events that take place in the simulation for each robot.
	There a set of preset tasks that occur each day.
	"""
	def __init__(self):
		self.simulation_time = 0
		self.publisher = rospy.Publisher('scheduler', std_msgs.msg.String, queue_size=10)

		rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock, self._clock_tick_event)
		rospy.Subscriber('human_status', std_msgs.msg.String, self._human_status_event)

	def _clock_tick_event(self, time):
		if not time.clock.nsecs:
			print "Simulation time: %d" % self.simulation_time
			self.simulation_time = time.clock.secs % 420
			if self.simulation_time in database.Database.SCHEDULED_TASKS:
				# (0, 'Resident.wake_up', 100, 'sofa')
				event_name = database.Database.SCHEDULED_TASKS[self.simulation_time]
				event_priority = database.Database.EVENTS[event_name]['priority']
				event_duration = database.Database.EVENTS[event_name]['duration']
				event_destination = database.Database.EVENTS[event_name]['destination']
				
				self.publisher.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))
				print "EVENT: %s" % database.Database.SCHEDULED_TASKS[self.simulation_time]
			#Should add in here for random events happening
			else:
				pass
	def _human_status_event(self, event):
		event_name = database.Database.STATUS_TASKS[event.data]
		event_priority = database.Database.EVENTS[event_name]['priority']
		event_duration = database.Database.EVENTS[event_name]['duration']
		event_destination = database.Database.EVENTS[event_name]['destination']

		self.publisher.publish("%d %s %d %s" % (event_priority, event_name, event_duration, event_destination))


if __name__ == '__main__':
	roslib.load_manifest('package1')
	rospy.init_node('scheduler')

	scheduler = Scheduler()

	rospy.spin()
