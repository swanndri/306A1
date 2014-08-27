import rospy
import node

class Cook(node.Robot):
	
	def __init__(self):
		super(self.__class__.__bases__[0], self).__init__(self.__class__.__name__)

	def _scheduler_event_callback(self, msg):
		if msg.data.startswith(self.__class__.__name__):
			self.jobs.put(tuple(msg.data.split()))

if __name__ == '__main__':
	rospy.init_node('cook_robot')
	cook = Cook()