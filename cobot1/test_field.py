# test_field.py
import time

import rclpy
import DR_init

from cobot1.initialize_ops import initialize_robot
from cobot1.config import ROBOT_ID, ROBOT_MODEL, ROBOT_TOOL, ROBOT_TCP, VELOCITY, ACC, JReady
from cobot1.motions.close_cover_ops import close_lid
from cobot1.motions.open_cover_ops import open_lid
from cobot1.motions.cup_ops import cup1, cup2, cup3, get_shared_cup_positions
from cobot1.motions.shaking_ops import shaking
from cobot1.motions.pouring_ops import last_pouring
from cobot1.motions.colander_ops import colander_operations
from cobot1.motions.colander_reverse_ops import colander_reverse_operations
from cobot1.motions.gripper_ops import release, grip_shaking_cup, grip_cup, grip_cover_cap, release1
from cobot1.motions.hello_ops import hello

# DR_init 기본 모델 설정
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL



def perform_task():
    """작업 시퀀스 실행"""
    from DSR_ROBOT2 import movej, amovel, posx, get_current_posx, movesj, posj
    from cobot1.config import VELOCITY, ACC, JReady
    
    release()
    movej(JReady, vel=VELOCITY, acc=ACC)
    cup3()
    


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("move_basic", namespace=ROBOT_ID)

    # 핵심: 이 할당이 끝난 이후에 각 함수들이 실행되면서 DSR_ROBOT2를 임포트하게 됩니다.
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        perform_task()
    except KeyboardInterrupt:
        print("\nNode interrupted by user. Shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        rclpy.shutdown()

if __name__ == "__main__":
    main()