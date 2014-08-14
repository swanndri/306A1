#!/usr/bin/env python


# Every python controller needs these lines
import roslib; roslib.load_manifest('package1')
import rospy

# The velocity command message
import geometry_msgs.msg
# The laser scan message
import sensor_msgs.msg

import nav_msgs.msg

# We use a hyperbolic tangent as a transfer function
import math

import random


class Stopper:
	def __init__(self, distance, max_speed=1, min_speed=0.01):
		# How close should we get to things, and what's our maximum speed?
		self.distance = distance
		self.max_speed = max_speed
		self.min_speed = min_speed
		self.xTarget = None
		self.yTarget = None
		self.xPos = None
		self.yPos = None
		self.turnCount = 10
		self.turn_count_2 = 10
		self.has_rotated = False
		self.atXTarget = False
		self.atYTarget = False

		def cmd_vel_received(msg):
			self.xTarget = msg.pose.pose.position.x
			self.yTarget = msg.pose.pose.position.y

		def cmd_vel_received2(msg):
			self.xPos = msg.pose.pose.position.x
			self.yPos = msg.pose.pose.position.y

			command = geometry_msgs.msg.Twist()

			#print ("Theta equals",msg.pose.pose.orientation.w)

			if self.xTarget is not None and self.yTarget is not None:
				# Buffer is 0.5 so that when a robot goes straight to the destination it doesnt collide with it and detects it
				if abs(self.xPos-self.xTarget) > 0.5 :

					if self.xPos > self.xTarget:
						command.linear.x = -1
						command.linear.y = 0.0
						command.linear.z = 0.0
						command.angular.x = 0.0
						command.angular.y = 0.0
						command.angular.z = 0.0
					elif self.xPos < self.xTarget:
						command.linear.x = 1
						command.linear.y = 0.0
						command.linear.z = 0.0
						command.angular.x = 0.0
						command.angular.y = 0.0
						command.angular.z = 0.0
				# Buffer is 0.5 so that when a robot goes straight to the destination it doesnt collide with it
				elif abs(self.xPos-self.xTarget) < 0.5 :

					command.linear.x = 0
					command.linear.y = 0.0
					command.linear.z = 0.0
					command.angular.x = 0.0
					command.angular.y = 0.0
					command.angular.z = 0.0
					self.atXTarget = True


				
				if self.atXTarget == True:
					if abs(self.yPos-self.yTarget) > 0.5 :

						if self.yPos > self.yTarget:
							command.linear.x = 0.0
							command.linear.y = 1
							command.linear.z = 0.0
							command.angular.x = 0.0
							command.angular.y = 0.0
							command.angular.z = 0.0

							if self.turnCount > 0:
								command.angular.z = math.pi/2
								self.turnCount -= 1
								self.has_rotated = True
							else:
								command.linear.x = -1


					elif self.yPos < self.yTarget:
						command.linear.x = 0
						command.linear.y = -1
						command.linear.z = 0.0
						command.angular.x = 0.0
						command.angular.y = 0.0
						command.angular.z = 0.0

						if self.turnCount > 0:
							command.angular.z = math.pi/2
							self.turnCount -= 1
							self.has_rotated = True
						else:
							command.linear.x = 1

					elif abs(self.yPos-self.yTarget) < 1:

						command.linear.x = 0
						command.linear.y = 0.0
						command.linear.z = 0.0
						command.angular.x = 0.0
						command.angular.y = 0.0
						command.angular.z = 0.0
						self.atYTarget = True

				# If robot is not at the target, it will need to robot back to its original orientation at some point
				if self.atXTarget == False and self.atYTarget == False:
					self.turn_count_2 = 10
				# Else if at the target, robot needs to be able to turn again if it gets a new target
				elif self.atXTarget == True and self.atYTarget == True:
					print "REACHED TARGET"
					#No idea what w is yet, something to do with it's rotation
					print ("Theta equals",msg.pose.pose.orientation.w)
					# Rotate robot back into original orientation
					if self.has_rotated:
						if self.turn_count_2 > 0:
							command.angular.z = -math.pi/2
							self.turn_count_2 -= 1
							#Let the robot be able to make another turn again
							self.turnCount = 10

					# If at the target, self.atXTarget and self.atYTarget will be set to True again in the code before this
					# so it won't cause problems. But if it gains a new target then this allows it to go towards that now instead
					self.atXTarget = False
					self.atYTarget = False

				#print(command)
				self.pub.publish(command)


		# Subscriber for the laser data
		#self.sub = rospy.Subscriber('/robot_2/base_scan', sensor_msgs.msg.LaserScan, self.laser_callback)
		self.sub2 = rospy.Subscriber('/robot_0/base_pose_ground_truth', nav_msgs.msg.Odometry, cmd_vel_received)
		self.sub3 = rospy.Subscriber('/robot_2/base_pose_ground_truth', nav_msgs.msg.Odometry, cmd_vel_received2)

		# Publisher for movement commands
		self.pub = rospy.Publisher('/robot_2/cmd_vel', geometry_msgs.msg.Twist)

		# Let the world know we're ready
		rospy.loginfo('Stopper initialized')

	
	

	def laser_callback(self, scan):
		# What's the closest laser reading
		closest = min(scan.ranges)
		
		# This is the command we send to the robot
		command = geometry_msgs.msg.Twist()

		# If we're much more than 50cm away from things, then we want
		# to be going as fast as we can.  Otherwise, we want to slow
		# down.  A hyperbolic tangent transfer function will do this
		# nicely
		
		command.linear.x = math.tanh(5 * (closest - self.distance)) * self.max_speed
		command.linear.y = 0.0
		command.linear.z = 0.0
		command.angular.x = 0.0
		command.angular.y = 0.0


		"""
		if command.linear.x < 0.9:
			if self.turn_direction:
				if self.turn_direction > 0.50:
					command.angular.z = random.randint(0, 6)
				else:
					command.angular.z = random.randint(-6, 0)
			else:
				self.turn_direction = random.random()
		else:
			self.turn_direction = None
		"""

		if closest < self.distance:
			command.linear.x = 0

		rospy.logdebug('Distance: {0}, speed: {1}'.format(closest, command.linear.x))

		# Send the command to the motors
		self.pub.publish(command)


if __name__ == '__main__':
	rospy.init_node('stopper')

	# Get the distance from the parameter server.  Default is 0.5
	distance = rospy.get_param('distance', 0.5)


	# Set up the controller
	stopper = Stopper(distance)

	# Hand control over to ROS
	rospy.spin()
