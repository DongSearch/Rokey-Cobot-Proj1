# main.py
from cobot1.motions.gripper_ops import release
import rclpy
import DR_init

from cobot1.initialize_ops import initialize_robot
from cobot1.config import ROBOT_ID, ROBOT_MODEL, ROBOT_TOOL, ROBOT_TCP, VELOCITY, ACC, JReady
from cobot1.motions.close_cover_ops import close_lid
from cobot1.motions.open_cover_ops import open_lid
from cobot1.motions.cup_ops import cup1, cup2, cup3
from cobot1.motions.shaking_ops import shaking
from cobot1.motions.pouring_ops import last_pouring
from cobot1.motions.colander_ops import colander_operations
from cobot1.motions.colander_reverse_ops import colander_reverse_operations

from std_msgs.msg import String
import json

# DR_init 기본 모델 설정
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

#설정
status = None

def cmd_callback(msg):
    global status
    print(f"제조시작: {msg.data}")
    try :
        status = json.loads(msg.data)
    except:
        status = msg.data


def perform_task(publisher):
    global status
    from DSR_ROBOT2 import wait, movej

    def send_status(step, percent):
        msg = String()
        data = {
            "process": step,
            "progress": percent
        }
        msg.data = json.dumps(data)
        publisher.publish(msg)

    """작업 시퀀스 실행"""
    print("Performing task...")
    release()
    movej(JReady, vel=VELOCITY, acc=ACC)

    send_status("cup3", 10)
    cup3()
    send_status("cup2", 20)
    cup2()
    send_status("cup1", 30)
    cup1()
    movej(JReady, vel=VELOCITY, acc=ACC)
    send_status("close_lid", 40)
    close_lid()
    movej(JReady, vel=VELOCITY, acc=ACC)
    send_status("shaking", 50)
    shaking()
    movej(JReady, vel=VELOCITY, acc=ACC)
    send_status("colander_operations", 60)
    colander_operations()
    movej(JReady, vel=VELOCITY, acc=ACC)
    send_status("open_lid", 70)
    open_lid()
    movej(JReady, vel=VELOCITY, acc=ACC)
    send_status("last_pouring", 80)
    last_pouring()
    send_status("colander_reverse_operations", 90)
    colander_reverse_operations()
    movej(JReady, vel=VELOCITY, acc=ACC)
    send_status("done", 100)
    wait(3)
    status = None


def main(args=None):
    global status
    rclpy.init(args=args)
    node = rclpy.create_node("main_node", namespace=ROBOT_ID)

    # 핵심: 이 할당이 끝난 이후에 각 함수들이 실행되면서 DSR_ROBOT2를 임포트하게 됩니다.
    DR_init.__dsr__node = node
    initialize_robot()
    node.create_subscription(
        String,
        "robot_cmd",
        cmd_callback,
        10
    )

    publisher = node.create_publisher(
        String,
        "robot_pub",
        10
    )

    try:
        # while rclpy.ok():
            # rclpy.spin_once(node, timeout_sec=0.1)

            # if isinstance(status,dict):
        perform_task(publisher)


    except KeyboardInterrupt:
        print("\nNode interrupted by user. Shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()