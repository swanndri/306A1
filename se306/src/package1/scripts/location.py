#!/usr/bin/env python

import roslib
import rospy
import rosgraph_msgs
import nav_msgs.msg

from std_msgs.msg import String


resident_coord = [None, None]
doctor_coord = [None, None]



pub = rospy.Publisher("location", String, queue_size=10)




def publish(actionmsg):		
		pub.publish(actionmsg)
		print(actionmsg)

			
		
def set_resident(location_data):
	resident_coord[0] = location_data.pose.pose.position.x
	resident_coord[1] = location_data.pose.pose.position.y

def set_doctor(location_data):
	doctor_coord[0] = location_data.pose.pose.position.x
	doctor_coord[1] = location_data.pose.pose.position.y



def find_location(actionmsg):
	
	response_msg = ""
	message = str(actionmsg).split("data: ")[1]
	print(message)

	if "resident" in message:
		response_msg = "resident: "+ str(resident_coord[0]) + " " + str(resident_coord[1])
		publish(response_msg)

	if "doctor" in message:
		response_msg = "resident: "+ str(visitor_coord[0]) + " " + str(visitor_coord[1])
		publish(response_msg)



roslib.load_manifest('package1')
rospy.init_node('location')

subscribe_to = "location_request"
rospy.Subscriber(subscribe_to, String, find_location)

subscribe_to = "/" + "robot_1" + "/base_pose_ground_truth"
rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, set_resident)

# Need to subscribe to doctor when it gets implemented


#subscribe_to = "/" + "robot_0" + "/base_pose_ground_truth"
#rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, set_visitor)


rospy.spin()
