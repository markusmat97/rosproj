import airsim
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Header
import cv2 #conda install opencv
import time

rospy.init_node('odom_pub',anonymous= True)
pub = rospy.Publisher('/my_odom',Odometry,queue_size= 2)

r=rospy.Rate(2)
odom = Odometry()
header = Header()
header.frame_id = '/odom'

# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
car_controls = airsim.CarControls()
start = time.time()
a = odom.pose.pose.position
b = odom.twist.twist.linear
c = odom.twist.twist.angular



while (cv2.waitKey(1) & 0xFF) == 0xFF:

    car_state = client.getCarState()
    pos = car_state.kinematics_estimated.position
    orientation = car_state.kinematics_estimated.orientation
    linvel = car_state.kinematics_estimated.linear_velocity
    angvel = car_state.kinematics_estimated.angular_velocity
    milliseconds = (time.time() - start) * 1000

    a= pos
    b=linvel
    c= angvel

    header.stamp = rospy.Time.now()
    odom.header = header

    pub.publish(odom)
    r.sleep()
