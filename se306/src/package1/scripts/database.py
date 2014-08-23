import math

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
			'cupboard': (-3.6, 4.2),
			'bedroom': (-3.6, 2.1),
			'bathroom': (-3.6, -3.7),
			'hallway_top': (-1.2, 1.9),
			'hallway_mid': (-1.2, 0.45),
			'hallway_bot': (-1.2, -3.7),
			'door': (-1.2, -6),
			'kitchen': (2.05, 3.5),
			'kitchen_entrance': (2.05, 1.6),
			'living_room_top_right': (4.5, 1.6),
			'living_room_middle': (2.05, 0.45),
			'cook_idle': (4.5, -1.85),
			'idle': (12, 4),
			'living_room_entrance': (1, 0.45),
			'living_room_sofa': (1, -3),
			'bed': (-2.3, -1.1),
			'sofa': (0.3, -3),
			'gym': (-4.450, 2.850),
			'sofa2': (1.500, -4.250),
			'toilet': (-4.350, -4.500),
			'sink': (-3.300, -3.400),
			'bathtub': (-4.350, -3.250),
			'fridge': (0.500, 3.000),
			'dishwasher': (3.750, 3.500)
		}

		# objects (mostly rooms) defined by their top left and bottom right points
		OBJECTS = {
			'cupboard': ((-5, 5), (-1.7, 3.6)),
			'room': ((-5, 3.6), (-1.7, -5)),
			'bathroom': ((-5, -2.3), (-1.7, -5)),
			'hallway': ((-1.7, 5), (-0.7, -5)),
			'kitchen': ((-0.7, 5), (5, 2.2)),
			'living_room': ((-0.7, 2.2), (5, -5)),
			'house': ((-5, 5), (5, -5))
		}

		# connected graph of points showing neighbours
		GRAPH = {
			'cupboard': ['bedroom'],
			'bedroom': ['bed', 'cupboard', 'gym', 'hallway_top'],
			'bathroom': ['bathtub', 'hallway_bot', 'sink', 'toilet'],
			'hallway_top': ['bedroom', 'hallway_mid'],
			'hallway_mid': ['hallway_bot', 'hallway_top', 'living_room_entrance'],
			'hallway_bot': ['bathroom', 'door', 'hallway_mid'],
			'door': ['hallway_bot'],
			'kitchen': ['dishwasher', 'fridge', 'kitchen_entrance', 'living_room_middle'],
			'kitchen_entrance': ['kitchen', 'living_room_middle', 'living_room_top_right'],
			'living_room_top_right': ['cook_idle', 'kitchen_entrance'],
			'living_room_middle': ['kitchen', 'kitchen_entrance', 'living_room_entrance', 'living_room_top_right'],
			'cook_idle': ['living_room_top_right'],
			'living_room_entrance': ['hallway_mid', 'living_room_sofa', 'living_room_middle'],
			'living_room_sofa': ['sofa', 'sofa2'],
			'bed': ['bedroom'],
			'sofa': ['living_room_sofa'],
			'gym': ['bedroom'],
			'sofa2': ['living_room_sofa'],
			'toilet': ['bathroom'],
			'sink': ['bathroom'],
			'bathtub': ['bathroom'],
			'fridge': ['kitchen'],
			'dishwasher': ['kitchen']
		}

		# scheduled events, their priorities and warning messages
		EVENTS = {
			'Resident.wakeup': {
				'explanation': 'Resident is currently waking up',
				'priority': 3
			},
			'Resident.sleep': {
				'explanation': 'Resident is going to sleep',
				'priority': 3
			},
			'Resident.eat_breakfast': {
				'explanation': 'Resident is eating breakfast',
				'priority': 3
			},
			'Resident.eat_lunch': {
				'explanation': 'Resident is eating lunch',
				'priority': 3
			},
			'Resident.eat_dinner': {
				'explanation': 'Resident is eating dinner',
				'priority': 3
			},
			'Resident.take_meds': {
				'explanation': 'Resident is taking medication',
				'priority': 1
			},
			'Resident.idle': {
				'explanation': 'Resident is not doing anything',
				'priority': 3
			},
			'Cook.cook_breakfast': {
				'explanation': 'Cook robot is cooking breakfast',
				'priority': 1
			},
			'Cook.cook_lunch': {
				'explanation': 'Cook robot is cooking lunch',
				'priority': 1
			},
			'Cook.cook_dinner': {
				'explanation': 'Cook robot is cooking dinner',
				'priority': 1
			},
			'Resident.take_meds': {
				'explanation': 'Resident is taking medication',
				'priority': 1
			},
			'Visitor.visit': {
				'explanation': 'Someone is visiting the house',
				'priority': 1
			}
		}

		LEVELS = {
			'fullness': {
				'warn_medium': 'Resident getting a bit hungry',
				'warn_low': 'Resident pretty damn hungry right now man',
				'warn_dangerous': 'Resident starving now...'
			}
			'health': {
				'warn_medium': 'Resident looks a bit unhealthy',
				'warn_low': 'Resident\'s health is concerning',
				'warn_dangerous': 'OW OW OWOWOWOW the resident is dying'
			},
			'entertainment': {
				'warn_medium': 'The resident looks quite bored',
				'warn_low': 'Resident is getting reallllly bored',
				'warn_dangerous': 'ENTERTAIN THE RESIDENT OR WE ALL DIE'
			},
			'sanity': {
				'warn_medium': 'Resident is losing sanity',
				'warn_low': 'Resident\'s behaviour is a bit concerning',
				'warn_dangerous': "Resident is going crazy right n- \
					AAAAAAAH"
			},
			'fitness': {
				'warn_medium': 'Resident is getting unfit',
				'warn_low': 'Resident is really unfit',
				'warn_dangerous': 'Resident is incredibly unfit'
			},
			'hydration': {
				'warn_medium': 'Me Tarzan. Resident thirsty.',
				'warn_low': 'Resident could really use some water',
				'warn_dangerous': 'RESIDENT NEEDS WATERRRR!!!!'
			},
			'hygene': {
				'warn_medium': 'Resident\'s hygiene is slightly bad',
				'warn_low': 'Resident\'s hygiene is really bad',
				'warn_dangerous': 'Resident is wallowing his own filth'
			}
		}
