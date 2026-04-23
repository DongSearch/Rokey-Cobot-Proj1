# shaking_ops.py
import time

from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip_shaking_cup

def hello():
    print("Hello, World!")
    from DSR_ROBOT2 import posx, posj, movej, movel, move_periodic, movesj,DR_TOOL, amovej, get_current_posx, get_current_posj, DR_QSTOP, drl_script_stop, DR_QSTOP_STO
    # pos1 = posx([352.54, 18.37, 801.48, 2.76, -14.92, -0.54])
    # pos2 = posx([526.81, 24.97, 802.90, 1.55, 13.97, 0.71])
    pos1=[1.86, 11.68, 89.66, 0.06, -87.37, 0.07]
    pos2=[1.86, 11.68, 89.66, 0.06, -116.26, 0.07]
    pos_list=[posj(1.86, 11.68, 89.66, 0.06, -87.37, 0.07), posj(1.86, 11.68, 89.66, 0.06, -116.26, 0.07),posj(1.86, 11.68, 89.66, 0.06, -87.37, 0.07), posj(1.86, 11.68, 89.66, 0.06, -116.26, 0.07),posj(1.86, 11.68, 89.66, 0.06, -87.37, 0.07), posj(1.86, 11.68, 89.66, 0.06, -116.26, 0.07)]

    # movej(JReady, vel=VELOCITY, acc=ACC)
    # movej(pos1, vel=100, acc=100)
    # movej(pos2, vel=100, acc=100)
    # movej(pos1, vel=100, acc=100)
    # movej(pos2, vel=100, acc=100)
    # movej(pos1, vel=100, acc=100)
    # movej(pos2, vel=100, acc=100)
    # movej(pos1, vel=100, acc=100)
    # stop(DR_QSTOP)
    movesj(pos_list,vel=200, acc=200)