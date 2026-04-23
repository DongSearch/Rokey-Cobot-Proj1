import rclpy
import DR_init
import time
from dsr_msgs2.srv import GetRobotState

# 추가: ROS 2 표준 메시지 타입 임포트
from std_msgs.msg import String, Int32 

# 로봇 설정 (환경에 맞게 수정)
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
ROBOT_TOOL = "Tool Weight"
ROBOT_TCP = "GripperDA_v1"
# 이동 속도 및 가속도 (필요에 따라 수정)
VELOCITY = 40
ACC = 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

# ---------------------------------------------------------
# 로봇 상태 코드 매핑 테이블 (매뉴얼 기준)
# ---------------------------------------------------------
ROBOT_STATE_MAP = {
    0: "STATE_INITIALIZING (초기화 중)",
    1: "STATE_STANDBY (대기 중 - 정상)",
    2: "STATE_MOVING (이동 중)",
    3: "STATE_SAFE_OFF (서보 꺼짐)",
    4: "STATE_TEACHING (티칭 모드)",
    5: "STATE_SAFE_STOP (안전 정지 - 외부 충격 등)",
    6: "STATE_EMERGENCY_STOP (비상 정지)",
    7: "STATE_HOMMING (호밍 중)",
    8: "STATE_RECOVERY (복구 모드)",
    9: "STATE_SAFE_STOP2 (안전 정지 2)",
    10: "STATE_SAFE_OFF2 (서보 꺼짐 2)",
    11: "STATE_RESERVED1",
    12: "STATE_RESERVED2",
    13: "STATE_RESERVED3",
    14: "STATE_RESERVED4",
    15: "STATE_NOT_READY (준비 안 됨)"
}

def initialize_robot():
    """로봇의 Tool과 TCP를 설정"""
    from DSR_ROBOT2 import set_tool, set_tcp, get_tool, get_tcp, ROBOT_MODE_MANUAL, ROBOT_MODE_AUTONOMOUS
    from DSR_ROBOT2 import get_robot_mode, set_robot_mode

    # Tool과 TCP 설정시 매뉴얼 모드로 변경해서 진행
    set_robot_mode(ROBOT_MODE_MANUAL)
    set_tool(ROBOT_TOOL)
    set_tcp(ROBOT_TCP)
    
    set_robot_mode(ROBOT_MODE_AUTONOMOUS)
    time.sleep(2)  # 설정 안정화를 위해 잠시 대기
    
    # 설정된 상수 출력
    print("#" * 50)
    print("Initializing robot with the following settings:")
    print(f"ROBOT_ID: {ROBOT_ID}")
    print(f"ROBOT_MODEL: {ROBOT_MODEL}")
    print(f"ROBOT_TCP: {get_tcp()}") 
    print(f"ROBOT_TOOL: {get_tool()}")
    print(f"ROBOT_MODE 0:수동, 1:자동 : {get_robot_mode()}")
    print(f"VELOCITY: {VELOCITY}")
    print(f"ACC: {ACC}")
    print("#" * 50)

def perform_task(node):
    """로봇 상태 모니터링 및 토픽 발행"""
    print("Performing task...")
    from DSR_ROBOT2 import get_robot_state

    # 1. Publisher 생성
    # 상태 코드(숫자)와 상태 설명(문자열)을 각각 발행하기 위해 두 개의 퍼블리셔 생성
    state_code_pub = node.create_publisher(Int32, f'/{ROBOT_ID}/robot_state_code', 10)
    state_desc_pub = node.create_publisher(String, f'/{ROBOT_ID}/robot_state_desc', 10)

    print(f"[{ROBOT_ID}] 로봇 상태 모니터링 및 토픽 발행 시작")
    print("ros2 topic echo /dsr01/robot_state_code")
    print("ros2 topic echo /dsr01/robot_state_desc")
    print("=" * 60)

    # 2. while True 대신 rclpy.ok()를 사용하여 ROS 노드 종료 신호(Ctrl+C 등)에 안전하게 대비
    while rclpy.ok():
        # 상태값 조회 및 매핑
        state_code = get_robot_state()
        state_desc = ROBOT_STATE_MAP.get(state_code, "UNKNOWN_STATE (알 수 없음)")
        
        # 터미널 출력용 강조 표시
        prefix = ">>>"
        if state_code in [5, 6, 9]: # 정지/비상 상황
            prefix = "!!!"
        elif state_code in [3, 10]: # 서보 꺼짐
            prefix = "***"

        # print(f"{prefix} Current Robot State: [{state_code}] -> {state_desc}")

        # 3. 토픽 데이터 구성 및 발행 (Publish)
        # 숫자 상태 코드 발행
        msg_code = Int32()
        msg_code.data = int(state_code)
        state_code_pub.publish(msg_code)

        # 문자열 상태 설명 발행
        msg_desc = String()
        msg_desc.data = state_desc
        state_desc_pub.publish(msg_desc)

        # 0.5초 간격으로 반복
        time.sleep(0.5) 

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("check_robot_state", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    try:
        initialize_robot()
        
        # node 객체를 perform_task 함수로 전달하여 퍼블리셔를 생성할 수 있게 함
        perform_task(node)

    except KeyboardInterrupt:
        print("\nNode interrupted by user. Shutting down...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 종료 처리
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()