import setup_path 
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

print("Time,Speed,Gear,PX,PY,PZ,OW,OX,OY,OZ")

# monitor car state while you drive it manually.
while (cv2.waitKey(1) & 0xFF) == 0xFF:
    # get state of the car
    car_state = client.getCarState()
    pos = car_state.kinematics_estimated.position
    orientation = car_state.kinematics_estimated.orientation
    milliseconds = (time.time() - start) * 1000
    print("%s,%d,%d,%f,%f,%f,%f,%f,%f,%f" % \
       (milliseconds, car_state.speed, car_state.gear, pos.x_val, pos.y_val, pos.z_val, 
        orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val))
    sshape.linear.x = linear_velocity.x_val
    sshape.linear.y = linear_velocity.y_val
    sshape.linear.z = linear_velocity.z_val
    sshape.angular.x = angular_velocity.x_val
    sshape.angular.y = angular_velocity.y_val
    sshape.angular.z = angular_velocity.z_val
    if not rospy.is_shutdown():
        pub.publish(sshape)
    
    time.sleep(0.1)
