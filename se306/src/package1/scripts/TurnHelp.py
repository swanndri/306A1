#!/usr/bin/env python
import math

class Angle:
	
	def __init__(self, current, target):
		#convert input rads to degrees
		current = math.degrees(current)
		target = math.degrees(target)
		self.angle_from = self.normalize(current)
		self.angle_to = self.normalize(target)
	
	# Check which direction is best to rotate (anti clockwise(-1) or clockwise(1))
	def check(self):
		move_angle = self.angle_to - self.angle_from
		
		if (((self.angle_from - self.angle_to) + 360) % 360) > 180:
			return 1
		else:
			return -1

		#if not move_angle:
		#	return 0
		
		#if move_angle > 180:
		#		move_angle = 360 - move_angle * -1
		
		#if move_angle > 0:
		#	return 1
		#else:
		#	return -1

	# Normalizes input angle
	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if new_angle < 0:
			new_angle += 360;
		return new_angle

	



# if __name__ == '__main__':
# 	# Get input from user
# 	angle = Angle(90,180)	
# 	# Check which direction is best to rotate
# 	print(angle.check())

# if __name__ == '__main__':
# 	# Get input from user
# 	angle = Angle()
# 	from_angle = input("Enter Angle from: ")
# 	to_angle = input("Enter Angle to: ")

# 	# Normalizes angles (makes positives)
# 	from_angle = angle.normalize(from_angle)
# 	to_angle = angle.normalize(to_angle)
	
# 	# Check which direction is best to rotate
# 	angle.check(from_angle, to_angle)
