import rclpy
from rclpy.node import Node

import firebase_admin
from firebase_admin import credentials, firestore

from std_msgs.msg import Int32
import time


class DBConnection(Node):

    def __init__(self):
        super().__init__('firebase_bridge')

        cred = credentials.Certificate(
            "/home/gidong/cobot_ws/serviceAccountKey.json"
        )
        if not firebase_admin._apps:
          firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.db_robot = self.db.collection("cocktail_robot")
        self.db_web = self.db.collection("cocktail_web")
        self.db_history = self.db.collection("history")

        self.start = 0

        # 상태
        self.status_data = {
            "order_num": 0,
            "step_index": 0,
            "is_busy": False,
            "progress": 0,
            "process": "Idle"
        }

        self.order_data = {}
        self.order_ref = None
        self.order_num = 0

        self.timer = self.create_timer(1.0, self.check_orders)

        self.status_subscriber = self.create_subscription(
            Int32,
            "dsr01/robot_status",
            self.robot_status_listener_callback,
            10
        )

        self.start_publisher = self.create_publisher(
            Int32,
            "dsr01/robot_start",
            10
        )
        self.create_timer(1,self.start_publish)

        self.prev_status = None
        self.prev_order = None
        self.last_db_time = 0
    
    def start_publish(self) :
        msg = Int32()
        msg.data = self.start
        self.start_publisher.publish(msg)


    # =========================
    # ROBOT STATUS
    # =========================
    def robot_status_listener_callback(self, msg):
        status = msg.data

        self.status_data["step_index"] = status
        self.status_data["order_num"] = self.order_num

        # order 없으면 보호
        if not self.order_data:
            return

        self.order_data["status"] = "in process"

        if status == 0:
            self.order_data["started_at"] = firestore.SERVER_TIMESTAMP
            self.status_data.update({"progress": 0, "process": "시작 대기"})
        elif status == 1:
            self.status_data.update({"progress": 10, "process": "컵1"})
        elif status == 2:
            self.status_data.update({"progress": 20, "process": "컵2"})
        elif status == 3:
            self.status_data.update({"progress": 30, "process": "컵3"})
        elif status == 4:
            self.status_data.update({"progress": 40, "process": "뚜껑 닫기"})
        elif status == 5:
            self.status_data.update({"progress": 50, "process": "쉐이킹"})
        elif status == 6:
            self.status_data.update({"progress": 80, "process": "뚜껑 열기"})
        elif status == 7:
            self.status_data.update({"progress": 90, "process": "필터링"})
        elif status == 8:
            self.status_data.update({"progress": 95, "process": "마지막"})
        elif status == 9:
            self.status_data.update({"progress": 100, "process": "완료"})
            self.order_data["finished_at"] = firestore.SERVER_TIMESTAMP
            self.start = 0

            # 순서 중요
            self.move_history()
            self.reset_order()

        self.send_db()

    # =========================
    # ORDER CHECK
    # =========================
    def check_orders(self):
        if self.status_data["is_busy"]:
            return

        if not self.status_data["is_busy"] :
            orders = self.db_web \
                .where("status", "==", "waiting") \
                .order_by("order_num") \
                .limit(1) \
                .get()

            for order in orders:
                data = order.to_dict()

                self.get_logger().info(f"주문 받음: {data}")
                self.start = 1

                self.order_ref = order.reference
                self.order_data = data

                self.order_num = data.get("order_num", 0)

                # 🔥 핵심: 먼저 lock
                self.status_data["is_busy"] = True

                # DB 상태 변경
                self.order_ref.update({"status": "in process"})

                break  # 1개만 처리

    # =========================
    # HISTORY
    # =========================
    def move_history(self):
        if not self.order_data:
            return

        self.order_data["status"] = "done"

        self.db_history.add(self.order_data)

        if self.order_ref:
            self.order_ref.delete()

    # =========================
    # RESET
    # =========================
    def reset_order(self):
        self.order_data = {}
        self.order_ref = None
        self.order_num = 0
        self.status_data["is_busy"] = False

    # =========================
    # DB UPDATE
    # =========================


    def send_db(self):
        now = time.time()

        if now - self.last_db_time < 1.0:
            return

        self.last_db_time = now

        self.db_robot.document("status").set(self.status_data)
        self.db_robot.document("order").set(self.order_data)

        self.order_data.pop("started_at", None)
        self.order_data.pop("finished_at", None)


def main():
    rclpy.init()
    node = DBConnection()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
