#!/usr/bin/env python3
import rospy
from duckietown_msgs.msg import Twist2DStamped
from duckietown_msgs.msg import FSMState

class Drive_Square:
    def __init__(self):
        self.cmd_msg = Twist2DStamped()
        rospy.init_node('drive_square_node', anonymous=True)
        
        self.pub = rospy.Publisher('/akandb/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=1)
        rospy.Subscriber('/akandb/fsm_node/mode', FSMState, self.fsm_callback, queue_size=1)
        
    def fsm_callback(self, msg):
        rospy.loginfo("State: %s", msg.state)
        if msg.state == "NORMAL_JOYSTICK_CONTROL":
            self.stop_robot()
        elif msg.state == "LANE_FOLLOWING":            
            rospy.sleep(1)
            self.move_robot()

    def stop_robot(self):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.0
        self.cmd_msg.omega = 0.0
        self.pub.publish(self.cmd_msg)

    def run(self):
        rospy.spin()

    def move_robot(self):
        # Drive a square: repeat (go straight + turn 90°) 4 times
        for _ in range(4):
            # --- Go straight for ~1 meter ---
            self.cmd_msg.header.stamp = rospy.Time.now()
            self.cmd_msg.v = 0.5        # forward velocity (m/s)
            self.cmd_msg.omega = 0.0
            self.pub.publish(self.cmd_msg)
            rospy.loginfo("Driving straight...")
            rospy.sleep(2.0)            # tune this so robot travels ~1 meter

            self.stop_robot()
            rospy.sleep(0.5)            # brief pause before turning

            # --- Turn 90 degrees in place ---
            self.cmd_msg.header.stamp = rospy.Time.now()
            self.cmd_msg.v = 0.0
            self.cmd_msg.omega = 1.5    # angular velocity (rad/s)
            self.pub.publish(self.cmd_msg)
            rospy.loginfo("Turning 90 degrees...")
            rospy.sleep(1.05)           # tune this: ~pi/2 / omega = 1.047s at 1.5 rad/s

            self.stop_robot()
            rospy.sleep(0.5)            # brief pause before next side

        self.stop_robot()
        rospy.loginfo("Square complete!")

if __name__ == '__main__':
    try:
        duckiebot_movement = Drive_Square()
        duckiebot_movement.run()        # <-- fixed: use run(), not move_robot()
    except rospy.ROSInterruptException:
        pass
