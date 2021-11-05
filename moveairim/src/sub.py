#!/usr/bin/env python
import rospy
import airsim
from geometry_msgs.msg  import Twist
from nav_msgs.msg import Odometry
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
import cv2 #conda install opencv
import time

class turtlebot():

    def __init__(self):
        #Creating our node,publisher and subscriber
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        #self.pose_subscriber = rospy.Subscriber('/odom', Odometry, self.callback)
        #self.odom = Odometry()
        self.rate = rospy.Rate(10)

    #Callback function implementing the pose value received
   # def callback(self, data):
    #    self.odom = data
    #    self.odom.pose.pose.position.x = round(self.odom.pose.pose.position.x, 4)
    #    self.odom.pose.pose.position.y = round(self.odom.pose.pose.position.y, 4)

    #def get_distance(self, goal_x, goal_y):
    #    distance = sqrt(pow((goal_x - self.odom.pose.pose.position.x), 2) + pow((goal_y - self.odom.pose.pose.position.y), 2))
    #    return distance

    def move2goal(self):
        # connect to the AirSim simulator
        client = airsim.CarClient()
        client.confirmConnection()
        car_controls = airsim.CarControls()

        start = time.time()
        #goal_pose = Pose()
        #goal_pose.x = input("Set your x goal:")
        #goal_pose.y = input("Set your y goal:")
        #distance_tolerance = input("Set your tolerance:")
        vel_msg = Twist()


        while (cv2.waitKey(1) & 0xFF) == 0xFF:
            # get state of the car
            car_state = client.getCarState()
            pos = car_state.kinematics_estimated.position
            orien = car_state.kinematics_estimated.orientation
            milliseconds = (time.time() - start) * 1000

            #Porportional Controller
            #linear velocity in the x-axis:
            vel_msg.linear.x = 1.5 * sqrt(pow((pos.x_val), 2) + pow((pos.y_val), 2))
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            #angular velocity in the z-axis:
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 4 * (atan2(pos.y_val,pos.x_val))

            #Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()
        #Stopping our robot after the movement is over
        vel_msg.linear.x = 0
        vel_msg.angular.z =0
        self.velocity_publisher.publish(vel_msg)

        rospy.spin()

if __name__ == '__main__':
    try:
        #Testing our function
        x = turtlebot()
        x.move2goal()

    except rospy.ROSInterruptException: pass