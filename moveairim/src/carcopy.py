#!/usr/bin/env python
import airsim
import rospy
from geometry_msgs.msg import Twist
import cv2 #conda install opencv
import time

rospy.init_node('s_shapes',anonymous= True)
pub = rospy.Publisher('/cmd_vel',Twist,queue_size= 2)
rate=rospy.Rate(2)
sshape= Twist()


# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
car_controls = airsim.CarControls()

start = time.time()
sshape.linear.x = 0
sshape.linear.y = 0
sshape.linear.z = 0
sshape.angular.x = 0
sshape.angular.y = 0
sshape.angular.z = 0



# monitor car state while you drive it manually.
while (cv2.waitKey(1) & 0xFF) == 0xFF:
    # get state of the car
    car_state = client.getCarState()
    pos = car_state.kinematics_estimated.position
    orientation = car_state.kinematics_estimated.orientation
    linvel = car_state.kinematics_estimated.linear_velocity
    angvel = car_state.kinematics_estimated.angular_velocity
    milliseconds = (time.time() - start) * 1000

    sshape.linear.x = linvel.x_val
    sshape.linear.y = linvel.y_val
    sshape.linear.z = linvel.z_val
    
    sshape.angular.x = angvel.x_val
    sshape.angular.y = angvel.y_val
    sshape.angular.z = angvel.z_val
    
    if not rospy.is_shutdown():
        pub.publish(sshape)
    
    time.sleep(0.1)
