#!/usr/bin/env python
"""
enable and configure webots robot sensors

The namespace is specified by vehicle | controllerArgs --name=webots
./sensor_setup.py __ns:=/webots

"""

import rospy
from webots_ros.srv import (
    set_bool,
    set_int,
)


class WebotsSensorSetup:
    def __init__(self):
        """
        gps position will appear on "gps/values" geometry_msgs/PointStamped
        imu on inertial_unit/quaternion sensor_msgs/Imu
        camera camera/image sensor_msgs/Image and also a camera_info

        the set_gear 1 will make automobile/set_throttle work for going forward
        """

        enable_services = {
            "gps/enable": 64,
            "inertial_unit/enable": 64,
            "camera/enable": 64,
            "automobile/set_gear": 1,  # this doesn't really belong here but it's convenient for quick setup
            "lidar/enable": 64,
        }

        for enable_service, sample_period in enable_services.items():
            rospy.wait_for_service(enable_service)
            enable_proxy = rospy.ServiceProxy(enable_service, set_int)
            rv = enable_proxy(value=sample_period)
            rospy.loginfo(f"{enable_service} {sample_period}: {rv}")

        bool_enable_services = {
            "lidar/enable_point_cloud": True,
        }
        for enable_service, value in bool_enable_services.items():
            enable_service = "lidar/enable_point_cloud"
            rospy.wait_for_service(enable_service)
            enable_proxy = rospy.ServiceProxy(enable_service, set_bool)
            rv = enable_proxy(value=value)
            rospy.loginfo(f"{enable_service}: {rv}")


def main():
    rospy.init_node("webots_sensor_setup")
    _ = WebotsSensorSetup()


if __name__ == "__main__":
    main()
