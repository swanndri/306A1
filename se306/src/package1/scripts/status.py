#!/usr/bin/env python


import roslib; roslib.load_manifest('package1')
import std_msgs.msg
import rospy

rospy.init_node('status', anonymous=True)

rate = rospy.Rate(40)


def callback(msg):
	if int(msg.data.split()[1]) <= 0:
		print "0/100"
	else:
		print msg.data + "/100"

def scheduler_callback(msg):
	msg = str(msg)
	if (msg == 'data: Resident.wakeup'):
		print("Resident is currently waking up")
	elif (msg == 'data: Resident.eat_breakfast'):
		print("Resident is walking to the kitchen to eat breakfast")
	elif (msg == 'data: Resident.take_meds'):
		print("Resident is walking to the cupboard to get and take their medication")
	elif (msg == 'data: Resident.eat_lunch'):
		print("Resident is walking to the kitchen to eat lunch")
	elif (msg =='data: Resident.eat_dinner'):
		print("Resident is walking to the kitchen to eat dinner")
	elif (msg =='data: Resident.sleep'):
		print("Resident is walking to the bedroom to go to sleep")

	if (msg == 'data: Cook.cook_breakfast'):
		print("Cook robot is moving to the kitchen to cook breakfast")
	elif (msg == 'data: Cook.cook_lunch'):
		print("Cook robot is moving to the kitchen to cook lunch")
	elif (msg =='data: Cook.cook_dinner'):
		print("Cook robot is moving to the kitchen to cook dinner")
		
	if (msg == 'data: Visitor.visit'):
		print("Visitor is visiting the residents house")
	#print msg


sub = rospy.Subscriber("human", std_msgs.msg.String, callback)
sub = rospy.Subscriber("scheduler", std_msgs.msg.String, scheduler_callback)

while not rospy.is_shutdown():
	rate.sleep()






