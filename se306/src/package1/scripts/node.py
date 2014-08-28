import rospy
import roslib
import rosgraph_msgs
import std_msgs.msg
import navigation
import Queue
import random

class Node(object):

	IDLE = 0
	RESPONDING = 1
	BUSY = 2

	def __init__(self, name):
		self.name = name
		self.status = Node.IDLE
		self.navigator = navigation.Navigator(name)
		self.jobs = Queue.PriorityQueue()
		self.current_job = None
		self.publisher = rospy.Publisher(name, std_msgs.msg.String, queue_size=10)
		self.rate = rospy.Rate(10)

		rospy.Subscriber('clock', rosgraph_msgs.msg.Clock, self._clock_tick_callback)
		rospy.Subscriber('scheduler', std_msgs.msg.String, self._scheduler_event_callback)

		self._loop()

	def _get_status(self):
		pass

	def _assign_job(self, job):
		self.current_job = job
		
		# request the node to move to new target coordinates
		self.navigator.navigate()

	def _assign_next_job_if_available(self):
		try:
			self._process_job(self.jobs.get_nowait())
		except Queue.Empty:
			self.current_job = None
			self.status = Node.IDLE

	def _loop(self):

		while not rospy.is_shutdown():

			self.rate.sleep()

			curr_job_priority, curr_job_description, curr_job_time = self.current_job if self.current_job else (None, None, None)

			# get next job without altering the queue to check if there is a job requiring immediate attention
			next_job_priority, next_job_description, next_job_time = self.jobs.queue[0] if self.jobs.qsize() else (None, None, None)

			# if there is a job we are attending to
			if self.current_job:

				# if the priority is 0, we need to stop everything and attend to it
				# if the priority is lower (1+) then that job will be processed only once the first completes
				if next_job_priority == 0 and next_job_priority < curr_job_priority:
					# stop everything, this is an emergency
					self._assign_next_job()
					continue

				# check if the current position of the node matches the location where the job should take place at
				if self.navigator.arrived(self.current_job):
					# if the job has not yet completed
					if curr_job_time > 0:
						# reassign the job with less time to finish it, so to eventually complete
						self.current_job = (curr_job_priority, curr_job_description, curr_job_time-1)
						self.status = Node.BUSY
						continue
					else:
						# out of time, job effectively completed
						# if there is another job in the queue, process it now
						self._assign_next_job_if_available()
						continue
				
				self.status = Node.RESPONDING
				continue

			self._assign_next_job_if_available()
			continue

	def _clock_tick_callback(self, msg):
		pass

	def _scheduler_event_callback(self, msg):
		pass

class Robot(Node):

	def __init__(self, name):
		super(self.__class__.__bases__[0], self).__init__(name)

class Human(Node):

	def __init__(self, name):
		super(self.__class__.__bases__[0], self).__init__(name)
		self.levels = {
			'fullness': 100,
			'health': 100,
			'entertainment': 100,
			'sanity': 100,
			'fitness': 100,
			'hydration': 100,
			'hygene': 100
		}

	def _clock_tick_callback(self, msg):
		# if this isn't the very first clock tick
		if int(msg.clock.secs) > 0:
			# if the clock tick is divisible evenly by 4
			if int(msg.clock.secs) % 4 == 0:
				# on a 50% chance
				if random.random() > 0.5:
					# reduce attribute levels by one unit
					self.levels['fullness'] -= 1
					self.levels['health'] -= 1
					self.levels['entertainment'] -= 1
					self.levels['sanity'] -= 1
					self.levels['fitness'] -= 1
					self.levels['hydration'] -= 1
					self.levels['hygene'] -= 1

		# loop through all attributes
		for attribute, value in self.levels.iteritems():
			# publish them
			self.publisher.publish("%s: %d" % (attribute, value))