#!/usr/bin/env python

from std_msgs.msg import String
import rospy
import re

current_wp = None
wp_cnt = 0

def get_target(s):
    n = re.findall('Target: \((.+?)\),', s)
    if len(n) > 0:
        x, y, z = re.split(', ', n[0])
        return (float(x), float(y), float(z))
    else:
        return None 

def str_target(target):
    x, y, z = target
    return '(' + str(x) + ', ' + str(y) + ', ' + str(z) + ')'

def print_wp(msg):
    global current_wp
    global wp_cnt

    target = get_target(msg.data)
    if not target is None:
        if current_wp is None:
            current_wp = target
            print str(wp_cnt) + ': ' + str_target(current_wp)
        else:
            if target != current_wp:
                wp_cnt += 1
                current_wp = target
                print str(wp_cnt) + ': ' + str_target(current_wp)

if __name__ == "__main__":
    rospy.init_node('print_wps')
    rospy.Subscriber('/tum_ardrone/com', String, print_wp)
    rospy.spin()
