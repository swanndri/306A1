import constants
import math

class Search:
	def __init__(self):
		self.graph = constants.Paths.graph		#graph of world (dict)
		self.points = constants.Paths.points 	#co-ordinates of all nodes (dict)

	def get_distance(self,start_node,end_node):
		start_points = self.points.get(start_node)
		end_points = self.points.get(end_node)
		x_dif = end_points[0] - start_points[0]
		y_dif = end_points[1] - start_points[1]
		distance = math.hypot(x_dif,y_dif)
		return distance

	def get_list(self,string):
		return string.split()

# Gets the neighbour with the lowest f_score
	def get_lowest_f_score(self,open_set,goal,g_score):
		lowest_f_cost = 100000000000000000
		for node in open_set:
			current_f_cost = g_score + self.get_distance(node,goal)
			if len(open_set) == 1:
				lowest_node = node
				break
			elif current_f_cost < lowest_f_cost:
				lowest_node = node
				lowest_f_cost = current_f_cost
		return lowest_node

	def create_path(self,came_from,current_node):
		if current_node in came_from:
			path = self.create_path(came_from, came_from[current_node])
			return (path + ' ' + current_node + ' ')
		else:
			return ' ' + current_node + ' '

	def find_path(self,start,goal):
		closed_set = []		#evaluated nodes
		open_set = [start]		#nodes waiting to be evaluated
		came_from = {}

		g_score = 0
		f_score = g_score + self.get_distance(start,goal)

		while len(open_set) > 0:
			#find the lowest f_score
			#itereate through open set and grab lowest f_score

			current_node = self.get_lowest_f_score(open_set,goal,g_score)
			#check if current is the goal
			if current_node == goal:
				return self.get_list(self.create_path(came_from,goal))

			# Mark current node as visited or expanded
			open_set.remove(current_node)
			closed_set.append(current_node)

			#iterate through all neighbours of the current node
			neighbours = self.graph.get(current_node)
			for neighbour in neighbours:
				# if already evaluated, check the next neighbour
				if neighbour in closed_set:
					continue

				neighbour_to_current_dist = self.get_distance(current_node,neighbour)
				current_g_score = self.get_distance(start,current_node)
				neighbour_g_score = self.get_distance(start,neighbour)
				tentative_g_score =  current_g_score + neighbour_to_current_dist

				# if neighbour hasn't been visited yet or has less cost than neighbour
				if neighbour not in open_set or tentative_g_score < neighbour_g_score:
					came_from[neighbour] = current_node
					neighbour_g_score = tentative_g_score
					neighbour_f_score = neighbour_g_score + self.get_distance(neighbour,goal)
					#add neighbour to the unvisited list
					if neighbour not in open_set:
						open_set.append(neighbour)

		return None		#returns None if failed to find path

# Tests to show finding the correct path
search = Search()
path = search.find_path("door","dishwasher")
print("path of door to dishwasher: ",path)
path = search.find_path("cupboard","cook_idle")
print("path of cupboard to cook_idle: ",path)
	
