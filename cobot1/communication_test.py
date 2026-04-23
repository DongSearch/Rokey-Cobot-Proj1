import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.create_subscription(
            String,
            '/robot_cmd',
            self.callback,
            10
        )

    def callback(self, msg):
        data = json.loads(msg.data)

        menu = data["menu"]
        opt = data["opt"]

        self.get_logger().info(f"주문: {menu}, 옵션: {opt}")

        # 👉 여기서 로봇 분기
        if menu == "MOJITO":
            self.make_mojito()

    def make_mojito(self):
        self.get_logger().info("🍸 모히토 제조 시작")


# 🔥 이게 없으면 실행 안됨
def main(args=None):
    rclpy.init(args=args)

    node = RobotController()

    try:
        rclpy.spin(node)   # 계속 대기하면서 메시지 받음
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


# 🔥 파이썬 직접 실행용
if __name__ == '__main__':
    main()