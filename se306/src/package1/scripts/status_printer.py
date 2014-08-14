#!/usr/bin/env python

class StatusPrinter:
	
	def __init__(self):
		self.health = 100
		self.bladder = 0
		
	def print_health(self):
		hash_count = (self.health_max//10)
		print " [ Health  : " + "#"*hash_count + " "*(10-hash_count) + " ] "
		
	def print_bladder(self):
		hash_count = (self.bladder_max//10)
		print " [ Bladder : " + "#"*hash_count + " "*(10-hash_count) + " ] "
		
	def display_status(self):
		print_health()
		print_bladder()
		
	def data_received(self, data):
		if datarelatedtohealth:
			self.health = data
		elif datarelatedtobladder:
			self.bladder = data
			
		self.display_status()
