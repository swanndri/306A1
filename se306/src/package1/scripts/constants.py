import math

class Statuses(object):

	#Resident Statuses

	resident_statuses = {

						"Resident.wakeup":"Resident is currently waking up",
						"Resident.eat_breakfast":"Resident is walking to the kitchen to eat breakfast",
						"Resident.take_meds":"Resident is walking to the cupboard to get and take their medication",
						"Resident.eat_lunch":"Resident is walking to the kitchen to eat lunch",
						"Resident.eat_dinner":"Resident is walking to the kitchen to eat dinner",
						"Resident.sleep":"Resident is walking to the bedroom to go to sleep",
						"Resident.idle":"Resident is currently doing nothing",
						"Cook.cook_breakfast":"Cook robot is moving to the kitchen to cook breakfast",
						"Cook.cook_lunch":"Cook robot is moving to the kitchen to cook lunch",
						"Cook.cook_dinner":"Cook robot is moving to the kitchen to cook dinner",
						"Visitor.visit":"Visitor is visiting the residents house"
						
						}

	mid = {	

			"Fullness":"#Testm",
			"Health":"#Testm",
			"Entertainment":"#Testm",
			"Sanity":"#Testm",
			"Fitness":"#Testm",
			"Thirst":"#Testm",
			"Hygiene":"#Testm"

			}

	low = {	

			"Fullness":"#Testl",
			"Health":"#Testl",
			"Entertainment":"#Testl",
			"Sanity":"#Testl",
			"Fitness":"#Testl",
			"Thirst":"#Testl",
			"Hygiene":"#Testl"

			}


	dangerous = {	

				"Fullness":"#Testd",
				"Health":"#Testd",
				"Entertainment":"#Testd",
				"Sanity":"#Testd",
				"Fitness":"#Testd",
				"Thirst":"#Testd",
				"Hygiene":"#Testd"

				}



class Paths(object):

	""" The Paths calls of constants is used in the Navigation class.

	This class contains the invisible nodes we will use to make robots
	travel from room to room, aswell as paths that robots are likely to
	take e.g. door_to_kitchen.

	Directions have also been entered for north south east west as these
	are constants within our code
	"""

	# Orientation constants
	east = 0.0
	west = math.pi
	north = math.pi / 2.0
	south = -math.pi / 2.0

	# Invisible nodes/points within our house
	cupboard = [-3.6, 4.2]
	bedroom = [-3.6, 2.1]
	bathroom = [-3.6, -3.7]
	hallway_top = [-1.2, 1.9]
	hallway_mid = [-1.2, 0.45]
	hallway_bot = [-1.2, -3.7]
	door = [-1.2, -6]
	kitchen = [2.05, 3.5]
	kitchen_entrance = [2.05, 1.6]
	living_room_top_right = [4.5, 1.6]
	living_room_middle = [2.05, 0.45]
	cook_idle = [4.5, -1.85]
	idle = [12,4]

	living_room_entrance = [1, 0.45]
	living_room_sofa = [1, -3]

	# Furniture
	bed = [-2.3, -1.1]
	kitchen_stove = []
	sofa = [0.3, -3]
	gym = [-4.450, 2.850]
	sofa2 = [1.500, -4.250]
	toilet = [-4.350, -4.500]
	sink = [-3.300, -3.400]
	bathttub = [-4.350, -3.250]
	fridge = [0.500, 3.000]
	dishwasher = [3.750, 3.500]


	# Paths robots can take
	door_to_kitchen = [door, hallway_mid, living_room_middle, kitchen]
	bedroom_to_living_room = [bedroom, hallway_top, hallway_mid, living_room_entrance, living_room_sofa, sofa]
	living_room_to_kitchen = [living_room_middle, kitchen]
	kitchen_to_bedroom = [kitchen, living_room_middle, hallway_mid, hallway_top, bedroom, bed]
	kitchen_to_cupboard = [kitchen, living_room_middle, hallway_mid, hallway_top, bedroom, cupboard, bedroom]
	cupboard_to_kitchen = [bedroom, hallway_top, hallway_mid, living_room_middle, kitchen]
	door_to_living_room = [door, hallway_mid, living_room_middle]
	kitchen_to_sofa = [kitchen, living_room_middle, living_room_sofa, sofa]
	cook_path = [cook_idle, living_room_top_right, kitchen_entrance, kitchen, kitchen_entrance, living_room_top_right, cook_idle]


class RosConstants(object):
	""" ROS-specific constants, such as the rate at which the main loop will iterate. """

	robot_rate = 10

if __name__ == "__main__":
	print "This was not intended to be run directly." 