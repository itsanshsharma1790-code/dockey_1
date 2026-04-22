#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState
 
class Drive_Square:
    def __init__(self):
        self.cmd_msg = Twist2DStamped()

        rospy.init_node('drive_square_node', anonymous=True)
        
        self.pub = rospy.Publisher('/akandb/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=1)

        rospy.sleep(2)
        self.move_robot()
        
    def stop_robot(self):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.0
        self.cmd_msg.omega = 0.0
        self.pub.publish(self.cmd_msg)
 
    def run(self):
        rospy.spin()

 def move_robot(self):

    rate = rospy.Rate(10)  # 10 Hz

    for i in range(4):

        # 🔹 Move forward
        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time).to_sec() < 2.0:
            self.cmd_msg.v = 0.3
            self.cmd_msg.omega = 0.0
            self.pub.publish(self.cmd_msg)
            rate.sleep()

        # 🔹 Stop briefly
        self.stop_robot()
        rospy.sleep(0.5)

        # 🔹 Turn in place
        start_time = rospy.Time.now()
        while (rospy.Time.now() - start_time).to_sec() < 1.2:
            self.cmd_msg.v = 0.0
            self.cmd_msg.omega = 2.0
            self.pub.publish(self.cmd_msg)
            rate.sleep()

        # 🔹 Stop briefly
        self.stop_robot()
        rospy.sleep(0.5)

    self.stop_robot()
 

if __name__ == '__main__':
    try:
        duckiebot_movement = Drive_Square()
        duckiebot_movement.run()
    except rospy.ROSInterruptException:
        pass
