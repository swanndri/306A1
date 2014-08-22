#!/usr/bin/env python

import roslib
import rospy
import std_msgs.msg
import navigation
import constants

from std_msgs.msg import String

class Cook(navigation.Navigation):

	''' When a message is passed out from the scheduler, determine whether it is
	relevant to this object. If so, take the neccessary action
	'''
	def process_event(self, action_msg):
		message = str(action_msg).split("data: ")[1]
		if ('Cook.cook_' in message):

			self.task_list.append(message)
			


	def perform_task(self, task):

		self.status = "active" 

		if ("Cook.cook_" in task):
			self.navigate.current_path = list(self.cook_path)
			self.navigate.target_coordinate = self.navigate.current_path.pop(0)


	# def laser_callback(self, scan):
	# 	# What's the closest laser reading
	# 	closest = min(scan.ranges)
		
	# 	# This is the command we send to the robot
	# 	command = geometry_msgs.msg.Twist()

	# 	# If we're much more than 50cm away from things, then we want
	# 	# to be going as fast as we can.  Otherwise, we want to slow
	# 	# down.  A hyperbolic tangent transfer function will do this
	# 	# nicely
		
	# 	command.linear.x = math.tanh(5 * (closest - self.distance)) * self.max_speed
	# 	command.linear.y = 0.0
	# 	command.linear.z = 0.0
	# 	command.angular.x = 0.0
	# 	command.angular.y = 0.0


	# 	"""
	# 	if command.linear.x < 0.9:
	# 		if self.turn_direction:
	# 			if self.turn_direction > 0.50:
	# 				command.angular.z = random.randint(0, 6)
	# 			else:
	# 				command.angular.z = random.randint(-6, 0)
	# 		else:
	# 			self.turn_direction = random.random()
	# 	else:
	# 		self.turn_direction = None
	# 	"""

	# 	if closest < self.distance:
	# 		command.linear.x = 0

	# 	rospy.logdebug('Distance: {0}, speed: {1}'.format(closest, command.linear.x))

	# 	# Send the command to the motors
	# 	self.pub.publish(command)

	def __init__(self):
		self.rate = rospy.Rate(constants.RosConstants.robot_rate)
		self.task_list = []
		self.status = "idle"
		# Create a navigation object which will be used to manage all the calls
		# relating to movement. Passed the robot's name so that the publisher 
		# and subscribers for it's navigation can be set up. 
		#Eventually we will make this input a variable instead of hardcoded
		self.navigate = navigation.Navigation("robot_2")
		rospy.Subscriber("scheduler", String, self.process_event)
		# rospy.Subscriber('/robot_2/base_scan', sensor_msgs.msg.LaserScan, self.laser_callback)


		while not rospy.is_shutdown():
			self.navigate.movement_publisher.publish(self.navigate.move_cmd)

			if (len(self.navigate.target_coordinate) == 0):
				self.status = "idle"


			if (len(self.task_list) > 0 and self.status == "idle"):
				self.perform_task(self.task_list.pop(0))

			self.rate.sleep()

if __name__ == '__main__':
	rospy.init_node('cook_robot')
	cook = Cook()
