#!/usr/bin/env python

import rospy
import smach_ros
import smach
from naoqi_bridge_msgs.msg import HeadTouch
from std_msgs.msg import String

class onTouch(smach.State):
    """ A module to detect if pepper's head is touched
    """
    def __init__(self):	
        smach.State.__init__(self, outcomes = ['touched','not_touched'])

    
    def execute(self, userdata):
	#pub = rospy.Publisher('/pepper_robot/head_touch', HeadTouch, queue_size=1)
        
	rospy.Subscriber("/pepper_robot/head_touch", HeadTouch)
	if (HeadTouch.state==1):
	    rospy.loginfo('touch detected')
	    return 'touched'
	
class sayHi(smach.State):
    ''' give a speech
    '''
    def __init__(self):	
        smach.State.__init__(self, outcomes = ['succeeded'])
    def execute(self, userdata):
	pub = rospy.Publisher('/speech', String, queue_size=1)
	hello_str = "ich bin pepper, mein Kopf wird angefasst."
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        #rate.sleep()
	return 'succeeded'
	
	    
	
        

def main():
    rospy.init_node('smach_touch_react')
    rate = rospy.Rate(10)
    sm_root = smach.StateMachine(outcomes=['success'])

    with sm_root:

        smach.StateMachine.add('ON_TOUCH', onTouch(), transitions={'not_touched':'SAY_HI', 'touched':'SAY_HI'})
	smach.StateMachine.add('SAY_HI', sayHi(), transitions={'succeeded':'SAY_HI'})

    # Execute SMACH plan
    sis = smach_ros.IntrospectionServer('sm_light', sm_root, '/SM_ROOT')
    sis.start()
    # Execute SMACH plan
    outcome = sm_root.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()
if __name__ == '__main__':
    main()
