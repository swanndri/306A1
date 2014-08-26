#!/usr/bin/env python

class Rectangle:
    def __init__(self, name, pt1, pt2):
        """Initialize a rectangle from two points."""
        self.name = name
        self.left = min(pt1[0], pt1[1])
        self.top = min(pt2[0], pt2[1])
        self.right  = max(pt1[0], pt1[1])
        self.bottom = max(pt2[0], pt2[1])

    def contains(self, pt):
        """Return true if a point is inside the rectangle."""
        x = pt[0]
        y = pt[1]
        return ((self.left <= x <= self.right) and (self.top <= y <= self.bottom))


if __name__ == '__main__':
    print("Main is for testing purposes only")
    r = Rectangle("Cuprboard", (-5, 5), (5, -5))
    print(r.contains([5,9]))
    print(r.name)