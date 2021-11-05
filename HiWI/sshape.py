import json
import time
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('s_shapes',anonymous= True)
pub = rospy.Publisher('/cmd_vel',Twist,queue_size= 2)
rate=rospy.Rate(2)
sshape= Twist()
with open('s_shape.json','r') as f:
    d = json.load(f)
x =d['data']
for i in x:
    for j in i:
        linear_vel = i[j]['CarState']['kinematics_estimated']['linear_velocity']
        angular_vel = i[j]['CarState']['kinematics_estimated']['angular_velocity']
        lx = linear_vel['x_val']
        ly = linear_vel['y_val']
        lz = linear_vel['z_val']
        ax = angular_vel['x_val']
        ay = angular_vel['y_val']
        az = angular_vel['z_val']
    sshape.linear.x = lx
    sshape.linear.y = ly
    sshape.linear.z = lz
    sshape.angular.x = ax
    sshape.angular.y = ay
    sshape.angular.z = az
    
    if not rospy.is_shutdown():
        pub.publish(sshape)
        # rate.sleep()

    # frequency in seconds
    time.sleep(0.1)
