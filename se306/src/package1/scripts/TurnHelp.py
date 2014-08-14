import math

class Angles:

	def check(angle_from, angle_to):
		diff = angle_from-angle_to
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

	def normalize(angle_norm):
		newAngle = int(angle_norm)
    		if newAngle < 0:
			newAngle += 360;
		return newAngle

	what = input("Enter Angle from: ")
	huh = input("Enter Angle to: ")
	#what = math.degrees(int(what))
	#huh = math.degrees(int(what))
	what = normalize(what)
	huh = normalize(huh)
	check(what, huh)




