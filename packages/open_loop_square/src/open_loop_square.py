#!/usr/bin/env python3

import rospy

from duckietown_msgs.msg import WheelsCmdStamped
from duckietown_msgs.msg import WheelEncoderStamped


class ClosedLoopSquare:

    def __init__(self):

        rospy.init_node("closed_loop_square_node", anonymous=True)

        # Publisher
        self.pub = rospy.Publisher(
            "/mybota002410/wheels_driver_node/wheels_cmd",
            WheelsCmdStamped,
            queue_size=1
        )

        # Subscribers
        rospy.Subscriber(
            "/mybota002410/right_wheel_encoder_node/tick",
            WheelEncoderStamped,
            self.right_encoder_callback
        )

        rospy.Subscriber(
            "/mybota002410/left_wheel_encoder_node/tick",
            WheelEncoderStamped,
            self.left_encoder_callback
        )

        self.msg = WheelsCmdStamped()

        # Encoder values
        self.right_tick = 0
        self.left_tick = 0

        self.rate = rospy.Rate(20)

        rospy.loginfo("Closed-loop node started")

        rospy.sleep(2)

        self.move_square()

    # -----------------------------
    # Encoder callbacks
    # -----------------------------

    def right_encoder_callback(self, msg):
        self.right_tick = msg.data

    def left_encoder_callback(self, msg):
        self.left_tick = msg.data

    # -----------------------------
    # Wheel publish helper
    # -----------------------------

    def publish_wheels(self, left, right):

        self.msg.header.stamp = rospy.Time.now()
        self.msg.vel_left = left
        self.msg.vel_right = right

        self.pub.publish(self.msg)

    # -----------------------------
    # Stop robot
    # -----------------------------

    def stop_robot(self):

        rospy.loginfo("Stopping robot")

        for _ in range(10):
            self.publish_wheels(0.0, 0.0)
            self.rate.sleep()

    # -----------------------------
    # Move straight using encoder
    # -----------------------------

    def move_straight(self, target_ticks=300, speed=0.4):

        rospy.loginfo("Moving straight")

        start_tick = self.right_tick

        while abs(self.right_tick - start_tick) < target_ticks and not rospy.is_shutdown():

            self.publish_wheels(speed, speed)

            rospy.loginfo(
                "Current ticks: %d / %d",
                abs(self.right_tick - start_tick),
                target_ticks
            )

            self.rate.sleep()

        self.stop_robot()

    # -----------------------------
    # Rotate using encoder
    # -----------------------------

    def rotate_in_place(self, target_ticks=120, speed=0.4):

        rospy.loginfo("Rotating in place")

        start_tick = self.right_tick

        while abs(self.right_tick - start_tick) < target_ticks and not rospy.is_shutdown():

            self.publish_wheels(speed, -speed)

            rospy.loginfo(
                "Rotation ticks: %d / %d",
                abs(self.right_tick - start_tick),
                target_ticks
            )

            self.rate.sleep()

        self.stop_robot()

    # -----------------------------
    # Square movement
    # -----------------------------

    def move_square(self):

        rospy.loginfo("Starting closed-loop square")

        for i in range(4):

            rospy.loginfo("Side %d of 4", i + 1)

            self.move_straight(
                target_ticks=300,
                speed=0.4
            )

            self.rotate_in_place(
                target_ticks=70,
                speed=0.4
            )

        rospy.loginfo("Square completed")

        self.stop_robot()

    # -----------------------------
    # Run node
    # -----------------------------

    def run(self):
        rospy.spin()


if __name__ == "__main__":

    try:
        node = ClosedLoopSquare()
        node.run()

    except rospy.ROSInterruptException:
        pass
