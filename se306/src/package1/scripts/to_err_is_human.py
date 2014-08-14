#goes in human
sub = rospy.Subscriber("clock", std_msgs.msg.String, callback)

pub = rospy.Publisher('human', std_msgs.msg.String, queue_size=10)
pub.publish(stringything)

def callback(msg):
	print msg.data
	if #condition:
		self.fullness -= 1
		pub.publish("Fullness: " + str(self.fullness))
		
	#condition modulo, when true, pub to /human
	# 
	#create self.fullness = 100
	#on true, subtract from self.fullness then pub.publish()gajfgk

#create self.fullness in human's init
