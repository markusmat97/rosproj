#!/usr/bin/env python
import rospy
import airsim
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
import time

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
car_controls = airsim.CarControls()

class GoForwardAvoid():
	def __init__(self):
		rospy.init_node('nav_test', anonymous=False)

# get state of the car
		car_state = client.getCarState()
		pos = car_state.kinematics_estimated.position
		orientation = car_state.kinematics_estimated.orientation
		linvel = car_state.kinematics_estimated.linear_velocity
		angvel = car_state.kinematics_estimated.angular_velocity


		#what to do if shut down (e.g. ctrl + C or failure)
		rospy.on_shutdown(self.shutdown)


		#tell the action client that we want to spin a thread by default
		self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
		rospy.loginfo("wait for the action server to come up")
		#allow up to 5 seconds for the action server to come up
		self.move_base.wait_for_server(rospy.Duration(5))

		#we'll send a goal to the robot to move 3 meters forward
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = 'base_link'
		goal.target_pose.header.stamp = rospy.Time.now()

		goal.target_pose.pose.position.x = pos.x_val
		goal.target_pose.pose.position.y = pos.y_val
		goal.target_pose.pose.position.z = pos.z_val

		goal.target_pose.pose.orientation.y = orientation.y_val
		goal.target_pose.pose.orientation.w = orientation.w_val
		goal.target_pose.pose.orientation.x = orientation.x_val
		goal.target_pose.pose.orientation.z = orientation.z_val

		#start moving
		self.move_base.send_goal(goal)

		#allow TurtleBot up to 60 seconds to complete task
		success = self.move_base.wait_for_result(rospy.Duration(60))
		if not success:
			self.move_base.cancel_goal()
			rospy.loginfo("The base failed to move forward 3 meters for some reason")
		else:
			state = self.move_base.get_state()
			if state == GoalStatus.SUCCEEDED:
				rospy.loginfo("Hooray, the base moved 3 meters forward")



	def shutdown(self):
		rospy.loginfo("Stop")


if __name__ == '__main__':
	try:
		GoForwardAvoid()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")
