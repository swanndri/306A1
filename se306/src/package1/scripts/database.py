import math
import collections

class Database(object):

	# how to judge orientation
	ORIENTATION = {
		'east': 0.0,
		'west': math.pi,
		'north': math.pi / 2.0,
		'south': -math.pi / 2.0
	}

	# single points defining the 'centre' of an object or room that nodes will travel to
	POINTS = {
		'cupboard': (-3.6, 4.0),
		'bedroom': (-3.6, 2.1),
		'bathroom': (-3.6, -3.7),
		'hallway_top': (-1.5, 1.9),
		'hallway_mid': (-1.5, 0.45),
		'hallway_bot': (-1.5, -3.7),
		'door': (-1.2, -6),
		'kitchen': (2.05, 3),
#			'kitchen_entrance': (2.05, 1.6),
#			'living_room_top_right': (4.5, 1.6),
		'living_room_middle': (2.05, 0.45),
		'living_room_entrance': (1.5, 0.45),
		'living_room_sofa': (1, -3),

		# robot starting positions
		'cook_idle': (0, 3),
		'medication_idle': (-4.2, 4.4),
		'entertainment_idle': (-2.2, -10),
		'companionship_idle': (-0.2, -10),

		# human starting positions
		'visitor_idle': (-1.2, -10),
		'nurse_idle': (0.8, -10),
		'doctor_idle': (1.8, -10),
		'caregiver_idle': (2.8, -10),

		'idle': (12, 4),

		'bed': (-2.8, -1.1),
		'kitchen_stove': (2.05, 3.5),
		'sofa': (0.3, -3),
		'gym': (-4.450, 2.850),
		'sofa2': (1.500, -4.250),
		'toilet': (-4.350, -4.500),
		'sink': (-3.300, -3.400),
		'bathtub': (-4.350, -3.250),
		'fridge': (0.500, 3.000),
		'dishwasher': (3.750, 3.500),
		'piano': (1, -1.1)
	}

	# objects (mostly rooms) defined by their top left and bottom right points
	OBJECTS = collections.OrderedDict([
		('cupboard', ((-5, 5), (-2.2, 3.6))),
		('bedroom', ((-5, 3.6), (-2.2, -5))),
		('bathroom', ((-5, -2.3), (-2.2, -5))),
		('hallway_mid', ((-1.7, 5), (-0.7, -5))),
		('kitchen', ((-0.7, 5), (5, 2.2))),
		('living_room_middle', ((-0.7, 2.2), (5, -5))),
		('house', ((-5, 5), (5, -5)))
	])

	# connected graph of points showing neighbours]

	GRAPH = {
		# Invisible nodes/points within our house
		'cupboard': ['bedroom','medication_idle'],
		'bedroom': ['bed','cupboard','gym','hallway_top','companionship_idle'],
		'bathroom': ['bathtub','hallway_bot','sink','toilet'],
		'hallway_top': ['bedroom','hallway_mid'],
		'hallway_mid': ['hallway_bot','hallway_top','living_room_entrance'],
		'hallway_bot': ['bathroom','door','hallway_mid'],
		'door': ['hallway_bot','visitor_idle','caregiver_idle','nurse_idle','doctor_idle'],
		'kitchen': ['dishwasher','fridge','living_room_middle','cook_idle','kitchen_stove'],	#can go straight to kitchen or through kitchen entrance - took out kitchen entrance also
#		'kitchen_entrance': ['kitchen','living_room_middle'], # took out living room top right - not used(cook_idle changed position)
#		'living_room_top_right': ['cook_idle','kitchen_entrance'],
		'living_room_middle': ['kitchen','living_room_entrance','living_room_sofa'], # took out living room top right and kitchen entrance - not used
		'living_room_entrance': ['hallway_mid','living_room_sofa','living_room_middle'],	#take out living room middle? do we need it?
		'living_room_sofa': ['sofa','sofa2','piano','entertainment_idle','living_room_entrance','living_room_middle'],
		
		# Robot idle positions
		'cook_idle': ['kitchen'],
		'medication_idle': ['cupboard'],
		'entertainment_idle': ['living_room_sofa'],
		'companionship_idle': ['bedroom'],
		
		# Human starting positions (excluding resident)
		'visitor_idle': ['door'],
		'nurse_idle': ['door'],
		'doctor_idle': ['door'],
		'caregiver_idle': ['door'],
		
		# Furniture
		'bed': ['bedroom'],
		'kitchen_stove': ['kitchen'],
		'sofa': ['living_room_sofa'],
		'gym': ['bedroom'],
		'sofa2': ['living_room_sofa'],
		'toilet': ['bathroom'],
		'sink': ['bathroom'],
		'bathtub': ['bathroom'],
		'fridge': ['kitchen'],
		'dishwasher': ['kitchen'],
		'piano': ['living_room_sofa']
	}

	# assigning the names of each robot to their idle positions (robot_0 = cook_robot)
	ROBOT_IDLES = {

		'robot_0' : 'visitor_idle',		#visitor
		'robot_2' : 'cook_idle'

	}

	# scheduled events, their priorities and warning messages
	EVENTS = {
		'Resident.wakeup': {
			'explanation': 'Resident is currently waking up',
			'priority': 3,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.sleep': {
			'explanation': 'Resident is going to sleep',
			'priority': 3,
			'destination': 'bed',
			'duration': 100
		},
		'Resident.eat_breakfast': {
			'explanation': 'Resident is eating breakfast',
			'priority': 3,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.eat_lunch': {
			'explanation': 'Resident is eating lunch',
			'priority': 3,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.eat_dinner': {
			'explanation': 'Resident is eating dinner',
			'priority': 3,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.eat_snack': {						#generated event for innovation
			'explanation': 'Resident is eating a snack',
			'priority': 1,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.take_meds': {
			'explanation': 'Resident is taking medication',
			'priority': 1,
			'destination': 'cupboard',
			'duration': 100
		},
		'Resident.idle': {
			'explanation': 'Resident is not doing anything',
			'priority': 3,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.gym': {
			'explanation': 'Resident is exercising',
			'priority': 1,
			'destination': 'gym',
			'duration': 100
		},
		'Resident.toilet': {
			'explanation': 'Resident is going toilet',
			'priority': 1,
			'destination': 'toilet',
			'duration': 100
		},
		'Resident.bath': {
			'explanation': 'Resident is having a bath',
			'priority': 1,
			'destination': 'bathtub',
			'duration': 100
		},
		'Cook.cook_breakfast': {
			'explanation': 'Cook robot is cooking breakfast',
			'priority': 1,
			'destination': 'kitchen',
			'duration': 100
		},
		'Cook.cook_lunch': {
			'explanation': 'Cook robot is cooking lunch',
			'priority': 1,
			'destination': 'kitchen',
			'duration': 100
		},
		'Cook.cook_dinner': {
			'explanation': 'Cook robot is cooking dinner',
			'priority': 1,
			'destination': 'kitchen',
			'duration': 100
		},
		'Visitor.visit': {
			'explanation': 'Someone is visiting the house',
			'priority': 1,
			'destination': 'living_room_middle',
			'duration': 100
		},
		'Resident.status_eat_med':  {
			'explanation': 'Resident is eating',
			'priority': 3,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.status_eat_low':  {
			'explanation': 'Resident is eating',
			'priority': 2,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.status_eat_dan':  {
			'explanation': 'Resident is eating',
			'priority': 1,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.status_med_med':  {
			'explanation': 'Resident is taking medication',
			'priority': 3,
			'destination': 'cupboard',
			'duration': 100
		},
		'Resident.status_med_low':  {
			'explanation': 'Resident is taking medication',
			'priority': 2,
			'destination': 'cupboard',
			'duration': 100
		},
		'Resident.status_med_dan':  {
			'explanation': 'Resident is taking medication',
			'priority': 1,
			'destination': 'cupboard',
			'duration': 100
		},
		'Resident.status_ent_med':  {
			'explanation': 'Resident is entertaining themselves',
			'priority': 3,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.status_ent_low':  {
			'explanation': 'Resident is entertaining themselves',
			'priority': 2,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.status_ent_dan':  {
			'explanation': 'Resident is entertaining themselves',
			'priority': 1,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.status_san_med':  {
			'explanation': 'Resident is going crazy with all these robots',
			'priority': 3,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.status_san_low':  {
			'explanation': 'Resident is going crazy with all these robots',
			'priority': 2,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.status_san_dan':  {
			'explanation': 'Resident is going crazy with all these robots',
			'priority': 1,
			'destination': 'sofa',
			'duration': 100
		},
		'Resident.status_fit_med':  {
			'explanation': 'Resident is exercising',
			'priority': 3,
			'destination': 'gym',
			'duration': 100
		},
		'Resident.status_fit_low':  {
			'explanation': 'Resident is exercising',
			'priority': 2,
			'destination': 'gym',
			'duration': 100
		},
		'Resident.status_fit_dan':  {
			'explanation': 'Resident is exercising',
			'priority': 1,
			'destination': 'gym',
			'duration': 100
		},
		'Resident.status_hyd_med':  {
			'explanation': 'Resident is hydrating',
			'priority': 3,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.status_hyd_low':  {
			'explanation': 'Resident is hydrating',
			'priority': 2,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.status_hyd_dan':  {
			'explanation': 'Resident is hydrating',
			'priority': 1,
			'destination': 'kitchen',
			'duration': 100
		},
		'Resident.status_hyg_med':  {
			'explanation': 'Resident is bathing',
			'priority': 3,
			'destination': 'bathroom',
			'duration': 100
		},
		'Resident.status_hyg_low':  {
			'explanation': 'Resident is bathing',
			'priority': 2,
			'destination': 'bathroom',
			'duration': 100
		},
		'Resident.status_hyg_dan':  {
			'explanation': 'Resident is bathing',
			'priority': 1,
			'destination': 'bathroom',
			'duration': 100
		},
		'Resident.status_rel_med':  {
			'explanation': 'Resident is peeing',
			'priority': 3,
			'destination': 'bathroom',
			'duration': 100
		},
		'Resident.status_rel_low':  {
			'explanation': 'Resident is peeing',
			'priority': 2,
			'destination': 'bathroom',
			'duration': 100
		},
		'Resident.status_rel_dan':  {
			'explanation': 'Resident is peeing',
			'priority': 1,
			'destination': 'bathroom',
			'duration': 100
		}
	}

	LEVELS = (
			'Fullness', 'Health', 'Entertainment', 'Sanity',
			'Fitness', 'Hydration', 'Hygiene', 'Relief'
	)
	
	# tasks run by the scheduler
	SCHEDULED_TASKS = {
		8: 'Resident.wakeup',
		23: 'Visitor.visit',
		30: 'Cook.cook_breakfast',
		45: 'Resident.eat_breakfast',
		55: 'Resident.take_meds',
		70: 'Cook.cook_lunch',
		85: 'Resident.eat_lunch',
		100: 'Resident.idle',
		120: 'Visitor.visit',
		150: 'Cook.cook_dinner',
		170: 'Resident.eat_dinner',
		200: 'Resident.sleep'
	}

	# resident status requirements
	STATUS_TASKS = {
		"Fullness: med": "Resident.status_eat_med",
		"Fullness: low": "Resident.status_eat_low",
		"Fullness: dan": "Resident.status_eat_dan",
		"Health: med": "Resident.status_med_med",
		"Health: low": "Resident.status_med_low",
		"Health: dan": "Resident.status_med_dan",
		"Entertainment: med": "Resident.status_ent_med",
		"Entertainment: low": "Resident.status_ent_low",
		"Entertainment: dan": "Resident.status_ent_dan",
		"Sanity: med": "Resident.status_san_med",
		"Sanity: low": "Resident.status_san_low",
		"Sanity: dan": "Resident.status_san_dan",
		"Fitness: med": "Resident.status_fit_med",
		"Fitness: low": "Resident.status_fit_low",
		"Fitness: dan": "Resident.status_fit_dan",
		"Hydration: med": "Resident.status_hyd_med",
		"Hydration: low": "Resident.status_hyd_low",
		"Hydration: dan": "Resident.status_hyd_dan",
		"Hygiene: med": "Resident.status_hyg_med",
		"Hygiene: low": "Resident.status_hyg_low",
		"Hygiene: dan": "Resident.status_hyg_dan",
		"Relief: med": "Resident.status_rel_med",
		"Relief: low": "Resident.status_rel_low",
		"Relief: dan": "Resident.status_rel_dan"
	}