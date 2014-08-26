import math

class Angle(object):
	
	def __init__(self, current, target):
		""" Convert input rads to degrees """

		current = math.degrees(current)
		target = math.degrees(target)
		self.angle_from = self.normalize(current)
		self.angle_to = self.normalize(target)
	
	
	def check(self):
		""" Check which direction is best to rotate based on current heading. """

		# -1 is anti-clockwise
		#  1 is clockwise

		move_angle = self.angle_to - self.angle_from
		
		if (move_angle > 0):
			if (abs(move_angle) > 180):
				return -1
			else:
				return 1
		else:
			if (abs(move_angle) > 180):
				return 1
			else:
				return -1

	def normalize(self, input_angle):
		""" Normalise input angle """

		new_angle = int(input_angle)
		if new_angle < 0:
			new_angle += 360
			
		return new_angle

if __name__ == "__main__":
	print("This was not intended to be run directly.")