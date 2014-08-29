#!/usr/bin/python

import rospy
import node
import database


class Doctor(node.Robot):
	''' 
	Class for Doctor robot.
	Inherits from Human class.
	This and all other robot/human classes are similar as they all work
	through inheritance
	'''	

	def __init__(self, name):
		super(Doctor, self).__init__(name)
		self.target_of_interest = [None, None]		
		self.target_set = False	
		self.target = None

		#subcribing to the location channel which returns the requested co-ordinate
		rospy.Subscriber("location", String, self.receive_location)
		#setting up channel for location requests
		self.pub = rospy.Publisher("location_request", String, queue_size=10)


	# callback method for when the requested co-ordinate comes back as a message
	# sets the target of interest fields with the appropriate co-ords returned from message
	def receive_location(self, msg):
		msg = str(msg).split("data: ")[1]
		if "resident" in msg:
			message = str(msg).split(" ")
			self.target_of_interest[0] = float(message[1])
			self.target_of_interest[1] = float(message[2])
			self.target_set = True
			# print(self.target_of_interest)
			# method for requesting location with the target passed and as string argument.
			# returns a list with the target co-ordinates


	def get_target_location(self, target):
		self.pub.publish("Requesting " + target +" co-ordinate")
		co_ord = []
		while (True):
			if(self.target_set == True):
				co_ord=[self.target_of_interest[0], self.target_of_interest[1]]
				break
			self.target_set = False
			return co_ord

	def _assign_job(self, job):
		self.current_job = job
		print "Assigning job %s" % str(job)

		# request the node to move to new target coordinates
		self.navigator.move(job[3])
		self.target = [self.target[0], self.target[1] - 0.5]
		self.navigator.current_path.append()

	def _loop(self):

		while not rospy.is_shutdown():

			self.rate.sleep()

			curr_job_priority, curr_job_description, curr_job_time, None = self.current_job if self.current_job else (None, None, None, None)			

			self.target = self.get_target_location("resident")
			pt = list(self.target)

			place = None
			for name, (p1, p2) in database.Database.OBJECTS.iteritems():
				if utils.Rectangle(p1, p2).contains(pt):
					place = name
			if(place == None):
				place = "visitor_idle"

			curr_job_destination = place		

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

						#dchanges the rate during events
						if 'eat' in curr_job_description:
							self.levels['Fullness'][1] = -2
						self.status = Node.BUSY
						continue
					else:
						# out of time, job effectively completed
						# if there is another job in the queue, process it now
						if 'eat' in curr_job_description:
								self.levels['Fullness'][1] = 1
								
						if self.type == "Robot":
							# return the robot to its idle position
							self.jobs.put((0, 'robot.returning', 0, self.idle_position))
						self._assign_next_job_if_available()
						continue
				
				self.status = Node.RESPONDING
				continue

			self._assign_next_job_if_available()
			continue


	def _scheduler_event_callback(self, msg):
		if msg.data.split()[1].startswith(self.__class__.__name__):
			self.jobs.append(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('robot_5')
	doctor = Doctor('robot_5')