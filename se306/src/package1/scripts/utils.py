class Rectangle(object):
	
	def __init__(self, name, pt1, pt2):
		x1, y1 = pt1
		x2, y2 = pt2

		self.left = min(x1, x2)
		self.right = max(x1, x2)
		self.top = max(y1, y2)
		self.bottom = min(y1, y2)

	def contains(self, pt3):
		x3, y3 = pt3
		return self.left <= x3 <= self.right and self.bottom <= y3 <= self.top
