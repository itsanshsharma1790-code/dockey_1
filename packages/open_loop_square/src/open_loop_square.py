
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
        for i in range(4):
            # move straight
            self.cmd_msg.header.stamp = rospy.Time.now()
            self.cmd_msg.v = 0.3
            self.cmd_msg.omega = 0.0
            self.pub.publish(self.cmd_msg)
            rospy.loginfo("Forward")
            rospy.sleep(2.0)

            # stop briefly
            self.stop_robot()
            rospy.sleep(0.5)

            # turn in place
            self.cmd_msg.header.stamp = rospy.Time.now()
            self.cmd_msg.v = 0.0
            self.cmd_msg.omega = 2.0
            self.pub.publish(self.cmd_msg)
            rospy.loginfo("Turning")
            rospy.sleep(1.0)

            # stop briefly
            self.stop_robot()
            rospy.sleep(0.5)
                
        self.stop_robot()

if __name__ == '__main__':
    try:
        duckiebot_movement = Drive_Square()
        duckiebot_movement.run()
    except rospy.ROSInterruptException:
        pass
