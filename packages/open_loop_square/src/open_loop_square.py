#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped

class DriveSquare:
    def __init__(self):
        rospy.init_node("drive_square_node", anonymous=True)

        # IMPORTANT:
        # Keep this as /akandb/... only if that topic exists on your robot.
        # If rostopic list shows /mybota002410/car_cmd_switch_node/cmd,
        # then change it to that instead.
        self.pub = rospy.Publisher(
            "/akandb/car_cmd_switch_node/cmd",
            Twist2DStamped,
            queue_size=1
        )

        self.cmd_msg = Twist2DStamped()

        rospy.loginfo("Node started successfully")
        rospy.loginfo("Waiting 2 seconds before starting movement...")
        rospy.sleep(2.0)

        self.move_robot()

    def publish_cmd(self, v, omega):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = v
        self.cmd_msg.omega = omega
        self.pub.publish(self.cmd_msg)

    def stop_robot(self):
        self.publish_cmd(0.0, 0.0)
        rospy.loginfo("Robot stopped")

    def move_forward(self, duration, speed=0.25):
        rospy.loginfo(f"Moving forward for {duration:.1f} seconds at speed {speed}")
        rate = rospy.Rate(20)
        start_time = rospy.Time.now()

        while (rospy.Time.now() - start_time).to_sec() < duration and not rospy.is_shutdown():
            self.publish_cmd(speed, 0.0)
            rate.sleep()

        self.stop_robot()
        rospy.sleep(0.5)

    def turn_in_place(self, duration, omega=3.0):
        rospy.loginfo(f"Turning in place for {duration:.1f} seconds at omega {omega}")
        rate = rospy.Rate(20)
        start_time = rospy.Time.now()

        while (rospy.Time.now() - start_time).to_sec() < duration and not rospy.is_shutdown():
            self.publish_cmd(0.0, omega)
            rate.sleep()

        self.stop_robot()
        rospy.sleep(0.5)

    def move_robot(self):
        rospy.loginfo("Starting square movement")

        for side in range(1, 5):
            rospy.loginfo(f"--- Side {side} of 4 ---")
            self.move_forward(duration=2.0, speed=0.25)
            self.turn_in_place(duration=1.3, omega=3.0)

        rospy.loginfo("Square completed successfully")
        self.stop_robot()

    def run(self):
        rospy.spin()


if __name__ == "__main__":
    try:
        node = DriveSquare()
        node.run()
    except rospy.ROSInterruptException:
        pass
