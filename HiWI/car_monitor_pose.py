import airsim
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
import cv2 #conda install opencv
import time

rospy.init_node('s_shapes',anonymous= True)
pub = rospy.Publisher('/pose',Twist,queue_size= 2)
rate=rospy.Rate(2)
sshape= Pose()


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
    sshape.position.x = pos.x_val
    sshape.position.y = pos.y_val
    sshape.position.z = pos.z_val
    sshape.orientation.x = orientation.x_val
    sshape.orientation.y = orientation.y_val
    sshape.orientation.z = orientation.z_val
    sshape.orientation.w = orientation.w_val
    if not rospy.is_shutdown():
        pub.publish(sshape)
    
    time.sleep(0.1)
