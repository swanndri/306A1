class Node(object):
	
	def __init__(self, name):
		print "Node init called"


class Robot(Node):
	
	def __init__(self, name):
		super(Robot, self).__init__(name)
		print "Robot init called"

class Human(Node):
	
	def __init__(self, name):
		super(Human, self).__init__(name)
		print "Human init called"