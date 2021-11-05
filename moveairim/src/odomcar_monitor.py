#!/usr/bin/env python
import airsim
import rospy
from nav_msgs.msg import Odometry
import cv2 #conda install opencv
import time

rospy.init_node('s_shapes',anonymous= True)
pub = rospy.Publisher('/odom',Odometry,queue_size= 2)
rate=rospy.Rate(2)
sshape= Odometry()


# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
car_controls = airsim.CarControls()

start = time.time()

print("Time,Speed,Gear,PX,PY,PZ,OW,OX,OY,OZ")

# monitor car state while you drive it manually.
while (cv2.waitKey(1) & 0xFF) == 0xFF:
    # get state of the car
    car_state = client.getCarState()
    pos = car_state.kinematics_estimated.position
    orientation = car_state.kinematics_estimated.orientation
    linvel = car_state.kinematics_estimated.linear_velocity
    angvel = car_state.kinematics_estimated.angular_velocity
    milliseconds = (time.time() - start) * 1000
    sshape.header.frame_id = "odom"

    sshape.pose.pose.position.x = 1
    sshape.pose.pose.position.y = 1
    sshape.pose.pose.position.z = 1
    sshape.pose.pose.orientation.x = 1
    sshape.pose.pose.orientation.y = 2
    sshape.pose.pose.orientation.z = 2
    sshape.pose.pose.orientation.w = 1

    sshape.child_frame_id = "base_link"

    sshape.twist.twist.linear.x = 0.2
    sshape.twist.twist.linear.y = 0.2
    sshape.twist.twist.linear.z = 0.2

    sshape.twist.twist.angular.x = 0.2
    sshape.twist.twist.angular.y = 0.2
    sshape.twist.twist.angular.z = 0.2
    if not rospy.is_shutdown():
        pub.publish(sshape)
    
  #  time.sleep(0.1)
