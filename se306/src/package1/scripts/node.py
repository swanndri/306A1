import rospy
import roslib
import rosgraph_msgs
import std_msgs.msg
import navigation
import Queue
import random
import database

class Node(object):

	IDLE = 0
	RESPONDING = 1
	BUSY = 2

	def __init__(self, name):
		self.name = name
		self.status = Node.IDLE
		self.navigator = navigation.Navigation(name)
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
		print "Assigning job %s" % str(job)

		# request the node to move to new target coordinates
		self.navigator.move(job[3])

	def _assign_next_job_if_available(self):
		try:
			self._assign_job(self.jobs.get_nowait())
		except Queue.Empty:
			self.current_job = None
			self.status = Node.IDLE

	def _loop(self):

		while not rospy.is_shutdown():

			self.rate.sleep()

			curr_job_priority, curr_job_description, curr_job_time, curr_job_destination = self.current_job if self.current_job else (None, None, None, None)

			try:
				# get next job without altering the queue to check if there is a job requiring immediate attention
				next_job_priority, next_job_description, next_job_time, next_job_destination = self.jobs.queue[0] if self.jobs.qsize() else (None, None, None, None)
			except ValueError:
				raise Exception("Bogus job: %s" % self.jobs.queue[0])

			# if there is a job we are attending to
			if self.current_job:

				# if the priority is 0, we need to stop everything and attend to it
				# if the priority is lower (1+) then that job will be processed only once the first completes
				if next_job_priority == 0 and next_job_priority < curr_job_priority:
					# stop everything, this is an emergency
					self._assign_next_job()
					continue

				# check if the current position of the node matches the location where the job should take place at
				self.navigator.movement_publisher.publish(self.navigator.move_cmd)
				if self.navigator.has_arrived():
					print self.current_job
					# if the job has not yet completed
					if curr_job_time > 0:
						# reassign the job with less time to finish it, so to eventually complete
						self.current_job = (curr_job_priority, curr_job_description, int(curr_job_time)-1, curr_job_destination)
						if 'eat' in curr_job_description:
							self.levels['Fullness'][1] = -2
						self.status = Node.BUSY
						continue
					else:
						# out of time, job effectively completed
						# if there is another job in the queue, process it now

						if self.type == "Robot":
							# return the robot to its idle position
							self.jobs.put((0, 'robot.returning', 0, self.idle_position))
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
		self.type = "Robot"
		self.idle_position = database.Database.ROBOT_IDLES.get(name)
		super(Robot, self).__init__(name)
# #!/usr/bin/python

# import rospy
# import node
# import database

# class Resident(node.Human):
	
# 	def __init__(self, name):
# 		super(Resident, self).__init__(name)

# 	def _scheduler_event_callback(self, msg):
# 		if msg.data.split()[1].startswith(self.__class__.__name__):
# 			self.jobs.put(tuple(msg.data.split()))

# if __name__ == '__main__':
# 	rospy.init_node('robot_1')
# 	resident = Resident('robot_1')
class Human(Node):
	levels = {}

	def __init__(self, name):

		for level in database.Database.LEVELS:
			self.levels[level] = [100, 0.5]		#status = (value,rate)
			if level == 'Sanity' or level == 'Health':
				self.levels[level][1] = 0.1
			elif level == 'Fullness':
				self.levels[level][1] = 1

			print self.levels[level]

		self.type = "Human"
		self.human_pub = rospy.Publisher("human", std_msgs.msg.String, queue_size=10)
		super(Human, self).__init__(name)

	def _clock_tick_callback(self, msg):
		# if this isn't the very first clock tick
		if int(msg.clock.secs) > 0:
			# if the clock tick is divisible evenly by 4
			if ((int(msg.clock.secs) % 3 == 0) and (int(msg.clock.nsecs)==0)):
				# reduce attribute levels by one unit

				self.levels['Fullness'][0] -= self.levels['Fullness'][1]
				self.levels['Health'][0] -= self.levels['Health'][1]
				self.levels['Entertainment'][0] -= self.levels['Entertainment'][1]
				self.levels['Sanity'][0] -= self.levels['Sanity'][1]
				self.levels['Fitness'][0] -= self.levels['Fitness'][1]
				self.levels['Hydration'][0] -= self.levels['Hydration'][1]
				self.levels['Hygiene'][0] -= self.levels['Hygiene'][1]
				self.levels['Relief'][0] -= self.levels['Relief'][1]

				for levels in self.levels:
					if (self.levels[levels][0] > 100):
						self.levels[levels][0] = 100
					if (self.levels[levels][0] <= 0):
						self.levels[levels][0] = 0



		# loop through all attributes
		for attribute, value in self.levels.iteritems():
			# publish them
			self.human_pub.publish("%s: %d" % (attribute, value[0]))
			print attribute, value[0]
