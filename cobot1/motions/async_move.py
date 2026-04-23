# shaking_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip_shaking_cup
import time

def recover_func():
    ...

def amove_l(pos,vel,acc):
    from DSR_ROBOT2 import posx, posj, amovej, amovel, movesj, move_periodic, drl_script_stop, get_current_posx, get_robot_state, DR_TOOL, DR_QSTOP_STO, wait
    
    print(f"Moving to position: {pos} with velocity: {vel} and acceleration: {acc}")
    amovel(pos, vel=vel, acc=acc)
    while True:
        x = list(get_current_posx()[0])
        x = [round(v, 2) for v in x]
        # print(x)
        if x==list(pos):
            break
        if get_robot_state()==5: # 복구 상태
            recover_func()
            break
            

        time.sleep(0.1)
    print("Movement completed.")