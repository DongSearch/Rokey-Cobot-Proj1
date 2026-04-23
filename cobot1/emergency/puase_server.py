# pause_server.py
import rclpy
import DR_init

from cobot1.initialize_ops import initialize_robot
from cobot1.config import ROBOT_ID, ROBOT_MODEL, ROBOT_TOOL, ROBOT_TCP, VELOCITY, ACC, JReady

# DR_init 기본 모델 설정
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

def pause():
    """로봇을 일시 정지하는 함수"""
    from DSR_ROBOT2 import MovePause
    print("Pausing the robot...")
    MovePause()

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("move_basic", namespace=ROBOT_ID)

    # 핵심: 이 할당이 끝난 이후에 각 함수들이 실행되면서 DSR_ROBOT2를 임포트하게 됩니다.
    DR_init.__dsr__node = node

    node.create_subscription()

    try:
        initialize_robot()
        pause()
    except KeyboardInterrupt:
        print("\nNode interrupted by user. Shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()