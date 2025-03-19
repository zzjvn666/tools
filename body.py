# -*- coding: utf-8 -*-
import time
import rclpy
from rclpy.node import Node
from ai_msgs.msg import PerceptionTargets

class Mono2DBodySubscriber(Node):
    def __init__(self):
        super().__init__('mono2d_body_subscriber')

        self.subscription = self.create_subscription(
            PerceptionTargets,
            '/hobot_mono2d_body_detection',
            self.listener_callback,
            10
        )
        self.latest_msg = None  # 存储最新的消息
        self.timer = self.create_timer(1.0, self.print_latest_data)  # 每 60 秒触发

    def listener_callback(self, msg):
        
        self.latest_msg = msg

    def print_latest_data(self):
        
        if self.latest_msg is None:
            self.get_logger().info("No data received yet.")
            return

        msg = self.latest_msg
        self.get_logger().info(f'Latest data: {len(msg.targets)} targets')

        for i, target in enumerate(msg.targets):
            print(f"\n?? Target {i+1}: Type = {target.type}, Track ID = {target.track_id}")

            # 打印ROI信息（检测框）
            for roi in target.rois:
                print(f"  - ROI Type: {roi.type}, X: {roi.rect.x_offset}, Y: {roi.rect.y_offset}, Width: {roi.rect.width}, Height: {roi.rect.height}, Confidence: {roi.confidence}")

            # 打印关键点信息
            if target.points:
                for j, point_data in enumerate(target.points):  # 遍历多个 `Point` 类型
                    print(f"  - Point Set {j+1}: Type = {point_data.type}")
                    for k, point in enumerate(point_data.point):
                        print(f"    - Keypoint {k+1}: X = {point.x}, Y = {point.y}")

        print("\n" + "="*50)  # 美化输出

def main(args=None):
    rclpy.init(args=args)
    node = Mono2DBodySubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
