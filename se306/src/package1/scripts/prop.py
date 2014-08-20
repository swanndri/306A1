import random

#r is the y in a r setting for the initial roll. 
#I.E setting it to 100 and y to 1 means theres a 1 in 100 chance
#this should be set by possibly the scheduler or at the beginning of each node being made
r = 100

#x will be a randomly generated number number between one and the initial range
x = random.randint(0,r)

#y will be the acceptable range of x
#I.E by setting this to 30 and r to 100, this means that there is a 30 in 100 chance of it happening
y = 30

#z is the increase in the probabilty between instances.
#the first instance would be 30/100, the next one increases by z to 31/100
z = 1

#this is just so it loops till succes
s = False

while(s is False):
	if x <= y:
		s = True
		print ("Success")
	else :
		x = random.randint(0,r)
		y += z



