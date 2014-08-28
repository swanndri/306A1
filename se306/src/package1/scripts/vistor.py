#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
import navigation
import constants

from std_msgs.msg import String

class Visitor(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		if ("Visitor" in message):
			
			self.task_list.append(message)

			

	def perform_task(self, task):

		self.status = "active" 

		if task =="Visitor.visit":
			
			co_ord = self.get_target_location("resident")
			print(co_ord)
			self.navigate.current_path = list(self.door_to_living_room) + (list(self.door_to_living_room[::-1]))
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)

	
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


	def __init__(self):		
		self.rate = rospy.Rate(constants.RosConstants.robot_rate)
		self.task_list = []
		self.target_of_interest = [None, None]
		self.target_set = False
		self.status = "idle"
		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up. 
		#Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_0")		
		rospy.Subscriber("scheduler", String, self.process_event)

		#subcribing to the location channel which returns the requested co-ordinate
		rospy.Subscriber("location", String, self.receive_location)

		#setting up channel for location requests
		self.pub = rospy.Publisher("location_request", String, queue_size=10)

		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)

			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"


			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))

			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('visitor_robot')
	visit = Visitor()
	