# shaking_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip_shaking_cup

def stanby():
    from DSR_ROBOT2 import posx, posj, movej, movel, movesj, move_periodic, DR_TOOL, get_current_posx
    
    release()
    pos1 = posx([133.17, 11.93, 809.83, 2.14, -17.43, 0.08])
    pos2 = posx([598.80, 27.78, 776.32, 1.86, 26.58, 0.42])

    movel(pos1, vel=50, acc=50)

    movel(pos2, vel=50, acc=50)