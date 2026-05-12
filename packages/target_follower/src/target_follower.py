#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import AprilTagDetectionArray

class Target_Follower:
    def __init__(self):
        rospy.init_node('target_follower_node', anonymous=True)
        rospy.on_shutdown(self.clean_shutdown)

        self.cmd_vel_pub = rospy.Publisher(
            '/mybota002410/car_cmd_switch_node/cmd',
            Twist2DStamped,
            queue_size=1
        )

        rospy.Subscriber(
            '/mybota002410/apriltag_detector_node/detections',
            AprilTagDetectionArray,
            self.tag_callback,
            queue_size=1
        )

        rospy.loginfo("Target follower started")
        rospy.spin()

    def tag_callback(self, msg):
        self.move_robot(msg.detections)

    def clean_shutdown(self):
        rospy.loginfo("System shutting down. Stopping robot...")
        self.stop_robot()

    def stop_robot(self):
        cmd_msg = Twist2DStamped()
        cmd_msg.header.stamp = rospy.Time.now()
        cmd_msg.v = 0.0
        cmd_msg.omega = 0.0
        self.cmd_vel_pub.publish(cmd_msg)

    def clamp(self, value, min_value, max_value):
        return max(min(value, max_value), min_value)

    def move_robot(self, detections):
        cmd_msg = Twist2DStamped()
        cmd_msg.header.stamp = rospy.Time.now()

        if len(detections) == 0:
            rospy.loginfo("No tag detected. Stopping.")
            self.stop_robot()
            return

        tag = detections[0]

        x = tag.transform.translation.x
        y = tag.transform.translation.y
        z = tag.transform.translation.z
        tag_id = tag.tag_id

        rospy.loginfo("Tag ID: %d | x: %.3f y: %.3f z: %.3f", tag_id, x, y, z)

        # x controls left/right alignment
        # z controls distance from tag

        # -------- angular control --------
        k_omega = 3.0
        omega = -k_omega * x

        # minimum turn to overcome friction
        if abs(omega) < 0.25 and abs(x) > 0.03:
            omega = 0.25 if omega > 0 else -0.25

        omega = self.clamp(omega, -1.5, 1.5)

        # -------- linear control --------
        desired_distance = 0.45
        distance_error = z - desired_distance

        k_v = 0.6
        v = k_v * distance_error

        # dead zone: stop forward/back if close enough
        if abs(distance_error) < 0.08:
            v = 0.0

        v = self.clamp(v, -0.25, 0.25)

        cmd_msg.v = v
        cmd_msg.omega = omega

        rospy.loginfo("Command | v: %.3f omega: %.3f", v, omega)
        self.cmd_vel_pub.publish(cmd_msg)

if __name__ == '__main__':
    try:
        target_follower = Target_Follower()
    except rospy.ROSInterruptException:
        pass
