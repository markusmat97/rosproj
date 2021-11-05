import time
import rospy
import json
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import math
from math import sin, cos, pi

rospy.init_node('odometry_publisher')

odom_pub = rospy.Publisher("/odom", Odometry, queue_size=50)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=50)
odom_broadcaster = tf.TransformBroadcaster()

with open('s_shape_1.json','r') as f:
    d = json.load(f)
x =d['data']

current_time = rospy.Time.now()
last_time = rospy.Time.now()

r = rospy.Rate(1.0)
while not rospy.is_shutdown():
    for i in x:
        for j in i:
            pos = i[j]['CarState']['kinematics_estimated']['position']
            orien = i[j]['CarState']['kinematics_estimated']['orientation']
            linear_vel = i[j]['CarState']['kinematics_estimated']['linear_velocity']
            angular_vel = i[j]['CarState']['kinematics_estimated']['angular_velocity']
            px = pos['x_val']
            py = pos['y_val']
            oz = orien['z_val']
            lx = linear_vel['x_val']
            ly = linear_vel['y_val']
            #lz = linear_vel['z_val']
            #ax = angular_vel['x_val']
            #ay = angular_vel['y_val']
            az = angular_vel['z_val']
            current_time = rospy.Time.now()
            last_time = rospy.Time.now()

             # compute odometry in a typical way given the velocities of the robot
            dt = (current_time - last_time).to_sec()
            delta_x = (lx * cos(oz) - ly * sin(oz)) * dt
            delta_y = (lx * sin(oz) + ly * cos(oz)) * dt
            delta_th = az * dt

            px += delta_x
            py += delta_y
            oz += delta_th

            # since all odometry is 6DOF we'll need a quaternion created from yaw
            odom_quat = tf.transformations.quaternion_from_euler(0, 0, oz)

            # first, we'll publish the transform over tf
            odom_broadcaster.sendTransform(
                (px, py, 0),
                odom_quat,
                current_time,
                "base_link",
                "odom"
            )

            # next, we'll publish the odometry message over ROS
            odom = Odometry()
            twis = Twist()
            odom.header.stamp = current_time
            odom.header.frame_id = "odom"

            # set the position
            odom.pose.pose = Pose(Point(px, py, 0), Quaternion(*odom_quat))

             # set the velocity
            #odom.child_frame_id = "base_link"
            #odom.twist.twist = Twist(Vector3(lx, ly, 0), Vector3(0, 0, az))
            twis.linear.x = lx
            twis.linear.y = ly
            twis.angular.z = az
            # publish the message
            odom_pub.publish(odom)
            pub.publish(twis)

            last_time = current_time
            r.sleep()
