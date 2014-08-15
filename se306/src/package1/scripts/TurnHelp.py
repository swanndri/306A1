#!/usr/bin/env python
import math

class Angle:

	# Check which direction is best to rotate (anti clockwise(1) or clockwise(-1))
	def check(self):
		diff = self.angle_from - self.angle_to
		if (self.angle_to >= 0) and (self.angle_to < 90): 
			if (self.angle_from >= 0) and (self.angle_from <= 90):
				if diff > 0:
					return -1
				else:
					return 1
			else:
				if diff > 0:
					return 1
				else:
					return -1
		else:
			if (self.angle_from >= 0) and (self.angle_from < 90):
				if (self.angle_to >= 180) and (self.angle_to <= 270):
					if diff < 0:
						return 1
					else:
						return -1
				else:
					if diff > 0:
						return -1
					else:
						return 1
			else:
				if diff <= 0:
					return 1
				else:
					return -1

	# Normalizes input angle
	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if new_angle < 0:
			new_angle += 360;
		return new_angle

	def __init__(self, current, target):
		#convert input rads to degrees
		current = math.degrees(current)
		target = math.degrees(target)
		self.angle_from = self.normalize(current)
		self.angle_to = self.normalize(target)



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
