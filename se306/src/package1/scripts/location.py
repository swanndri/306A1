class Location:




def __init__(self, robot_name):

		self.resident_coord = []
		self.visitor_coord = []
		self.cook_coord = []

		

		

		subscribe_to = "/" + "robot_0" + "/base_pose_ground_truth"
		rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, self.resident)

		subscribe_to = "/" + "robot_1" + "/base_pose_ground_truth"
		rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, self.visitor)

		subscribe_to = "/" + "robot_2" + "/base_pose_ground_truth"
		rospy.Subscriber(subscribe_to, nav_msgs.msg.Odometry, self.cook)






		publish_to = "/" + "robot_1" + "/base_pose_ground_truth"		
		self.movement_publisher = rospy.Publisher(publish_to, geometry_msgs.msg.Twist, queue_size=10)		
		
		
def set_resident(self, location_data):
	self.resident_coord[0] = position_data.pose.pose.position.x
	self.resident_coord[1] = position_data.pose.pose.position.y

def set_visitor(self, location_data):
	self.visitor_coord[0] = position_data.pose.pose.position.x
	self.visitor_coord[1] = position_data.pose.pose.position.y

def set_cook(self, location_data):
	self.cook_coord[0] = position_data.pose.pose.position.x
	self.cook_coord[1] = position_data.pose.pose.position.y

