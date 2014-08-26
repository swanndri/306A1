#!/usr/bin/env python

class Rectangle:
    def __init__(self, name, pt1, pt2):
        """Initialize a rectangle from two points."""
        self.name   = name
        self.left   = min(pt1[0], pt2[0])
        self.right  = max(pt1[0], pt2[0])

        self.top    = max(pt1[1], pt2[1])
        self.bottom = min(pt1[1], pt2[1])

    def contains(self, pt):
        """Return true if a point is inside the rectangle."""
        x = pt[0]
        y = pt[1]
        return (self.left <= x <= self.right) and (self.bottom <= y <= self.top)


if __name__ == '__main__':
    print("Main is for testing purposes only")
    r = Rectangle("Living_room", [-0.7, 2.2], [5, -5])
    print(r.contains([4,-1.9]))
    print(r.name)