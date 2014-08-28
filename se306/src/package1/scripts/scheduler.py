#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs
import std_msgs.msg

class Scheduler(object):

	SCHEDULED_TASKS = {
		8: 'Resident.wakeup',
		23: 'Visitor.visit',
		30: 'Cook.cook_breakfast',
		45: 'Resident.eat_breakfast',
		55: 'Resident.take_meds',
		70: 'Cook.cook_lunch',
		85: 'Resident.eat_lunch',
		100: 'Resident.idle',
		120: 'Visitor.visit',
		150: 'Cook.cook_dinner',
		170: 'Resident.eat_dinner',
		200: 'Resident.sleep'
	}

	def __init__(self):
		self.simulation_time = 0
		self.publisher = rospy.Publisher('scheduler', std_msgs.msg.String, queue_size=10)

		rospy.Subscriber('/clock', rosgraph_msgs.msg.Clock, self._clock_tick_event)

	def _clock_tick_event(self, time):
		if not time.clock.nsecs:
			print "Simulation time: %d" % self.simulation_time
			self.simulation_time = time.clock.secs % 420
			if self.simulation_time in Scheduler.SCHEDULED_TASKS:
				self.publisher.publish(Scheduler.SCHEDULED_TASKS[self.simulation_time])
				print "EVENT: %s" % Scheduler.SCHEDULED_TASKS[self.simulation_time]

if __name__ == '__main__':
	roslib.load_manifest('package1')
	rospy.init_node('scheduler')

	scheduler = Scheduler()

	rospy.spin()
