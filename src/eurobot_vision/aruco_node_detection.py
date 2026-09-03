#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ArucoDetector(Node):
    def __init__(self):
        super().__init__("aruco_detection_node")
        self.get_logger().info("ArUco node has successfully started!")
        
        self.subscription = self.create_subscription(
            Image, 
            'camera/image_raw', 
            self.image_callback, 
            10
        )
        
        self.bridge = CvBridge()
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        
        # Use the legacy parameter creation method for older OpenCV versions
        self.parameters = cv2.aruco.DetectorParameters_create()

    def image_callback(self, msg: Image):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"CvBridge Error: {e}")
            return

        if frame is None or frame.size == 0:
            self.get_logger().warn("Received empty frame!")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Pass the NumPy array (gray), not the ROS message
        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(
            gray, self.dictionary, parameters=self.parameters
        )
        
        if marker_ids is not None and len(marker_ids) > 0:
            ids_flat = marker_ids.flatten()
            
            combined = []
            for i, marker_id in enumerate(ids_flat):
                corners = marker_corners[i][0] 
                center_x = np.mean(corners[:, 0])
                combined.append((center_x, marker_id, marker_corners[i]))
            
            combined.sort(key=lambda x: x[0])
            
            sorted_ids = [item[1] for item in combined]
            sorted_corners = [item[2] for item in combined]
            
            self.get_logger().info(f"Left-to-Right Markers: {sorted_ids}")
            
            cv2.aruco.drawDetectedMarkers(frame, sorted_corners, np.array(sorted_ids))

def main(args=None):
    rclpy.init(args=args)
    node = ArucoDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown() 

if __name__ == '__main__':
    main()