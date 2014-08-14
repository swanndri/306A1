
class Angle:

	# Check which direction is best to rotate (anti clockwise or clockwise)
	def check(self, angle_from, angle_to):
		diff = angle_from - angle_to
		if (angle_to >= 0) and (angle_to < 90): 
			if (angle_from >= 0) and (angle_from <= 90):
				if diff > 0:
					print ("Anti-Clockwise")
				else:
					print ("Clockwise")
			else:
				if diff > 0:
					print ("Clockwise")
				else:
					print ("Anti-Clockwise")
		else:
			if (angle_from >= 0) and (angle_from < 90):
				if (angle_to >= 180) and (angle_to <= 270):
					if diff < 0:
						print ("Anti-Clockwise")
					else:
						print ("Clockwise")
				else:
					if diff > 0:
						print ("Anti-Clockwise")
					else:
						print ("Clockwise")
			else:
				if diff <= 0:
					print ("Clockwise")
				else:
					print ("Anti-Clockwise")

	# Normalizes input angle
	def normalize(self, input_angle):
		new_angle = int(input_angle)
    		if new_angle < 0:
			new_angle += 360;
		return new_angle

if __name__ == '__main__':
	# Get input from user
	angle = Angle()
	from_angle = input("Enter Angle from: ")
	to_angle = input("Enter Angle to: ")

	# Normalizes angles (makes positives)
	from_angle = angle.normalize(from_angle)
	to_angle = angle.normalize(to_angle)
	
	# Check which direction is best to rotate
	angle.check(from_angle, to_angle)




