#!/usr/bin/env python

from wifi_logger.msg import Quality
import subprocess
import rospy
import re

def contains(s, ss):
    return re.search(ss, s)

def extract_val(s, ss):
    return re.findall(ss+'=(.+?) ', s)[0]

def get_link_quality(s):
    lq = re.split('/', extract_val(s, 'Link Quality'))
    return int(lq[0]), int(lq[1])

def get_signal_level(s):
    return int(extract_val(s, 'Signal level'))

def get_noise_level(s):
    return int(extract_val(s, 'Noise level'))

def poll():
    proc = subprocess.Popen(["iwconfig", "wlan0"], stdout=subprocess.PIPE, universal_newlines=True)
    out, _ = proc.communicate()

    quality = Quality()
    quality.stamp = rospy.Time.now()

    if contains(out, 'Link Quality'):
        quality.link_quality_num = get_link_quality(out)[0]
        quality.link_quality_den = get_link_quality(out)[1]

    if contains(out, 'Signal level'):
        quality.signal_level = get_signal_level(out)

    if contains(out, 'Noise level'):
        quality.noise_level = get_noise_level(out)

    return quality

def logger():
    rospy.init_node('wifi_logger', anonymous=True)
    pub = rospy.Publisher('channel_quality', Quality, queue_size=100)
    rate = rospy.Rate(500)

    while not rospy.is_shutdown():
        pub.publish(poll())
        rate.sleep()

if __name__ == "__main__":
    logger()
