import math

class Paths:

	east = 0.0
	west = math.pi
	north = math.pi / 2.0
	south = -math.pi / 2.0


	cupboard 		=	[-11,12]
	bedroom 		=	[-11,6]
	bathroom		=	[-10,-11]
	hallway_top		=	[-4,6]
	hallway_mid		=	[-4,1]
	hallway_bot		=	[-4,-11]
	door			=	[-4,-14]
	kitchen			=	[6,11]
	living_room		=	[6,1]
	cook_idle		= 	[13,-13]
	idle			=	[12,4]

	
	door_to_kitchen				=	[door, hallway_mid, living_room, kitchen]
	bedroom_to_living_room		=	[bedroom, hallway_top, hallway_mid, living_room, idle]
	living_room_to_kitchen		=	[living_room, kitchen]
	kitchen_to_bedroom			=	[kitchen, living_room, hallway_mid, hallway_top, bedroom]
	kitchen_to_cupboard			=	[kitchen, living_room, hallway_mid, hallway_top, bedroom, cupboard, bedroom]
	cupboard_to_kitchen			=	[bedroom, hallway_top, hallway_mid, living_room, kitchen]
	door_to_living_room			=	[door, hallway_mid, living_room]
	kitchen_to_idle				=	[kitchen, living_room, idle]
	cook_path					=	[cook_idle, living_room, kitchen, living_room, cook_idle]