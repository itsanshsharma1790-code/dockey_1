#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import time

def move_square():
    rospy.init_node('square_turtle_node', anonymous=True)
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    
    rate = rospy.Rate(10)  # 10 Hz

    side_duration = 2.0   # time to move straight
    turn_duration = 1.57  # approx 90 degree turn

    while not rospy.is_shutdown():
        for _ in range(4):  # 4 sides of square
            
            # Move forward
            vel_msg.linear.x = 2.0
            vel_msg.angular.z = 0.0
            
            t0 = time.time()
            while time.time() - t0 < side_duration:
                pub.publish(vel_msg)
                rate.sleep()
            
            # Stop before turning
            vel_msg.linear.x = 0.0
            pub.publish(vel_msg)
            time.sleep(0.5)

            # Turn 90 degrees
            vel_msg.angular.z = 1.0
            vel_msg.linear.x = 0.0
            
            t0 = time.time()
            while time.time() - t0 < turn_duration:
                pub.publish(vel_msg)
                rate.sleep()
            
            # Stop after turning
            vel_msg.angular.z = 0.0
            pub.publish(vel_msg)
            time.sleep(0.5)

if __name__ == '__main__':
    try:
        move_square()
    except rospy.ROSInterruptException:
        pass
