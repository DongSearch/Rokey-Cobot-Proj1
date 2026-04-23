# colander_ops.py
from cobot1.config import VELOCITY, ACC, JReady
from cobot1.motions.gripper_ops import release, grip

def colander_operations():
    from DSR_ROBOT2 import posx, movej, movel
    release()
    delta_x = 10
    pos1 = posx([466.06+delta_x,-99.48,333.65,86.19,-111.52,-5.78]) # 체반 집기 또는 놓기 위치
    pos2 = posx([470.77+delta_x,23.42,381.15,86.45,-111.49,-5.5]) # 체반 들고 빼기 또는 놓기 전 위치

    pos3 = posx([548.45,138.33,157.21,95.9,-92.97,-5.21]) # 컵 위에 올리기 전 위치
    pos4 = posx([548.45,138.33,137.21+5,95.9,-92.97,-5.21]) # 컵 위에 올리기
    pos5 = posx([528.45,138.33,137.21,95.9,-92.97,-5.21]) # 컵 위에 올리고 빼기
    
    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos1, vel=VELOCITY, acc=ACC)
    grip()
    movel(pos2, vel=VELOCITY, acc=ACC)
    movel(pos3, vel=VELOCITY, acc=ACC)
    movel(pos4, vel=VELOCITY, acc=ACC)
    release()
    movel(pos5, vel=VELOCITY, acc=ACC)