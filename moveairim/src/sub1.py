#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Pose
import airsim
#from turtlesim.msg import Pose
from math import pow, atan2, sqrt
import cv2 #conda install opencv
import time

class TurtleBot:
  def __init__(self):
    #Creates a node with name 'turtlebot_controller' and make sure it is a
    # unique node (using anonymous=True).
    rospy.init_node('turtlebot_controller', anonymous=True)
    # Publisher which will publish to the topic '/turtle1/cmd_vel'.
    self.velocity_publisher = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
    # when a message of type Pose is received.
    self.pose_subscriber = rospy.Subscriber('/pose',Pose, self.update_pose)
    self.pose = Pose()
    self.rate = rospy.Rate(10)

  def update_pose(self, data):
    self.pose = data
    self.pose.x = round(self.pose.x, 4)
    self.pose.y = round(self.pose.y, 4)

  def euclidean_distance(self, goal_pose):
    return sqrt(pow((goal_pose.x - self.pose.x), 2) +pow((goal_pose.y - self.pose.y), 2))

  def linear_vel(self, goal_pose, constant=1.5):
    return constant * self.euclidean_distance(goal_pose)

  def steering_angle(self, goal_pose):
    return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

  def angular_vel(self, goal_pose, constant=6):
    return constant * (self.steering_angle(goal_pose) - self.pose.theta)

  def move2goal(self):
    goal_pose = Pose()
    # Get the input from the user.
    #goal_pose.x = float(input("Set your x goal: "))
    #goal_pose.y = float(input("Set your y goal: "))
     # Please, insert a number slightly greater than 0 (e.g. 0.01).
    #distance_tolerance = input("Set your tolerance: ")
    vel_msg = Twist()
    while (cv2.waitKey(1) & 0xFF) == 0xFF:
      # get state of the car
      car_state = client.getCarState()
      pos = car_state.kinematics_estimated.position
      orien = car_state.kinematics_estimated.orientation
      milliseconds = (time.time() - start) * 1000

      goal_pose.x = pox.x_val
      goal_pose.y = pox.y_val

      vel_msg.linear.x = self.linear_vel(goal_pose)
      vel_msg.linear.y = 0
      vel_msg.linear.z = 0
      # Angular velocity in the z-axis.
      vel_msg.angular.x = 0
      vel_msg.angular.y = 0
      vel_msg.angular.z = self.angular_vel(goal_pose)
        # Publishing our vel_msg
      self.velocity_publisher.publish(vel_msg)
      self.rate.sleep()
      vel_msg.linear.x = 0
      vel_msg.angular.z = 0
      self.velocity_publisher.publish(vel_msg)
        # If we press control + C, the node will stop.
      rospy.spin()

if __name__ == '__main__':
  try:
    x = TurtleBot()
    x.move2goal()
  except rospy.ROSInterruptException:
    pass