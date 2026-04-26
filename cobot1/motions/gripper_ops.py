# gripper_ops.py
from cobot1.config import ON, OFF


def release(): # 그립 해제
    from DSR_ROBOT2 import set_digital_output, wait, get_robot_state
    state = get_robot_state()
    if state != 1:
        print("Warning: Robot is not in a normal state. Current state code:", state)
        return
    print("Releasing...")
    set_digital_output(1, OFF)
    set_digital_output(2, ON)
    set_digital_output(3, OFF)
    wait(1)

def release1():
    from DSR_ROBOT2 import set_digital_output, wait, get_robot_state
    state = get_robot_state()
    if state != 1:
        print("Warning: Robot is not in a normal state. Current state code:", state)
        return
    print("Releasing...")
    set_digital_output(3, OFF)
    set_digital_output(1, OFF)
    set_digital_output(2, ON)
    wait(1)

def grip(): # 그립
    from DSR_ROBOT2 import set_digital_output, wait, get_robot_state
    state = get_robot_state()
    if state != 1:
        print("Warning: Robot is not in a normal state. Current state code:", state)
        return
    print("Gripping...")
    set_digital_output(1, ON)
    set_digital_output(2, OFF)
    set_digital_output(3, OFF)
    wait(1)

def grip_cup(): # 계량 컵 그립 80mm
    from DSR_ROBOT2 import set_digital_output, wait, get_robot_state
    state = get_robot_state()
    if state != 1:
        print("Warning: Robot is not in a normal state. Current state code:", state)
        return
    print("Gripping cup...")
    set_digital_output(1, OFF)
    set_digital_output(2, OFF)
    set_digital_output(3, ON)
    wait(1)
    print("Cup grip action completed.")

def grip_shaking_cup(): # 쉐이킹 컵 그립 83mm
    from DSR_ROBOT2 import set_digital_output, wait, get_robot_state
    state = get_robot_state()
    if state != 1:
        print("Warning: Robot is not in a normal state. Current state code:", state)
        return
    print("Gripping shaking cup...")
    set_digital_output(1, OFF)
    set_digital_output(2, ON)
    set_digital_output(3, ON)
    wait(1)
    print("Cup grip action completed.")

def grip_cover_cap(): # 덮개 그립 99mm
    from DSR_ROBOT2 import set_digital_output, wait, get_robot_state
    state = get_robot_state()
    if state != 1:
        print("Warning: Robot is not in a normal state. Current state code:", state)
        return
    print("Gripping...")
    # release()
    set_digital_output(1, ON)
    set_digital_output(2, ON)
    set_digital_output(3, ON)
    wait(1)
    print("Cover cap grip action completed.")
    
def wait_digital_input(sig_num):
    from DSR_ROBOT2 import get_digital_input, wait
    while not get_digital_input(sig_num):
        wait(0.5)