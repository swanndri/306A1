#!/usr/bin/env python


import roslib
import rospy
import rosgraph_msgs
import std_msgs.msg
import navigation
import constants
import os

from std_msgs.msg import String

class Resident(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):

		task = action_msg.data		
		print task
		if ("Resident.eat" in task):
			self.task_list.append(task)
			self.fullness[0] += 30
			if (self.fullness[0] > 100):
				self.fullness[0] = 100
		elif ("Resident" in task):
			self.task_list.append(task)
		# print("Message", message)
		# print("Fullness", self.fullness)


	def perform_task(self, task):
		self.status = "active"

		if (task == 'Resident.wakeup'):
			self.navigate.current_path = list(self.bedroom_to_living_room)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

		if (task == 'Resident.eat_breakfast'):
			self.navigate.current_path = list(self.living_room_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

		if (task == 'Resident.take_meds'):
			self.navigate.current_path = list(self.kitchen_to_cupboard)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.eat_lunch'):
			self.navigate.current_path = list(self.cupboard_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.eat_dinner'):
			self.navigate.current_path = list(self.living_room_to_kitchen)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.sleep'):
			self.navigate.current_path = list(self.kitchen_to_bedroom)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)
		
		if (task == 'Resident.idle'):
			self.navigate.current_path = list(self.kitchen_to_sofa)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)


	def __init__(self):
		self.fullness = [100, 1]
		self.health = 100
		self.entertainment = 100
		self.sanity = 100
		self.fitness = 100
		self.hydration = 100
		self.hygiene = 100
		self.relief = 100

		self.rate = rospy.Rate(constants.RosConstants.robot_rate)
		self.task_list = []
		self.status = "idle"

		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up. 
		#Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_1")		
		rospy.Subscriber("scheduler", String, self.process_event)
		sub = rospy.Subscriber("clock", rosgraph_msgs.msg.Clock, self.callback)
		self.pub = rospy.Publisher('human', std_msgs.msg.String, queue_size=10)


		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)
			# print statement for debugging path
			#print (self.task_list, self.status, self.navigate.target_coordinate)
			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"


			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))

			self.rate.sleep()	



	def callback(self, msg):
		# Old hunger rate
		# if ((int(msg.clock.secs) % 42 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0))
		
		#hunger/fullness
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.fullness[0] > 0:
				self.fullness[0] -= self.fullness[1]
				self.pub.publish("Fullness: " + str(self.fullness[0]))
		
		#health		
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.health > 0:
				self.health -= 1
				self.pub.publish("Health: " + str(self.health))
				
		#entertainment	
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):		
			if self.entertainment > 0:
				self.entertainment -= 1
				self.pub.publish("Entertainment: " + str(self.entertainment))
				
		#sanity
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.sanity > 0:
				self.sanity -= 1
				self.pub.publish("Sanity: " + str(self.sanity))
				
		#fitness
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.fitness > 0:
				self.fitness -= 1
				self.pub.publish("Fitness: " + str(self.fitness))
				
		#hydration
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.hydration > 0:
				self.hydration -= 1
				self.pub.publish("Hydration: " + str(self.hydration))
				
		#hygiene
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.hygiene > 0:
				self.hygiene -= 1
				self.pub.publish("Hygiene: " + str(self.hygiene))

		#Relief
		if ((int(msg.clock.secs) % 4 == 0) and (not int(msg.clock.secs) == 0) and ((int(msg.clock.nsecs)) == 0)):
			if self.relief > 0:
				self.relief -= 1
				self.pub.publish("Relief: " + str(self.relief))


				
if __name__ == '__main__':
	rospy.init_node('resident_robot')
	resident = Resident()
