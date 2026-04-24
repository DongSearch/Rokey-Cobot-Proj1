# main.py

import threading
import rclpy
import time
import DR_init
from rclpy.executors import SingleThreadedExecutor
from std_srvs.srv import Trigger
from dsr_msgs2.srv import MoveStop


from cobot1.initialize_ops import initialize_robot
from cobot1.config import ROBOT_ID, ROBOT_MODEL, VELOCITY, ACC, JReady
from cobot1.motions.close_cover_ops import close_lid
from cobot1.motions.open_cover_ops import open_lid
from cobot1.motions.cup_ops import cup1, cup2, cup3
from cobot1.motions.shaking_ops import shaking
from cobot1.motions.pouring_ops import last_pouring
from cobot1.motions.colander_ops import colander_operations
from cobot1.motions.colander_reverse_ops import colander_reverse_operations
from cobot1.motions.gripper_ops import release
from cobot1.motions.stanby_ops import stanby
from cobot1.motions.hello_ops import hello
from dsr_msgs2.srv import SetRobotControl # ★ 핵심: 제어 상태 강제 변환 서비스


from std_msgs.msg import Int32

# DR_init 설정
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

CONTROL_RESET_SAFE_STOP = 2  # 보호 정지 해제
CONTROL_RESET_SAFE_OFF = 3   # 서보 켜기 (Safe Off -> Standby)

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

def call_set_robot_control(control_value):
    """로봇 제어 상태를 강제로 리셋하거나 변경하는 함수"""
    node = DR_init.__dsr__node
    srv_name = f'/{ROBOT_ID}/system/set_robot_control'
    cli = node.create_client(SetRobotControl, srv_name)
    
    if not cli.wait_for_service(timeout_sec=1.0):
        print(f"[Err] {srv_name} 서비스를 찾을 수 없습니다.")
        return False

    req = SetRobotControl.Request()
    req.robot_control = control_value
    
    future = cli.call_async(req)
    
    # 결과 대기 (블로킹 없이 처리하기 위해 spin_once 사용)
    start_wait = time.time()
    while not future.done():
        rclpy.spin_once(node, timeout_sec=0.01)
        
        # [수정] 타임아웃을 3.0초 -> 5.0초로 증가 (컨트롤러 처리 지연 대비)
        if time.time() - start_wait > 5.0: 
            print("[Err] 서비스 호출 시간 초과 (컨트롤러 응답 지연)")
            return False

    try:
        res = future.result()
        return res.success
    except Exception as e:
        print(f"[Err] 서비스 호출 실패: {e}")
        return False
# ======================
# 🔥 전역 상태
# ======================
status = 0
step = 0 # 실행 안할 시 -1로 설정 할 것

global_robot_state = None
global_error_publisher = None

global_recovery_start = False
global_recovery_finished = False
global_recovery_success = False

global_pass_start = False
global_pass_finished = False
global_pass_success = False

# ======================
# 📡 ROS 콜백
# ======================
def cmd_callback(msg):
    global status
    status = msg.data

# ======================
# 📡 상태 함수
# ======================
def check_robot_state():
    from DSR_ROBOT2 import get_robot_state
    global global_error_publisher, global_recovery_start, global_recovery_finished, global_recovery_success
    global global_pass_start, global_pass_finished, global_pass_success
    state = get_robot_state()
    print("현재 로봇 상태 코드:", state)
    while True:
        state = get_robot_state()
        if state == 5:   # SAFE_STOP
            print("🚨 충돌 감지! 작업 중단")
            print("   -> 상태 코드 5 (안전 정지) 퍼블리시")
            global_error_publisher.publish(Int32(data=5))  # 상태 코드 5 (안전 정지) 퍼블리시
            
            print("   -> 복구 신호 대기 중...")
            # while global_recovery_start == False:
            #     time.sleep(0.1)  # 복구 시작 신호 대기
            time.sleep(3)
            print("   -> 복구 신호 수신! 복구 작업 시작")
            if recovery_action():  # 복구 작업 실행
                print("   -> 복구 성공! 작업 재개")
                global_recovery_success = True
                global_recovery_finished = True  # 복구 완료 신호 설정

                # while global_pass_start == False: # 복구 성공 후 패스 신호 대기
                #     time.sleep(0.1)  # 패스 시작 신호 대기
                time.sleep(3)
                print("   -> 패스 신호 수신! 패스 작업 시작")
                pass_action()  # 패스 작업 실행
                global_pass_success = True
                global_pass_finished = True  # 패스 완료 신호 설정


        elif state == 3: # SAFE_OFF
            print("⚠️ 서보 꺼짐 감지! 작업 중단")
            print("   -> 상태 코드 3 (서보 꺼짐) 퍼블리시")
            global_error_publisher.publish(Int32(data=3))  # 상태 코드 3 (서보 꺼짐) 퍼블리시

            print("   -> 복구 신호 대기 중...")
            # while global_recovery_start == False:
            #     time.sleep(0.1)  # 복구 시작 신호 대기
            time.sleep(3)
            print("   -> 복구 신호 수신! 복구 작업 시작")
            if recovery_3_action():  # 복구 작업 실행
                print("   -> 서보 ON 복구 성공! 작업 재개")
                global_recovery_success = True
                global_recovery_finished = True  # 복구 완료 신호 설정

                # while global_pass_start == False: # 복구 성공 후 패스 신호 대기
                #     time.sleep(0.1)  # 패스 시작 신호 대기
                time.sleep(3)
                print("   -> 패스 신호 수신! 패스 작업 시작")
                pass_action()  # 패스 작업 실행
                global_pass_success = True
                global_pass_finished = True  # 패스 완료 신호 설정
            else:
                print("   -> 서보 ON 복구 실패! 수동 조치 필요")
                global_recovery_success = False
                global_recovery_finished = True  # 복구 시도는 했으나 실패했으므로 일단 완료 신호 설정 (수동 조치 필요)
            
        elif state == 6: # EMERGENCY_STOP
            print("🚨 비상 정지 감지! 작업 중단")
            print("   -> 상태 코드 6 (비상 정지) 퍼블리시")
            global_error_publisher.publish(Int32(data=6))  # 상태 코드 6 (비상 정지) 퍼블리시
            print("   -> 비상 정지 상태 유지 중...")
            while get_robot_state() == 6:
                time.sleep(0.1)  # 비상 정지 상태 유지 대기
            print("   -> 비상 정지 해제 감지! 수동으로 복구 후 작업 재개 가능")
            print("현재 로봇 상태 코드:", get_robot_state())
        
        elif state == 1:
            print("✅ 로봇 정상 상태")
            break  # 정상 상태로 돌아오면 루프 종료
        time.sleep(0.1)  # 상태 체크 간격
        


# ======================
# 🤖 로봇 작업
# ======================
def perform_task():
    global step, global_robot_state

    from DSR_ROBOT2 import wait, movej, get_robot_state

    print("🚀 Performing task...")
    msg = Int32()
    
    


    while step <= 9:
        msg.data = step 
        global_robot_state.publish(msg)
        if step == 0:
            print("Step 0: 시작 위치로 이동")
            release()
            movej(JReady, vel=VELOCITY, acc=ACC)
            step = 1
            print("✅ Step 0 완료: 초기 위치로 이동")
            check_robot_state()

        elif step == 1:
            print("Step 1: 컵 작업 시작")
            cup3()
            step = 2
            print("✅ Step 1 완료: 컵 작업 완료")
            check_robot_state()


        elif step == 2:
            print("Step 2: 컵 위치로 이동")
            cup2()
            step = 3
            print("✅ Step 2 완료: 컵 위치로 이동")
            check_robot_state()

        elif step == 3:
            print("Step 3: 컵 집기")
            cup1()
            movej(JReady, vel=VELOCITY, acc=ACC)
            step = 4
            print("✅ Step 3 완료: 컵 집기")
            check_robot_state()
            

        elif step == 4:
            print("Step 4: 뚜껑 닫기")
            close_lid()
            movej(JReady, vel=VELOCITY, acc=ACC)
            step = 5
            print("✅ Step 4 완료: 뚜껑 닫기")
            

        elif step == 5:
            print("Step 5: 흔들기")
            shaking()
            movej(JReady, vel=VELOCITY, acc=ACC)
            step = 6
            print("✅ Step 5 완료: 흔들기")
            

        elif step == 6:
            print("Step 6: 체로 거르기")
            colander_operations()
            movej(JReady, vel=VELOCITY, acc=ACC)
            step = 7
            print("✅ Step 6 완료: 체로 거르기")
            

        elif step == 7:
            print("Step 7: 뚜껑 열기")
            open_lid()
            movej(JReady, vel=VELOCITY, acc=ACC)
            step = 8
            print("✅ Step 7 완료: 뚜껑 열기")
            

        elif step == 8:
            print("Step 8: 마지막 붓기")
            last_pouring()
            colander_reverse_operations()
            step = 9
            print("✅ Step 8 완료: 마지막 붓기 및 체로 거르기 완료")
            

        elif step == 9:
            print("Step 9: 작업 완료 - 초기 위치로 이동")
            movej(JReady, vel=VELOCITY, acc=ACC)
            wait(3)
            print("✅ Task done")
            step = 0
            break

def pass_action():
    from DSR_ROBOT2 import movej, get_robot_state, wait, movel, posx
    from cobot1.config import VELOCITY, ACC, JReady
    from cobot1.motions.gripper_ops import release
    print("   -> 패스 작업 실행")
    print("  -> 초기 위치로 이동")
    movel(posx(448.12,-199.34,670.56,91.94,-89.27,90.14),vel = 80, acc = 80)
    movel(posx(191.09,-278.16,613.62,89.42,-90.08,91.69),vel = 80, acc = 80)
    movel(posx(191.09,-278.16,444.55,89.42,-90.08,91.69),vel = 80, acc = 80)
    release()
    movel(posx(447.53,60.53,514.81,127.33,-87.66,94.36),vel = 80, acc = 30)
    movej(JReady, vel=VELOCITY, acc=ACC)

    print("   -> 패스 작업 완료")
    # wait(3)
    # release()
    print("   -> 패스 작업 후 초기 위치에서 그리퍼 오픈 완료")
    wait(3)
    print("   -> 패스 작업 완전히 종료")

    


def recovery_action():
    from DSR_ROBOT2 import get_robot_state, drl_script_stop, DR_QSTOP_STO,get_last_alarm

    print("🛠 recovery 동작 실행")

    if call_set_robot_control(2): # 리셋 명령 전송
        print("   -> 리셋 명령 전송됨. 복구 대기 중...")
    time.sleep(2.0)
    if get_robot_state() == 1:
        print("   -> [Success] 보호 정지 해제. 설정을 다시 로드합니다.")
        initialize_robot() # 초기화 재수행
        return True  # ✅ 복구 성공 반환

def recovery_3_action():
    from DSR_ROBOT2 import get_robot_state, drl_script_stop, DR_QSTOP_STO,get_last_alarm
    # [복구 로직] STATE_SAFE_OFF (서보 꺼짐)
    state_code = get_robot_state()
    state_desc = ROBOT_STATE_MAP.get(state_code, "UNKNOWN_STATE")
    print(f"\n*** [Error] 서보 꺼짐 감지 ({state_desc}) ***")
    print("*** 서보 ON (Reset Safe Off)을 시도합니다. ***")
    
    # 1. 기존 스크립트 정지 (필수)
    drl_script_stop(DR_QSTOP_STO)
    time.sleep(0.5)
    
    # 2. ★ SetRobotControl(3)으로 서보 ON 시도
    if call_set_robot_control(CONTROL_RESET_SAFE_OFF):
        print("   -> 서보 ON 명령 전송됨. 기동 대기 중...")
        time.sleep(3.0)
        if get_robot_state() == 1:
            print("   -> [Success] 서보 ON 완료.")
            initialize_robot() # 초기화 재수행
            return True  # ✅ 복구 성공 반환
        else:
            print("   -> [Fail] 서보 ON 명령이 전송되었으나, 대기 상태(1)로 복구되지 않았습니다.")
            return False # ❌ 복구 실패 반환 (명령은 들어갔으나 상태가 안 바뀜)
    else:
        # 여전히 3번 상태라면 하드웨어 스위치 문제
        alarm = get_last_alarm()
        print(f">>> [Fail] 서보 ON 실패. 현재 상태: {state_code}")
        if alarm:
            print(f"   - 거절 사유(알람): {alarm}")
        print("   !!! 조치 필요: [비상정지 버튼] 해제 또는 [티칭 펜던트 스위치(Auto)] 확인 필요 !!!\n")
        time.sleep(2)
        return False # ❌ 복구 실패 반환 (명령 자체가 거절됨)


# ======================
# 🔁 작업 루프
# ======================
def task_loop():
    global status
    from DSR_ROBOT2 import movej, amovel, posx, get_current_posx, movesj, posj, wait
    from cobot1.config import VELOCITY, ACC, JReady

    release()
    movej(JReady, vel=VELOCITY, acc=ACC)  # 초기 위치로 이동
    movej([1.86, -17.35, 115.41, 0.07, -114.99, 0.06], vel=100, acc=100)
    while rclpy.ok():
        # ======================================
        # pos1 = posx([133.17, 11.93, 809.83, 2.14, -17.43, 0.08])
        # pos2 = posx([598.80, 27.78, 776.32, 1.86, 26.58, 0.42])
        pos1 = posx([133.1, 11.9, 809.8, 2.1, -17.4, 0.0])
        pos2 = posx([598.8, 27.7, 776.3, 1.8, 26.5, 0.4])

        amovel(pos1, vel=50, acc=50)
        while True:
            if status == 1:
                break
            x = list(get_current_posx()[0])
            x = [round(v, 1) for v in x]
            if x==list(pos1):
                break
        amovel(pos2, vel=50, acc=50)
        while True:
            if status == 1:
                break
            x = list(get_current_posx()[0])
            x = [round(v, 1) for v in x]
            if x==list(pos2):
                break
        # ======================================
        if status == 1:
            # ROS2 환경에서의 정지 상수 (DR_QSTOP과 동일한 역할)
            STOP_TYPE_QUICK = 1 
            STOP_TYPE_QUICK_STO = 2

            # 퍼블리셔 생성 및 정지 명령 퍼블리시
            stop_client = DR_init.__dsr__node.create_client(MoveStop, '/dsr01/motion/move_stop')
            req = MoveStop.Request()
            # 2. 요청(Request) 데이터를 담을 빈 객체를 생성할 때 사용합니다.
            req = MoveStop.Request()
            req.stop_mode = 1  # 1: Quick Stop, 2: Soft Stop 등

            # 3. 로봇에게 정지 요청 전송
            future = stop_client.call_async(req)
            time.sleep(3)  # 0.05초씩 쉬면서 ROS 2 엔진이 응답을 받을 수 있게 숨통을 트여줌
            hello()
            perform_task()
            pos1_r=[1.86, -17.35, 115.41, 0.07, -114.99, 0.06]
            movej(pos1_r, vel=100, acc=100)

            status = 0
        time.sleep(0.1)

def my_recovery_action():
    """
    서비스가 호출되었을 때 실제로 작동할 내용을 여기에 작성합니다.
    (예: 로봇 에러 초기화, 특정 위치로 이동, 상태 변수 리셋 등)
    """
    global global_recovery_start, global_recovery_finished
    global_recovery_finished = False  # 복구 시작 시점에 완료 상태 초기화
    global_recovery_start = True  # 복구 시작 신호 설정
    print("   -> 실제 복구 작업이 실행됩니다.")
    while not global_recovery_finished:
        time.sleep(1)
    return global_recovery_success  # 복구 성공 여부 반환


def recovery_service_callback(request, response):
    """
    '/recovery' 서비스 요청이 들어오면 자동으로 실행되는 콜백 함수입니다.
    """
    print("📬 'recovery' 서비스 호출을 수신했습니다.")
    
    try:
        # 클라이언트(요청자)에게 성공했음을 알림
        response.success = my_recovery_action()
        response.message = "Recovery action executed successfully."
    except Exception as e:
        # 실행 중 에러가 발생했을 경우
        print(f"❌ 오류 발생: {e}")
        response.success = False
        response.message = f"Failed to execute recovery: {str(e)}"
        
    return response

def my_pass_action():
    """
    서비스가 호출되었을 때 실제로 작동할 내용을 여기에 작성합니다.
    (예: 로봇 에러 초기화, 특정 위치로 이동, 상태 변수 리셋 등)
    """
    global global_pass_start, global_pass_finished, global_pass_success
    global_pass_finished = False  # 패스 시작 시점에 완료 상태 초기화
    global_pass_start = True  # 패스 시작 신호 설정
    print("   -> 실제 패스 작업이 실행됩니다.")
    while not global_pass_finished:
        time.sleep(1)
    return global_pass_success  # 패스 성공 여부 반환

def pass_service_callback(request, response):
    """
    '/pass' 서비스 요청이 들어오면 자동으로 실행되는 콜백 함수입니다.
    """
    print("📬 'pass' 서비스 호출을 수신했습니다.")
    
    try:
        # 클라이언트(요청자)에게 성공했음을 알림
        response.success = my_pass_action()
        response.message = "Pass action executed successfully."
    except Exception as e:
        # 실행 중 에러가 발생했을 경우
        print(f"❌ 오류 발생: {e}")
        response.success = False
        response.message = f"Failed to execute pass: {str(e)}"
        
    return response

# ======================
# 🚀 main
# ======================
def main(args=None):
    global global_error_publisher, global_robot_state
    rclpy.init(args=args)

    # 🤖 로봇 노드
    robot_node = rclpy.create_node("robot_control_node", namespace=ROBOT_ID)
    DR_init.__dsr__node = robot_node
    initialize_robot()

    # 📡 통신 노드
    comm_node = rclpy.create_node("communication_node", namespace=ROBOT_ID)

    comm_node.create_subscription(Int32, "robot_start", cmd_callback, 10)
    global_error_publisher = comm_node.create_publisher(Int32, "robot_error", 10)
    global_robot_state = comm_node.create_publisher(Int32, "robot_status", 10)
    recovery_srv = comm_node.create_service(Trigger, 'recovery', recovery_service_callback)
    pass_srv = comm_node.create_service(Trigger, 'pass', pass_service_callback)

    # 🧠 executor
    executor = SingleThreadedExecutor()
    executor.add_node(comm_node)

    # 🔥 작업 쓰레드
    threading.Thread(target=task_loop, daemon=True).start()


    print("🚀 시스템 시작")

    try:
        executor.spin()   # 🔥 단 하나의 spin
    finally:
        robot_node.destroy_node()
        comm_node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()