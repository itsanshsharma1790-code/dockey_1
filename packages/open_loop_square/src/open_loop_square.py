#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import WheelsCmdStamped

class OpenLoopSquare:

    def __init__(self):
        rospy.init_node("open_loop_square_node", anonymous=True)

        self.pub = rospy.Publisher(
            "/mybota002410/wheels_driver_node/wheels_cmd",
            WheelsCmdStamped,
            queue_size=1
        )

        self.msg = WheelsCmdStamped()
        self.rate = rospy.Rate(10)

        rospy.loginfo(" Node started successfully")
        rospy.sleep(2)

        self.move_square()

    def move_forward(self, duration=2.0, speed=0.4):
        rospy.loginfo(" Moving forward")

        start = rospy.Time.now()
        while (rospy.Time.now() - start).to_sec() < duration and not rospy.is_shutdown():
            self.msg.vel_left = speed
            self.msg.vel_right = speed
            self.pub.publish(self.msg)
            self.rate.sleep()

        self.stop_robot()

    def turn_right(self, duration=1.0, speed=0.4):
        rospy.loginfo(" Turning right")

        start = rospy.Time.now()
        while (rospy.Time.now() - start).to_sec() < duration and not rospy.is_shutdown():
            self.msg.vel_left = speed
            self.msg.vel_right = -speed
            self.pub.publish(self.msg)
            self.rate.sleep()

        self.stop_robot()

    def stop_robot(self):
        rospy.loginfo(" Stopping")

        for _ in range(10):
            self.msg.vel_left = 0.0
            self.msg.vel_right = 0.0
            self.pub.publish(self.msg)
            self.rate.sleep()

        rospy.sleep(0.5)

    def move_square(self):
        rospy.loginfo(" Starting square movement")

        for i in range(4):
            rospy.loginfo(f" Side {i+1}")
            self.move_forward()
            self.turn_right()

        rospy.loginfo(" Square completed")
        self.stop_robot()

    def run(self):
        rospy.spin()


if __name__ == "__main__":
    try:
        node = OpenLoopSquare()
        node.run()
    except rospy.ROSInterruptException:
        pass
