import rclpy
from cobot1.config import ROBOT_ID
import DR_init
from dsr_msgs2.srv import MoveStop

def emergency_stop(stop_mode=0):
    """
    로봇 비상 정지 함수
    - stop_mode: 0 (가장 빠른 급정지, 기본값), 1 (부드러운 감속 정지)
    """
    
    node = rclpy.create_node("main_node", namespace=ROBOT_ID)
    node = DR_init.__dsr__node
    if node is None:
        print("🚨 노드가 초기화되지 않아 정지 명령을 내릴 수 없습니다.")
        return
        
    # 1. 서비스 클라이언트 생성 (로봇 ID 네임스페이스 자동 적용)
    service_name = f'/{DR_init.__dsr__id}/motion/move_stop'
    stop_client = node.create_client(MoveStop, service_name)
    
    # 2. 서비스 서버가 살아있는지 확인 (1초 대기)
    if not stop_client.wait_for_service(timeout_sec=1.0):
        print(f"🚨 {service_name} 서비스에 연결할 수 없습니다!")
        return
        
    # 3. 요청(Request) 객체 생성 및 파라미터(stop_mode) 설정
    req = MoveStop.Request()
    req.stop_mode = stop_mode
    
    # 4. 컨트롤러로 정지 명령 발사! (비동기로 실행되어 파이썬 코드가 멈추지 않음)
    stop_client.call_async(req)
    print("🛑 로봇 정지 명령 전송 완료!")

# --- 실제 사용 예시 ---
# 센서 감지나 비상 상황 발생 시 아래처럼 함수만 호출하면 즉시 멈춥니다.
emergency_stop()